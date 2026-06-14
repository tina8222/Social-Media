from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        FOLLOW = "FOLLOW", "Follow"
        LIKE = "LIKE", "Like"
        COMMENT = "COMMENT", "Comment"
        FOLLOW_REQUEST = "FOLLOW_REQUEST", "Follow Request"
        MENTION = "MENTION", "Mention"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications")

    actor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="notifications_sent")

    notification_type = models.CharField(max_length=30,choices=NotificationType.choices,db_index=True,)

    object_id = models.PositiveIntegerField(null=True, blank=True)

    is_read = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["recipient", "is_read"]),
            models.Index(fields=["notification_type"]),
        ]

    def __str__(self):
        return f"{self.recipient} - {self.notification_type}"
