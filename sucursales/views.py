from django.shortcuts import render


def sucursales(request):
    return render(request, "sucursales/sucursales.html")
