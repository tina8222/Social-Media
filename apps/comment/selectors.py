from django.shortcuts import get_object_or_404
from apps.post.models import Post
from .models import Comment


def get_post_by_id(*, post_id):

    return get_object_or_404(
        Post.objects.only(
            "id",
            "comments_enabled",
            "comments_count",
        ),
        id=post_id,
    )


def get_comment_by_id(*, comment_id):

    return get_object_or_404(
        Comment.objects.select_related(
            "post",
        ),
        id=comment_id,
    )



def get_comment_by_id_for_owner(*,comment_id,owner):

    return get_object_or_404(Comment,id=comment_id,user=owner)