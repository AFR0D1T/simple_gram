from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from accounts.serizlizer import UserSerializer, LoginSerializer
from core.settings import SECRET_KEY
from datetime import datetime, timedelta
import uuid
import jwt


class RegistrationViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MyProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        data = {'id':user.pk,
                'username':user.username,
                'email':user.email
                }
        return Response(data, status=status.HTTP_200_OK)
