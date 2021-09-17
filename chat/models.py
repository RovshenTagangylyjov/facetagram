from django.db import models
from django.conf import settings


class Room(models.Model):
    room_id = models.IntegerField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField(max_length=5000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
