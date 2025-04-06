from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = {
         'male': 'M',
         'female': 'F',
         'other': 'O'
    }
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True)
    interests = models.TextField(blank=True)
    profession = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    about = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)