# Generated by Django 3.2.3 on 2021-06-19 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_user_gender'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Friend',
            new_name='Friendship',
        ),
    ]
