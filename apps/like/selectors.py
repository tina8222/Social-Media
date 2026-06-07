from apps.post.models import Post

def get_post_by_id(post_id: int):
    return Post.objects.get(id=post_id)

