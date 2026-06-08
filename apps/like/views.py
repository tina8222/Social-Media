from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .services import like_post, unlike_post



class LikePostView(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self, request, post_id):
        try:
            like_post(user=request.user, post_id=post_id)
            detail_created = {"detail": "post liked successfully"}
            return Response(detail_created, status=status.HTTP_201_CREATED)
        except ValueError as error:
            error_detail = {"detail": str(error)}
            return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)


class UnlikePostView(APIView):

    permission_classes = [IsAuthenticated,]

    def delete(self, request, post_id):
        try:
            unlike_post(user=request.user, post_id=post_id)
            detail_unliked = {"detail": "post unliked successfully"}
            return Response(detail_unliked, status=status.HTTP_200_OK)
        except ValueError as error:
            error_detail = {"detail": str(error)}
            return Response(error_detail, status=status.HTTP_400_BAD_REQUEST)