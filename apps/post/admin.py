from django.contrib import admin

from apps.post.models import Post, PostMedia

admin.site.register(Post)
admin.site.register(PostMedia)
