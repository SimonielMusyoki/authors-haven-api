from django.urls import path

from .views import FavouriteAPIView, ListUserFavouriteArticlesAPIView

urlpatterns = [
    path("<slug:slug>/", FavouriteAPIView.as_view(), name="favourite-article"),
    path(
        "articles/me/", ListUserFavouriteArticlesAPIView.as_view(), name="my-favourites"
    ),
]
