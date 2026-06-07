
from django.urls import path
from .views import CreateCommentView , UpdateCommentView, DeleteCommentView


urlpatterns = [
    path("posts/<int:post_id>/comments/",CreateCommentView.as_view(),name="create-comment"),
    path("comments/<int:comment_id>/update/",UpdateCommentView.as_view(),name="update-comment"),
    path("comments/<int:comment_id>/delete/",DeleteCommentView.as_view(),name="delete-comment"),

]