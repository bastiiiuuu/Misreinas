from django.shortcuts import render  # Permite transformar la plantilla de Nosotros en una respuesta HTTP.
def nosotros(request):  # Recibe la petición HTTP que el resolvedor de rutas entrega a esta función.
    return render(request, "about/nosotros.html")  # Usa el namespace about para localizar el template correcto.
