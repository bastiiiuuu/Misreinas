from django.apps import AppConfig  # Importa la clase base que configura una app de Django.
class AboutConfig(AppConfig):  # Define los metadatos de la app independiente de Nosotros.
    default_auto_field = "django.db.models.BigAutoField"  # Fija el tipo de id automático para eventuales modelos de esta app.
    name = "about"  # Coincide con el paquete Python incluido en INSTALLED_APPS.
    verbose_name = "Nosotros"  # Proporciona un nombre legible para esta app.
