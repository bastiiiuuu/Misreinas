from django.urls import path  # Importa la función que vincula rutas con vistas y nombres.
from . import views  # Importa las vistas de esta misma app mediante una referencia relativa.
urlpatterns = [  # Declara las rutas locales que incluye misreinas/urls.py; Inicio contiene el catálogo paginado de ofertas.
    path("", views.inicio, name="inicio"),  # La ruta vacía atiende /; el nombre inicio permite generar enlaces con la etiqueta url.
]  # Cierra las rutas; no declaramos app_name para usar los nombres simples exigidos en los menús.
