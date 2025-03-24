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
    article = instance.article
    stats, _ = ArticleRatingStats.objects.get_or_create(article=article)
    ratings = article.ratings.all()

    stats_data = ratings.aggregate(
        total_count=Count("id"),
        avg_rating=Avg("score"),
        highest_rating=Max("score"),
        lowest_rating=Min("score"),
        score_1=Count(Case(When(score=1, then=1), output_field=IntegerField())),
        score_2=Count(Case(When(score=2, then=1), output_field=IntegerField())),
        score_3=Count(Case(When(score=3, then=1), output_field=IntegerField())),
        score_4=Count(Case(When(score=4, then=1), output_field=IntegerField())),
        score_5=Count(Case(When(score=5, then=1), output_field=IntegerField())),
    )

    stats.total_count = stats_data["total_count"]
    stats.avg_rating = stats_data["avg_rating"] or 0
    stats.highest_rating = stats_data["highest_rating"] or 0
    stats.lowest_rating = stats_data["lowest_rating"] or 0
    stats.rating_distribution = {
        1: stats_data["score_1"],
        2: stats_data["score_2"],
        3: stats_data["score_3"],
        4: stats_data["score_4"],
        5: stats_data["score_5"],
    }
    stats.save()
