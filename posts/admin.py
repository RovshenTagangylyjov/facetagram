from django.contrib import admin
from .models import Post, LikePost, Comment

admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Comment)