

from django.contrib import admin
from .models import Sucursal

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "created", "updated")
    search_fields = ("nombre", "direccion", "descripcion")
    list_filter = ("created",)
    readonly_fields = ("created", "updated")
    fields = ("nombre", "direccion", "descripcion", "imagen", "created", "updated")
    ordering = ("nombre", "pk")
    list_per_page = 10
    date_hierarchy = "created"
