from django.contrib import admin

from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_filter = ("owner", "created_at", "updated_at")
    list_display = ("name", "owner", "created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"
    search_fields = ("name", "owner")
