from django.shortcuts import render  # Combina una plantilla con su contexto y devuelve un HttpResponse.
from .models import Sucursal  # Importa el modelo que representa las filas consultadas mediante el ORM.

def listado_sucursales(request):  # request es el HttpRequest con el método, la URL y los parámetros enviados por el navegador.
    sucursales = Sucursal.objects.all().order_by("-created", "-pk")  # Consulta los tres locales reales; el listado paginado de diez registros ahora corresponde a Oferta en core/views.py.
    contexto = {"sucursales": sucursales}  # Entrega las instancias de los locales al bucle del template bajo el nombre sucursales.
    return render(request, "sucursales/sucursales.html", contexto)  # Renderiza el template de esta app y devuelve su HTML al navegador.
