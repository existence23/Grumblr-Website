# Generated by Django 2.1.1 on 2018-10-18 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grumblr', '0012_comment_last_changed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='last_changed',
        ),
    ]