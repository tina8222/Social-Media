
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.db.models import Q



from .models import User, Follow, RestrictUser, BlockUser,FollowRequest
from .selectors import (get_user_by_email_or_username,get_user_profile, get_follow,
                        get_followers_count, get_following_count, get_restrict_user,
                        get_restricted_users,is_user_blocked,
)


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


@transaction.atomic
def unfollow_user(*, user, target_username):
    if not target_username:
        error = {"error": "username is required"}
        return error

    target_user = get_user_by_email_or_username(target_username)
    follow_obj = get_follow(follower=user, following=target_user)
    if not follow_obj:
        error = {"error": "you are not following this user"}
        return error

    follow_obj.delete()
    detail = {"detail": f"you unfollowed user {target_username}"}
    return detail


@transaction.atomic
def followers_count(*, target_username):
    target_user = get_user_by_email_or_username(target_username)
    followers = get_followers_count(following=target_user)
    data = {
        "username": target_user.username,
        "followers_count": followers
    }
    return data

@transaction.atomic
def following_count(*, target_username):
    target_user = get_user_by_email_or_username(target_username)
    following = get_following_count(follower=target_user)
    data = {
        "username": target_user.username,
        "following_count": following
    }
    return data


@transaction.atomic
def restrict_user(*, user, target_username):
    target_user = get_user_by_email_or_username(target_username)
    if user == target_user:
        data = {"error": "you cannot restrict yourself"}
        return data

    restrict_user_obj, created = RestrictUser.objects.get_or_create(user=user, restricted_user=target_user)
    if created == False:
        data = {"error": "you restricted this user before"}
        return data

    data = {
        "detail": f"you restricted {target_username}",
    }
    return data


@transaction.atomic
def unrestrict_user(*, user, target_username):
    target_user = get_user_by_email_or_username(target_username)
    obj = get_restrict_user(user=user, restricted_user=target_user)
    if not obj:
        data = {
            "error": f"you're not restrict {target_username}"
        }
        return data

    obj.delete()
    data = {
        f"{target_username} unrestricted"
    }
    return data


@transaction.atomic
def unrestrict_selected_users(*, usernames, user):
    users = get_restricted_users(user=user)
    deleted, _ = RestrictUser.objects.filter(user=user, restricted_user__username__in=usernames).delete()
    data = {
        "detail": "selected users unrestricted"
    }
    return data



@transaction.atomic
def block_user(*, blocker, blocked):
    
    if blocker == blocked:
        raise ValidationError({"error": "you cannot block yourself"})

    if is_user_blocked(blocker, blocked):
        raise ValidationError({"error": "you have already blocked this user"})

    block = BlockUser.objects.create(blocker=blocker,blocked=blocked)


    Follow.objects.filter(
        Q(follower=blocker, following=blocked) |
        Q(follower=blocked, following=blocker)
    ).delete()

    
    FollowRequest.objects.filter(
        Q(from_user=blocker, to_user=blocked) |
        Q(from_user=blocked, to_user=blocker)
    ).delete()

    return block

@transaction.atomic
def unblock_user(*, blocker, blocked):

    if not is_user_blocked(blocker=blocker,blocked=blocked):
        raise ValidationError({"error": "you have not blocked this user"})

    BlockUser.objects.filter(blocker=blocker,blocked=blocked).delete()


@transaction.atomic
def remove_blocked_users(*, blocker, usernames):

    deleted_count, _ = (
        BlockUser.objects.filter(
            blocker=blocker,
            blocked__username__in=usernames,
        ).delete()
    )

    return deleted_count
