"""La página 404 común solo sustituye respuestas HTML. Los errores JSON de la API se conservan para que el cliente pueda tratarlos sin interpretar una plantilla."""
from .views import pagina_no_encontrada

class Pagina404Middleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        es_html = response.get("Content-Type", "").startswith("text/html")

        ya_personalizada = getattr(response, "es_404_misreinas", False)

        if response.status_code == 404 and es_html and not ya_personalizada:
            return pagina_no_encontrada(request)
        return response
