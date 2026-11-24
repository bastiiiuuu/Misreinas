

from django.shortcuts import render

def inicio(request):
    return render(request, "core/index.html")

def pagina_no_encontrada(request, exception=None):
    response = render(request, "core/404.html", status=404)
    response.es_404_misreinas = True
    return response
