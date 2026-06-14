from django.contrib import admin
from .models import User, UserProfile, RestrictUser, Follow,BlockUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "username", "email", "password", "phone_number"]
    search_fields = ["email", "username"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "bio", "avatar", "website", "gender"]
    search_fields = ["user",]


@admin.register(RestrictUser)
class RestrictUserAdmin(admin.ModelAdmin):
    list_display = ["user", "restricted_user", "created_at"]
    search_fields = ["restricted_user",]

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ["follower", "following", "created_at"]
    search_fields = ["follower", "following"]

@admin.register(BlockUser)
class BlockUserAdmin(admin.ModelAdmin):
    list_display = ["blocker","blocked","created_at"]
    search_fields = ["blocker__username","blocked__username","blocker__email","blocked__email"]