from django.contrib import admin

from apps.post.models import Post, PostMedia, SavedPost

admin.site.register(Post)
admin.site.register(PostMedia)


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    search_fields = ["user"]

