from django.contrib.auth import get_user_model

from .models import UserProfile, Follow, RestrictUser

User = get_user_model()
def get_user_by_email_or_username(value):
    return (
        User.objects.filter(username=value).first()
        or User.objects.filter(email=value).first()
    )

def get_my_profile(*, user):
    return user.user_profile

def get_user_profile(*, username):
    return UserProfile.objects.filter(user__username=username).first()

def get_follow(*, follower, following):
    return Follow.objects.filter(follower=follower, following=following).first()

def get_followers_list(*, user):
    return Follow.objects.filter(following=user).select_related("follower").order_by("-created_at")

def get_following_list(*, user):
    return Follow.objects.filter(follower=user).select_related("following").order_by("-created_at")

def get_followers_count(*, following):
    return Follow.objects.filter(following=following).count()

def get_following_count(*, follower):
    return Follow.objects.filter(follower=follower).count()

def get_restrict_user(*, user, restricted_user):
    return RestrictUser.objects.filter(user=user, restricted_user=restricted_user)

