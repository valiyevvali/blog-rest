from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=60)
    content=models.TextField()