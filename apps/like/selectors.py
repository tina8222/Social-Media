from apps.post.models import Post
from .models import Like


def get_post_by_id(post_id: int):
    return Post.objects.get(id=post_id)

def get_likes_by_post_id(post_id:int):
    return Like.objects.filter(post__id=post_id)