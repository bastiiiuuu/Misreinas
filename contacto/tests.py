from django.test import Client, TestCase
from django.urls import reverse
from .models import MensajeContacto


class ContactoTests(TestCase):
    datos = {
        "nombre": "Cliente de prueba",
        "contacto": "cliente@example.com",
        "sucursal": "delfines",
        "mensaje": "Quisiera consultar por los horarios del local.",
    }

    def test_mensaje_valido_se_guarda_y_actualizar_no_duplica(self):
        response = self.client.post(reverse("contacto:contacto"), self.datos, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tu mensaje quedó registrado")
        self.assertEqual(MensajeContacto.objects.count(), 1)
        mensaje = MensajeContacto.objects.get()
        self.assertEqual(mensaje.mensaje, self.datos["mensaje"])
        self.client.get(reverse("contacto:contacto"))
        self.assertEqual(MensajeContacto.objects.count(), 1)

    def test_telefono_chileno_tambien_es_valido(self):
        response = self.client.post(reverse("contacto:contacto"), {**self.datos, "contacto": "+56 9 1234 5678"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MensajeContacto.objects.count(), 1)

    def test_datos_invalidos_no_se_guardan_y_conservan_entrada(self):
        response = self.client.post(reverse("contacto:contacto"), {
            **self.datos, "contacto": "invalido", "sucursal": "inexistente", "mensaje": "corto",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MensajeContacto.objects.count(), 0)
        self.assertIn("contacto", response.context["form"].errors)
        self.assertIn("sucursal", response.context["form"].errors)
        self.assertIn("mensaje", response.context["form"].errors)
        self.assertContains(response, self.datos["nombre"])

    def test_csrf_es_obligatorio_para_guardar(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("contacto:contacto"), self.datos)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(MensajeContacto.objects.count(), 0)
        client.get(reverse("contacto:contacto"))
        token = client.cookies["csrftoken"].value
        response = client.post(reverse("contacto:contacto"), {**self.datos, "csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MensajeContacto.objects.count(), 1)
