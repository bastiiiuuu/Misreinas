"""Importa el CSV de referencia de Líder y guarda sus imágenes localmente."""
import csv
import time
from io import BytesIO
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from PIL import Image, UnidentifiedImageError
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from inicio.models import Producto


def descargar_imagen(url):
    parsed = urlsplit(url)
    host = parsed.hostname or ""
    if parsed.scheme != "https" or not host.endswith(".walmartimages.cl"):
        raise CommandError("La imagen debe provenir del CDN público walmartimages.cl por HTTPS.")
    try:
        request = Request(url, headers={"User-Agent": "CatalogoEducativo/1.0"})
        with urlopen(request, timeout=30) as response:
            if urlsplit(response.url).hostname != host:
                raise CommandError("La imagen redirigió fuera de su servidor de origen.")
            data = response.read(8 * 1024 * 1024 + 1)
        if len(data) > 8 * 1024 * 1024:
            raise CommandError("La imagen supera el límite de 8 MB.")
        with Image.open(BytesIO(data)) as image:
            extension = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}.get(image.format)
            image.verify()
        if not extension:
            raise CommandError("Formato de imagen no admitido.")
        return data, extension
    except (HTTPError, URLError, TimeoutError, UnidentifiedImageError, OSError) as exc:
        raise CommandError(f"No se pudo descargar/validar la imagen. Importación detenida: {exc}") from exc


class Command(BaseCommand):
    help = "Agrega productos de referencia desde CSV sin sobrescribir productos existentes."

    def add_arguments(self, parser):
        parser.add_argument("--csv", type=Path, default=Path(settings.BASE_DIR) / "inicio/data/catalogo_lider.csv")
        parser.add_argument("--pausa", type=float, default=1.0)

    def handle(self, *args, **options):
        if options["pausa"] < 1:
            raise CommandError("Usa una pausa de al menos un segundo entre imágenes.")
        try:
            with options["csv"].open(encoding="utf-8-sig", newline="") as file:
                reader = csv.DictReader(file)
                required = {"id", "nombre", "precio_clp", "imagen"}
                if not required.issubset(reader.fieldnames or []):
                    raise CommandError("El CSV necesita id, nombre, precio_clp e imagen.")
                rows = list(reader)
        except OSError as exc:
            raise CommandError(str(exc)) from exc
        pending, names, identifiers = [], set(), set()
        existing = 0
        for row in rows:
            identifier, name = row["id"].strip(), row["nombre"].strip()
            if not identifier.isdigit() or not name or len(name) > 100:
                raise CommandError("ID o nombre inválido en el CSV.")
            if identifier in identifiers or name in names:
                raise CommandError(f"ID o nombre repetido en el CSV: {name}.")
            identifiers.add(identifier)
            names.add(name)
            try:
                price = int(row["precio_clp"])
                if price < 1:
                    raise ValueError()
            except ValueError as exc:
                raise CommandError(f"Precio inválido: {name}.") from exc
            if (Producto.objects.filter(nombre=name).exists()
                    or Producto.objects.filter(imagen__startswith=f"productos/lider-{identifier}.").exists()):
                existing += 1
                continue
            pending.append((row, identifier, name, price))

        # Validar todas las imágenes antes de modificar la base de datos.
        prepared = []
        for index, (row, identifier, name, price) in enumerate(pending):
            if index:
                time.sleep(options["pausa"])
            self.stdout.write(f"Imagen {index + 1}/{len(pending)}: {name}")
            data, extension = descargar_imagen(row["imagen"])
            prepared.append((row, identifier, name, price, data, extension))
        saved = []
        try:
            with transaction.atomic():
                for row, identifier, name, price, data, extension in prepared:
                    product = Producto(nombre=name, descripcion="", categoria="bebidas",
                                       precio=price, unidad=row.get("unidad_precio") or "unidad")
                    product.imagen.save(f"lider-{identifier}.{extension}", ContentFile(data), save=False)
                    saved.append(product.imagen.name)
                    product.full_clean()
                    product.save()
        except Exception:
            # Solo archivos creados por esta operación y registrados por Storage.
            storage = Producto._meta.get_field("imagen").storage
            for filename in saved:
                storage.delete(filename)
            raise
        self.stdout.write(self.style.SUCCESS(
            f"{len(prepared)} productos agregados, {existing} existentes conservados; total {Producto.objects.count()}."
        ))
