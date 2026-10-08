"""Carga el catálogo inicial y la cuenta solicitada en la evaluación."""
from pathlib import Path
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from inicio.models import Producto


PRODUCTOS = [
    ("Pan amasado", "Pan individual para acompañar el desayuno o la once.", "panaderia", "pan", 350, "unidad"),
    ("Leche entera 1 L", "Envase de un litro. Producto genérico de demostración.", "abarrotes", "leche", 1200, "caja de 1 L"),
    ("Arroz 1 kg", "Una opción para la despensa y las comidas de cada día.", "abarrotes", "arroz", 1500, "bolsa de 1 kg"),
    ("Fideos 400 g", "Pasta seca en envase de 400 gramos.", "abarrotes", "fideos", 1000, "paquete de 400 g"),
    ("Alimento para perros 1 kg", "Porción de alimento seco para mascotas.", "mascotas", "mascotas", 2500, "bolsa de 1 kg"),
    ("Agua purificada 6 L", "Bidón de agua para el consumo diario.", "bebidas", "agua", 2000, "bidón de 6 L"),
    ("Helado individual", "Un antojo para disfrutar durante el día.", "abarrotes", "helado", 800, "unidad"),
    ("Chocolate 100 g", "Tableta de chocolate en presentación individual.", "abarrotes", "chocolate", 1500, "tableta de 100 g"),
    ("Bebida cola 1,5 L", "Bebida sin alcohol en botella familiar.", "bebidas", "bebida", 1800, "botella de 1,5 L"),
    ("Huevos · pack de 6", "Media docena de huevos para tu cocina.", "abarrotes", "huevos", 2200, "pack de 6"),
]
FOTOS = {producto[3]: f"inicio/static/inicio/img/productos/{producto[3]}.png" for producto in PRODUCTOS}


class Command(BaseCommand):
    help = "Agrega 10 ofertas y el usuario root si todavía no existen; conserva los cambios realizados."

    def handle(self, *args, **options):
        nuevos = 0
        for nombre, descripcion, categoria, foto, precio, unidad in PRODUCTOS:
            if Producto.objects.filter(nombre=nombre).exists():
                continue
            producto = Producto(nombre=nombre, descripcion=descripcion, categoria=categoria, precio=precio, unidad=unidad)
            source = Path(settings.BASE_DIR) / FOTOS[foto]
            try:
                with transaction.atomic():
                    with source.open("rb") as image:
                        producto.imagen.save(source.name, File(image), save=False)
                    producto.save()
            except Exception:
                if producto.imagen.name:
                    producto.imagen.delete(save=False)
                raise
            nuevos += 1
        user_model = get_user_model()
        if not user_model.objects.filter(username="root").exists():
            user_model.objects.create_superuser(username="root", email="", password="rootroot")
            self.stdout.write("Superusuario de evaluación creado: root.")
        self.stdout.write(self.style.SUCCESS(
            f"Catálogo listo: {Producto.objects.count()} registros, {nuevos} nuevos."
        ))
