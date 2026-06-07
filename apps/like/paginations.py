from rest_framework.pagination import PageNumberPagination

class PostLikeListPagination(PageNumberPagination):
    page_size = 20