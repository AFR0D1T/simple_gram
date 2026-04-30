from rest_framework import serializers
from api import models


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id', 'author', 'image', 'description', 'created_at']


class PostCreateSerializer(PostBaseSerializer):
    class Meta(PostBaseSerializer.Meta):
        fields = ['author', 'image', 'description']


class PostListSerializer(PostBaseSerializer):
    class Meta(PostBaseSerializer.Meta):
        fields = ['id', 'image', 'description', 'author']


class PostDetailSerializer(PostBaseSerializer):
    likes = serializers.IntegerField()

    class Meta(PostBaseSerializer.Meta):
        fields = ['id', 'author', 'image', 'description', 'likes', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['user', 'post']
