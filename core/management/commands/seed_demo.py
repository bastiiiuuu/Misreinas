"""Añade ejemplos identificados sin reemplazar los registros existentes."""
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from categorias.models import Categoria
from ofertas.models import Oferta
from sucursales.models import Sucursal


class Command(BaseCommand):
    help = "Crea un catálogo sintético e idempotente, sin usuarios ni credenciales."

    @transaction.atomic
    def handle(self, *args, **options):
        category, _ = Categoria.objects.get_or_create(slug="demostracion", defaults={"nombre":"Demostración", "descripcion":"Datos ficticios para explorar el proyecto."})
        branch, _ = Sucursal.objects.get_or_create(nombre="DEMO · Local de ejemplo", defaults={"direccion":"Dirección ficticia, Chile", "descripcion":"Este local solo existe para demostrar el sistema."})
        image = Image.new("RGB", (640, 420), "#211b31")
        drawing = ImageDraw.Draw(image)
        drawing.rounded_rectangle((60, 60, 580, 360), radius=30, outline="#a78bfa", width=4)
        drawing.text((110, 185), "PRODUCTO DE DEMOSTRACION", fill="white", font_size=24)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        for number in range(1, 8):
            offer, created = Oferta.objects.get_or_create(nombre=f"DEMO · Producto {number}", sucursal=branch, defaults={"descripcion":"Producto ficticio para probar filtros, paginación y API.","precio":number*1000})
            if created:
                offer.imagen.save(f"demo-{number}.png", ContentFile(buffer.getvalue()))
                offer.categorias.add(category)
        self.stdout.write(self.style.SUCCESS("Catálogo DEMO preparado. No se han creado usuarios ni cambiado registros existentes."))
