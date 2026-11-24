

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("explorar-api/", TemplateView.as_view(template_name="ofertas/api.html"), name="api-demo"),
    path("", views.listado, name="ofertas"),
]
