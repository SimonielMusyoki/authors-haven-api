from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "article", "body", "created_at", "updated_at"]

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.created_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M")
        return formatted_date

    def get_author(self, obj):
        return obj.author.username

    def get_article(self, obj):
        return obj.article.title


class CommentListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.user.username")
    article = serializers.ReadOnlyField(source="article.title")
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M")
        return formatted_date

    def get_updated_at(self, obj):
        then = obj.created_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M")
        return formatted_date

    class Meta:
        model = Comment
        fields = ["id", "author", "article", "body", "created_at", "updated_at"]
