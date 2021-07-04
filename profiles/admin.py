from django.contrib import admin
from .models import User, Notification, Friendship

admin.site.register(User)
admin.site.register(Notification)
admin.site.register(Friendship)