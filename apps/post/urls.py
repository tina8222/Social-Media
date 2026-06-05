from django.urls import path
from .views import CreatePostView , UpdatePostView

urlpatterns = [
path("create/", CreatePostView.as_view(),name="create-post"),
path("<int:post_id>/update/", UpdatePostView.as_view(),name="update-post"),

]
