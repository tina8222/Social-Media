from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (RegisterView,LoginView,LogoutView, MyProfileView)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
    path("refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("my-profile/", MyProfileView.as_view()),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("my-profile/", MyProfileView.as_view()),
]