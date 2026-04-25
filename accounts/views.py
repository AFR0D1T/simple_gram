from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from accounts.serizlizer import UserSerializer, LoginSerializer
from core.settings import SECRET_KEY
from datetime import datetime, timedelta
import uuid


class RegistrationViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        key = SECRET_KEY
        access_payload = {
            'token_type':'access',
            'exp': (datetime.now() + timedelta(seconds=15)).timestamp(),
            "iat": datetime.now().timestamp(),
            "jti": str(uuid.uuid4()),
            "user_id": user.pk
        }

        access_token = jwt.encode(access_payload, key, algorithm='HS256')
