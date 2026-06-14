from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import (
    UserProfile,
    Follow,
    RestrictUser,
    BlockUser,
)

User = get_user_model()


def get_user_by_email_or_username(value):
    return (
        User.objects.filter(username=value).first()
        or User.objects.filter(email=value).first()
    )


def get_my_profile(*, user):
    return user.user_profile


def get_user_profile(*, username):
    return UserProfile.objects.filter(
        user__username=username
    ).first()


def get_follow(*, follower, following):
    return Follow.objects.filter(
        follower=follower,
        following=following,
    ).first()


def get_followers_list(*, user):
    return (
        Follow.objects.filter(
            following=user
        )
        .select_related("follower")
        .order_by("-created_at")
    )


def get_following_list(*, user):
    return (
        Follow.objects.filter(
            follower=user
        )
        .select_related("following")
        .order_by("-created_at")
    )


def get_followers_count(*, following):
    return Follow.objects.filter(
        following=following
    ).count()


def get_following_count(*, follower):
    return Follow.objects.filter(
        follower=follower
    ).count()


def get_restrict_user(*, user, restricted_user):
    return RestrictUser.objects.filter(
        user=user,
        restricted_user=restricted_user,
    ).first()


def get_restricted_users(*, user):
    return RestrictUser.objects.filter(
        user=user
    )




def is_user_blocked(*, blocker, blocked):
    return BlockUser.objects.filter(
        blocker=blocker,
        blocked=blocked,
    ).exists()


def has_block_relation(user1, user2):
    return BlockUser.objects.filter(
        Q(blocker=user1, blocked=user2)
        | Q(blocker=user2, blocked=user1)
    ).exists()


def get_blocked_users(*, user):
    return (
        BlockUser.objects.filter(
            blocker=user
        )
        .select_related("blocked")
        .order_by("-created_at")
    )