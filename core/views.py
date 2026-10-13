from django.core.paginator import Paginator  # Importa la clase que divide el QuerySet en objetos Page con un límite de registros.
from django.shortcuts import render  # Combina una plantilla con el contexto y devuelve la respuesta HTTP de Inicio.
from .models import Oferta  # Importa el modelo de las promociones administradas desde el panel de Django.
def inicio(request):  # request es el HttpRequest que contiene la URL y los parámetros GET enviados por el navegador.
    ofertas = Oferta.objects.all().order_by("-created", "-pk")  # Selecciona todas las ofertas con orden definido; el QuerySet es perezoso y aún no carga todas las filas.
    paginator = Paginator(ofertas, 5)  # Fija cinco registros por página; el valor predeterminado orphans=0 impide fusionar la última página con la anterior.
    page_number = request.GET.get("page")  # Obtiene ?page=2 como cadena o None cuando no se envía el parámetro.
    page_obj = paginator.get_page(page_number)  # Devuelve un Page; sin número o con texto inválido usa la primera página, y fuera de rango usa la última.
    contexto = {"page_obj": page_obj}  # La clave page_obj es el nombre que el template utiliza para acceder a las ofertas y los métodos de navegación.
    return render(request, "core/index.html", contexto)  # Ejecuta el template de esta app con los datos de la página seleccionada y devuelve HTML ya renderizado.
