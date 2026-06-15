from .models import Notification


ALLOWED_ORDERINGS = {
    "newest": "-created_at",
    "oldest": "created_at",
}


def get_user_notifications(*, user, ordering="newest"):

    return (Notification.objects.filter(recipient=user).select_related("actor").order_by(ALLOWED_ORDERINGS.get(ordering, "-created_at")))
