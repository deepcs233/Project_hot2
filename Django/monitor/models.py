from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserToUrls(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(max_length=100)
    update_time  = models.DateTimeField(auto_now_add=True)
