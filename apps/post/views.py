from rest_framework import permissions
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    CreatePostSerializer,
    PostSerializer,
)
from .services import create_post


class CreatePostView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = CreatePostSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        post = create_post(
            owner=request.user,
            caption=serializer.validated_data.get("caption"),
            visibility=serializer.validated_data.get("visibility"),
            comments_enabled=serializer.validated_data.get("comments_enabled"),
            media_files=serializer.validated_data.get("media_files")
        )

        return Response(PostSerializer(post).data,status=status.HTTP_201_CREATED)