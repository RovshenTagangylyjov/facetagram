import json

from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.db.models.expressions import Exists, OuterRef, Q, Value, F
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.templatetags.static import static

from .forms import UpdateProfileForm
from .models import User, Notification
from posts.models import LikePost
from chat.models import Room


class ProfileDetailView(LoginRequiredMixin, ListView, SingleObjectMixin):
    template_name = "profiles/profiles_detail.html"
    context_object_name = 'posts'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        user = self.request.user
        is_friend = Exists(user.friends.filter(pk=OuterRef("pk")))
        is_waiting = Exists(Notification.objects.filter(sender=user, receiver_id=OuterRef("pk")))
        self.object = self.get_object(queryset=User.objects.annotate(is_friend=is_friend, is_waiting=is_waiting))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object
        return context

    def get_queryset(self):
        user = self.request.user
        is_liked = Exists(LikePost.objects.filter(user=user, post_id=OuterRef("id"), value=1))
        is_disliked = Exists(LikePost.objects.filter(user=user, post_id=OuterRef("id"), value=-1))
        return self.object.post_set.annotate(is_liked=is_liked, is_disliked=is_disliked)


class ProfileListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'profiles/profiles_list.html'
    context_object_name = 'profiles'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        search = self.request.GET.get('search') or ''
        filter = self.request.GET.get("filter")
        is_friend = Exists(user.friends.filter(pk=OuterRef("pk")))
        is_waiting = Exists(Notification.objects.filter(sender=user, receiver_id=OuterRef("pk")))
        if filter == "friends":
            return user.friends.filter(username__icontains=search)\
                .only('username', 'pk', 'avatar', 'id')\
                .annotate(is_friend=is_friend, is_waiting=is_waiting)
        return User.objects.filter(username__icontains=search)\
            .exclude(pk=user.pk)\
            .only('username', 'pk', 'avatar', 'id')\
            .annotate(is_friend=is_friend, is_waiting=is_waiting)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/profiles_update.html'
    form_class = UpdateProfileForm
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)


class FriendRequest(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        user = request.user
        if body["profile_id"] == user.pk:
            raise PermissionDenied
        friend = get_object_or_404(User, id=body.get('profile_id'))
        value = body.get('value')
        is_friend = user.friends.filter(pk=friend.pk)
        notification_exists = Notification.objects.filter(
            Q(sender=user, receiver=friend) | Q(sender=friend, receiver=user)
        ).exists()
        if value == 'add' and is_friend:
            return JsonResponse({})
        elif value == 'add' and not (notification_exists or is_friend):
            Notification.objects.create(sender=user, receiver=friend)
        elif value == 'cancel' and notification_exists and not is_friend:
            Notification.objects.get(sender=user, receiver=friend).delete()
        elif value == 'deny' and notification_exists and not is_friend:
            Notification.objects.get(sender=friend, receiver=user).delete()
        elif value == 'remove' and is_friend:
            user.friends.remove(friend)
        return JsonResponse({})


class CreateFriendshipView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        user = request.user
        if body["user"] == user.pk:
            raise PermissionDenied
        friend = get_object_or_404(User, id=body['user'])
        room_id = user.generate_room_id(friend.pk)
        if user.friends.filter(pk=friend.pk).exists():
            return JsonResponse({})
        if not Room.objects.filter(room_id=room_id).exists():
            Room.objects.create(room_id=room_id)
        user.friends.add(friend)
        notification = get_object_or_404(Notification, id=body['notification'])
        notification.delete()
        return JsonResponse({})


class EndFriendshipView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request):
        body = json.load(request.body)
        user = request.user
        if body["pk"] == user.pk:
            raise PermissionDenied
        try:
            friend = get_object_or_404(User, pk=body["pk"])
            user.friends.remove(friend)
        except  ObjectDoesNotExist:
            return JsonResponse({})
        return JsonResponse({})


class JSONSearchProfile(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request):
        user = self.request.user
        body = json.loads(request.body)
        search = body.get("search")
        friends = body.get("friends")
        users = User.objects
        if friends:
            users = user.friends
        qs = users.filter(username__istartswith=search).exclude(pk=user.pk)
        context = list(qs.values("id", "username"))
        return JsonResponse(context, safe=False)


class JSONGetNotifications(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request):
        user = self.request.user
        body = json.loads(request.body)
        qs = user.receiver.filter(id__gt=body["last_notification_id"]).annotate(
            sender_username=F("sender__username"),
            sender_avatar=F("sender__avatar"),
            default_avatar=Value(static("img/default_avatar.png"))
        )
        context = list(qs.values())
        return JsonResponse(context, safe=False)
