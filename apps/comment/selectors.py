from django.shortcuts import get_object_or_404
from apps.post.models import Post
from .models import Comment

ALLOWED_ORDERING = {
    "newest": "-created_at",
    "oldest": "created_at",
}


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
            "post__owner",
        ),
        id=comment_id,
    )



def get_comment_by_id_for_owner(*,comment_id,owner):

    return get_object_or_404(Comment,id=comment_id,user=owner)





def get_post_comments(*,post_id,ordering="oldest"):

    return (Comment.objects.select_related("user").filter(post_id=post_id,parent=None).order_by(ALLOWED_ORDERING.get(ordering,"created_at")))


def get_comment_replies(*,comment_id):

    return (Comment.objects.select_related("user").filter(parent_id=comment_id).order_by("created_at"))