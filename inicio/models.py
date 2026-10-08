from django.db import models
from django.core.validators import MinValueValidator


class Producto(models.Model):
    """Oferta del negocio, administrada desde el panel de Django."""
    CATEGORIAS = [
        ("panaderia", "Panadería"),
        ("abarrotes", "Abarrotes"),
        ("bebidas", "Bebidas"),
        ("mascotas", "Mascotas"),
        ("servicios", "Servicios"),
    ]
    nombre = models.CharField("nombre", max_length=100, unique=True)
    descripcion = models.TextField("descripción", blank=True)
    categoria = models.CharField("categoría", max_length=20, choices=CATEGORIAS)
    imagen = models.ImageField("imagen", upload_to="productos/")
    precio = models.PositiveIntegerField(
        "precio de ejemplo (CLP)", null=True, blank=True,
        validators=[MinValueValidator(1)],
        help_text="Precio ficticio para el prototipo. Sin precio, el producto no se agrega al carrito.",
    )
    unidad = models.CharField("unidad de venta", max_length=60, default="unidad")
    created = models.DateTimeField("fecha de creación", auto_now_add=True)
    updated = models.DateTimeField("última actualización", auto_now=True)

    class Meta:
        ordering = ["pk"]
        verbose_name = "producto o servicio"
        verbose_name_plural = "productos y servicios"

    def __str__(self):
        return self.nombre
