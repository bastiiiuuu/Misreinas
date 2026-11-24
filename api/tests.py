"""Prueba el contrato HTTP usando una base independiente y datos de ejemplo."""
from django.test import Client, TestCase
from django.urls import reverse
from categorias.models import Categoria
from ofertas.models import Oferta
from sucursales.models import Sucursal


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.branch = Sucursal.objects.create(nombre="Local de prueba", direccion="Dirección de prueba", descripcion="Ejemplo")
        cls.category = Categoria.objects.create(nombre="Categoría de prueba", slug="categoria-prueba")
        for number in range(7):
            offer = Oferta.objects.create(nombre=f"Producto {number}", descripcion="Descripción de prueba", precio=1000+number, sucursal=cls.branch)
            offer.categorias.add(cls.category)

    def test_existing_html_pages_and_filters(self):
        for route in ["inicio", "nosotros", "contacto", "sucursales", "ofertas", "api-demo"]:
            self.assertEqual(self.client.get(reverse(route)).status_code, 200, route)
        response = self.client.get(reverse("ofertas"), {"categoria": self.category.slug})
        self.assertEqual(response.context["page_obj"].paginator.count, 7)

    def test_pagination_preserves_filters_and_prices_are_decimal_strings(self):
        response = self.client.get(reverse("api-ofertas"), {"categoria":self.category.slug, "page_size":2})
        data = response.json()
        self.assertEqual(data["count"], 7)
        self.assertEqual(len(data["results"]), 2)
        self.assertIsInstance(data["results"][0]["precio_clp"], str)
        self.assertIn("categoria=categoria-prueba", data["next"])
        self.assertEqual(self.client.get(data["next"]).json()["page"], 2)

    def test_invalid_parameters_are_bounded_and_return_json(self):
        for params in [{"page":"-1"},{"page_size":"101"},{"q":"a"*121},{"sucursal":"1 OR 1=1"}]:
            response = self.client.get(reverse("api-ofertas"), params)
            self.assertEqual(response.status_code, 400)
            self.assertIn("error", response.json())

    def test_missing_records_and_pages_return_404_json(self):
        for url in [reverse("api-oferta", args=[99999]), reverse("api-ofertas")+"?categoria=no-existe", reverse("api-ofertas")+"?page=999"]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)
            self.assertIn("error", response.json())

    def test_api_is_read_only(self):
        count = Oferta.objects.count()
        response = self.client.post(reverse("api-ofertas"), {"nombre":"No crear"})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Oferta.objects.count(), count)

    def test_no_price_is_null_and_output_excludes_internal_fields(self):
        item = Oferta.objects.first()
        item.precio = None
        item.save()
        data = self.client.get(reverse("api-oferta", args=[item.pk])).json()
        self.assertIsNone(data["precio_clp"])
        self.assertEqual(set(data), {"id","nombre","descripcion","precio_clp","imagen","sucursal","categorias"})

    def test_queries_do_not_grow_with_each_offer(self):
        with self.assertNumQueries(3):
            self.client.get(reverse("api-ofertas"))

    def test_contact_validates_server_side_and_csrf(self):
        response = self.client.post(reverse("contacto"), {"nombre":"x","email":"incorrecto"})
        self.assertFalse(response.context["validado"])
        self.assertTrue(response.context["form"].errors)
        guarded = Client(enforce_csrf_checks=True)
        self.assertEqual(guarded.post(reverse("contacto"), {}).status_code, 403)

    def test_valid_contact_is_explicitly_a_validation_demo(self):
        response = self.client.post(reverse("contacto"), {"nombre":"Persona Ejemplo","email":"persona@example.com","telefono":"","sucursal":self.branch.pk,"asunto":"otro","mensaje":"Consulta de demostración"})
        self.assertTrue(response.context["validado"])
        self.assertContains(response, "no envía mensajes")

    def test_html_escapes_offer_names(self):
        item = Oferta.objects.first()
        item.nombre = '<script>alert(1)</script>'
        item.save()
        response = self.client.get(reverse("ofertas"))
        self.assertNotContains(response, '<script>alert(1)</script>', html=False)
        self.assertContains(response, '&lt;script&gt;')
