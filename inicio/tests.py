"""Pruebas de datos, paginación y edición real desde el administrador."""
from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import csv
from unittest.mock import patch
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse
from .models import Producto


def imagen_de_prueba():
    buffer = BytesIO()
    Image.new("RGB", (24, 24), "navy").save(buffer, format="PNG")
    return SimpleUploadedFile("producto.png", buffer.getvalue(), content_type="image/png")


class ConImagenesTemporales(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.media.cleanup)
        self.addCleanup(self.settings_override.disable)


class CatalogoTests(ConImagenesTemporales):
    def setUp(self):
        super().setUp()
        for index in range(1, 11):
            Producto.objects.create(
                nombre=f"Oferta {index:02}", descripcion=f"Descripción de prueba {index}",
                categoria="abarrotes", imagen=imagen_de_prueba(),
            )

    def test_diez_registros_en_dos_paginas_sin_repeticiones(self):
        primera = self.client.get(reverse("inicio:inicio"))
        segunda = self.client.get(reverse("inicio:inicio"), {"page": 2})
        ids_primera = [p.pk for p in primera.context["page_obj"]]
        ids_segunda = [p.pk for p in segunda.context["page_obj"]]
        self.assertEqual(len(ids_primera), 5)
        self.assertEqual(len(ids_segunda), 5)
        self.assertFalse(set(ids_primera) & set(ids_segunda))
        self.assertEqual(set(ids_primera + ids_segunda), set(Producto.objects.values_list("pk", flat=True)))
        self.assertContains(primera, "Página 1 de 2")
        self.assertContains(primera, 'href="?page=2#catalogo" rel="next"')
        self.assertNotContains(primera, 'rel="prev"')
        self.assertContains(segunda, 'href="?page=1#catalogo" rel="prev"')
        self.assertNotContains(segunda, 'rel="next"')

    def test_paginas_invalidas_y_catalogo_vacio(self):
        for valor, esperada in [("abc", 1), ("999", 2), ("-1", 2)]:
            with self.subTest(valor=valor):
                response = self.client.get(reverse("inicio:inicio"), {"page": valor})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context["page_obj"].number, esperada)
        Producto.objects.all().delete()
        response = self.client.get(reverse("inicio:inicio"))
        self.assertContains(response, "Pronto encontrarás")
        self.assertContains(response, "Página 1 de 1")

    def test_once_registros_generan_tercera_pagina(self):
        producto = Producto.objects.create(nombre="Oferta nueva", descripcion="Nueva oferta del negocio.", categoria="bebidas", imagen=imagen_de_prueba())
        response = self.client.get(reverse("inicio:inicio"), {"page": 3})
        self.assertEqual(list(response.context["page_obj"]), [producto])
        self.assertContains(response, "Página 3 de 3")

    def test_cuatro_secciones_y_herencia_de_plantilla(self):
        for app in ("inicio", "nosotros", "sucursales", "contacto"):
            with self.subTest(app=app):
                response = self.client.get(reverse(f"{app}:{app}"))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f"{app}/{app}.html")
                self.assertTemplateUsed(response, "inicio/base.html")
                self.assertContains(response, 'class="active" aria-current="page"', count=1)
                self.assertNotContains(response, 'href="index.html"')
                self.assertNotContains(response, "https://i.postimg.cc/")

    def test_texto_del_catalogo_se_escapa_y_la_imagen_existe(self):
        producto = Producto.objects.first()
        producto.nombre = '<script>alert("x")</script>'
        producto.save()
        response = self.client.get(reverse("inicio:inicio"))
        self.assertNotContains(response, producto.nombre)
        self.assertContains(response, "&lt;script&gt;")
        self.assertContains(response, producto.imagen.url)
        self.assertTrue(Path(producto.imagen.path).is_file())


class AdministracionTests(ConImagenesTemporales):
    def setUp(self):
        super().setUp()
        self.root = get_user_model().objects.create_superuser("root", "", "rootroot")

    def test_login_y_crud_persisten_en_el_frontend(self):
        self.assertTrue(self.client.login(username="root", password="rootroot"))
        response = self.client.post(reverse("admin:inicio_producto_add"), {
            "nombre": "Producto administrado", "descripcion": "Descripción original desde el panel.",
            "categoria": "abarrotes", "imagen": imagen_de_prueba(), "_save": "Guardar",
            "precio": 1200, "unidad": "unidad",
        })
        self.assertEqual(response.status_code, 302)
        producto = Producto.objects.get(nombre="Producto administrado")
        creacion = producto.created
        self.assertIsNotNone(creacion)
        self.assertIsNotNone(producto.updated)
        self.assertTrue(Path(producto.imagen.path).is_file())
        response = self.client.post(reverse("admin:inicio_producto_change", args=[producto.pk]), {
            "nombre": producto.nombre, "descripcion": "Texto editado que debe verse en Inicio.",
            "categoria": "bebidas", "_save": "Guardar",
            "precio": 1800, "unidad": "botella de 1 L",
        })
        self.assertEqual(response.status_code, 302)
        producto.refresh_from_db()
        self.assertEqual(producto.created, creacion)
        self.assertEqual(producto.categoria, "bebidas")
        self.assertEqual(producto.precio, 1800)
        self.assertEqual(producto.unidad, "botella de 1 L")
        self.assertGreater(producto.updated, producto.created)
        # Una nueva petición vuelve a consultar la base, sin depender del formulario.
        self.assertContains(self.client.get(reverse("inicio:inicio")), producto.descripcion)
        response = self.client.post(reverse("admin:inicio_producto_delete", args=[producto.pk]), {"post": "yes"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Producto.objects.filter(pk=producto.pk).exists())
        self.assertNotContains(self.client.get(reverse("inicio:inicio")), producto.nombre)

    def test_imagen_invalida_no_crea_producto(self):
        self.client.force_login(self.root)
        response = self.client.post(reverse("admin:inicio_producto_add"), {
            "nombre": "Archivo inválido", "descripcion": "Esto no es una imagen.", "categoria": "servicios",
            "imagen": SimpleUploadedFile("falsa.jpg", b"no es una foto", content_type="image/jpeg"),
            "precio": 1000, "unidad": "unidad",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Producto.objects.exists())
        self.assertIn("imagen", response.context["adminform"].form.errors)

    def test_precio_cero_y_negativo_no_se_guardan(self):
        self.client.force_login(self.root)
        for precio in (0, -1):
            response = self.client.post(reverse("admin:inicio_producto_add"), {
                "nombre": "Precio inválido", "descripcion": "Producto de demostración.",
                "categoria": "abarrotes", "imagen": imagen_de_prueba(),
                "precio": precio, "unidad": "unidad", "_save": "Guardar",
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn("precio", response.context["adminform"].form.errors)
        self.assertFalse(Producto.objects.exists())


class CarritoCatalogoTests(ConImagenesTemporales):
    def test_catalogo_json_incluye_otra_pagina_y_excluye_sin_precio(self):
        for i in range(6):
            Producto.objects.create(nombre=f"Producto {i}", descripcion="Ejemplo", categoria="abarrotes", imagen=imagen_de_prueba(), precio=1000 + i, unidad="paquete")
        Producto.objects.create(nombre="Sin precio", descripcion="Consultar", categoria="servicios", imagen=imagen_de_prueba())
        response = self.client.get(reverse("inicio:inicio"))
        self.assertEqual(len(response.context["page_obj"]), 5)
        self.assertEqual(len(response.context["catalogo_carrito"]), 6)
        self.assertEqual(response.context["catalogo_carrito"][-1]["precio"], 1005)
        self.assertNotIn("Sin precio", [p["nombre"] for p in response.context["catalogo_carrito"]])
        self.assertContains(response, "Modo demostración")
        self.assertContains(response, 'id="catalogo-carrito" type="application/json"')

    def test_nombre_malicioso_no_cierra_el_json_y_precio_admin_se_refleja(self):
        producto = Producto.objects.create(nombre='</script><script>alert(1)</script>', descripcion="Ejemplo", categoria="abarrotes", imagen=imagen_de_prueba(), precio=1200)
        response = self.client.get(reverse("inicio:inicio"))
        self.assertNotContains(response, producto.nombre)
        self.assertContains(response, '\\u003C/script\\u003E')
        producto.precio = 1800
        producto.save()
        response = self.client.get(reverse("inicio:inicio"))
        self.assertEqual(response.context["catalogo_carrito"][0]["precio"], 1800)


class PrepararDemoTests(ConImagenesTemporales):
    def test_carga_idempotente_y_conserva_ediciones(self):
        output = StringIO()
        call_command("preparar_demo", stdout=output)
        self.assertEqual(Producto.objects.count(), 10)
        root = get_user_model().objects.get(username="root")
        self.assertTrue(root.is_superuser)
        self.assertTrue(root.check_password("rootroot"))
        producto = Producto.objects.first()
        producto.descripcion = "Modificado desde el administrador."
        producto.save()
        call_command("preparar_demo", stdout=output)
        self.assertEqual(Producto.objects.count(), 10)
        producto.refresh_from_db()
        self.assertEqual(producto.descripcion, "Modificado desde el administrador.")
        for producto in Producto.objects.all():
            self.assertTrue(Path(producto.imagen.path).is_file())


class ImportarCatalogoTests(ConImagenesTemporales):
    def csv_de_prueba(self):
        path = Path(self.media.name) / "catalogo.csv"
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "nombre", "precio_clp", "imagen"])
            writer.writeheader()
            writer.writerows([
                {"id": "001", "nombre": "Bebida uno", "precio_clp": 1200, "imagen": "https://i5.walmartimages.cl/uno.jpg"},
                {"id": "002", "nombre": "Bebida dos", "precio_clp": 1500, "imagen": "https://i5.walmartimages.cl/dos.jpg"},
            ])
        return path

    @patch("inicio.management.commands.importar_catalogo.time.sleep")
    @patch("inicio.management.commands.importar_catalogo.descargar_imagen")
    def test_importacion_carrito_e_idempotencia_con_edicion(self, download, sleep):
        download.return_value = (imagen_de_prueba().read(), "png")
        path = self.csv_de_prueba()
        call_command("importar_catalogo", csv=path, stdout=StringIO())
        self.assertEqual(Producto.objects.count(), 2)
        product = Producto.objects.get(nombre="Bebida uno")
        self.assertTrue(Path(product.imagen.path).is_file())
        self.assertEqual(product.descripcion, "")
        product.nombre = "Nombre editado en administrador"
        product.precio = 2000
        product.save()
        call_command("importar_catalogo", csv=path, stdout=StringIO())
        self.assertEqual(download.call_count, 2)
        self.assertEqual(Producto.objects.count(), 2)
        product.refresh_from_db()
        self.assertEqual(product.precio, 2000)
        response = self.client.get(reverse("inicio:inicio"))
        self.assertContains(response, product.nombre)
        self.assertIn(product.pk, [p["id"] for p in response.context["catalogo_carrito"]])

    @patch("inicio.management.commands.importar_catalogo.time.sleep")
    @patch("inicio.management.commands.importar_catalogo.descargar_imagen")
    def test_imagen_fallida_no_importa_datos_parciales(self, download, sleep):
        download.side_effect = [(imagen_de_prueba().read(), "png"), CommandError("HTTP 403")]
        with self.assertRaises(CommandError):
            call_command("importar_catalogo", csv=self.csv_de_prueba(), stdout=StringIO())
        self.assertFalse(Producto.objects.exists())
