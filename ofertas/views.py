"""Los filtros se aplican antes de paginar y se conservan al navegar. Los identificadores inexistentes devuelven 404 en vez de mostrar silenciosamente todo el catálogo."""
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from categorias.models import Categoria
from sucursales.models import Sucursal
from .models import Oferta

def listado(request):

    ofertas = Oferta.objects.select_related("sucursal").prefetch_related("categorias").order_by("-created", "-pk")

    categoria_slug = request.GET.get("categoria")
    sucursal_id = request.GET.get("sucursal")
    categoria_actual = None
    sucursal_actual = None

    if categoria_slug is not None:
        categoria_actual = get_object_or_404(Categoria, slug=categoria_slug)
        ofertas = ofertas.filter(categorias=categoria_actual)

    if sucursal_id is not None:

        if not sucursal_id.isascii() or not sucursal_id.isdecimal() or len(sucursal_id) > 18:
            raise Http404("La sucursal indicada no existe.")
        sucursal_actual = get_object_or_404(Sucursal, pk=int(sucursal_id))
        ofertas = ofertas.filter(sucursal=sucursal_actual)

    paginator = Paginator(ofertas, 5)

    page_obj = paginator.get_page(request.GET.get("page"))

    parametros = request.GET.copy()

    parametros.pop("page", None)
    filtro_query = parametros.urlencode()

    contexto = {
        "page_obj": page_obj,
        "categorias": Categoria.objects.all(),
        "sucursales_filtro": Sucursal.objects.all(),
        "categoria_actual": categoria_actual,
        "sucursal_actual": sucursal_actual,
        "filtro_query": filtro_query,
    }

    return render(request, "ofertas/ofertas.html", contexto)
