"""Entrada WSGI para servidores que usan el protocolo síncrono de Python."""
import os  # Permite configurar la variable de entorno con los settings.
from django.core.wsgi import get_wsgi_application  # Construye la aplicación WSGI de Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misreinas.settings")  # Selecciona el paquete existente en minúsculas salvo que el servidor indique otros settings.
application = get_wsgi_application()  # Expone el callable application que recibe las solicitudes del servidor WSGI.
