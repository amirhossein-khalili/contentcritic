from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Article, Rating


class RatingSignalTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(phone="1234567890", password="pass123")
        self.user2 = User.objects.create_user(phone="1234567891", password="pass123")
        self.article = Article.objects.create(
            title="Signal Test Article", content="Content for signal testing."
        )

    def test_rating_signal_on_create(self):
        """
        When a rating is created, the ArticleRatingStats for the article should update accordingly.
        """
        Rating.objects.create(article=self.article, user=self.user, score=4)
        # Refresh stats from DB
        self.article.rating_stats.refresh_from_db()
        self.assertEqual(self.article.rating_stats.total_count, 1)
        self.assertAlmostEqual(float(self.article.rating_stats.avg_rating), 4.0)
        self.assertEqual(self.article.rating_stats.highest_rating, 4)
        self.assertEqual(self.article.rating_stats.lowest_rating, 4)
        # Access using string key "4"
        self.assertEqual(self.article.rating_stats.rating_distribution["4"], 1)

    def test_rating_signal_on_update(self):
        """
        When an existing rating is updated, the ArticleRatingStats should reflect the new score.
        """
        rating = Rating.objects.create(article=self.article, user=self.user, score=3)
        # Update rating score
        rating.score = 5
        rating.save()
        self.article.rating_stats.refresh_from_db()
        self.assertEqual(self.article.rating_stats.total_count, 1)
        self.assertAlmostEqual(float(self.article.rating_stats.avg_rating), 5.0)
        self.assertEqual(self.article.rating_stats.highest_rating, 5)
        self.assertEqual(self.article.rating_stats.lowest_rating, 5)
        self.assertEqual(self.article.rating_stats.rating_distribution["5"], 1)

    def test_rating_signal_with_multiple_ratings(self):
        """
        With multiple ratings, the aggregated stats should be calculated correctly.
        """
        Rating.objects.create(article=self.article, user=self.user, score=3)
        Rating.objects.create(article=self.article, user=self.user2, score=5)
        self.article.rating_stats.refresh_from_db()
        self.assertEqual(self.article.rating_stats.total_count, 2)
        self.assertAlmostEqual(
            float(self.article.rating_stats.avg_rating), 4.0
        )  # (3+5)/2
        self.assertEqual(self.article.rating_stats.highest_rating, 5)
        self.assertEqual(self.article.rating_stats.lowest_rating, 3)
        self.assertEqual(self.article.rating_stats.rating_distribution["3"], 1)
        self.assertEqual(self.article.rating_stats.rating_distribution["5"], 1)
