from django.db.models import Avg, Count, Max, Min
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

    stats, created = ArticleRatingStats.objects.get_or_create(article=article)

    ratings = article.ratings.all()

    stats.total_count = ratings.count()
    stats.avg_rating = ratings.aggregate(Avg("score"))["score__avg"] or 0
    stats.highest_rating = ratings.aggregate(Max("score"))["score__max"] or 0
    stats.lowest_rating = ratings.aggregate(Min("score"))["score__min"] or 0

    distribution = {}
    for i in range(1, 6):
        distribution[i] = ratings.filter(score=i).count()

    stats.rating_distribution = distribution
    stats.save()
