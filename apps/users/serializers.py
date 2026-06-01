from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
        )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value    

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )


class LoginSerializer(serializers.Serializer):

    login = serializers.CharField(required=True)

    password = serializers.CharField(
        write_only=True,
        required=True,
    )


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    
