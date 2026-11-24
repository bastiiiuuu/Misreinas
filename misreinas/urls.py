

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/", include("api.urls")),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("ofertas/", include("ofertas.urls")),
    path("nosotros/", include("about.urls")),
    path("contacto/", include("contact.urls")),
    path("sucursales/", include("sucursales.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.pagina_no_encontrada"
