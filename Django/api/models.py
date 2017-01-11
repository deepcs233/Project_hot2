from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Word(models.Model):

    content=models.CharField(max_length=20)

class Word_History(models.Model):
    word=models.ForeignKey(Word)
    history=models.TextField()

class Word_Detail(models.Model):
    word=models.ForeignKey(Word)
    hot = models.IntegerField()
    fromTopic=models.CharField(max_length=100)

class Topic(models.Model):
    conetent=models.CharField(max_length=10)
    hot = models.IntegerField()
    fromNews=models.TextField()

class News(models.Model):
    content=models.CharField(max_length=20)
    hot = models.IntegerField()
    fromTopic = models.CharField(max_length=100)
    url=models.CharField(max_length=100)

class UsertoUrl(models.Model):
    user=models.ForeignKey(User)
    url = models.CharField(max_length=100)

class UsertoWord(models.Model):
    user=models.ForeignKey(User)
    word=models.ForeignKey(Word)

class UsertoTopic(models.Model):
    user=models.ForeignKey(User)
    topic=models.ForeignKey(Topic)