
from django.conf import settings
from django.db import models
from apps.post.models import Post


class Comment(models.Model):

    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="comments")
    parent = models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True,related_name="replies")
    content = models.TextField()
    is_edited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

        indexes = [
            models.Index(fields=["post", "created_at"]),
            models.Index(fields=["parent"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Comment {self.id}"