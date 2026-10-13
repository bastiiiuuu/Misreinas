from django.apps import AppConfig  # Importa la clase que permite registrar los metadatos de esta app.
class SucursalesConfig(AppConfig):  # Configura la app independiente de Sucursales.
    default_auto_field = "django.db.models.BigAutoField"  # Hace que el modelo reciba un id automático de 64 bits.
    name = "sucursales"  # Coincide con el paquete del modelo, las migraciones y el Admin.
    verbose_name = "Sucursales"  # Define cómo se identifica esta app en el panel de Django.
