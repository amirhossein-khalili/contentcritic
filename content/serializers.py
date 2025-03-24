from rest_framework import serializers

from .models import Article, Rating


class ArticleListSerializer(serializers.ModelSerializer):
    user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ["id", "title", "user_rating"]

    def get_user_rating(self, obj):
        if hasattr(obj, "user_rating_list") and obj.user_rating_list:
            return obj.user_rating_list[0].score
        return None


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["article", "score"]
        read_only_fields = ["article"]

    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Score must be between 0 and 5.")
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        return Rating.objects.create(user=user, **validated_data)


class RatingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["article", "score"]

    def validate_score(self, value):
        if not (0 <= value <= 5):
            raise serializers.ValidationError("Score must be between 0 and 5.")
        return value