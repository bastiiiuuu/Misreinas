from django.apps import AppConfig  # Importa la clase base de configuración de apps.
class ContactConfig(AppConfig):  # Define los metadatos de la app independiente de Contacto.
    default_auto_field = "django.db.models.BigAutoField"  # Configura el id automático de cualquier futuro modelo de contacto.
    name = "contact"  # Indica el paquete Python que Django debe registrar.
    verbose_name = "Contacto"  # Establece su etiqueta legible en Django.
