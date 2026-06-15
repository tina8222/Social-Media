from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    actor_username = serializers.CharField(source="actor.username",read_only=True)

    class Meta:
        model = Notification
        fields = (
            "id",
            "actor_username",
            "notification_type",
            "object_id",
            "is_read",
            "created_at",
        )