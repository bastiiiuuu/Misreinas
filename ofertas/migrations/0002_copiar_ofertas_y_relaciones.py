

from django.db import migrations

def copiar_ofertas(apps, schema_editor):
    anterior = apps.get_model("core", "Oferta")
    nueva = apps.get_model("ofertas", "Oferta")
    categoria_model = apps.get_model("categorias", "Categoria")
    sucursal_model = apps.get_model("sucursales", "Sucursal")
    alias = schema_editor.connection.alias
    nombres = {"lacteos": "Lácteos", "huevos": "Huevos", "carnes": "Carnes", "bebidas": "Bebidas", "desayuno": "Desayuno", "despensa": "Despensa"}
    etiquetas = {}
    for slug, nombre in nombres.items():
        etiquetas[slug], _ = categoria_model.objects.using(alias).get_or_create(slug=slug, defaults={"nombre": nombre})
    for original in anterior.objects.using(alias).all():
        es_bebida = "jack" in original.nombre.lower() or "stella" in original.nombre.lower()
        patron_local = "Lobos" if es_bebida else "Delfines"
        local = sucursal_model.objects.using(alias).filter(nombre__icontains=patron_local).first()
        if local is None:
            raise RuntimeError("Falta el local de las ofertas antiguas; restaura las sucursales antes de migrar.")
        oferta = nueva.objects.using(alias).create(id=original.pk, nombre=original.nombre, descripcion=original.descripcion, precio=original.precio, imagen=original.imagen.name, sucursal_id=local.pk)
        nueva.objects.using(alias).filter(pk=oferta.pk).update(created=original.created, updated=original.updated)
        nombre = original.nombre.lower()
        if es_bebida:
            oferta.categorias.add(etiquetas["bebidas"])
        elif "pollo" in nombre:
            oferta.categorias.add(etiquetas["carnes"])
        elif "huevo" in nombre:
            oferta.categorias.add(etiquetas["huevos"], etiquetas["desayuno"])
        else:
            oferta.categorias.add(etiquetas["lacteos"], etiquetas["desayuno"])

def restaurar_ofertas(apps, schema_editor):
    anterior = apps.get_model("core", "Oferta")
    nueva = apps.get_model("ofertas", "Oferta")
    alias = schema_editor.connection.alias
    for oferta in nueva.objects.using(alias).all():
        anterior.objects.using(alias).update_or_create(pk=oferta.pk, defaults={"nombre": oferta.nombre, "descripcion": oferta.descripcion, "precio": oferta.precio, "imagen": oferta.imagen.name})
        anterior.objects.using(alias).filter(pk=oferta.pk).update(created=oferta.created, updated=oferta.updated)

class Migration(migrations.Migration):

    dependencies = [("ofertas", "0001_initial"), ("core", "0001_initial")]

    operations = [migrations.RunPython(copiar_ofertas, restaurar_ofertas)]
