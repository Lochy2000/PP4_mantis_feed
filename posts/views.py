import os
import requests
import logging 

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import Coalesce

from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Comment, Category
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def fetch_new_articles():
    """
    fetch news article api. GNew free api used.
    """
    try:
        news_api_key = os.environ.get('NEWS_API_KEY')
        if not news_api_key:
            raise ValueError("News API Key not found")

        news_url = f"https://gnews.io/api/v4/search?q=web+development+OR+javascript+OR+python&lang=en&max=5&apikey={news_api_key}"
        response = requests.get(news_url)
        response.raise_for_status()
        return response.json().get('articles',[])[:4]  
    except Exception as e:
        logger.error(f"Error fetching new: {str(e)}")
        return []

#display posts and comments

def post_list(request):
    """
    Displays lists of posts, top posts, new api and category section
    
    request : HTTP request object

    returns : rendered post list template + its context
    """
    #query parameters
    category_id = request.GET.get('category')
    page_number = request.GET.get('page', 1)

    #checking status
    base_query = Post.objects.all() if request.user.is_staff else Post.objects.filter(status='published')

    #applying categories, if required
    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            posts = base_query.filter(category=selected_category)
        except Category.DoesNotExist:
            messages.warning(request, "Selected category has not been found.")

    #page ordering
    posts = base_query.order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page_number)

    top_posts = base_query.annotate(
        score=Coalesce(Count('upvotes', distinct=True),0) -
              Coalesce(Count('downvotes', distinct=True),0)  
    ).order_by('-score', 'created_at')[:3]

    #fetcj newsapi
    news_articles = fetch_new_articles()

    context = {
        'page_obj' : page_obj,
        'posts' : posts,
        'top_posts' : top_posts,
        'categories': Category.objects.all(),
        'selected_category': selected_category,
        'news_articles' : news_articles
    }

    return render(request, 'posts/post_list.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    comments = post.comments.filter(parents=None)
    

    return render(request, 'posts/post_detail.html',{
        'post': post,
        'comments' : comments
    })

#create posts
@login_required 
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        status = request.POST.get('status')

        if not all([title, content]):
            messages.error(request,"Please fill in all fields.")
            return redirect('posts:post_create')

        try: 
            category = None 
            if category_id:
                category = Category.objects.get(id=category_id)

            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user,
                category=category,
                status=status or 'published'
            )
            messages.success(request, "Post created successfully!")
            return redirect('posts:post_detail', post_id=post.id)
        except Exception as e:
            messages.error(request, f"Error creating post: {str(e)}")
            return redirect('posts:post_create')
        
    #post = None
    categories =Category.objects.all()
    return render (request, 'posts/post_form.html', {
        'post': None,
        'categories': categories
    })

# update / edit posts
def post_edit(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    categories = Category.objects.all()

    if request.user != post.author: 
        messages.error(request, "You can't edit this post.")
        return redirect('posts:post_detail', post_id = post.id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        status = request.POST.get('status')

        if not all([title, content]):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                post.title = title 
                post.content = content
                post.status = status
                if category_id:
                    post.category = Category.objects.get(id=category_id)
                else:
                    post.category = None
                post.save()
                messages.success(request, "Post updated successfully")
                return redirect('posts:post_detail', post_id=post.id)
            except Exception as e:
                messages.error(request, f"Error updating post: {str(e)}")
            
    return render(request, 'posts/post_form.html',{
        'post':post,
        'categories':categories
        })

#Deleting posts
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "You cannot delete this post.")
        return redirect ('posts:post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post succesfully deleted!")
        return redirect('posts:post_list')
    
    return render(request, 'posts/post_confirm_delete.html', {'post' : post})




#--------- Comment Sections -----------
@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get ('content')
        parent_id = request.POST.get ('parent_id')

        if not content:
            messages.error(request, "Comment cannot be empty.")
            return redirect ('posts:post_detail', post_id=post.id)
        
        try: 
            comment = Comment(
                post=post,
                author=request.user,
                content=content
            )
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                comment.parent = parent_comment

            comment.save()
            messages.success(request, "Comment added successfully!")

        except Exception as e:
            messages.error(request, f"Error adding comment :{str(e)}")

    return redirect('posts:post_detail', post_id=post.id)

#deleting comments
@login_required
def comment_delete(request, post_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        messages.error(request, "You cannot delete this comment!")
        return redirect('posts:post_detail', post_id=post_id)
    try:
        comment.delete()
        messages.success(request, "Comment successfully deleted!")
    except Exception as e:
        messages.error(request, f"Errror deleting comment: {str(e)}")
    
    return redirect('posts:post_detail', post_id=post_id)


#----------------- UP / DOWN Votes ----------------------------

@login_required 
def post_upvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post.downvotes.remove(request.user)
        post.upvotes.add(request.user)
        post.author.userprofile.update_karma()
        print(f"new karma total: {post.author.userprofile.karma}")
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def post_downvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post.upvotes.remove(request.user)
        post.downvotes.add(request.user)
        post.author.userprofile.update_karma()  
    return redirect('posts:post_detail', post_id=post_id)
