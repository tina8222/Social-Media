from django.contrib.auth import get_user_model

from .models import UserProfile, Follow

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
