from gc import get_objects

from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from api import serializers
from rest_framework import viewsets, permissions, status
from api.models import Post, Like
from api.serializers import PostUpdateSerializer


class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        serializer = serializers.PostListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = serializers.PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Post, id=pk)
        serializer = serializers.PostDetailSerializer(post)
        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        post = get_object_or_404(Post, id=pk)
        if post.author != self.request.user:
            return Response({'Error':"You don't have a license."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostUpdateSerializer(instance=post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'status': 'successfully'}, status=status.HTTP_200_OK)
