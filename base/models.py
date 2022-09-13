
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Post(models.Model):
    topic = models.ForeignKey(Topic,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=150)
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete= models.CASCADE,        
    )
    timeUpdated = models.DateTimeField(auto_now_add=True)
    timeCreated = models.DateTimeField(auto_created=True,auto_now_add=True)
    class Meta:
        ordering = ('-timeUpdated','-timeCreated')    
    def __str__(self):
        return self.title    
class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body = models.TextField(max_length=250)
    timeCreated = models.DateTimeField(auto_created=True,auto_now_add=True)
    class Meta:
        ordering = ('-timeCreated',)
    def __str__(self):
        return self.body[0:50]
