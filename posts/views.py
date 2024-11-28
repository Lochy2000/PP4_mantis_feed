from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib import messages 
from .models import Post, Comment
from django.db.models import Count

# Create your views here.

#display posts and comments

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    top_posts = Post.objects.annotate(
        total_score = Count('upvotes') - Count('downvotes')
    ).order_by('-total_score')[:5]

    return render(request, 'posts/post_list.html',{
        'posts' : posts,
        'top_posts' : top_posts
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

        if not all ([title.content]):
            messages.error(request,"Please fill in all fields.")
            return redirect('posts:post_create')

        try: 
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messages.success(request, "Post created successfully!")
            return redirect('posts:post_detail', post_id=post.id)
        except Exception as e:
            messages.error(request, f"Error creating post: {str(e)}")
            return redirect('posts:post_create')

    return render (request, 'post/post_form',{'post':post})

# update / edit posts
def post_edit(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    if request.user != post.author: 
        messages.error(request, "You can't edit this post.")
        return redirect('posts:post_detail', post_id = post.id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not all([title, content]):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                post.title = title 
                post.content = content 
                post.save()
                messages.success(request, "Post updated successfully")
                return redirect('posts:post_detail', post_id=post.id)
            except Exception as e:
                messages.error(request, f"Error updating post: {str(e)}")
            
    return render(request, 'post/post_form.html',{'post':post})

#Deleting posts
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "You cannot delete this post.")
        return redirect ('posts:post_detail', post_id=post.id)
    
    if request.method == 'Post':
        post.delete()
        messages.success(request, "Post succesfully deleted!")
        return redirect('posts:post_detial', post_id=post.id)
    
    return render(request, 'sts/post_confirm_delete.html', {'post' : post})




#--------- Comment Sections -----------
@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get ('content')
        parent_id = request.POST.get ('parent_id')

        if not content:
            messages.error(request, "Comment cannot be empty.")
            return redirect ('post:post_detail', post_id=post.id)
        
        try: 
            comment = Comment(
                post=post,
                author=request.user,
                conent=content
            )
            if parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_comment)
                comment.parents = parent_comment

            comment.save()
            messages.success(request, "Comment added successfully!")

        except Exception as e:
            messages.error(request, f"Error adding comment :{str(e)}")

    return redirect('post:post_detail', post_id=post.id)

#deleting comments
@login_required
def comment_delete(request, post_id,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user != comment.author:
        messages.error(request, "You cannot delete this comment!")
        return redirect('post:post_detail', post_id=post_id)
    try:
        comment.delete()
        messages.success(request, "Comment successfully deleted!")
    except Exception as e:
        messages.error(request, f"Errror deleting comment: {str(e)}")
    
    return redirect('post:post_detial', post_id=post_id)


#----------------- UP / DOWN Votes ----------------------------

@login_required 
def post_upvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.downvotes.remove(request.user)
    post.upvotes.add(request.user)
    return redirect('posts: post_detai', post_id=post_id)

@login_required
def post_downvote(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.upvotes.remove(request.user)
    post.downvotes.add(request.user)
    return redirect('posts: post_detai', post_id=post_id)
