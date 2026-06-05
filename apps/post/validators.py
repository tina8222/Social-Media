from rest_framework import serializers


class MediaValidationMixin:

    media_required = False
  
    def validate_media_files(self, files):

        if self.media_required and not files:
            raise serializers.ValidationError("At least one media file is required.")

        if len(files) > 10:
            raise serializers.ValidationError("Maximum 10 files allowed.")

        allowed_image_types = {
            "image/jpeg",
            "image/png",
            "image/webp",
        }

        allowed_video_types = {
            "video/mp4",
            "video/quicktime",
            "video/x-msvideo",
        }

        allowed_types = (
            allowed_image_types |
            allowed_video_types
        )

        max_image_size = 5 * 1024 * 1024
        max_video_size = 50 * 1024 * 1024

        for file in files:

            content_type = getattr(file,"content_type",None)

            if content_type not in allowed_types:
                raise serializers.ValidationError(f"{file.name} format is not supported.")

            if content_type.startswith("image"):

                if file.size > max_image_size:
                    raise serializers.ValidationError(f"{file.name} exceeds 5MB.")

            if content_type.startswith("video"):

                if file.size > max_video_size:
                    raise serializers.ValidationError(f"{file.name} exceeds 50MB.")

        return files