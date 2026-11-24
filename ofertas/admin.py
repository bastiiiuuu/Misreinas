

from django.contrib import admin
from .models import Oferta

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):

    list_display = ("nombre", "precio", "sucursal", "created", "updated")
    list_display_links = ("nombre",)
    list_filter = ("categorias", "sucursal", "created")
    search_fields = ("nombre", "descripcion", "sucursal__nombre")

    readonly_fields = ("created", "updated")
    fields = ("nombre", "descripcion", "precio", "imagen", "sucursal", "categorias", "created", "updated")
    filter_horizontal = ("categorias",)

    date_hierarchy = "created"
    list_per_page = 10
    ordering = ("-created", "-pk")
    list_select_related = ("sucursal",)

    save_on_top = True
