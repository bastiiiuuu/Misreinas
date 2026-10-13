# Migración generada por makemigrations con Django 5.2.18; se documenta sin cambiar sus operaciones.

from django.db import migrations, models  # Importa las operaciones de migración y los tipos de campos que describen el esquema histórico.


class Migration(migrations.Migration):  # Django descubre esta clase para aplicar o revertir los cambios del esquema de la app.

    initial = True  # Marca este archivo como la primera migración de sucursales.

    dependencies = []  # El modelo no tiene relaciones con otras tablas, así que no requiere migraciones previas de otras apps.

    operations = [  # Enumera los cambios que migrate ejecutará; definir el modelo en Python por sí solo no crea su tabla.
        migrations.CreateModel(  # Crea el modelo histórico y su tabla usando el backend SQLite configurado.
            name='Sucursal',  # Con el nombre de app, genera por defecto la tabla sucursales_sucursal.
            fields=[  # Describe la clave primaria implícita y los seis campos explícitos de models.py.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),  # id es automático, identifica cada fila, y serialize=False evita duplicarlo como campo ordinario en serializaciones del modelo.
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre')),  # Conserva el tipo, longitud máxima y etiqueta del nombre.
                ('direccion', models.CharField(max_length=255, verbose_name='Dirección')),  # Conserva el campo obligatorio de dirección.
                ('descripcion', models.TextField(help_text='Incluye el horario y los servicios; puedes separarlos con saltos de línea.', verbose_name='Descripción')),  # Conserva el texto largo y la ayuda del formulario.
                ('imagen', models.ImageField(upload_to='sucursales/', verbose_name='Imagen')),  # Guarda una ruta relativa y conserva el subdirectorio de subida.
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),  # Conserva el timestamp automático de creación como metadato del campo histórico.
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),  # Conserva el timestamp automático de edición; este comportamiento es de Django, no un trigger SQL.
            ],  # Cierra la lista de columnas del modelo histórico.
            options={  # Conserva opciones del modelo que también forman parte del estado de migración.
                'verbose_name': 'Sucursal',  # Etiqueta singular del modelo.
                'verbose_name_plural': 'Sucursales',  # Etiqueta plural del modelo.
                'ordering': ('-created', '-pk'),  # Guarda el orden por defecto del ORM; no equivale al orden físico de filas en SQLite.
            },  # Cierra las opciones históricas.
        ),  # Cierra la operación de creación del modelo.
    ]  # Cierra las operaciones de esta migración inicial.
