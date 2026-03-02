from django_filters import rest_framework as filters
from .models import Location


class LocationFilter(filters.FilterSet):
    min_popularity = filters.NumberFilter(
        field_name="popularity_score", lookup_expr="gte"
    )
    max_popularity = filters.NumberFilter(
        field_name="popularity_score", lookup_expr="lte"
    )
    category = filters.NumberFilter(field_name="category")

    class Meta:
        model = Location
        fields = ["category", "min_popularity", "max_popularity"]
