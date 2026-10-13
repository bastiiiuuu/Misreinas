from django.urls import path  # Importa el constructor de rutas con nombre.
from . import views  # Importa la vista paginada de esta app.
urlpatterns = [  # Declara las rutas relativas al prefijo sucursales/ del proyecto.
    path("", views.listado_sucursales, name="sucursales"),  # Atiende /sucursales/ y registra el nombre usado por enlaces y paginación.
]  # Cierra las rutas de la sección dinámica.
