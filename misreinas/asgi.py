"""Entrada ASGI para servidores compatibles con el protocolo asíncrono de Python."""
import os  # Permite configurar la variable de entorno con los settings.
from django.core.asgi import get_asgi_application  # Construye la aplicación ASGI de Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misreinas.settings")  # Selecciona el paquete existente en minúsculas, igual que manage.py.
application = get_asgi_application()  # Expone el callable application que recibe solicitudes de un servidor ASGI.
