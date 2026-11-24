"""Los datos compartidos de las sucursales permiten que las páginas mantengan referencias comunes. Las consultas deben evaluarse durante la petición y no al importar el módulo."""
from .models import Sucursal

def informacion_locales(request):
    locales = list(Sucursal.objects.order_by("nombre", "pk"))
    return {"locales_del_negocio": locales, "total_locales": len(locales)}
