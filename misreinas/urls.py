from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("inicio.urls")),
    path("nosotros/", include("nosotros.urls")),
    path("sucursales/", include("sucursales.urls")),
    path("contacto/", include("contacto.urls")),
    path("admin/", admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Administración de Mis Reinas"
admin.site.site_title = "Mis Reinas"
admin.site.index_title = "Catálogo y mensajes"
