from rest_framework import serializers
from .models import Like

class LikeSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Like
        fields = ["username", "first_name", "last_name", "created_at"]