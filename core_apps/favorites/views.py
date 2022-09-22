from email import generator
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound

from core_apps.articles.models import Article
from core_apps.articles.serializers import ArticleCreateSerializer

from .exceptions import AlreadyFavourited
from .models import Favourite
from .serializers import FavouriteSerializer


class FavouriteAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavouriteSerializer

    def post(self, request, slug, *args, **kwargs):
        data = request.data
        try:
            article = Article.objects.get(slug=slug)
        except:
            raise NotFound("Article with that slug does not exist in our catalog")
        user = request.user

        favourite = Favourite.objects.filter(user=user, article=article.pkid).first()
        if favourite:
            raise AlreadyFavourited
        else:
            data["article"] = article.pkid
            data["user"] = user.pkid
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["message"] = "Article added to favourites"
            return Response(data, status=status.HTTP_201_CREATED)


class ListUserFavouriteArticlesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        Favorites = Favourite.objects.filter(user_id=request.user.pkid)

        favorite_articles = []
        for favorite in Favorites:
            article = Article.objects.get(pkid=favorite.article.pkid)
            article = ArticleCreateSerializer(
                article, context={"article": article.slug, "request": request}
            ).data
            favorite_articles.append(article)
        favorites = {"my_favorites": favorite_articles}
        return Response(data=favorites, status=status.HTTP_200_OK)
