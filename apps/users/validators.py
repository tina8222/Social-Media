from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

def validator_target_user(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError("user does not exist")

