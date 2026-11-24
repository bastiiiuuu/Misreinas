"""El servidor valida los datos aunque JavaScript esté desactivado. La sucursal debe existir en la base y el teléfono opcional se normaliza al formato chileno admitido por el ejercicio."""
import re
from django import forms
from sucursales.models import Sucursal

class ContactoForm(forms.Form):

    nombre = forms.CharField(
        label="Nombre completo",
        min_length=3, max_length=80,
        widget=forms.TextInput(attrs={"autocomplete": "name"}),
    )
    email = forms.EmailField(
        label="Correo electrónico", max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "tucorreo@ejemplo.com"}),
    )
    telefono = forms.CharField(
        label="Teléfono / WhatsApp (opcional)", required=False, max_length=25,
        widget=forms.TextInput(attrs={"autocomplete": "tel", "placeholder": "+56 9 1234 5678"}),
    )

    sucursal = forms.ModelChoiceField(
        queryset=Sucursal.objects.none(), label="Sucursal de interés", empty_label="Selecciona un local",
    )
    asunto = forms.ChoiceField(
        label="Asunto", choices=(("", "Selecciona un asunto"), ("productos", "Productos y ofertas"), ("horarios", "Horarios y atención"), ("otro", "Otra consulta")),
    )
    mensaje = forms.CharField(
        label="Mensaje", min_length=10, max_length=2000,
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Escribe tu consulta"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sucursal"].queryset = Sucursal.objects.order_by("nombre", "pk")

    def clean_nombre(self):

        nombre = " ".join(self.cleaned_data["nombre"].split())

        if len(nombre) < 3 or not all(caracter.isalpha() or caracter in " '-" for caracter in nombre):
            raise forms.ValidationError("Escribe un nombre de al menos tres caracteres, usando letras, espacios, apóstrofes o guiones.")
        return nombre

    def clean_telefono(self):
        telefono = re.sub(r"[\s()-]", "", self.cleaned_data["telefono"])
        if not telefono:
            return ""

        if not re.fullmatch(r"(?:\+?56)?9[0-9]{8}", telefono):
            raise forms.ValidationError("Ingresa un celular chileno válido, por ejemplo +56 9 1234 5678.")
        return "+56" + telefono[-9:]
