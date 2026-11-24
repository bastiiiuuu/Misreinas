

import django.core.validators
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre de la oferta')),
                ('descripcion', models.TextField(help_text='Indica qué incluye el precio y añade el enlace de la publicación de Facebook.', verbose_name='Descripción')),
                ('precio', models.DecimalField(blank=True, decimal_places=0, help_text='Deja vacío si no aparece un precio; el sitio mostrará Consultar precio.', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Precio publicado (CLP)')),
                ('imagen', models.ImageField(upload_to='ofertas/', verbose_name='Imagen de la oferta')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
            ],
            options={
                'verbose_name': 'Oferta',
                'verbose_name_plural': 'Ofertas',
                'ordering': ('-created', '-pk'),
            },
        ),
    ]
