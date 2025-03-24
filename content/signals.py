from django.db.models import Avg, Case, Count, IntegerField, Max, Min, When
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Article, ArticleRatingStats, Rating


@receiver(post_save, sender=Article)
def create_article_rating_stats(sender, instance, created, **kwargs):
    if created:
        ArticleRatingStats.objects.create(article=instance)


@receiver(post_save, sender=Rating)
def update_article_rating_stats(sender, instance, **kwargs):
    """
    Updates the ArticleRatingStats for the article associated with the saved Rating instance.
    Recalculates total count, average rating, highest/lowest ratings, and rating distribution (1-5).

    Args:
        sender: The model class that sent the signal (Rating).
        instance: The Rating instance that was saved.
        **kwargs: Additional signal arguments.
    """
    article = instance.article
    score_range = range(0, 6)
    stats, _ = ArticleRatingStats.objects.get_or_create(article=article)

    aggregation = {
        "total_count": Count("id"),
        "avg_rating": Avg("score"),
        "highest_rating": Max("score"),
        "lowest_rating": Min("score"),
    }
    for score in score_range:
        aggregation[f"score_{score}"] = Count(
            Case(When(score=score, then=1), output_field=IntegerField())
        )

    stats_data = article.ratings.aggregate(**aggregation)

    stats.total_count = stats_data.get("total_count", 0)
    stats.avg_rating = stats_data.get("avg_rating", 0)
    stats.highest_rating = stats_data.get("highest_rating", 0)
    stats.lowest_rating = stats_data.get("lowest_rating", 0)

    stats.rating_distribution = {
        score: stats_data.get(f"score_{score}", 0) for score in score_range
    }

    stats.save()
