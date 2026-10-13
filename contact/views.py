from django.shortcuts import render  # Renderiza la plantilla de Contacto usando el motor de Django.
def contacto(request):  # Recibe la solicitud HTTP de /contacto/; el formulario conserva su demostración frontend.
    return render(request, "contact/contacto.html")  # Sirve la página; esta evaluación no implementa envío ni almacenamiento de mensajes.
