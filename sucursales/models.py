"""Las imágenes se guardan en media y la base conserva su ruta. Las copias de seguridad de datos deben incluir ambos recursos para recuperar el catálogo."""
from django.db import models

class Sucursal(models.Model):

    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre",
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name="Dirección",
    )
    descripcion = models.TextField(
        verbose_name="Descripción",
        help_text="Incluye el horario y los servicios; puedes separarlos con saltos de línea.",
    )

    imagen = models.ImageField(
        upload_to="sucursales/",
        verbose_name="Imagen",
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización",
    )

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"
        ordering = ("-created", "-pk")

    def __str__(self):
        return self.nombre
