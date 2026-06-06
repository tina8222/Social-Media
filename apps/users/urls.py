from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    MyProfileView,
    FollowUserView,
    UnfollowUserView,
    FollowersListView,
    FollowingListView,
    UserFollowersCountView,
    UserFollowingCountView,
    RestrictUserView,
    UnrestrictUserView,
    RestrictedUsersListView
)

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",LoginView.as_view(),name="login"),
    path("refresh/",TokenRefreshView.as_view(),name="token_refresh"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("my-profile/", MyProfileView.as_view()),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("my-profile/", MyProfileView.as_view(), name="my_profile"),
    path("follow-user/", FollowUserView.as_view(), name="follow_user"),
    path("unfollow-user/", UnfollowUserView.as_view(), name="unfollow_user"),
    path("followers/", FollowersListView.as_view(), name="followers_list"),
    path("followings/", FollowingListView.as_view(), name="following_list"),
    path("followers-count/", UserFollowersCountView.as_view(), name="followers_count"),
    path("following-count/", UserFollowingCountView.as_view(), name="following_count"),
    path("restrict-user/", RestrictUserView.as_view(), name="restrict_user"),
    path("unrestrict-user/", UnrestrictUserView.as_view(), name="unrestrict_user"),
    path("restricted-users/", RestrictedUsersListView.as_view(), name="restricted_users")
]