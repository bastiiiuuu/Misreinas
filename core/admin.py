from django.contrib import admin  # Importa el panel administrativo que genera formularios a partir de los modelos.
from .models import Oferta  # Importa el modelo de esta misma app; el punto indica una importación relativa al paquete core.

@admin.register(Oferta)  # Registra Oferta una sola vez y la asocia con la configuración de la clase siguiente.
class OfertaAdmin(admin.ModelAdmin):  # Personaliza la edición de ofertas; no crea una tabla adicional ni modifica el modelo.
    list_display = ("nombre", "precio", "created", "updated")  # Muestra nombre, precio y fechas como columnas de la lista administrativa.
    search_fields = ("nombre", "descripcion")  # Habilita búsqueda por producto, local o texto de la publicación almacenada.
    list_filter = ("created",)  # Permite filtrar las filas por su fecha de carga al proyecto.
    readonly_fields = ("created", "updated")  # Muestra las fechas automáticas sin permitir escribirlas manualmente.
    fields = ("nombre", "descripcion", "precio", "imagen", "created", "updated")  # Ordena los seis atributos en el formulario de agregar y editar.
