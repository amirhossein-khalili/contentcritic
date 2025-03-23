from django.urls import path

from .views import ArticleListView, RatingCreateView

app_name = "content"
urlpatterns = [
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/ratings/create/", RatingCreateView.as_view(), name="rating-create"),
]
