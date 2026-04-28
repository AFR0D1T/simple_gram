from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from accounts.serizlizer import UserSerializer, LoginSerializer, PasswordSerializer
from rest_framework.decorators import action
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

    @action(detail=False, methods=['get'])
    def profile(self, request, *args, **kwargs):
        user = self.request.user
        data = {'id':user.pk,
                'username':user.username,
                'email':user.email
                }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def update_profile(self, request, *args, **kwargs):
        if not request.data:
            return Response({"status": 'No data'}, status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        serializers = UserSerializer(data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)

        user.username = serializers.validated_data.get('username')
        user.email = serializers.validated_data.get('email')

        return Response({'status': 'successfully'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def update_password(self, request, *args, **kwargs):
        user = self.request.user
        serializers = PasswordSerializer(data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)

        password_old = serializers.validated_data.get('password_old')
        password_new = serializers.validated_data.get('password_new')

        if user.check_password(password_old):
            user.set_password(password_new)
            user.save()
            return Response({'status': 'successfully'}, status=status.HTTP_200_OK)

        return Response({'status':'uncorrected data'}, status=status.HTTP_400_BAD_REQUEST)
