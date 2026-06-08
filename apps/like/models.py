from django.db import models
from apps.users.models import User
from apps.post.models import Post


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_post")
    created_at = models.DateTimeField(auto_now_add=True)
  # comment

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["post"]),
            models.Index(fields=["created_at"])
        ]

        constraints = [
            models.UniqueConstraint(fields=["user", "post"], name="unique_user_post_like")
        ]


    def __str__(self):
        return f"{self.post} from user {self.user.username}"
