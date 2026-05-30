from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager

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
            models.Index(fields=["phone_number"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE, related_name="user_profile")
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, upload_to="avatars/", default="avatars/avatar.png")
    website = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices)
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
        return f"{self.user.username} Profile"





class Follow(models.Model):

    class FollowStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACCEPTED = "ACCEPTED", "Accepted"
        REJECTED = "REJECTED", "Rejected"
        CANCELED = "CANCELED" , "Canceled"

    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relationships"
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relationships"
    )

    status = models.CharField(
        max_length=20,
        choices=FollowStatus.choices,
        default=FollowStatus.PENDING
    )

    is_close_friend = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "following"],
                name="unique_follow_relation"
            )
        ]

        indexes = [
            models.Index(fields=["follower"]),
            models.Index(fields=["following"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.follower.email} -> {self.following.email}"



class FollowRequest(models.Model):

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_follow_requests"
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_follow_requests"
    )

    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-created_at"]
        constraints =[
            models.UniqueConstraint(
                fields=["from_user","to_user"],
                name="unique_follow_request"
            )
        ]

        indexes = [
            models.Index(fields=["from_user"]),
            models.Index(fields=["to_user"]),
            models.Index(fields=["created_at"]),

        ]

    def __str__(self):
        return f"{self.from_user.email} -> {self.to_user.email}"

    
class BlockUser(models.Model):
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocker_user")
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blocked_user")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["blocker", "blocked"],
                name="unique_block"
            )
        ]

        indexes = [
            models.Index(fields=["blocker"]),
            models.Index(fields=["blocked"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"user {self.blocker.username} blocked {self.blocked.username}"

