from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone 


# Create your models here.
# ----- Categories  --------

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

# ----- Post --------
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ('draft','Draft'),
            ('published','Published'),
            ('removed','Removed')
        ],
        default='published'
    )

    class Meta:
        ordering = ['-created_at'] #orders posts form newest to oldest

    def __str__(self):
        return self.title  #returns blog title in admin panel
    
    def score(self):
        score = self.upvotes.count() - self.downvotes.count()
        print (f"calculating score for posts {self.id}:{score}")
        return score #this will calculate the most upvoted posts.
        
    
    def vote(self, user, direction): #handles voting logic. user presses up it removed any downvote they may have added and adds it to the upvote. 
        if direction == 'up':
            self.downvotes.remove(user)
            self.upvotes.add(user)
        elif direction == 'down':
            self.upvotes.remove(user)
            self.downvotes.add(user) 


# ----- Comments --------

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    update_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parents = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")

    class Meta: 
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def get_replies(self):
        return self.replies.all()


