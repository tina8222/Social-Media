from rest_framework.pagination import PageNumberPagination

class FollowListPaginations(PageNumberPagination):
    page_size = 10


class RestrictedUsersListPagination(PageNumberPagination):
    page_size = 15