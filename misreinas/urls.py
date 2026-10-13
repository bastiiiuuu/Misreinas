from django.conf import settings  # Accede a MEDIA_URL y MEDIA_ROOT de la configuración activa.
from django.conf.urls.static import static  # Construye rutas para servir archivos subidos durante desarrollo con DEBUG=True.
from django.contrib import admin  # Proporciona las rutas internas del panel administrativo.
from django.urls import include, path  # path define prefijos y include delega el resto de la URL a cada app.

urlpatterns = [  # Django recorre estas rutas para encontrar la primera coincidencia válida.
    path("admin/", admin.site.urls),  # Monta el Admin en /admin/ con sus propias rutas de acceso y edición.
    path("", include("core.urls")),  # Delega la raíz a Inicio; core solo contiene la ruta vacía.
    path("nosotros/", include("about.urls")),  # Quita el prefijo nosotros/ y consulta las rutas de la app about.
    path("contacto/", include("contact.urls")),  # Delega /contacto/ a la app independiente de Contacto.
    path("sucursales/", include("sucursales.urls")),  # Delega /sucursales/ a la app que consulta y pagina el modelo.
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Asocia /media/ con su carpeta física; este helper solo añade rutas con DEBUG=True.
