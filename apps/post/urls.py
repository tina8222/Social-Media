from django.urls import path
from .views import (
    CreatePostView , 
    UpdatePostView ,
    DeletePostView ,
    PostDetailView,
    MyPostsView,
    PostListView,
    FeedView,
    ExploreView,
    SavePostView,
    UnsavePostView
)


urlpatterns = [ 

    path("create/", CreatePostView.as_view(),name="create-post"),
    path("<int:post_id>/update/", UpdatePostView.as_view(),name="update-post"),
    path("<int:post_id>/delete/", DeletePostView.as_view(),name="delete-post"),
    path("<int:post_id>/", PostDetailView.as_view(),name="post_detail"),
    path("me/", MyPostsView.as_view(),name="my_post"),
    path("posts/", PostListView.as_view(),name="post-list"),
    path("feed/", FeedView.as_view(),name="feed"),
    path("explore/", ExploreView.as_view(), name="explore"),
    path("save/", SavePostView.as_view(), name="save_post"),
    path("unsave/", UnsavePostView.as_view(), name="unsave_post"),

]
