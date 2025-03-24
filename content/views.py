from django.db.models import Prefetch
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Article, Rating
from .pagination import ArticlePagination
from .serializers import ArticleListSerializer, RatingCreateSerializer


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = (
            Article.objects.all()
            .order_by("-created_at")
            .prefetch_related("rating_stats")
        )
        if self.request.user.is_authenticated:
            user_ratings_prefetch = Prefetch(
                "ratings",
                queryset=Rating.objects.filter(user=self.request.user),
                to_attr="user_rating_list",
            )
            queryset = queryset.prefetch_related(user_ratings_prefetch)
        return queryset


class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        article = validated_data["article"]
        score = validated_data["score"]

        rating, created = Rating.objects.update_or_create(
            article=article, user=user, defaults={"score": score}
        )

        serializer = self.get_serializer(rating)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
