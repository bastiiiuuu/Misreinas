

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('ofertas', '0002_copiar_ofertas_y_relaciones'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Oferta',
        ),
    ]
