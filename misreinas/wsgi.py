

"""Entrada WSGI para servidores que usan el protocolo síncrono de Python."""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misreinas.settings")
application = get_wsgi_application()
