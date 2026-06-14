
from django.urls import path
from .views import CreateCommentView , UpdateCommentView, DeleteCommentView , PostCommentsView,CommentRepliesView


urlpatterns = [
    path("posts/<int:post_id>/comments/create/",CreateCommentView.as_view(),name="create-comment"),
    path("comments/<int:comment_id>/update/",UpdateCommentView.as_view(),name="update-comment"),
    path("comments/<int:comment_id>/delete/",DeleteCommentView.as_view(),name="delete-comment"),
    path("posts/<int:post_id>/comments/",PostCommentsView.as_view(),name="post-comments"),
    path("comments/<int:comment_id>/replies/",CommentRepliesView.as_view(),name="comment-replies"),
]

