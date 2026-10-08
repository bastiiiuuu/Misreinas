from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import ContactoForm


def contacto(request):
    form = ContactoForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tu mensaje quedó registrado. Gracias por escribirnos.")
        return redirect("contacto:contacto")
    return render(request, "contacto/contacto.html", {"form": form})
