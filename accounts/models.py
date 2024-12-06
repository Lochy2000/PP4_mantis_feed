from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import reciever

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, blank=True)
    Karama = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def update_karama(self):
        post_karma = sum(post.sore() for post in self.user.posts.all())
        self.Karama  = post_karma
        self.save()

@reciever(post_save, sender=User)
def create_user_profile(send, instance, created, **kwargs):
    if created: 
        UserProfile.objects.create(user=instance)
@reciever(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()