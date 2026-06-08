from django.urls import path
from .views import (
    LikePostView
)



urlpatterns = [
    path("like-post/<int:post_id>", LikePostView.as_view(), name="like_post"),
]