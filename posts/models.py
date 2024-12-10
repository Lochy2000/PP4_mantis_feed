from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone 


# Create your models here.
# ----- Categories  --------
class Category(models.Model):
    """
    This Model represents posts categories

    attributes :
        name (str) : name of the category (unique)
        description (textfield) : optional text to add
        created_at (datetime) : when the category is created

    """
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
    """
    Moder representing user posts

    Attributes: 
        Title (str) : post title
        content (textfield) : main content of post
        created_at (datetime) : when was the post created
        updated_at (datatime) : when was the post updated
        upvotes (manytomany) : tracks users upvotes
        downvotes (manytomany) : tracks users who down voted
        category (foreignkey / Category) : pick an optional category 
        status (str) : choose the current status of post (draft / published / removed )
    """
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

    STATUS_CHOICES = [ 
        ('draft','Draft'),
        ('published','Published'),
        ('removed','Removed')
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )

    class Meta:
        ordering = ['-created_at'] 

    def __str__(self):
        return self.title  
    
    def score(self):
        """
        Calculate posts score (upvotes - downvotes)

        Rreturns a int value for total score for posts
        """
        score = self.upvotes.count() - self.downvotes.count()
        print (f"calculating score for posts {self.id}:{score}")
        return score 
        
    
    def vote(self, user, direction):
        """
        handles voting logic. 
        
        user (User): user voting
        direction (str): vote direction (up or down)

        opposite vote is removed if it exisits before adding a new vote.

        """
        if direction == 'up':
            self.downvotes.remove(user)
            self.upvotes.add(user)
        elif direction == 'down':
            self.upvotes.remove(user)
            self.downvotes.add(user) 


# ----- Comments --------

class Comment(models.Model):
    """
    model represeting comments for posts

    attributes :
    contet (textfield): content for comment
    created_at (datetime): when was the comment created
    updated_at (datatime): when was the comment updated/edited
    posts (foreignkey: Post): which post the comment belongs to 
    parent(foreigKey: Comment): parents comment if there is a reply to the comment
    """
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
        """
        Get all replies to the comment. 
        Returns a queryset for all reply for the comment.
        """
        return self.replies.all()


