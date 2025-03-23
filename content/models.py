from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ArticleRatingStats(models.Model):
    article = models.OneToOneField(
        Article, related_name="rating_stats", on_delete=models.CASCADE
    )
    total_count = models.PositiveIntegerField(default=0)
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    rating_distribution = models.JSONField(default=dict)
    highest_rating = models.IntegerField(default=0)
    lowest_rating = models.IntegerField(default=0)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Article Rating Stats"
        verbose_name_plural = "Article Rating Stats"

    def __str__(self):
        return f"Rating stats for {self.article.title}"


class Rating(models.Model):
    article = models.ForeignKey(
        Article, related_name="ratings", on_delete=models.CASCADE
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("article", "user")
        indexes = [
            models.Index(fields=["article"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"Rating {self.score} for {self.article.title} by {self.user.phone}"
