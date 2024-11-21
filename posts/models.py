from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone 

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)

    class Meta:
        ordering = ['-created_at'] #orders posts form newest to oldest

    def __str__(self):
        return self.title  #returns blog title in admin panel
    
    def score(self):
        return self.upvotes.count() - self.downvotes.count() #this will calculate the most upvoted posts.
    
    def vote(self, user, direction): #handles voting logic. user presses up it removed any downvote they may have added and adds it to the upvote. 
        if direction == 'up':
            self.downvotes.remove(user)
            self.upvotes.add(user)
        elif direction == 'down':
            self.upvotes.remove(user)
            self.downvotes.add(user) 