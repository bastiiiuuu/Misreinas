from django.core.validators import MinValueValidator  # Aporta un validador de formulario/modelo para rechazar precios menores que un peso.
from django.db import models  # Importa los campos y Model del ORM; Django traduce esta definición a una tabla mediante migraciones.

class Oferta(models.Model):  # Cada instancia representa una oferta; heredar Model aporta consulta, validación y persistencia mediante el ORM.
    nombre = models.CharField(  # Atributo 1: identifica el producto o promoción en las tarjetas y en el Admin.
        max_length=150,  # Limita la longitud de los nombres y permite títulos como una promoción de varios productos.
        verbose_name="Nombre de la oferta",  # Cambia la etiqueta del formulario sin cambiar el nombre Python del campo.
    )  # Cierra el campo; blank=False y null=False predeterminados lo hacen obligatorio en el formulario.
    descripcion = models.TextField(  # Atributo 2: explica cantidad, unidad, local y procedencia de la publicación histórica.
        verbose_name="Descripción",  # Identifica este texto largo en el formulario del Admin.
        help_text="Indica qué incluye el precio y añade el enlace de la publicación de Facebook.",  # Orienta al editor; no se guarda como parte de cada registro.
    )  # Cierra el campo obligatorio; TextField admite texto largo sin fijar aquí un max_length.
    precio = models.DecimalField(  # Atributo 3: conserva el precio publicado con precisión decimal, evitando errores de punto flotante.
        max_digits=10,  # Permite hasta diez dígitos en total; define la capacidad del campo de precio.
        decimal_places=0,  # Usa pesos chilenos enteros; este atributo controla la escala decimal del valor almacenado.
        blank=True,  # Permite dejar vacío el formulario si la publicación no informa un precio verificable.
        null=True,  # Almacena NULL en la BD cuando no se conoce el precio, distinguiéndolo de cero o de una oferta gratuita.
        validators=[MinValueValidator(1)],  # Exige al menos un peso cuando se ingresa un valor; los formularios del Admin ejecutan esta validación.
        verbose_name="Precio publicado (CLP)",  # Identifica la moneda y que el dato corresponde a una publicación histórica.
        help_text="Deja vacío si no aparece un precio; el sitio mostrará Consultar precio.",  # Evita inventar importes cuando solo se dispone de una fotografía.
    )  # Cierra precio; los validadores se ejecutan en el Admin o full_clean(), no automáticamente en cualquier save() del ORM.
    imagen = models.ImageField(  # Atributo 4: referencia la fotografía o afiche de la oferta; Pillow valida el archivo en el Admin.
        upload_to="ofertas/",  # Guarda los bytes dentro de MEDIA_ROOT/ofertas/ con el almacenamiento local configurado.
        verbose_name="Imagen de la oferta",  # Etiqueta del selector de archivo del formulario administrativo.
    )  # Cierra imagen; la BD conserva su ruta relativa y el archivo se almacena en media, sin incrustar sus bytes en SQLite.
    created = models.DateTimeField(  # Atributo 5: registra cuándo se creó esta fila en el proyecto, no cuándo se publicó en Facebook.
        auto_now_add=True,  # Fija el timestamp al primer save(); las ediciones posteriores no regeneran la fecha de creación.
        verbose_name="Fecha de creación",  # Hace comprensible el timestamp automático en la interfaz del Admin.
    )  # Cierra created; auto_now_add implica editable=False y no requiere que el estudiante ingrese una fecha.
    updated = models.DateTimeField(  # Atributo 6: registra la última edición realizada mediante un guardado normal.
        auto_now=True,  # Actualiza este campo durante save(); QuerySet.update() no llama a save() y no lo modifica automáticamente.
        verbose_name="Última actualización",  # Distingue la fecha de edición de la fecha de creación.
    )  # Cierra updated; si se utiliza save(update_fields=...), debe incluirse updated para activar su actualización.

    class Meta:  # Define metadatos; esta clase no agrega columnas ni cuenta como atributo del modelo.
        verbose_name = "Oferta"  # Nombre singular mostrado por Django Admin.
        verbose_name_plural = "Ofertas"  # Nombre de la lista de registros administrables.
        ordering = ("-created", "-pk")  # Ordena primero los registros nuevos y desempata por clave primaria para paginar una colección en orden definido.

    def __str__(self):  # self es la instancia actual; este método proporciona su representación textual.
        return self.nombre  # Hace que el Admin y la consola identifiquen la oferta por un nombre legible.
