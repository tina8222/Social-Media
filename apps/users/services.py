from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .selectors import get_user_by_email_or_username


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