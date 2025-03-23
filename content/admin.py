from django.contrib import admin

from .models import Article, ArticleRatingStats, Rating


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    search_fields = ("title", "content")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "article", "user", "score", "created_at")
    list_filter = ("score", "created_at")
    search_fields = ("article__title", "article__id", "user__phone")
    # autocomplete_fields = ["article", "user"]
    ordering = ("-created_at",)


@admin.register(ArticleRatingStats)
class ArticleRatingStatsAdmin(admin.ModelAdmin):
    list_display = (
        "article",
        "total_count",
        "avg_rating",
        "highest_rating",
        "lowest_rating",
        "last_updated_at",
    )
    readonly_fields = ("last_updated_at",)
    autocomplete_fields = ["article"]
