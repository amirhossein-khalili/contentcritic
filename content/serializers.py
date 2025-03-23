from rest_framework import serializers

from .models import Article, Rating


class ArticleListSerializer(serializers.ModelSerializer):
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "title", "user_rating"]

    def get_user_rating(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            rating = Rating.objects.filter(article=obj, user=user).first()
            return rating.score if rating else None
        return None


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["article", "score"]

    def validate_score(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Score must be between 1 and 5.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return Rating.objects.create(user=user, **validated_data)
