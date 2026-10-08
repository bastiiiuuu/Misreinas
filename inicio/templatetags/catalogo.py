from django import template

register = template.Library()


@register.filter
def pesos(value):
    """Pesos chilenos enteros, con el mismo formato que el carrito."""
    return f"${value:,}".replace(",", ".") if value is not None else ""
