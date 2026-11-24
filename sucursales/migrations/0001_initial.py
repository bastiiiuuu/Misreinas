

from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=120, verbose_name='Nombre')),
                ('direccion', models.CharField(max_length=255, verbose_name='Dirección')),
                ('descripcion', models.TextField(help_text='Incluye el horario y los servicios; puedes separarlos con saltos de línea.', verbose_name='Descripción')),
                ('imagen', models.ImageField(upload_to='sucursales/', verbose_name='Imagen')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Sucursal',
                'verbose_name_plural': 'Sucursales',
                'ordering': ('-created', '-pk'),
            },
        ),
    ]
