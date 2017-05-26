from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class UserPostInfo(models.Model):
    user = models.ForeignKey(User)
    email = models.CharField(max_length=100)
    acceptPost = models.IntegerField()
    update_time = models.DateTimeField(auto_now_add=True)


class UserWatchTag(models.Model):
    user = models.ForeignKey(User)
    word = models.CharField(max_length=10)


class UserBrowseNews(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=100)
    update_time = models.DateTimeField(auto_now_add=True)
