"""El slug identifica las categorías en los filtros públicos. Debe conservarse estable si se comparten enlaces que lo utilizan."""
from django.db import models

class Categoria(models.Model):

    nombre = models.CharField(max_length=80, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=90, unique=True, verbose_name="Identificador de filtro")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Última actualización")

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ("nombre", "pk")

    def __str__(self):
        return self.nombre
