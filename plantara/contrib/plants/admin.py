from django.contrib import admin

from plantara.admin import admin_site

from .models import Plant


class PlantAdmin(admin.ModelAdmin):
    list_filter = ("owner", "created_at", "updated_at")
    list_display = ("name", "owner", "created_at", "updated_at")
    list_per_page = 20
    date_hierarchy = "created_at"
    search_fields = ("name", "owner")


admin_site.register(Plant, PlantAdmin)
