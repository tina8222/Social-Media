from django.db.models import Q
from .models import BlockUser

def is_user_blocked(blocker, blocked):
    return BlockUser.objects.filter(
        blocker=blocker,
        blocked=blocked,
    ).exists()

def has_block_relation(user1, user2):

    return BlockUser.objects.filter(
        Q(blocker=user1, blocked=user2) |
        Q(blocker=user2, blocked=user1)
    ).exists()

def get_blocked_users(user):
    
    return (BlockUser.objects.filter(blocker=user).select_related("blocked").order_by("-created_at"))
