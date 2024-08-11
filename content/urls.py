from django.urls import include, path

from . import views

app_name = "content"
urlpatterns = [
    path("list/", views.ArticleListView.as_view()),
    path(
        "<int:article_id>/rate/",
        AddArticleRatingView.as_view(),
    ),
]
