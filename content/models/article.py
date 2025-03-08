from django.db import models
from django.conf import settings

class Article(models.Model):
    """
    Article command model - Stores authoritative data in SQL.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    review_count = models.PositiveIntegerField(default=0)
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.title
