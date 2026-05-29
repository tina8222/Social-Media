from django.db import models
from django.contrib.auth.models import AbstractUser
from .usermanager import UserManager


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


