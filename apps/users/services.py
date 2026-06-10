from django.db import transaction
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from .models import (BlockUser,Follow,FollowRequest)
from .selectors import has_block_relation , is_user_blocked


@transaction.atomic
def block_user(*, blocker, blocked):
    
    if blocker == blocked:
        raise ValidationError({"error": "you cannot block yourself"})

    if is_user_blocked(blocker, blocked):
        raise ValidationError({"error": "you have already blocked this user"})

    block = BlockUser.objects.create(blocker=blocker,blocked=blocked)


    Follow.objects.filter(
        Q(follower=blocker, following=blocked) |
        Q(follower=blocked, following=blocker)
    ).delete()

    
    FollowRequest.objects.filter(
        Q(from_user=blocker, to_user=blocked) |
        Q(from_user=blocked, to_user=blocker)
    ).delete()

    return block

@transaction.atomic
def unblock_user(*, blocker, blocked):

    if not is_user_blocked(blocker=blocker,blocked=blocked):
        raise ValidationError({"error": "you have not blocked this user"})

    BlockUser.objects.filter(blocker=blocker,blocked=blocked).delete()


@transaction.atomic
def remove_blocked_users(*, blocker, usernames):

    deleted_count, _ = (
        BlockUser.objects.filter(
            blocker=blocker,
            blocked__username__in=usernames,
        ).delete()
    )

    return deleted_count