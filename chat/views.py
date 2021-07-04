import json
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core import serializers

from .models import Room, Message
from profiles.models import User, Friendship, Notification


class ChatView(LoginRequiredMixin, DetailView):
    template_name = 'chat/chat.html'
    context_object_name = 'room'
    model = Room

    def get_queryset(self):
        room_ids = self.request.user.my_friend.values_list('room_id')
        return Room.objects.filter(room_id__in=room_ids)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ChatView, self).get_context_data()
        friendship = self.request.user.my_friend.get(room_id=self.object.room_id)
        context['messages'] = self.object.message_set.all()
        context['friend'] = friendship.friend
        context['notifications'] = Notification.objects.filter(receiver=self.request.user).order_by('-date_created')
        return context


class TextView(View):

    def post(self, request):
        body = json.loads(request.body)
        room_id = body['room_id']
        text = body['text']
        if not text or text.isspace():
            return JsonResponse({'status': 'Empty text'})
        room = get_object_or_404(Room, room_id=room_id)
        Message.objects.create(room=room, user=request.user, text=text)
        return JsonResponse({'status': 'ok'})


class GetTextView(View):
    def post(self, request):
        body = json.loads(request.body)
        room = get_object_or_404(Room, room_id=body['room_id'])
        message_id = body['message']
        if message_id == -1:
            qs = Message.objects.filter(room=room)
        else:
            date = Message.objects.get(id=message_id).date_created
            qs = Message.objects.filter(date_created__gt=date, room=room)
        return JsonResponse(list(qs.values()), safe=False)
