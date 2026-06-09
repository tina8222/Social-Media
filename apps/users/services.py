from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import transaction

from .models import User, Follow
from .selectors import get_user_by_email_or_username, get_user_profile, get_follow


def register_user(*, validated_data:dict):
    user = User.objects.create_user(**validated_data)
    refresh = RefreshToken.for_user(user)

    data = {
        "user": user,
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }
    return data


def login_user(*, validated_data:dict):
    user = get_user_by_email_or_username(validated_data["login"])
    if user is None or not user.check_password(validated_data["password"]):
        raise AuthenticationFailed("Invalid credentials")

    refresh = RefreshToken.for_user(user)
    data = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return data


def logout_user(*, validated_data:dict):
    try:
        token = RefreshToken(validated_data["refresh"])
        token.blacklist()
        data = {"detail": "Logged out successfully"}
        return data

    except Exception:
        data = {"detail": "Invalid refresh token"}
        return data

@transaction.atomic
def update_profile(*, profile, validated_data):
    user_data = validated_data.pop("user", None)
    if user_data:
        profile.user.username = user_data["username"]
        profile.user.save(update_fields=["username"])

    for field, value in validated_data.items():
        setattr(profile, field, value)

    profile.save()
    return profile


@transaction.atomic
def check_user_profile(*, username):
    user = get_user_profile(username=username)
    if not user:
        raise ValueError(f"user with username {username} dos not exist!")
    return user

@transaction.atomic
def follow_user(*, user, target_username):
    if not target_username:
        error = {"error": "username is required"}
        return error

    target_user = get_user_by_email_or_username(target_username)
    if target_user == user:
        error = {"error": "you cannot follow yourself"}
        return error

    already_follow = get_follow(follower=user, following=target_user)
    if already_follow:
        error = {"error": "you already follow this user"}
        return error

    Follow.objects.create(follower=user, following=target_user, status=Follow.FollowStatus.ACCEPTED)
    data = {"detail": f"you're now following {target_username}"}
    return data




