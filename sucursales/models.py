from django.db import models  # Importa el ORM: convierte clases y campos Python en una estructura de base de datos.

class Sucursal(models.Model):  # Heredar de Model aporta el ORM y representa una tabla con una fila por sucursal.
    nombre = models.CharField(  # Campo 1: texto corto para identificar la sucursal en el sitio y en el Admin.
        max_length=120,  # Limita a 120 caracteres; se refleja en el formulario y en la definición del campo.
        verbose_name="Nombre",  # Etiqueta legible que mostrará el formulario administrativo.
    )  # Cierra nombre; blank=False y null=False son los valores predeterminados, por lo que el campo es obligatorio.
    direccion = models.CharField(  # Campo 2: dirección postal como texto, sin crear un modelo adicional para esta evaluación.
        max_length=255,  # Permite escribir calle, número, sector y comuna con un límite explícito.
        verbose_name="Dirección",  # Muestra la etiqueta con tilde en el Admin.
    )  # Cierra direccion; no usamos unique porque dos registros de prueba pueden compartir una dirección.
    descripcion = models.TextField(  # Campo 3: texto largo para explicar horarios y servicios sin una longitud fija de CharField.
        verbose_name="Descripción",  # Identifica el contenido que se editará desde el Admin.
        help_text="Incluye el horario y los servicios; puedes separarlos con saltos de línea.",  # Explica al editor qué escribir en este campo.
    )  # Cierra descripcion; concentrar estos datos en texto mantiene exactamente seis campos explícitos.
    imagen = models.ImageField(  # Campo 4: gestiona un archivo de imagen; el formulario valida su formato usando Pillow.
        upload_to="sucursales/",  # Guarda el archivo dentro de MEDIA_ROOT/sucursales/ con el almacenamiento local predeterminado.
        verbose_name="Imagen",  # Etiqueta del selector de archivo que verá el editor en el Admin.
    )  # Cierra imagen; la BD almacena la ruta relativa, no los bytes del archivo, y el campo exige una imagen en el Admin.
    created = models.DateTimeField(  # Campo 5: registra cuándo se creó por primera vez esta fila.
        auto_now_add=True,  # Django fija la fecha y hora en el primer save(); las ediciones posteriores no la regeneran.
        verbose_name="Fecha de creación",  # Da un nombre comprensible al timestamp en el Admin.
    )  # Cierra created; auto_now_add implica editable=False y blank=True, por lo que no se introduce manualmente en un formulario.
    updated = models.DateTimeField(  # Campo 6: registra la fecha y hora del último guardado normal del modelo.
        auto_now=True,  # Se actualiza en save(); QuerySet.update() omite save() y no activa este comportamiento automáticamente.
        verbose_name="Última actualización",  # Permite distinguir el timestamp de edición del de creación.
    )  # Cierra updated; con save(update_fields=...) debe incluirse updated para ejecutar su actualización automática.

    class Meta:  # Configura metadatos del modelo; esta clase no agrega atributos de base de datos.
        verbose_name = "Sucursal"  # Etiqueta singular utilizada por Django Admin.
        verbose_name_plural = "Sucursales"  # Etiqueta plural que identifica la lista de registros.
        ordering = ("-created", "-pk")  # Ordena de más nuevo a más antiguo y desempata por id para estabilizar la paginación.

    def __str__(self):  # self es la instancia actual; este método define su representación textual para el Admin y la consola.
        return self.nombre  # Devuelve una cadena útil en vez de la representación genérica Sucursal object (id).
