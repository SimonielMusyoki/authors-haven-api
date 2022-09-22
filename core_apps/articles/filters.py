import django_filters as filters

from .models import Article


class ArticleFilter(filters.FilterSet):
    authors = filters.CharFilter(
        field_name="author__first_name",
        lookup_expr="icontains",
    )
    title = filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
    )
    tags = filters.CharFilter(
        field_name="tags",
        lookup_expr="iexact",
        method="get_article_tags",
    )
    created_at = filters.IsoDateTimeFilter(field_name="created_at")
    updated_at = filters.IsoDateTimeFilter(field_name="updated_at")

    def get_article_tags(self, queryset, tags, value):
        tag_values = value.replace(" ", "").split(",")
        return queryset.filter(tags__tag__in=tag_values).distinct()

    class Meta:
        model = Article
        fields = ["author", "title", "tags", "created_at", "updated_at"]
