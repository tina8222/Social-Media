
from django.conf import settings
from django.db import models
from piptools.scripts.options import user


class Post(models.Model):

    class VisibilityChoices(models.TextChoices):
        PUBLIC = "PUBLIC", "Public"
        
        

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="posts")

    caption = models.TextField(blank=True,null=True)

    visibility = models.CharField(max_length=20,choices=VisibilityChoices.choices,default=VisibilityChoices.PUBLIC,db_index=True)

    comments_enabled = models.BooleanField(default=True)

    likes_count = models.PositiveIntegerField(default=0)

    comments_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["visibility"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Post {self.id} - {self.owner.email}"



class PostMedia(models.Model):

    class MediaTypeChoices(models.TextChoices):
        IMAGE = "IMAGE", "Image"
        VIDEO = "VIDEO", "Video"

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="media")

    file = models.FileField(upload_to="posts/")

    media_type = models.CharField(max_length=10,choices=MediaTypeChoices.choices)

    order = models.PositiveSmallIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "id"]

        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["media_type"]),
        ]

    def __str__(self):
        return f"{self.media_type} - {self.post_id}"



class SavedPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_saved_post")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_save")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["post"]),
            models.Index(fields=["created_at"])
        ]

        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_user_post_save")
        ]

    def __str__(self):
        return f"post {self.post} saved by {self.user.username}"






