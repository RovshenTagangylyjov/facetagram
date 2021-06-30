import json
from django.http import JsonResponse, HttpResponse
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core import serializers

from .forms import UpdateProfileForm
from .models import User, Notification, Friendship
from posts.forms import PostForm
from posts.models import LikePost
from chat.models import Room


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'profiles/profiles_update.html'
    form_class = UpdateProfileForm
    context_object_name = 'user'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class ProfileDetailView(LoginRequiredMixin, ListView, SingleObjectMixin):
    template_name = "profiles/profiles_detail.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=User.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object
        context['likes'] = LikePost.objects.filter(user=self.request.user)
        context['form'] = PostForm
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        context['has_access'] = self.object.my_friend.filter(friend=self.request.user).exists() \
                                or self.object == self.request.user \
                                or not self.object.is_private
        return context

    def get_queryset(self):
        return self.object.post_set.all()


class SearchProfileView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'profiles/search_profile.html'
    context_object_name = 'profiles'
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('search') or ''
        return User.objects.filter(username__icontains=search).exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(SearchProfileView, self).get_context_data(**kwargs)
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        context['friends'] = User.objects.filter(my_friend__friend=self.request.user)
        return context


class FriendRequest(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        user = request.user
        friend = get_object_or_404(User, id=body['profile_id'])
        value = body['value']
        notification_exists = Notification.objects.filter(sender=friend, receiver=user).exists()
        if (value == 'send' or value == 'deny') and Friendship.objects.filter(user=user, friend=friend).exists():
            return JsonResponse({'status': "You're friend alredy"})
        if value == 'send' and not notification_exists:
            Notification.objects.create(sender=user, receiver=friend)
        elif value == 'cancel' and notification_exists:
            Notification.objects.get(sender=user, receiver=friend).delete()
        elif value == 'deny' and notification_exists:
            Notification.objects.get(sender=friend, receiver=user).delete()
        elif value == 'end-friendship' and Friendship.objects.filter(friend=friend, user=user).exists():
            user.my_friend.get(friend=friend).delete()
            user.i_friend.get(user=friend).delete()
        return JsonResponse({'status': 'OK'})


def create_room(user1_id, user2_id):
    users = sorted([user1_id, user2_id])
    return int('0'.join([str(users[0]), str(users[1])]))


class JSONSearchProfile(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        search = body['search']
        user = self.request.user
        qs = User.objects.filter(username__istartswith=search).exclude(id=user.id).defer('password')
        context = list(qs.values())
        for i in range(len(context)):
            profile = get_object_or_404(User, id=context[i]['id'])
            if Friendship.objects.filter(user=user, friend=profile).exists():
                context[i]['status'] = 'friend'
            elif Notification.objects.filter(sender=user, receiver=profile).exists():
                context[i]['status'] = 'waiting'
            else:
                context[i]['status'] = 'stranger'
            if profile.date_of_birth:
                context[i]['age'] = profile.get_age()
            context[i]['avatar'] = profile.get_avatar_url()
        return JsonResponse(context, safe=False)


class CreateFriendshipView(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        user1 = request.user
        user2 = get_object_or_404(User, id=body['user'])
        room_id = create_room(user1.id, user2.id)
        if Friendship.objects.filter(user=user1, friend=user2, room_id=room_id).exists():
            return JsonResponse({'status': "You're friend alredy"})
        Friendship.objects.create(user=user1, friend=user2, room_id=room_id)
        Friendship.objects.create(user=user2, friend=user1, room_id=room_id)
        if not Room.objects.filter(room_id=room_id).exists():
            Room.objects.create(room_id=room_id)
        notification = get_object_or_404(Notification, id=body['notification'])
        notification.delete()
        return JsonResponse({'status': 'ok'})


class FriendsView(LoginRequiredMixin, ListView):
    template_name = 'profiles/friends_list.html'
    context_object_name = 'friendships'
    model = User
    paginate_by = 3

    def get_queryset(self):
        search = self.request.GET.get('search') or ''
        return self.request.user.my_friend.filter(friend__username__icontains=search)

    def get_context_data(self, **kwargs):
        context = super(FriendsView, self).get_context_data(**kwargs)
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class JSONSearchFriend(LoginRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request):
        body = json.loads(request.body)
        search = body['search']
        user = self.request.user
        qs = User.objects.filter(username__istartswith=search).exclude(id=user.id).defer('password')
        # context = serializers.serialize('json', qs)
        context = list(qs.values())
        for i in range(len(context)):
            profile = get_object_or_404(User, id=context[i]['id'])
            context[i]['avatar'] = profile.get_avatar_url()
            print(context[i])

        return JsonResponse(context, safe=False)
        # return HttpResponse(json.dumps(context), content_type='application/json')
