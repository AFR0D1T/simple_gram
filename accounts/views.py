from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
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


class LoginViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        key = SECRET_KEY
        access_payload = {
            'token_type':'access',
            'exp': (datetime.now() + timedelta(minutes=55)).timestamp(),
            "iat": datetime.now().timestamp(),
            "jti": str(uuid.uuid4()),
            "user_id": user.pk
        }

        access_token = jwt.encode(access_payload, key, algorithm='HS256')

        refresh_payload = {
            'token_type': 'refresh',
            'exp': (datetime.now() + timedelta(minutes=55)).timestamp(),
            "iat": datetime.now().timestamp(),
            "jti": str(uuid.uuid4()),
            "user_id": user.pk
        }

        refresh_token = jwt.encode(refresh_payload, key, algorithm='HS256')

        contents = {"access":access_token, "refresh":refresh_token}
        return Response(contents, status=status.HTTP_200_OK)


class RefreshView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        token = request.data.get['refresh']
        key = SECRET_KEY

        try:
            decode = jwt.decode(token, key, algorithms='HS256')
        except jwt.ExpiredSignatureError as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

        if not decode.get('token_type') == 'refresh':
            return Response({"Error":"Token type not refresh"}, status=status.HTTP_400_BAD_REQUEST)

        if datetime.now().timestamp() > decode.get('exp'):
            return Response({'Error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_model().objects.get(pk=decode.get('user_id'))

        access_payload = {
            "token_type": "access",
            'exp': (datetime.now() + timedelta(minutes=55)).timestamp(),
            "iat": datetime.now().timestamp(),
            "jti": str(uuid.uuid4()),
            "user_id": user.pk
        }

        access_token = jwt.encode(access_payload, key, algorithm='HS256')

        return Response({'access': access_token}, status=status.HTTP_200_OK)
