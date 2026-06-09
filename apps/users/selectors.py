from django.contrib.auth import get_user_model



User = get_user_model()
def get_user_by_email_or_username(value):
    return (
        User.objects.filter(username=value).first()
        or User.objects.filter(email=value).first()
    )

