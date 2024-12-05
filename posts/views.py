import os
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages 
from .models import Post, Comment, Category
from django.db.models import Count, F
from django.db.models.functions import Coalesce


# Create your views here.
# categories 
# def is_superuser(user):
#     return user.is_superuser

# @user_passes_test(is_superuser)
# def catergory_create(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         description = request.POST.get('description')

#         if not name: 
#             messages.error(request, "Category name is required.")
#             return redirect('posts:category_create')
        
#         try:
#             category = Category.objects.create(
#                 name=name,
#                 description=description
#             )
#             messages.success(request="Category successfully created.")
#             return redirect('posts:category_list')
#         except Exception as e:
#             messages.error(request, f"error creating category: {str(e)}")
#             return redirect('posts:category_create')
        
#     return render (request, 'posts/category_form.html')

# def category_list(request):
#     categories = Category.objects.all()
#     return render(request,'posts/category_list.hrml',{
#         'categories': categories
#     })

# def category_detail(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     posts =category.posts.all()
#     return render(request, 'posts/category_detail.html',{
#         'category':category,
#         'posts':posts
#     })


#display posts and comments

def post_list(request):
    category_id = request.GET.get('category')
    categories = Category.objects.all()

    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            posts = Post.objects.filter(category=selected_category).order_by('-created_at')
        except Category.DoesNotExist:
            selected_category = None
            posts = Post.objects.all().order_by('-created_at')
    else:
        selected_category = None
        posts = Post.objects.all().order_by('-created_at')


    #print("number of posts:", posts.count())
    #print("Posts:", [p.title for p in posts])

    top_posts = Post.objects.annotate(
        #total_score = Count('upvotes') - Count('downvotes')
        score=Coalesce(Count('upvotes', distinct=True),0) -
              Coalesce(Count('downvotes', distinct=True),0)  
    ).order_by('-score', 'created_at')[:3]

    try:
        news_api_key = os.environ.get('NEWS_API_KEY')
        news_url = f"https://gnews.io/api/v4/search?q=tech OR programming OR AI&lang=en&country=us&max=5&apikey={news_api_key}"

        print("API Key:", news_api_key)
        response = requests.get(news_url)
        news_data = response.json()
        news_articles = news_data.get ('articles',[])[:2]
    except: #Exception as e 
        #print(f'error fetch news {str(e)}')
        news_articles = [ ]

    return render(request, 'posts/post_list.html',{
        'posts' : posts,
        'top_posts' : top_posts,
        'categories':categories,
        'selected_category': selected_category,
        'news_articles' : news_articles
    })



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
                category=category
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

        if not all([title, content]):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                post.title = title 
                post.content = content
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
    post.downvotes.remove(request.user)
    post.upvotes.add(request.user)
    return redirect('posts:post_detail', post_id=post_id)

@login_required
def post_downvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes.remove(request.user)
    post.downvotes.add(request.user)
    return redirect('posts:post_detail', post_id=post_id)
