from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import listView, DetailView, CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTextMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonRepsonse
from django.urls import reverse_lazy, reverse
from django.contrib import messages 
from .models import Posts, comment
from django.db.models import count

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
def Post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not all ([title.content]):
            messages.error(request,"Please fill in all fields.")
            return redirct('posts:post_create')

        try: 
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            messges.success(request, "Post created successfully!")
            return redirect('posts:post_detail', post_id=post.id)
        except Exception as e:
            messages.error(request, f"Error creating post: {str(e)}")
            return redirct('posts:post_create')

    return render (request, 'post/post_form',{'post':post})
# update / edit posts
def post_edit(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    if request.user != post.author: 
        messages.error(request, "You can't edit this post.")
        return redirect('posts:post_detail', post_id = post.id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = reuqest.POST.get('content')

        if nto all([title, content]):
            messages.error(reques, "Please fill in all fields.")
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