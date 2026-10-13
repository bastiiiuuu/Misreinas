from django.urls import path  # Vincula una ruta local con su función de vista.
from . import views  # Importa las vistas de la app about.
urlpatterns = [  # Declara las rutas que siguen al prefijo nosotros/ del proyecto.
    path("", views.nosotros, name="nosotros"),  # Atiende /nosotros/ y registra el nombre usado por los menús.
]  # Cierra la lista de rutas de esta app.
