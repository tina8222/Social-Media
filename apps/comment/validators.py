from rest_framework import serializers


class CommentValidationMixin:

    def validate_content(self, value):

        value = value.strip()

        if not value:
            raise serializers.ValidationError("Comment content cannot be empty.")

        if len(value) > 2000:
            raise serializers.ValidationError("Maximum 2000 characters allowed.")

        return value