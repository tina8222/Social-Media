from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .selectors import get_user_notifications
from .serializers import NotificationSerializer
from .pagination import NotificationPagination


class NotificationsListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        ordering = request.query_params.get("ordering","newest")

        notifications = get_user_notifications(user=request.user,ordering=ordering)

        paginator = NotificationPagination()

        page = paginator.paginate_queryset(notifications,request)

        serializer = NotificationSerializer(page,many=True)

        return paginator.get_paginated_response(serializer.data)