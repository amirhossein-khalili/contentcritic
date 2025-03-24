from rest_framework import serializers

from .models import Article, Rating


class ArticleListSerializer(serializers.ModelSerializer):
    user_rating = serializers.SerializerMethodField()
    avg_rating = serializers.DecimalField(
        source="rating_stats.avg_rating", max_digits=3, decimal_places=2, read_only=True
    )

    class Meta:
        model = Article
        fields = ["id", "title", "avg_rating", "user_rating"]

    def get_user_rating(self, obj):
        if hasattr(obj, "user_rating_list") and obj.user_rating_list:
            return obj.user_rating_list[0].score
        return None


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["article", "score"]

    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Score must be between 0 and 5.")
        return value
