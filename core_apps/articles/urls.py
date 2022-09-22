from django.urls import path
from .views import (
    ArticleCreateAPIView,
    ArticleDeleteAPIView,
    ArticleDetailView,
    ArticleListAPIView,
    update_article_api_view,
)

urlpatterns = [
    path("all/", ArticleListAPIView.as_view(), name="articles"),
    path("create/", ArticleCreateAPIView.as_view(), name="article-new"),
    path("details/<slug:slug>/", ArticleDetailView.as_view(), name="article-details"),
    path("update/<slug:slug>/", update_article_api_view, name="article-update"),
    path("delete/<str:slug>/", ArticleDeleteAPIView.as_view(), name="article-delete"),
]
