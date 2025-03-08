from django.db import models
from django.conf import settings
from django.db.models import Q

class Review(models.Model):
    """
    Review command model - Stores authoritative data in SQL.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    article = models.ForeignKey(
        "content.Article",
        related_name="reviews",
        on_delete=models.CASCADE,
    )

    rating = models.IntegerField()

    class Meta:
        unique_together = ("user", "article")  # Fix: Use field names, not `_id`
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=0) & Q(rating__lte=5),
                name="rating_range",
            )
        ]

    def __str__(self):
        return f"Review of article {self.article.title} by {self.user.username}"
