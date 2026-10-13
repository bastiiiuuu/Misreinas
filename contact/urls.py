from django.urls import path  # Define la correspondencia entre una ruta y una vista.
from . import views  # Carga las vistas del paquete contact.
urlpatterns = [  # Agrupa las rutas internas de la sección Contacto.
    path("", views.contacto, name="contacto"),  # Atiende /contacto/ y permite generar enlaces con el nombre contacto.
]  # Cierra las rutas de esta app independiente.
