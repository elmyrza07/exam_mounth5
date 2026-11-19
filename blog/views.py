from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


# POSTS

class PostListAPIView(generics.ListCreateAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.select_related('author').order_by('-created_at')

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_published=True) |
                Q(author=self.request.user)
            ).distinct()

        return queryset.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = PostSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        queryset = Post.objects.select_related('author')

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_published=True) |
                Q(author=self.request.user)
            ).distinct()

        return queryset.filter(is_published=True)


# COMMENTS

class CommentListCreateAPIView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get_post(self):
        queryset = Post.objects.all()

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(is_published=True) |
                Q(author=self.request.user)
            )
        else:
            queryset = queryset.filter(is_published=True)

        return get_object_or_404(
            queryset,
            pk=self.kwargs['post_id']
        )

    def get_queryset(self):
        post = self.get_post()

        queryset = Comment.objects.filter(
            post=post
        ).select_related('author', 'post').order_by('-created_at')

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_approved=True) |
                Q(author=self.request.user) |
                Q(post__author=self.request.user)
            ).distinct()

        return queryset.filter(is_approved=True)

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs['post_id'],
            is_published=True
        )

        serializer.save(
            author=self.request.user,
            post=post
        )


# COMMENT DETAIL

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CommentSerializer

    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        queryset = Comment.objects.select_related(
            'author',
            'post'
        )

        if self.request.user.is_authenticated:
            return queryset.filter(
                Q(is_approved=True) |
                Q(author=self.request.user) |
                Q(post__author=self.request.user)
            ).distinct()

        return queryset.filter(is_approved=True)