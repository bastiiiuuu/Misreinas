

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categorias', '0001_initial'),
        ('sucursales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre del producto')),
                ('descripcion', models.TextField(help_text='Indica qué cantidad incluye el precio de la promoción.', verbose_name='Descripción')),
                ('precio', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Precio (CLP)')),
                ('imagen', models.ImageField(upload_to='ofertas/', verbose_name='Imagen')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('categorias', models.ManyToManyField(related_name='ofertas', to='categorias.categoria', verbose_name='Etiquetas')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ofertas', to='sucursales.sucursal', verbose_name='Sucursal')),
            ],
            options={
                'verbose_name': 'Oferta',
                'verbose_name_plural': 'Ofertas',
                'ordering': ('-created', '-pk'),
            },
        ),
    ]
