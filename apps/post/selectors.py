from django.shortcuts import get_object_or_404
from .models import Post


def get_post_by_id_for_owner(*, post_id, owner):
    return get_object_or_404(Post.objects.prefetch_related("media"),id=post_id,owner=owner)