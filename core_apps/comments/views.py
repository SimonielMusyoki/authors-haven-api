from functools import partial
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from core_apps.articles.models import Article

from .models import Comment
from .serializers import CommentListSerializer, CommentSerializer


class CommentAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get(self, request, **kwargs):
        try:
            slug = self.kwargs.get("slug")
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("That article does not exist in our catalog")

        try:
            comments = Comment.objects.filter(article_id=article.pkid)
        except Comment.DoesNotExist:
            raise NotFound("No comments Found")

        serializer = CommentListSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(
            {
                "num_comments": len(serializer.data),
                "comments": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        try:
            slug = self.kwargs.get("slug")
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise NotFound("That article does not exist in our catalog")
        comment = request.data
        author = request.user
        comment["author"] = author.pkid
        comment["article"] = article.pkid
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentUpdateDeleteAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def put(self, request, slug, id):
        try:
            comment_to_update = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")
        data = request.data
        serializer = self.serializer_class(comment_to_update, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "message": "Comment Updated Successfully",
            "comment": serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request, slug, id):
        try:
            comment_to_delete = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")
        comment_to_delete.delete()
        return Response(
            {"message": "comment Deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
