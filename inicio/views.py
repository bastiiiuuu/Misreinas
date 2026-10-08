from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Producto


def inicio(request):
    # El orden por ID evita que los registros cambien de página sin motivo.
    productos = Producto.objects.all().order_by("pk")
    paginator = Paginator(productos, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Los IDs y cantidades se conservan en el navegador. Los nombres y precios
    # se vuelven a leer de Django al cambiar de página, incluso si se editaron.
    catalogo_carrito = list(productos.filter(precio__gt=0).values("id", "nombre", "precio", "unidad"))
    return render(request, "inicio/inicio.html", {
        "page_obj": page_obj,
        "catalogo_carrito": catalogo_carrito,
    })
