from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=5000, null=True, blank=True)
    image = models.ImageField(upload_to='posts')
    date_created = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50, null=True, blank=True)

    def get_like_count(self):
        return self.likepost_set.filter(value=1).count()

    def get_dislike_count(self):
        return self.likepost_set.filter(value=-1).count()

    def get_comment_count(self):
        return self.comment_set.count()

    def get_absolute_url(self):
        return reverse('posts:detail', args=[str(self.pk)])


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_like_count(self):
        return self.likecomment_set.filter(value=1).count()

    def get_dislike_count(self):
        return self.likecomment_set.filter(value=-1).count()

    def get_absolute_url(self):
        return reverse('posts:detail', args=[str(self.post)])


class LikePost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)


class LikeComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
