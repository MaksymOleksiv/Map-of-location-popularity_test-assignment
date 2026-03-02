from rest_framework import serializers
from .models import Category, Location, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)

    user_name = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Review
        fields = [
            "id",
            "location",
            "user_name",
            "text",
            "rating",
            "likes_count",
            "dislikes_count",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class LocationSerializer(serializers.ModelSerializer):
    reviews_count = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    popularity_score = serializers.FloatField(read_only=True)

    author_name = serializers.ReadOnlyField(source="author.username")
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = Location
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_name",
            "latitude",
            "longitude",
            "author_name",
            "reviews_count",
            "avg_rating",
            "popularity_score",
            "created_at",
        ]
        read_only_fields = ["id", "author_name", "created_at"]
