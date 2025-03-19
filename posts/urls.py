from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    path('post/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    path('post/<int:post_id>/upvote', views.post_upvote, name='post_upvote'),
    path('post/<int:post_id>/downvote', views.post_downvote, name='post_downvote'),
]