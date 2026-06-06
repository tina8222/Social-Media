from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from yaml import serialize

from .models import UserProfile, Follow, FollowRequest
from .validators import validator_target_user
from .paginations import FollowListPaginations

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    FollowersListSerializer,
    FollowingListSerializer,
    FollowersCountSerializer
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


class FollowUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.query_params.get("username")
        if not username:
            error_username_required = {"error": "username is required"}
            return Response(error_username_required, status=status.HTTP_400_BAD_REQUEST)

        target_user = validator_target_user(username)
        if request.user == target_user:
            error_follow_yourself = {"error": "you cannot follow yourself"}
            return Response(error_follow_yourself, status=status.HTTP_400_BAD_REQUEST)

        already_follow = Follow.objects.filter(follower=request.user, following=target_user).first()
        if already_follow:
            error_already_follow = {"error": "you already follow this user"}
            return Response(error_already_follow, status=status.HTTP_400_BAD_REQUEST)

        already_requested = FollowRequest.objects.filter(from_user=request.user, to_user=target_user).first()
        if already_requested:
            error_already_requested = {"error": "follow request already sent"}
            return Response(error_already_requested, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(follower=request.user, following=target_user, status=Follow.FollowStatus.PENDING)

        created_detail_text = {"detail": "Follow request sent"}
        return Response(created_detail_text, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        username = request.query_params.get("username")
        if not username:
            error_username_required = {"error": "username is required"}
            return Response(error_username_required, status=status.HTTP_400_BAD_REQUEST)

        target_user = validator_target_user(username)

        following = Follow.objects.filter(follower=request.user, following=target_user).first()
        request_follow = FollowRequest.objects.filter(from_user=request.user, to_user=target_user)

        if not following:
            error_not_follow = {"error": "you are not following this user"}
            return Response(error_not_follow, status=status.HTTP_400_BAD_REQUEST)

        request_follow.delete()
        following.delete()
        delete_detail = {"detail": "success"}
        return Response(delete_detail, status=status.HTTP_200_OK)


class FollowersListView(ListAPIView):
    pagination_class = FollowListPaginations
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = Follow.objects.filter(following=request.user).order_by("-created_at")
        serializer = FollowersListSerializer(instance=users, many=True)
        if not serializer:
            return Response(serializer.errors)
        return Response(serializer.data)


class FollowingListView(ListAPIView):
    pagination_class = FollowListPaginations
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = Follow.objects.filter(follower=request.user).order_by("-created_at")
        serializer = FollowingListSerializer(instance=users, many=True)
        if not serializer:
            return Response(serializer.errors)
        return Response(serializer.data)


class FollowRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.query_params.get("username")
        target_user = get_object_or_404(User, username=username)

        if request.user == target_user:
            error_request_yourself = {"error": "you cannot send follow request to yourself"}
            return Response(error_request_yourself, status=status.HTTP_400_BAD_REQUEST)

        already_requested = FollowRequest.objects.filter(from_user=request.user, to_user=target_user).first()
        if already_requested:
            error_already_requested = {"error": "follow request already sent"}
            return Response(error_already_requested, status=status.HTTP_400_BAD_REQUEST)

        FollowRequest.objects.create(from_user=request.user, to_user=target_user, )
        detail_request_sent = {"detail": "follow request sent"}
        return Response(detail_request_sent, status=status.HTTP_201_CREATED)


class UserFollowersCountView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        username = request.query_params.get("username")
        target_user = validator_target_user(username)
        followers_count = Follow.objects.filter(following=target_user).count()

        data = {
            "username": target_user.username,
            "followers_count": followers_count
        }

        serializer = FollowersCountSerializer(data)
        return Response(serializer.data)