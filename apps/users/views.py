from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .validators import validator_target_user
from .services import *
from .selectors import get_my_profile, get_followers_list, get_following_list, get_restricted_users,get_blocked_users
from .models import FollowRequest
from .paginations import FollowListPaginations, RestrictedUsersListPagination,BlockedUsersListPagination
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProfileSerializer,
    FollowersListSerializer,
    FollowingListSerializer,
    RestrictUserSerializer,
    BlockUserSerializer,
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
        logout = logout_user(validated_data=serializer.validated_data)
        return Response(logout, status=status.HTTP_200_OK)


class MyProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        my_profile = get_my_profile(user=request.user)
        serializer = ProfileSerializer(my_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def put(self, request):
        profile = get_my_profile(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        profile = update_profile(profile=profile, validated_data=serializer.validated_data)

        updated_serializer = ProfileSerializer(profile)
        return Response(updated_serializer.data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        username = request.GET.get("username")
        profile = check_user_profile(username=username)
        serilizer = ProfileSerializer(instance=profile)
        return Response(serilizer.data, status=status.HTTP_200_OK)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        username = request.query_params.get("username")
        follow = follow_user(user=request.user, target_username=username)
        return Response(follow, status=status.HTTP_201_CREATED)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated,]
    def delete(self, request):
        username = request.query_params.get("username")
        unfollow = unfollow_user(user=request.user, target_username=username)
        return Response(unfollow, status=status.HTTP_200_OK)


class FollowersListView(ListAPIView):
    pagination_class = FollowListPaginations
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        username = request.query_params.get("username")
        user = get_user_by_email_or_username(username)
        users = get_followers_list(user=user)
        serializer = FollowersListSerializer(instance=users, many=True)
        return Response(serializer.data)


class FollowingListView(ListAPIView):
    pagination_class = FollowListPaginations
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        username = request.query_params.get("username")
        user = get_user_by_email_or_username(username)
        users = get_following_list(user=user)
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
        data = followers_count(target_username=username)
        return Response(data, status=status.HTTP_200_OK)


class UserFollowingCountView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        username = request.query_params.get("username")
        data = following_count(target_username=username)
        return Response(data, status=status.HTTP_200_OK)


class RestrictUserView(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self, request):
        username = request.query_params.get("username")
        data = restrict_user(user=request.user, target_username=username)
        return Response(data)
        # comments get restrict
        # have restricted activity


class UnrestrictUserView(APIView):
    permission_classes = [IsAuthenticated,]
    def delete(self, request):
        username = request.query_params.get("username")
        data = unrestrict_user(user=request.user, target_username=username)
        return Response(data)


class RestrictedUsersListView(ListAPIView):
    pagination_class = RestrictedUsersListPagination
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        users = get_restricted_users(user=request.user)
        serializer = RestrictUserSerializer(instance=users, many=True)
        return Response(serializer.data)

    def delete(self, request):
        usernames = request.query_params.getlist("username")
        data = unrestrict_selected_users(user=request.user,usernames=usernames)
        return Response(data,status=status.HTTP_200_OK)
        

class BlockUserView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request):

        username = request.query_params.get("username")
        target_user = validator_target_user(username)

        block = block_user(blocker=request.user,blocked=target_user)

        serializer = BlockUserSerializer(instance=block)

        return Response(serializer.data,status=status.HTTP_201_CREATED)


class UnblockUserView(APIView):

    permission_classes = [IsAuthenticated,]

    def delete(self, request):
        username = request.query_params.get("username")

        target_user = validator_target_user(username)

        unblock_user(blocker=request.user,blocked=target_user)

        return Response(
            {
                "detail": (f"{target_user.username} ""unblocked successfully")
            },
            status=status.HTTP_200_OK,
        )

class BlockedUsersListView(ListAPIView):

    permission_classes = [IsAuthenticated,]
    pagination_class = BlockedUsersListPagination

    def get(self, request):
        blocked_users = get_blocked_users(request.user)

        page = self.paginate_queryset(blocked_users)

        serializer = BlockUserSerializer(instance=page,many=True)

        return self.get_paginated_response(serializer.data)

    def delete(self, request):
        usernames = request.query_params.getlist("username")

        if not usernames:
            return Response(
                {
                    "error": (
                        "at least one username "
                        "is required"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        remove_blocked_users(blocker=request.user,usernames=usernames)

        return Response(
            {
                "detail": (
                    "selected users "
                    "unblocked successfully"
                )
            },
            status=status.HTTP_200_OK,
        )

