from django.urls import path

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    CommentListCreateAPIView,
    CommentDetailAPIView
)


urlpatterns = [

    # Posts
    path(
        'posts/',
        PostListAPIView.as_view(),
        name='post-list'
    ),

    path(
        'posts/<int:pk>/',
        PostDetailAPIView.as_view(),
        name='post-detail'
    ),

    # Comments
    path(
        'posts/<int:post_id>/comments/',
        CommentListCreateAPIView.as_view(),
        name='comment-list-create'
    ),

    path(
        'comments/<int:pk>/',
        CommentDetailAPIView.as_view(),
        name='comment-detail'
    ),

]