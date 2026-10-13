from django.contrib import admin  # Importa el sistema de administración que genera formularios a partir del modelo.
from .models import Sucursal  # Importa el modelo de esta app mediante una ruta relativa.

@admin.register(Sucursal)  # Registra el modelo una sola vez y asocia la configuración de la clase siguiente al panel.
class SucursalAdmin(admin.ModelAdmin):  # Personaliza el Admin; no crea otra tabla ni modifica los campos del modelo.
    list_display = ("nombre", "direccion", "created", "updated")  # Selecciona las columnas visibles en la lista de sucursales.
    search_fields = ("nombre", "direccion", "descripcion")  # Permite buscar registros por estos campos de texto.
    list_filter = ("created",)  # Añade el filtro lateral por fecha de creación.
    readonly_fields = ("created", "updated")  # Muestra los timestamps en el formulario, aunque sus campos no son editables.
    fields = ("nombre", "direccion", "descripcion", "imagen", "created", "updated")  # Define el orden de los campos al agregar o editar.
