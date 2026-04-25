from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views

router = DefaultRouter()
router.register('register', views.RegistrationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
