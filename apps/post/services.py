from django.db import transaction
from .models import PostMedia , Post
from rest_framework.exceptions import ValidationError
from django.db.models import Max


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
            raise ValueError("Unsupported media type")

        media_objects.append(
            PostMedia(
                post=post,
                file=file,
                media_type=media_type,
                order=order,
            )
        )

    PostMedia.objects.bulk_create(media_objects)

    return post




@transaction.atomic
def update_post(
    *,
    post,
    caption=None,
    visibility=None,
    media_files=None,
    delete_media_ids=None,
):

    post = Post.objects.select_for_update().get(id=post.id)

    if caption is not None:
        post.caption = caption

    if visibility is not None:
        post.visibility = visibility

    post.save()

    delete_ids = delete_media_ids or []
    new_files = media_files or []


    media_qs = post.media.all()

    delete_qs = media_qs.filter(id__in=delete_ids)
    delete_count = delete_qs.count()

    current_count = media_qs.count()
    new_count = len(new_files)

    final_count = current_count - delete_count + new_count

    if final_count <= 0:
        raise ValidationError("Post must contain at least one media file.")

    if final_count > 10:
        raise ValidationError("Maximum 10 media files allowed.")


    did_delete = False

    if delete_qs.exists():
        did_delete = True

        for media in delete_qs:
            if media.file:
                media.file.delete(save=False)

        delete_qs.delete()


    if did_delete:
        remaining_media = list(post.media.order_by("order", "id"))

        for index, media in enumerate(remaining_media):
            if media.order != index:
                media.order = index

        if remaining_media:
            PostMedia.objects.bulk_update(remaining_media, ["order"])


    if new_files:
        max_order = (post.media.aggregate(max_order=Max("order"))["max_order"] or -1)

        media_objects = []

        for i, file in enumerate(new_files, start=max_order + 1):

            content_type = getattr(file, "content_type", "")

            if content_type.startswith("image"):
                media_type = PostMedia.MediaTypeChoices.IMAGE

            elif content_type.startswith("video"):
                media_type = PostMedia.MediaTypeChoices.VIDEO

            else:
                raise ValidationError("Unsupported media type.")

            media_objects.append(
                PostMedia(
                    post=post,
                    file=file,
                    media_type=media_type,
                    order=i,
                )
            )

        PostMedia.objects.bulk_create(media_objects)

    return post