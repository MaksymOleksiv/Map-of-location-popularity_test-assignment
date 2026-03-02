from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
import pandas as pd
from .models import Category, Location, Review, Vote, Subscription
from .serializers import CategorySerializer, LocationSerializer, ReviewSerializer
from .permissions import IsAuthorOrReadOnly
from .filters import LocationFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by("-popularity_score")
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = LocationFilter
    search_fields = ["title", "description"]
    ordering_fields = ["popularity_score", "created_at"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def export_csv(self, request):
        locations = self.filter_queryset(self.get_queryset())

        data = []
        for loc in locations:
            data.append(
                {
                    "ID": loc.id,
                    "Title": loc.title,
                    "Description": loc.description,
                    "Category": loc.category.name if loc.category else "N/A",
                    "Popularity": loc.popularity_score,
                    "Author": loc.author.username,
                }
            )

        df = pd.DataFrame(data)
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="locations.csv"'
        df.to_csv(path_or_buf=response, index=False)
        return response

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def subscribe(self, request, pk=None):
        location = self.get_object()
        subscription, created = Subscription.objects.get_or_create(
            user=request.user, 
            location=location
        )
        if not created:
            subscription.delete()
            return Response({"status": "Unsubscribed", "subscribed": False})
        return Response({"status": "Subscribed", "subscribed": True})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["location"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def vote(self, request, pk=None):
        review = self.get_object()
        value = request.data.get("value")

        if value not in [1, -1]:
            return Response(
                {"error": "Value must be 1 or -1"}, status=status.HTTP_400_BAD_REQUEST
            )

        if review.user == request.user:
            return Response({"error": "Cannot vote for your own review"}, status=400)

        _, _ = Vote.objects.update_or_create(
            user=request.user, review=review, defaults={"value": value}
        )
        return Response({"status": "Vote recorded"})
