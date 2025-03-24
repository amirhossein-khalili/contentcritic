from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from content.models import Article, Rating


class ArticleListViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(phone="1234567890", password="pass123")
        self.article1 = Article.objects.create(title="Article 1", content="Content 1")
        self.article2 = Article.objects.create(title="Article 2", content="Content 2")
        # Create a rating for article1 for the test user.
        Rating.objects.create(article=self.article1, user=self.user, score=4)

    def test_article_list_unauthenticated(self):
        """
        The article list should return articles with the 'user_rating' field as None when not authenticated.
        """
        url = reverse("content:article-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # Check that each article includes the expected fields.
        for article in response.data.get("results", []):
            self.assertIn("id", article)
            self.assertIn("title", article)
            self.assertIn("avg_rating", article)
            self.assertIn("user_rating", article)
            self.assertIsNone(article["user_rating"])

    def test_article_list_authenticated(self):
        """
        When authenticated, the user should see his own rating for articles where available.
        """
        url = reverse("content:article-list")
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # article1 should include a rating from the user; article2 should not.
        for article in response.data.get("results", []):
            if article["id"] == self.article1.id:
                self.assertEqual(article["user_rating"], 4)
            elif article["id"] == self.article2.id:
                self.assertIsNone(article["user_rating"])


class RatingCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(phone="1234567890", password="pass123")
        self.article = Article.objects.create(
            title="Rating Article", content="Some content for rating."
        )
        self.url = reverse("content:rating-create")

    def test_create_rating_authenticated(self):
        """
        An authenticated user should be able to create a rating.
        """
        self.client.force_authenticate(user=self.user)
        data = {"article": self.article.id, "score": 3}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)
        rating = Rating.objects.get(article=self.article, user=self.user)
        self.assertEqual(rating.score, 3)

    def test_create_rating_update_existing(self):
        """
        Posting a rating for an article that the user already rated should update the existing rating.
        """
        self.client.force_authenticate(user=self.user)
        # Create the initial rating.
        data = {"article": self.article.id, "score": 2}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 201)
        # Update the rating.
        data = {"article": self.article.id, "score": 4}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 200)
        rating = Rating.objects.get(article=self.article, user=self.user)
        self.assertEqual(rating.score, 4)

    def test_create_rating_unauthenticated(self):
        """
        An unauthenticated user should not be allowed to create a rating.
        """
        data = {"article": self.article.id, "score": 3}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_rating_invalid_score(self):
        """
        Creating a rating with an invalid score (outside 0-5) should return a 400 error.
        """
        self.client.force_authenticate(user=self.user)
        data = {"article": self.article.id, "score": 6}  # Invalid score
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("score", response.data)
