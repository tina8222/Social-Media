from django.db import transaction
from .models import Post
from .models import PostMedia


@transaction.atomic
def create_post(
    *,
    owner,
    caption,
    visibility,
    comments_enabled,
    media_files
):

    post = Post.objects.create(
        owner=owner,
        caption=caption,
        visibility=visibility,
        comments_enabled=comments_enabled,
    )

    media_objects = []

    for order, file in enumerate(media_files):

        content_type = file.content_type

        if content_type.startswith("image"):
            media_type = PostMedia.MediaTypeChoices.IMAGE

        elif content_type.startswith("video"):
            media_type = PostMedia.MediaTypeChoices.VIDEO

        else:
            raise ValueError(
                "Unsupported media type"
            )

        media_objects.append(
            PostMedia(
                post=post,
                file=file,
                media_type=media_type,
                order=order,
            )
        )

    PostMedia.objects.bulk_create(
        media_objects
    )

    return post