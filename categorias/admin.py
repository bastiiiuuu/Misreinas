

from django.contrib import admin
from .models import Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "created", "updated")
    search_fields = ("nombre", "descripcion")
    list_filter = ("created",)
    prepopulated_fields = {"slug": ("nombre",)}
    readonly_fields = ("created", "updated")
    fields = ("nombre", "slug", "descripcion", "created", "updated")
    ordering = ("nombre", "pk")
    list_per_page = 20
