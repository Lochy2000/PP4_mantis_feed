import os
import requests
import logging 

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import Coalesce

from django.contrib import messages 
from django.contrib.auth.decorators import login_required

from .models import Post, Comment, Category

# Create your views here.

def fetch_new_articles(request):
    """
    fetch news article api. GNew free api used.
    """
    try:
        news_api_key = os.environ.get('NEWS_API_KEY')
        if not news_api_key:
            messages.error(request, "unable to fetch news: API key not vonfigured")
            return[]

        news_url = f"https://gnews.io/api/v4/search?q=web+development+OR+javascript+OR+python&lang=en&max=5&apikey={news_api_key}"
        response = requests.get(news_url)
        response.raise_for_status()
        return response.json().get('articles',[])[:4]
    
    except Exception as e:
        messages.warning(request, "unable to load news")
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

    #checking status
    
    if request.user.is_staff:
        base_query = Post.objects.all() 
    else:
        base_query = Post.objects.filter(status='published')

    #applying categories, if required
    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            base_query = base_query.filter(category=selected_category)
            messages.success(request, F"Showing posts in category: {selected_category.name}")
        except Category.DoesNotExist:
            messages.warning(request, "Selected category has not been found.")

    #page ordering
    try:
        posts = base_query.order_by('-created_at')
        if not posts.exists():
            messages.info(request, "no posts found matching you criteria.")

        top_posts = base_query.annotate(
            score=Coalesce(Count('upvotes', distinct=True),0) -
                Coalesce(Count('downvotes', distinct=True),0)  
        ).order_by('-score', 'created_at')[:3]

    except Exception as e:  
        messages.error(request, "threre was an error retriveing posts. Please try again later.")
        posts = Post.objects.none()
        top_posts =[]

    #fetcj newsapi
    news_articles = fetch_new_articles(request)

    context = {
        'posts' : posts,
        'top_posts' : top_posts,
        'categories': Category.objects.all(),
        'selected_category': selected_category,
        'news_articles' : news_articles
    }

    return render(request, 'posts/post_list.html', context)


def post_detail(request, post_id):
    """
    Display a specific post and its comments.

    arguments:
        request
        post_id
    returns:
        post = get_object_or_404(Post, id = post_id)
    Raises: http404 if not found
    """

    try:
        post = get_object_or_404(Post,id=post_id)
        if post.status != 'published' and not request.user.is_staff and request.user != post.authot:
            messages.error(request, "you do not have permison to view this post")
            return redirect('posts:post_list')
        
        comments = post.comments.filter(parents=None)
        
        if not comments.exists():
            messages.info(request, "no comments yet! why not be the first?")

        return render(request, 'posts/post_detail.html',{
            'post': post,
            'comments' : comments
        })
    
    except Exception as e:
        messages.error(request, "Error loading post form. Please try again later.")
        return redirect('posts:post_list')

#create posts
@login_required 
def post_create(request):
    """
    Create a new post.

    Arguments:
            request: http

    returns:
            rendered post from template or redirects to post details
    """
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
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.warning(request, "selected category not found. Post will be created without a category.")

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
        
    #Display an empty form
    try:
        categories =Category.objects.all()
        if not categories.exists():
            messages.info(request,"no categoires avaliable.")

        return render (request, 'posts/post_form.html', {
            'post': None,
            'categories': categories
        })
    
    except Exception as e:
        messages.error(request, "Error loading post form. Please try again later.")
        return redirect('posts:post_list')
    

# update / edit posts
def post_edit(request, post_id):
    """
    Edit created posts 

    arguments :
        request:http request object
        post_id: id of the post that wants to be edited 
    
    returns:
        shows post form temlpate or redirects to post details
    """

    try:
        post = get_object_or_404(Post, id = post_id)

        if request.user != post.author and or not request.user.is.is_staff: 
            messages.error(request, "You can't edit this post.")
            return redirect('posts:post_detail', post_id = post.id)

        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category')
            status = request.POST.get('status')

            if not title:
                messages.error(request,"Post title cannot be empty!")
                return render(request, 'post/post_form.html',{
                    'post':post,
                    'categories': Category.objects.all()
                })
            if not content:
                messages.error(request, "Post content cannot be empty")
                return render(request, 'post/post_form.html',{
                    'post':post,
                    'categories': Category.objects.all()
                })
            
            try:
                post.title = title 
                post.content = content
                post.status = status
                if category_id:
                    try:
                        post.category = Category.objects.get(id=category_id)
                    except Category.DoesNotExist:
                        messages.warning(request, "selected category was not found.")
                else:
                    post.category = None
                post.save()
                messages.success(request, "Post updated successfully")
                return redirect('posts:post_detail', post_id=post.id)

            except Exception as e:
                messages.error(request, f"Error updating post: {str(e)}")

        categories = Category.objects.all()    
        return render(request, 'posts/post_form.html',{
            'post':post,
            'categories':categories
            })
    
    except Exception as e:
        messages.error(request, "Error accessing post. Try again later, please.")
        return redirect ('posts:post_list')
        

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
