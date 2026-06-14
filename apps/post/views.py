from rest_framework import permissions
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import get_post_by_id_for_owner , get_post_by_id , get_user_posts, get_posts

from .serializers import (
    CreatePostSerializer,
    PostSerializer,
    UpdatePostSerializer,
)
from .services import (create_post, update_post, delete_post,get_feed,)
from .pagination import PostPagination

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

class UpdatePostView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self,request,post_id,):

        post = get_post_by_id_for_owner(post_id=post_id,owner=request.user)

        serializer = UpdatePostSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        post = update_post(
            post=post,
            caption=serializer.validated_data.get("caption"),
            visibility=serializer.validated_data.get("visibility"),
            media_files=serializer.validated_data.get("media_files"),
            delete_media_ids=serializer.validated_data.get("delete_media_ids"),
        )

        return Response(PostSerializer(post).data,status=status.HTTP_200_OK)

class DeletePostView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, post_id):

        post = get_post_by_id_for_owner(post_id=post_id,owner=request.user)

        delete_post(post=post)

        return Response(status=status.HTTP_204_NO_CONTENT)

class PostDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,post_id):
        post = get_post_by_id(post_id=post_id)

        serializer = PostSerializer(post)

        return Response(serializer.data,status=status.HTTP_200_OK)

class MyPostsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        ordering = request.query_params.get("ordering","newest")

        posts = get_user_posts(owner=request.user,ordering=ordering)

        paginator = PostPagination()

        page = paginator.paginate_queryset(posts,request)

        serializer = PostSerializer(page,many=True)

        return paginator.get_paginated_response(serializer.data)

class PostListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        ordering = request.query_params.get("ordering","newest")
        owner_id = request.query_params.get("owner_id")

        posts = get_posts(ordering=ordering, owner_id=owner_id)

        paginator = PostPagination()

        page = paginator.paginate_queryset(posts,request)

        serializer = PostSerializer(page,many=True)

        return paginator.get_paginated_response(serializer.data)


class FeedView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        ordering = request.query_params.get("ordering", "newest")

        posts = get_feed(user=request.user,ordering=ordering)

        paginator = PostPagination()

        page = paginator.paginate_queryset(posts,request)

        serializer = PostSerializer(page,many=True)

        return paginator.get_paginated_response(serializer.data)