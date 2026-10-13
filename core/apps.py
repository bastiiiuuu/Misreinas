from django.apps import AppConfig  # Importa la clase base que describe una app instalada.
class CoreConfig(AppConfig):  # Define los metadatos de la app independiente de Inicio.
    default_auto_field = "django.db.models.BigAutoField"  # Define la clave primaria id automática de 64 bits que utiliza el modelo Oferta.
    name = "core"  # Debe coincidir con el paquete Python que contiene esta app.
    verbose_name = "Inicio"  # Define el nombre legible de la app para la interfaz administrativa.
