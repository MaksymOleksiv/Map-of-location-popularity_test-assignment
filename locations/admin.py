from django.contrib import admin
from .models import Location, Category, Review, Vote


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Review)
admin.site.register(Vote)
