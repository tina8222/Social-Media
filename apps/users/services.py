from rest_framework_simplejwt.tokens import RefreshToken

from .models import User




def register_user(*, validated_data: dict) -> dict:
    user = User.objects.create_user(**validated_data)
    refresh = RefreshToken.for_user(user)

    data = {
        "user": user,
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }

    return data