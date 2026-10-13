#!/usr/bin/env python
"""Punto de entrada para ejecutar comandos administrativos de este proyecto."""
import os  # Permite indicar qué módulo de configuración debe cargar Django.
import sys  # Proporciona los argumentos escritos después de python manage.py.

def main():  # Agrupa el arranque para poder importar el archivo sin ejecutar comandos.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misreinas.settings")  # Usa el nombre exacto del paquete existente, en minúsculas, sin sobrescribir una configuración externa.
    from django.core.management import execute_from_command_line  # Importa el ejecutor después de definir el módulo de settings.
    execute_from_command_line(sys.argv)  # Entrega a Django el comando y sus opciones, por ejemplo migrate o runserver.

if __name__ == "__main__":  # Solo entra cuando este archivo se ejecuta directamente desde la terminal.
    main()  # Inicia el procesamiento del comando solicitado por el estudiante.
