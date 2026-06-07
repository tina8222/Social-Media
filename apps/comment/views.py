from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    CreateCommentSerializer,
    CommentSerializer,
    UpdateCommentSerializer,
)
from .selectors import (
    get_post_by_id,
    get_comment_by_id,
    get_comment_by_id_for_owner,
)

from .services import create_comment , update_comment, delete_comment


class CreateCommentView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,post_id):

        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        post = get_post_by_id(post_id=post_id)
        parent = None

        parent_id = serializer.validated_data.get("parent_id")

        if parent_id:

            parent = get_comment_by_id(comment_id=parent_id)

        comment = create_comment(
            user=request.user,
            post=post,
            content=serializer.validated_data["content"],
            parent=parent,
        )

        return Response(CommentSerializer(comment).data,status=status.HTTP_201_CREATED)



class UpdateCommentView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def patch(self,request,comment_id):

        comment = (get_comment_by_id_for_owner(comment_id=comment_id,owner=request.user))
        serializer = (UpdateCommentSerializer(data=request.data))

        serializer.is_valid(raise_exception=True)

        comment = update_comment(
            comment=comment,
            content=serializer.validated_data.get("content")
        )

        return Response(CommentSerializer(comment).data,status=status.HTTP_200_OK)





class DeleteCommentView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, comment_id):

        comment = get_comment_by_id(comment_id=comment_id)

        is_comment_owner = comment.user_id == request.user.id
        is_post_owner = comment.post.owner_id == request.user.id

        if not (is_comment_owner or is_post_owner):
            raise PermissionDenied("You are not allowed to delete this comment")

        delete_comment(comment=comment)

        return Response(status=status.HTTP_204_NO_CONTENT)