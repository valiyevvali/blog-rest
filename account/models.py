from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    note=models.CharField(max_length=150)
    twitter=models.CharField(max_length=150)

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    print(sender)
    print(instance)
    print(created)
    print(kwargs)
    if created:
        Profile.objects.create(user=instance)
    print(instance.profile)
    print(instance.username)
    instance.profile.save()

