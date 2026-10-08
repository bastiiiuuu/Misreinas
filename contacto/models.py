from django.db import models


class MensajeContacto(models.Model):
    SUCURSALES = [
        ("delfines", "Almacén Mis Reinas"),
        ("lobos", "Minimarket Mis Reinas"),
        ("botilleria", "Botillería Mis Reinas"),
    ]
    nombre = models.CharField(max_length=100)
    contacto = models.CharField("teléfono o correo", max_length=150)
    sucursal = models.CharField(max_length=20, choices=SUCURSALES)
    mensaje = models.TextField()
    created = models.DateTimeField("fecha de recepción", auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"

    def __str__(self):
        return f"{self.nombre} · {self.get_sucursal_display()}"
