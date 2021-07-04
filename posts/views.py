import json
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q

from .models import Post, LikePost, LikeComment, Comment
from .forms import PostForm, UpdatePostForm, CommentForm
from profiles.models import Notification, User


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePostView, self).form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    template_name = 'posts/posts_list.html'
    model = Post
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        friends = User.objects.filter(my_friend__friend=self.request.user)
        return Post.objects.filter(Q(user__in=friends) | Q(user=self.request.user)).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = self.request.user.likepost_set.all()
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class DetailPostView(LoginRequiredMixin, DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'posts/posts_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(DetailPostView, self).get_context_data()
        context['post_likes'] = self.object.likepost_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_likes'] = LikeComment.objects.filter(comment__post=self.object)
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'posts/posts_update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user != kwargs['pk']:
            return redirect(reverse('posts:list'))
        return super(UpdatePostView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UpdatePostView, self).get_context_data(**kwargs)
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class DeletePostView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        post_id = body.get('id')
        post = get_object_or_404(Post, id=post_id)
        if request.user != post.user:
            return JsonResponse({'status': "You don't have access"})
        post.delete()
        return JsonResponse({'status': 'Deleted'})


class LikePostView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        post_id = body.get('id')
        post = get_object_or_404(Post, id=post_id)
        value = body.get('value')
        user = request.user
        if LikePost.objects.filter(user=user, post=post).exists():
            like = LikePost.objects.get(user=user, post=post)
            like.value = value
        else:
            like = LikePost.objects.create(user=user, post=post, value=value)
        
        if like.value == 0:
            like.delete()
        else:
            like.save()

        context = {
            'dislikes': post.get_dislike_count(),
            'likes': post.get_like_count(),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


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
        return reverse('posts:detail', args=[str(self.object.pk)])


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    queryset = Post.objects.all()
    template_name = 'posts/posts_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        context['post_likes'] = self.object.likepost_set.all()
        context['comments'] = self.object.comment_set.all()
        context['comment_likes'] = LikeComment.objects.filter(comment__post=self.object)
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class PostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostCommentView.as_view()
        return view(request, *args, **kwargs)


class JSONCommentView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        post = get_object_or_404(Post, id=body.get('id'))
        user = request.user
        text = body.get('text')
        Comment.objects.create(user=user, post=post, text=text);
        context = {
            'comment_count': post.comment_set.count()
        }
        return HttpResponse(json.dumps(context), content_type='application/json')


class LikeCommentView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        comment_id = body.get('id')
        comment = get_object_or_404(Comment, id=comment_id)
        value = body.get('value')
        user = request.user
        if LikeComment.objects.filter(user=user, comment=comment).exists():
            like = LikeComment.objects.get(user=user, comment=comment)
            like.value = value
        else:
            like = LikeComment.objects.create(user=user, comment=comment, value=value)
        
        if like.value == 0:
            like.delete()
        else:
            like.save()

        context = {
            'dislikes': comment.get_dislike_count(),
            'likes': comment.get_like_count(),
        }
        return HttpResponse(json.dumps(context), content_type='application/json')
