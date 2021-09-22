import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.templatetags.static import static
from django.urls import reverse

from helpers.image_compression import get_compressed_image_content


GENDER = (
    ('Female', 'Female'),
    ('Male', 'Male'),
    ('Others', 'Others'),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER, null=True, blank=True)
    biography = models.TextField(max_length=10000, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)
    is_private = models.BooleanField(default=False, blank=True)
    friends = models.ManyToManyField("self", null=True, blank=True)

    def get_age(self):
        today = datetime.date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day)
                                                       < (self.date_of_birth.month, self.date_of_birth.day))

    def save(self, *args, **kwargs):
        if self.avatar:
            self.avatar = get_compressed_image_content(self.avatar, [256, 256])
        super().save(*args, **kwargs)

    def get_avatar_url(self):
        if not self.avatar:
            return static('img/default_avatar.png')
        return self.avatar.url

    def generate_room_id(self, user_id) -> int:
        users = sorted([self.id, user_id])
        return int('0'.join([str(users[0]), str(users[1])]))


    @staticmethod
    def get_absolute_url():
        return reverse('posts:list')


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_query_name='sender', related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                 related_query_name='receiver', related_name='receiver')
    date_created = models.DateTimeField(auto_now_add=True)
