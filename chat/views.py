import json
from typing import List
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Room, Message
from profiles.models import Notification


class ChatView(LoginRequiredMixin, ListView, SingleObjectMixin):
    template_name = 'chat/chat.html'
    context_object_name = 'messages'
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        user = self.request.user
        room_ids = [user.generate_room_id(friend.pk) for friend in user.friends.only("pk", "username", "avatar")] 
        self.object = self.get_object(queryset=Room.objects.filter(room_id__in=room_ids))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.message_set.order_by("-date_created")
    
    def get_context_data(self, **kwargs):
        context = super(ChatView, self).get_context_data(**kwargs)
        user = self.request.user
        for friend in user.friends.all():
            if self.object.pk == user.generate_room_id(friend.pk):
                context['friend'] = friend
                break
        return context


class SendTextView(View):

    def post(self, request):
        body = json.loads(request.body)
        room_id = body['room_id']
        text = body['text']
        if not text or text.isspace():
            return JsonResponse({})
        room = get_object_or_404(Room, room_id=room_id)
        Message.objects.create(room=room, user=request.user, text=text)
        return JsonResponse({})


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
