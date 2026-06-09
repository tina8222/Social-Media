from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .services import register_user, login_user

from .models import UserProfile, Follow, FollowRequest, RestrictUser
from .validators import validator_target_user
from .paginations import FollowListPaginations, RestrictedUsersListPagination
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    FollowersListSerializer,
    FollowingListSerializer,
    FollowersCountSerializer,
    FollowingCountSerializer,
    RestrictUserSerializer,
)


User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        register = register_user(validated_data=serializer.validated_data)

        response = {
            "access": register["access"],
            "refresh": register["refresh"]
        }
        return Response(response, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        login = login_user(validated_data=serializer.validated_data)
        return Response(login, status=status.HTTP_200_OK)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated,]

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

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        serializer = ProfileSerializer(request.user.user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):

    permission_classes = [IsAuthenticated,]

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

    permission_classes = [IsAuthenticated,]

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

    permission_classes = [IsAuthenticated,]

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
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        users = Follow.objects.filter(following=request.user).select_related("follower").order_by("-created_at")
        serializer = FollowersListSerializer(instance=users, many=True)
        return Response(serializer.data)


class FollowingListView(ListAPIView):
    pagination_class = FollowListPaginations
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        users = Follow.objects.filter(follower=request.user).select_related("following").order_by("-created_at")
        serializer = FollowingListSerializer(instance=users, many=True)
        return Response(serializer.data)


class FollowRequestView(APIView):
    permission_classes = [IsAuthenticated,]

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

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        username = request.query_params.get("username")
        target_user = validator_target_user(username)
        followers_count = Follow.objects.filter(following=target_user).count()

        data = {
            "username": target_user.username,
            "followers_count": followers_count
        }

        serializer = FollowersCountSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowingCountView(APIView):

    permission_classes = [IsAuthenticated,]

    def get(self, request):
        username = request.query_params.get("username")
        target_user = validator_target_user(username)
        following_count = Follow.objects.filter(follower=target_user).count()

        data = {
            "username": target_user.username,
            "following_count": following_count
        }

        serializer = FollowingCountSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RestrictUserView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):
        username = request.query_params.get("username")
        target_user = validator_target_user(username)
        if target_user == request.user:
            error_cannot_restrict_yourself = {"error": "you cannot restrict yourself"}
            return Response(error_cannot_restrict_yourself, status=status.HTTP_400_BAD_REQUEST)

        restrict_user_obj, created = RestrictUser.objects.get_or_create(user=request.user, restricted_user=target_user)
        if created == False:
            error_restricted_before = {"error": "you restricted this user before"}
            return Response(error_restricted_before, status=status.HTTP_400_BAD_REQUEST)

        serializer = RestrictUserSerializer(instance=restrict_user_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # comments get restrict
        # have restricted activity

class UnrestrictUserView(APIView):

    permission_classes = [IsAuthenticated,]

    def delete(self, request):
        username = request.query_params.get("username")
        target_user = validator_target_user(username)
        restrict_query = RestrictUser.objects.get(user=request.user, restricted_user=target_user)
        if restrict_query:
            restrict_query.delete()
            message = {"detail": f"{target_user.username} unrestricted!"}
            return Response(message, status=status.HTTP_200_OK)


class RestrictedUsersListView(ListAPIView):
    pagination_class = RestrictedUsersListPagination
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        restricted_users = RestrictUser.objects.filter(user=request.user)
        serializer = RestrictUserSerializer(instance=restricted_users, many=True)
        return Response(serializer.data)

    def delete(self, request):
        restricted_users = RestrictUser.objects.filter(user=request.user)
        usernames = request.query_params.getlist("username")
        deleted, _ = RestrictUser.objects.filter(user=request.user, restricted_user__username__in=usernames).delete()
        deleted_text_detail = {"detail": "selected users unrestricted"}
        return Response(deleted_text_detail, status=status.HTTP_200_OK)