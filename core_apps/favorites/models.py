from django.contrib.auth import get_user_model
from django.db import models

from core_apps.articles.models import Article
from core_apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Favourite(TimeStampedUUIDModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favourites")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_favourites"
    )

    def __str__(self):
        return f"{self.user.username} fvourited {self.article.title}"

    def is_favourited(self, user, article):
        try:
            article = self.article
            user = self.user
        except Article.DoesNotExist:
            pass

        queryset = Favourite.objects.filter(article_id=article, user_id=user)

        if queryset:
            return True
        return False
