from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('register', views.RegistrationViewSet, basename='registration')
router.register('me', views.MyProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view())
]
