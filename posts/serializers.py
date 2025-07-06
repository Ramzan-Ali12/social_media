from typing import __all__
from rest_framework import serializers
from .models import Post, Like
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']  # Make sure 'author' is included here

    def get_like_count(self, obj):
        return obj.likes.count()

class LikeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'author', 'post', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
