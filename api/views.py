"""Contrato público de consulta del catálogo.

La API expone datos comerciales ya visibles en la web. Las escrituras continúan en
Django Admin, con autenticación y CSRF, para evitar crear un segundo canal de edición.
Los campos se seleccionan expresamente y los precios viajan como texto decimal.
"""
from functools import wraps

from django.core.paginator import EmptyPage, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from categorias.models import Categoria
from ofertas.models import Oferta
from sucursales.models import Sucursal


def json_get(view):
    """Mantiene también los errores de método en JSON, sin habilitar escrituras."""
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        if request.method not in {"GET", "HEAD"}:
            response = JsonResponse({"error": "Solo se permiten GET y HEAD."}, status=405)
            response["Allow"] = "GET, HEAD"
            return response
        return view(request, *args, **kwargs)
    return wrapped


def integer_parameter(request, name, default, maximum):
    value = request.GET.get(name, str(default))
    if not value.isascii() or not value.isdecimal() or len(value) > 18:
        raise ValueError(f"{name} debe ser un entero positivo.")
    number = int(value)
    if not 1 <= number <= maximum:
        raise ValueError(f"{name} debe estar entre 1 y {maximum}.")
    return number


def serialize_offer(item):
    """Devuelve un contrato estable sin exponer campos internos del modelo.

    El precio puede ser null cuando no existe un importe publicado. No se convierte
    a float porque el cliente no debe recibir una aproximación de un valor monetario.
    Las imágenes usan rutas del mismo sitio y pueden ser null en datos de prueba.
    """
    return {
        "id": item.pk, "nombre": item.nombre, "descripcion": item.descripcion,
        "precio_clp": str(item.precio) if item.precio is not None else None,
        "imagen": item.imagen.url if item.imagen else None,
        "sucursal": {"id": item.sucursal_id, "nombre": item.sucursal.nombre},
        "categorias": [{"id": category.pk, "nombre": category.nombre, "slug": category.slug} for category in item.categorias.all()],
    }


@json_get
def index(request):
    return JsonResponse({"version": "1", "documentation": reverse("api-demo"), "endpoints": {
        "ofertas": reverse("api-ofertas"), "categorias": reverse("api-categorias"), "sucursales": reverse("api-sucursales")}})


@json_get
def ofertas(request):
    """Filtra antes de paginar y conserva los parámetros en los enlaces siguientes.

    select_related y prefetch_related evitan una consulta adicional por sucursal o
    categoría al serializar cada tarjeta. Los límites impiden descargar todo el
    catálogo con una sola petición accidental.
    """
    items = Oferta.objects.select_related("sucursal").prefetch_related("categorias").order_by("-created", "-pk")
    try:
        page_number = integer_parameter(request, "page", 1, 10**9)
        page_size = integer_parameter(request, "page_size", 10, 100)
        query = request.GET.get("q", "").strip()
        if len(query) > 120:
            raise ValueError("q no puede superar 120 caracteres.")
        if query:
            items = items.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
        category = request.GET.get("categoria")
        if category is not None:
            if len(category) > 90 or not Categoria.objects.filter(slug=category).exists():
                return JsonResponse({"error": "Categoría inexistente."}, status=404)
            items = items.filter(categorias__slug=category)
        if "sucursal" in request.GET:
            branch_id = integer_parameter(request, "sucursal", 1, 10**18-1)
            if not Sucursal.objects.filter(pk=branch_id).exists():
                return JsonResponse({"error": "Sucursal inexistente."}, status=404)
            items = items.filter(sucursal_id=branch_id)
    except ValueError as error:
        return JsonResponse({"error": str(error)}, status=400)
    paginator = Paginator(items, page_size)
    try:
        page = paginator.page(page_number)
    except EmptyPage:
        return JsonResponse({"error": "Página inexistente."}, status=404)

    def page_link(number):
        params = request.GET.copy()
        params["page"] = str(number)
        return reverse("api-ofertas") + "?" + params.urlencode()

    return JsonResponse({"count": paginator.count, "page": page.number, "pages": paginator.num_pages,
        "next": page_link(page.next_page_number()) if page.has_next() else None,
        "previous": page_link(page.previous_page_number()) if page.has_previous() else None,
        "results": [serialize_offer(item) for item in page]})


@json_get
def oferta(request, pk):
    item = Oferta.objects.select_related("sucursal").prefetch_related("categorias").filter(pk=pk).first()
    if item is None:
        return JsonResponse({"error": "Oferta inexistente."}, status=404)
    return JsonResponse(serialize_offer(item))


@json_get
def categorias(request):
    return JsonResponse({"results": list(Categoria.objects.order_by("nombre", "pk").values("id", "nombre", "slug", "descripcion"))})


@json_get
def sucursales(request):
    return JsonResponse({"results": list(Sucursal.objects.order_by("nombre", "pk").values("id", "nombre", "direccion", "descripcion"))})
