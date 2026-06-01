from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import UserProfile


from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer
)

User = get_user_model()

class RegisterView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        login = serializer.validated_data["login"]
        password = serializer.validated_data["password"]

        user = (
            User.objects.filter(email=login).first()
            or User.objects.filter(username=login).first()
        )

        if user is None or not user.check_password(password):

            return Response(
                {
                    "detail": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(serializer.validated_data["refresh"])
            token.blacklist()
            return Response( 
                {
                    "detail": "Logged out successfully"
                },
                status=status.HTTP_200_OK,
            )
            
        except Exception:
            return Response(
                {
                    "detail":"Invalid refresh token"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

class MyProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        profile = request.user.user_profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(request.data, status=status.HTTP_200_OK)


class ProfileView(APIView):

    def get(self, request):
        username = request.GET.get("username")
        profile = get_object_or_404(UserProfile, user__username=username)
        serilizer = ProfileSerializer(instance=profile)
        if serilizer:
            return Response(serilizer.data, status=status.HTTP_200_OK)
        return Response(serilizer.data, status=status.HTTP_400_BAD_REQUEST)