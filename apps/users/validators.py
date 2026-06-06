from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

User = get_user_model()

def validator_target_user(username):
    if not username:
        error = {"error": "username is required"}
        return Response(error, status=HTTP_400_BAD_REQUEST)

    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError("user does not exist")

