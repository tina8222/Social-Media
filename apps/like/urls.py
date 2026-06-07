from django.urls import path
from .views import (
    LikePostView,
    UnlikePostView
)



urlpatterns = [
    path("like-post/<int:post_id>", LikePostView.as_view(), name="like_post"),
    path("unlike-post/<int:post_id>", UnlikePostView.as_view(), name="unlike_post"),
]