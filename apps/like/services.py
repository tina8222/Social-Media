from django.db import transaction
from django.db.models import F
from rest_framework.response import Response

from .models import Like
from apps.post.models import Post

from .selectors import get_post_by_id

@transaction.atomic
def like_post(*, user, post_id:int):
    post = get_post_by_id(post_id)

    like_obj, created = Like.objects.get_or_create(user=user, post=post)
    if not created:
        raise ValueError("you already liked this post")

    Post.objects.filter(id=post.id).update(likes_count=F("likes_count") + 1)


@transaction.atomic
def unlike_post(*, user, post_id:int):
    post = get_post_by_id(post_id)

    like = Like.objects.get(user=user, post=post)
    if like:
        like.delete()
        Post.objects.filter(id=post.id).update(likes_count=F("likes_count") - 1)
