from rest_framework import serializers
from .models import Comment
from .validators import CommentValidationMixin


class CreateCommentSerializer(CommentValidationMixin,serializers.Serializer):

    content = serializers.CharField()
    parent_id = serializers.IntegerField(required=False,allow_null=True)


class CommentSerializer(serializers.ModelSerializer):

    user_id = serializers.IntegerField(source="user.id",read_only=True)

    class Meta:
        model = Comment

        fields = (
            "id",
            "user_id",
            "post",
            "parent",
            "content",
            "is_edited",
            "created_at",
            "updated_at",
        )

class UpdateCommentSerializer(CommentValidationMixin,serializers.Serializer):

    content = serializers.CharField(required=False)
