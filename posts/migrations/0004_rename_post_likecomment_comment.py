# Generated by Django 3.2.3 on 2021-06-13 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20210612_2335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='likecomment',
            old_name='post',
            new_name='comment',
        ),
    ]