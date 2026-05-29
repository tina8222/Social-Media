from django.db import models
from django.contrib.auth.models import AbstractUser
from .usermanager import UserManager
from ..constants import USER_PROFILE_GENDER_CHOICES

class User(AbstractUser):

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20,unique=True,null=True,blank=True)
    is_verified = models.BooleanField(default=False,db_index=True)
    is_private = models.BooleanField(default=False)
    last_seen = models.DateTimeField(null=True,blank=True)
    last_login_ip = models.GenericIPAddressField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["username"]),
            models.Index(fields=["phone_number"]),
        ]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to="avatars/", default="avatars/avatar.png")
    website = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=USER_PROFILE_GENDER_CHOICES)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"])
        ]


    def __str__(self):
        return self.user