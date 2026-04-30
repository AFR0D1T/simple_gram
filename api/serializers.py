from rest_framework import serializers
from api import models
from rest_framework.exceptions import ValidationError


class PostBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Post
        fields = ['id', 'author', 'image', 'description', 'created_at']


class PostCreateSerializer(PostBaseSerializer):
    class Meta(PostBaseSerializer.Meta):
        fields = ['image', 'description']


class PostListSerializer(PostBaseSerializer):
    class Meta(PostBaseSerializer.Meta):
        fields = ['id', 'image', 'description', 'author']


class PostDetailSerializer(PostBaseSerializer):
    likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta(PostBaseSerializer.Meta):
        fields = ['id', 'author', 'image', 'description', 'likes', 'created_at']


class PostUpdateSerializer(PostBaseSerializer):
    class Meta(PostBaseSerializer.Meta):
        fields = ['author', 'image', 'description',]

    def validate(self, attrs):
        if not attrs:
            raise ValidationError("No data provided")

        fields = set(self.initial_data.keys()) - set(self.fields.keys())
        if fields:
            raise ValidationError(f'Unknow fields: {fields}')

        return attrs


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = ['user', 'post']
