from django.contrib import admin
from .models import MensajeContacto


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sucursal", "contacto", "created")
    list_filter = ("sucursal", "created")
    search_fields = ("nombre", "contacto", "mensaje")
    readonly_fields = ("created",)
