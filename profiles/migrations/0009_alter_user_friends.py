# Generated by Django 3.2.7 on 2021-09-25 07:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_profiles_user_friends_+', to=settings.AUTH_USER_MODEL),
        ),
    ]