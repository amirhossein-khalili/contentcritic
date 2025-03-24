from django.test import TestCase

from content.models import Article


class ArticleModelTests(TestCase):
    def test_article_creation_creates_rating_stats(self):
        """
        When an Article is created, an ArticleRatingStats record should be automatically created.
        """
        article = Article.objects.create(title="Test Article", content="Some content")

        self.assertIsNotNone(article.rating_stats)
        self.assertEqual(article.rating_stats.total_count, 0)
        self.assertEqual(article.rating_stats.avg_rating, 0)
        self.assertEqual(
            article.rating_stats.rating_distribution,
            {score: 0 for score in range(0, 6)},
        )
