

from django.shortcuts import render
from .models import Sucursal

def listado_sucursales(request):
    sucursales = Sucursal.objects.all().order_by("-created", "-pk")
    contexto = {"sucursales": sucursales}
    return render(request, "sucursales/sucursales.html", contexto)
