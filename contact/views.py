"""El contacto es una demostración de validación del servidor. Una confirmación no implica que se haya enviado un correo o guardado una consulta."""
from django.shortcuts import render
from .forms import ContactoForm

def contacto(request):

    validado = False

    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            validado = True
            form = ContactoForm()
    else:
        form = ContactoForm()

    return render(request, "contact/contacto.html", {"form": form, "validado": validado})
