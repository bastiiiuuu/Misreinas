from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="api-index"),
    path("ofertas/", views.ofertas, name="api-ofertas"),
    path("ofertas/<int:pk>/", views.oferta, name="api-oferta"),
    path("categorias/", views.categorias, name="api-categorias"),
    path("sucursales/", views.sucursales, name="api-sucursales"),
]
