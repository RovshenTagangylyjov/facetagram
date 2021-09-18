# Generated by Django 3.2.5 on 2021-08-06 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'There is already a user with that email.'}, max_length=254, unique=True),
        ),
    ]