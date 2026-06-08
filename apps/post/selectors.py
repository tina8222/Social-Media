from django.shortcuts import get_object_or_404
from .models import Post

ALLOWED_ORDERINGS = {
    "newest":"-created_at",
    "oldest":"created_at",
}


def get_post_by_id_for_owner(*, post_id, owner):
    return get_object_or_404(Post.objects.prefetch_related("media"),id=post_id,owner=owner)

def get_post_by_id(*,post_id):
    return get_object_or_404(Post.objects.select_related("owner").prefetch_related("media"),id =post_id,)

def get_user_posts(*,owner,ordering="newest"):

    return (Post.objects.filter(owner=owner).prefetch_related("media").order_by(ALLOWED_ORDERINGS.get(ordering,"-created_at")))


def get_posts(*,ordering="newest",owner_id=None):

    queryset = (Post.objects.prefetch_related("media"))

    if owner_id:queryset = queryset.filter(owner_id=owner_id)

    return queryset.order_by(ALLOWED_ORDERINGS.get(ordering,"-created_at"))