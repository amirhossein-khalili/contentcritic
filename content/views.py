from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from content.models import Article

from .models import Rating
from .pagination import ArticlePagination
from .serializers import ArticleListSerializer, RatingCreateSerializer


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        article = request.data.get("article")
        score = request.data.get("score")

        rating = Rating.objects.filter(user=user, article=article).first()

        if rating:
            rating.score = score
            rating.save()
            serializer = self.get_serializer(rating)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
