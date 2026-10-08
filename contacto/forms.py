import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import MensajeContacto


class ContactoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sucursal"].empty_label = "Selecciona un local"

    class Meta:
        model = MensajeContacto
        fields = ("nombre", "contacto", "sucursal", "mensaje")
        labels = {
            "nombre": "Nombre completo",
            "contacto": "Teléfono / WhatsApp o correo",
            "sucursal": "Sucursal de interés",
            "mensaje": "Mensaje",
        }
        widgets = {
            "nombre": forms.TextInput(attrs={"autocomplete": "name", "minlength": 3}),
            "contacto": forms.TextInput(attrs={"placeholder": "+56 9 1234 5678 o tucorreo@ejemplo.com"}),
            "mensaje": forms.Textarea(attrs={"rows": 5, "minlength": 10}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("Ingresa un nombre de al menos 3 caracteres.")
        return nombre

    def clean_contacto(self):
        contacto = self.cleaned_data["contacto"].strip()
        try:
            validate_email(contacto)
        except ValidationError:
            telefono = re.sub(r"[\s()-]", "", contacto)
            if not re.fullmatch(r"(?:\+?56)?9?\d{8}", telefono):
                raise forms.ValidationError("Ingresa un teléfono chileno o un correo válido.")
        return contacto

    def clean_mensaje(self):
        mensaje = self.cleaned_data["mensaje"].strip()
        if len(mensaje) < 10:
            raise forms.ValidationError("Escribe un mensaje de al menos 10 caracteres.")
        return mensaje
