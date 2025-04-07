import os
import requests

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Category


def fetch_new_articles(request):
    """
    fetch news article api. GNew free api used.
    """
    try:
        news_api_key = os.environ.get('NEWS_API_KEY')
        if not news_api_key:
            messages.error(request, "Unable to fetch news: API key not configured")
            return []

        url_base = "https://gnews.io/api/v4/search"
        query = "web+development+OR+javascript+OR+python"
        news_url = f"{url_base}?q={query}&lang=en&max=5&apikey={news_api_key}"
        response = requests.get(news_url)
        response.raise_for_status()
        return response.json().get('articles', [])[:4]
    except Exception:
        messages.warning(request, "Unable to load news")
        return []

# Display posts and comments

def post_list(request):
    """
    Displays lists of posts, top posts, new api and category section
    
    request : HTTP request object

    returns : rendered post list template + its context
    """

    category_id = request.GET.get('category')

    # Get all posts
    base_query = Post.objects.all()

    if not request.user.is_staff:
        base_query = base_query.filter(status='published')

    # Get all posts sorted by creation date
    all_posts = list(base_query)
    
    # Sort posts by score (using the score method) and then by creation date
    all_posts.sort(key=lambda post: (-post.score(), -post.created_at.timestamp()))
    
    # Get the top 3 posts
    top_posts = all_posts[:3]
    

    selected_category = None
    if category_id:
        try:
            selected_category = Category.objects.get(id=category_id)
            base_query = base_query.filter(category=selected_category)
            messages.success(request, f"Showing posts in category: {selected_category.name}")
        except Category.DoesNotExist:
            messages.warning(request, "Selected category has not been found.")

    try:
        posts = base_query.order_by('-created_at')
        if not posts.exists():
            messages.info(request, "No posts found matching your criteria.")

    except Exception:
        messages.error(request, "There was an error retrieving posts. Please try again later.")
        posts = Post.objects.none()
        top_posts = []


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
        post = get_object_or_404(Post, id=post_id)
    Raises: http404 if not found
    """

    try:
        # Get the post by ID
        post = get_object_or_404(Post, id=post_id)
        
        # Calculate score using the model's score method
        # This will ensure consistent score calculation across the app

        if post.status != 'published' and not request.user.is_staff and request.user != post.author:
            messages.error(request, "You do not have permission to view this post")
            return redirect('posts:post_list')
        
        comments = post.comments.filter(parent=None).order_by('-created_at')
        
        if not comments.exists():
            messages.info(request, "No comments yet! Why not be the first?")

        context = {
            'post': post,
            'comments': comments
        }

        return render(request, 'posts/post_detail.html', context)
    
    except Exception:
        messages.error(request, "Error loading post form. Please try again later.")
        return redirect('posts:post_list')

# Create posts


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
            messages.error(request, "Please fill in all fields.")
            return redirect('posts:post_create')

        try:
            category = None
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                except Category.DoesNotExist:
                    messages.warning(request, "Selected category not found. Post will be created without a category.")

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
        
    # Display an empty form
    try:
        categories = Category.objects.all()
        if not categories.exists():
            messages.info(request, "No categories available.")

        return render(request, 'posts/post_form.html', {
            'post': None,
            'categories': categories
        })
    except Exception:
        messages.error(request, "Error loading post form. Please try again later.")
        return redirect('posts:post_list')
    

# Update / edit posts


def post_edit(request, post_id):
    """
    Edit created posts

    Arguments:
        request: HTTP request object
        post_id: ID of the post that wants to be edited 
    
    Returns:
        Shows post form template or redirects to post details
    """

    try:
        post = get_object_or_404(Post, id=post_id)

        if request.user != post.author and not request.user.is_staff:
            messages.error(request, "You can't edit this post.")
            return redirect('posts:post_detail', post_id=post.id)

        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            category_id = request.POST.get('category')
            status = request.POST.get('status')

            if not title:
                messages.error(request, "Post title cannot be empty!")
                return render(request, 'post/post_form.html', {
                    'post': post,
                    'categories': Category.objects.all()
                })
            if not content:
                messages.error(request, "Post content cannot be empty")
                return render(request, 'post/post_form.html', {
                    'post': post,
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
                        messages.warning(request, "Selected category was not found.")
                else:
                    post.category = None
                post.save()
                messages.success(request, "Post updated successfully")
                return redirect('posts:post_detail', post_id=post.id)

            except Exception as e:
                messages.error(request, f"Error updating post: {str(e)}")

        categories = Category.objects.all()
        return render(request, 'posts/post_form.html', {
            'post': post,
            'categories': categories
            })
    
    except Exception:
        messages.error(request, "Error accessing post. Try again later, please.")
        return redirect('posts:post_list')
        

# Deleting posts
@login_required
def post_delete(request, post_id):
    """
    Delete existing posts

    Args:
        request: HTTP request object
        post_id: ID of the post to be deleted
    
    Returns:
        Post_confirm_delete template or redirects to post list
    """
    try:
        post = get_object_or_404(Post, id=post_id)

        if request.user != post.author:
            messages.error(request, "You cannot delete this post.")
            return redirect('posts:post_detail', post_id=post.id)
        
        if request.method == 'POST':
            try:
                title = post.title
                post.delete()
                messages.success(request, f"Post '{title}' succesfully deleted!")
                return redirect('posts:post_list')
            except Exception:
                messages.error(request, "Error accessing post. Try again later, please.")
                return redirect('posts:post_list', post_id=post.id)
            
        return render(request, 'posts/post_confirm_delete.html', {
            'post': post
            })
    
    except Exception:
        messages.error(request, "Error accessing post. Try again later, please.")
        return redirect('posts:post_list')


# --------- Comment Sections -----------


@login_required
def comment_create(request, post_id):
    """
    Creates a new comment on a post

    Args:
        request: HTTP request object
        post_id: ID of the post to comment on
    Returns:
        Redirects to post detail page
    """
    try:
        post = get_object_or_404(Post, id=post_id)

        if post.status == "removed":
            messages.error(request, "You cannot comment on this post.")
            return redirect('posts:post_detail', post_id=post.id)

        if request.method == 'POST':
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')

            if not content:
                messages.error(request, "Comment cannot be empty.")
                return redirect('posts:post_detail', post_id=post.id)
            if len(content) > 500:
                messages.error(request, "Comment is too long. Please keep it under 500 characters.")
                return redirect('posts:post_detail', post_id=post.id)
            
            try:
                comment = Comment(post=post,
                                   author=request.user,
                                   content=content)
                if parent_id:
                    try:
                        parent_comment = get_object_or_404(Comment, id=parent_id)

                        if parent_comment.post != post:
                            raise ValueError("Invalid parent comment")
                        if parent_comment.parent:
                            messages.error(request, "Cannot reply to a reply")
                            return redirect('posts:post_detail', post_id=post.id)
                            
                        # Only set parent if all checks pass
                        comment.parent = parent_comment
                        messages.success(request, "Reply added successfully!")
                    except Comment.DoesNotExist:
                        messages.error(request, "Invalid parent comment")
                        return redirect('posts:post_detail', post_id=post.id)
                    
                else:
                    messages.success(request, "Comment added successfully!")

                comment.save()
            

            except Exception as e:
                messages.error(request, f"Error adding comment :{str(e)}")

        return redirect('posts:post_detail', post_id=post.id)
    
    except Exception:
        messages.error(request, "Error accessing post. Try again later, please.")
        return redirect('posts:post_list')

# Deleting comments


@login_required
def comment_delete(request, post_id, comment_id):
    """
    Delete existing comments

    Args:
        request: HTTP request object
        post_id: ID of the post the comment belongs to 
        comment_id: ID of the comment to delete

    Returns: 
        Redirects to post detail page
    """

    try:
        comment = get_object_or_404(Comment, id=comment_id)

        if request.user != comment.author and not request.user.is_staff:
            messages.error(request, "You cannot delete this comment!")
            return redirect('posts:post_detail', post_id=post_id)
        try:
            replies_exist = comment.replies.exists()
            if replies_exist:
                comment.content = "[comment deleted]"
                comment.save()
                messages.success(request, "Comment marked as deleted.")
            else:
                comment.delete()
                messages.success(request, "Comment successfully deleted!")

        except Exception as e:
            messages.error(request, f"Error deleting comment: {str(e)}")
        
        return redirect('posts:post_detail', post_id=post_id)
    
    except Comment.DoestNotExist:
        messages.error(request, "Comment not found")
        return redirect('posts:post_detail', post_id=post_id)
    except Exception:
        messages.error(request, "Error accessing post. Try again later, please.")
        return redirect('posts:post_list')

# ----------------- UP / DOWN Votes ----------------------------

@login_required
def post_upvote(request, post_id):
    """
    Handle upvoting a post
    
    Args: 
        request: HTTP request object
        post_id: ID of the post to upvote
    Returns:
        Redirect to post details
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        
        # Check post status and user permission
        if post.status == 'removed':
            messages.error(request, "Cannot vote on this post")
            return redirect('posts:post_detail', post_id=post_id)
        if request.user == post.author:
            messages.warning(request, "You cannot vote on your own post.")
            return redirect('posts:post_detail', post_id=post_id)
        
        # Check if user already has votes
        user_has_upvoted = request.user in post.upvotes.all()
        user_has_downvoted = request.user in post.downvotes.all()
        
        # Remove downvote if exists
        if user_has_downvoted:
            post.downvotes.remove(request.user)
            messages.info(request, "Your downvote has been removed.")
        
        # Toggle upvote
        if user_has_upvoted:
            post.upvotes.remove(request.user)
            messages.success(request, "Upvote removed successfully.")
        else:
            post.upvotes.add(request.user)
            messages.success(request, "Post upvoted successfully.")
        
        # Update karma
        try:
            post.author.userprofile.update_karma()
        except Exception as e:
            print(f"Error updating karma: {str(e)}")
            # Don't show karma error to the user, just log it
            
        return redirect('posts:post_detail', post_id=post_id)
    
    except Exception as e:
        print(f"Error processing vote: {str(e)}")
        messages.error(request, "Error processing vote. Please try again.")
        return redirect('posts:post_detail', post_id=post_id)

@login_required
def post_downvote(request, post_id):
    """
    Handle downvotes

    Args:
        request: HTTP request object
        post_id: ID of the post to downvote
    Returns: 
        Redirect to post detail page
    """
    try:
        post = get_object_or_404(Post, id=post_id)

        if post.status == 'removed':
            messages.error(request, "Cannot vote on this post")
            return redirect('posts:post_detail', post_id=post_id)
        if request.user == post.author:
            messages.warning(request, "You cannot vote on your own post.")
            return redirect('posts:post_detail', post_id=post_id)
        
        # Check if user already has votes
        user_has_upvoted = request.user in post.upvotes.all()
        user_has_downvoted = request.user in post.downvotes.all()
        
        # Remove upvote if exists
        if user_has_upvoted:
            post.upvotes.remove(request.user)
            messages.info(request, "Your upvote has been removed.")
        
        # Toggle downvote
        if user_has_downvoted:
            post.downvotes.remove(request.user)
            messages.success(request, "Downvote removed successfully.")
        else:
            post.downvotes.add(request.user)
            messages.success(request, "Post downvoted successfully.")
        
        # Update karma
        try:
            post.author.userprofile.update_karma()
        except Exception as e:
            print(f"Error updating karma: {str(e)}")
            # Don't show karma error to the user, just log it
            
        return redirect('posts:post_detail', post_id=post_id)
    
    except Exception as e:
        print(f"Error processing vote: {str(e)}")
        messages.error(request, "Error processing vote. Please try again.")
        return redirect('posts:post_detail', post_id=post_id)
