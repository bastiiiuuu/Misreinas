from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "precio", "unidad", "created", "updated")
    list_filter = ("categoria",)
    search_fields = ("nombre", "descripcion")
    readonly_fields = ("created", "updated")
    fields = ("nombre", "descripcion", "categoria", "imagen", "precio", "unidad", "created", "updated")
    list_per_page = 10
