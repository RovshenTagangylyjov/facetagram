import json

from django.core.exceptions import PermissionDenied
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models.expressions import Q, Exists, OuterRef

from .models import Post, LikePost, LikeComment, Comment
from .forms import PostForm, CommentForm


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        if not (form.cleaned_data["description"] or form.cleaned_data["image"]):
            return redirect(reverse_lazy("posts:list"))
        return super(CreatePostView, self).form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    template_name = 'posts/posts_list.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        is_liked = Exists(LikePost.objects.filter(user=user, post_id=OuterRef("id"), value=1))
        is_disliked = Exists(LikePost.objects.filter(user=user, post_id=OuterRef("id"), value=-1))
        return Post.objects.filter(Q(user__in=user.friends.all()) | Q(user=user) | Q(user__is_private=False))\
            .annotate(is_liked=is_liked, is_disliked=is_disliked)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'posts/posts_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        user = self.request.user
        is_liked = Exists(LikePost.objects.filter(user=user, post_id=OuterRef("id"), value=1))
        is_disliked = Exists(LikePost.objects.filter(user=user, post_id=OuterRef("id"), value=-1))
        return Post.objects.filter(Q(user__in=user.friends.all()) | Q(user=user) | Q(user__is_private=False))\
            .annotate(is_liked=is_liked, is_disliked=is_disliked)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        user = self.request.user
        is_liked = Exists(LikeComment.objects.filter(user=user, comment_id=OuterRef("id"), value=1))
        is_disliked = Exists(LikeComment.objects.filter(user=user, comment_id=OuterRef("id"), value=-1))
        context['comments'] = self.object.comment_set.annotate(is_liked=is_liked, is_disliked=is_disliked)
        return context


class PostCommentView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'posts/posts_detail.html'
    model = Post
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:detail', args=[self.object.pk])


class PostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentView.as_view()
        return view(request, *args, **kwargs)


class DeletePostView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        post_id = body.get('id')
        post = get_object_or_404(Post, id=post_id)
        if request.user != post.user:
            raise PermissionDenied
        post.delete()
        return JsonResponse({})


class RatePostView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        post_id = body.get('id')
        post = get_object_or_404(Post, id=post_id)
        value = body.get('value')
        user = request.user
        LikePost.objects.update_or_create(user=user, post=post, defaults={"value": value})
        context = {
            'dislikes': post.get_dislike_count(),
            'likes': post.get_like_count(),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


class RateCommentView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        comment_id = body.get('id')
        comment = get_object_or_404(Comment, id=comment_id)
        value = body.get('value')
        user = request.user
        LikeComment.objects.update_or_create(user=user, comment=comment, defaults={"value": value})
        context = {
            'dislikes': comment.get_dislike_count(),
            'likes': comment.get_like_count(),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')
