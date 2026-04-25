from django.shortcuts import render
from rest_framework import generics, views, permissions
from rest_framework.response import Response
from accounts.models import User
from accounts.serizlizer import UserSerializer


# Create your views here.

class RegistrationView(generics.CreateAPIView):
    pass
