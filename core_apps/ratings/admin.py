from django.contrib import admin

from core_apps.ratings.models import Rating
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ["article", "rated_by", "value"]
