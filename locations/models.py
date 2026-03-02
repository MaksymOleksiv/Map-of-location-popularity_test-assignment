from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator as Min, MaxValueValidator as Max
from django.db.models import Avg
from .managers import LocationManager, ReviewManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return str(self.name)


class Location(models.Model):

    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="locations"
    )

    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="locations"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = LocationManager()

    def __str__(self) -> str:
        return str(self.title)

    def get_popularity(self):
        if hasattr(self, "popularity_score"):
            return self.popularity_score
        count = self.reviews.count()
        avg = self.reviews.aggregate(Avg("rating"))["rating__avg"] or 0
        return (count * 2) + (float(avg) * 5)


class Review(models.Model):
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="reviews"
    )

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reviews"
    )

    text = models.TextField()

    rating = models.PositiveSmallIntegerField(
        validators=[
            Min(1, message="Rating must be at least 1"),
            Max(5, message="Rating cannot be more than 5"),
        ],
        verbose_name="Rating (1-5)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReviewManager()

    def __str__(self) -> str:
        return f"Review by {self.user.username} for {self.location.title} ({self.pk})"

    @property
    def rating_balance(self):
        likes = getattr(self, "likes_count", 0)
        dislikes = getattr(self, "dislikes_count", 0)
        return likes - dislikes


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, "Like"),
        (-1, "Dislike"),
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="votes"
    )
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("user", "review")


class Subscription(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="subscriptions"
    )
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="subscriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "location")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} subscribed to {self.location.title}"
