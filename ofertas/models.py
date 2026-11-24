"""Una oferta pertenece a una sucursal protegida frente a borrado y puede llevar varias categorías. El precio desconocido se guarda como null para distinguirlo de un producto gratuito."""
from django.core.validators import MinValueValidator
from django.db import models

class Oferta(models.Model):

    nombre = models.CharField(max_length=150, verbose_name="Nombre del producto")
    descripcion = models.TextField(verbose_name="Descripción", help_text="Indica qué cantidad incluye el precio de la promoción.")

    precio = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        blank=True,
        null=True,
        validators=[MinValueValidator(1)],
        verbose_name="Precio (CLP)",
    )

    imagen = models.ImageField(upload_to="ofertas/", verbose_name="Imagen")

    sucursal = models.ForeignKey(
        "sucursales.Sucursal",
        on_delete=models.PROTECT,
        related_name="ofertas",
        verbose_name="Sucursal",
    )

    categorias = models.ManyToManyField(
        "categorias.Categoria",
        related_name="ofertas",
        verbose_name="Etiquetas",
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
        ordering = ("-created", "-pk")

    def __str__(self):
        return self.nombre
