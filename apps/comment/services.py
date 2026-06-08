from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError
from apps.post.models import Post
from .models import Comment


@transaction.atomic
def create_comment(
    *,
    user,
    post,
    content,
    parent=None,
):

    if not post.comments_enabled:raise ValidationError("Comments are disabled for this post.")

    if parent and parent.post_id != post.id:raise ValidationError("Reply must belong to the same post.")

    comment = Comment.objects.create(
        post=post,
        user=user,
        parent=parent,
        content=content,
    )

    Post.objects.filter(id=post.id).update(comments_count=F("comments_count") + 1)

    return comment



@transaction.atomic
def update_comment(*,comment,content=None):

    comment = (Comment.objects.select_for_update().get(id=comment.id))
    updated_fields = []

    if content is not None:

        comment.content = content
        comment.is_edited = True

        updated_fields.extend([
            "content",
            "is_edited",
        ])

    if updated_fields:

        comment.save(update_fields=updated_fields)

    return comment



@transaction.atomic
def delete_comment(*, comment):

    comment_id = comment_id
    post = comment_post

    comment.delete()

    post.__class__.objects.filter(id=post.id).update(comments_count=F("comments_count") - 1)

    return True