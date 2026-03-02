from django.db import models
from django.db.models import Avg, Count, ExpressionWrapper, F, FloatField, Q, Sum
from django.db.models.functions import Coalesce


class LocationQuerySet(models.QuerySet):
    def with_all_stats(self):
        return self.annotate(
            reviews_count=Count("reviews", distinct=True),
            avg_rating=Coalesce(Avg("reviews__rating"), 0.0, output_field=FloatField()),
        ).annotate(
            popularity_score=ExpressionWrapper(
                F("reviews_count") * 2.0 + F("avg_rating") * 5.0,
                output_field=FloatField(),
            )
        )


class LocationManager(models.Manager):
    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db).with_all_stats()


class ReviewQuerySet(models.QuerySet):
    def with_votes(self):
        return self.annotate(
            likes_count=Coalesce(Sum("votes__value", filter=Q(votes__value=1)), 0),
            dislikes_count=Coalesce(Sum("votes__value", filter=Q(votes__value=-1)), 0),
        )


class ReviewManager(models.Manager):
    def get_queryset(self):
        return ReviewQuerySet(self.model, using=self._db).with_votes()
