# Guía para explicar Mis Reinas

Esta guía sirve para estudiar el proyecto. Las preguntas reales las decide el profesor.

## Recorrido de una petición

1. El navegador pide una URL, por ejemplo `/?page=2`.
2. `misreinas/urls.py` deriva la ruta al archivo `urls.py` de la app.
3. La vista `inicio()` consulta `Producto` con el ORM y ordena los registros por ID.
4. `Paginator(productos, 5)` divide el QuerySet. `request.GET.get("page")` obtiene el número solicitado y `get_page()` devuelve un objeto `Page`.
5. `render()` entrega ese objeto al template con la clave `page_obj`.
6. El template recorre los cinco objetos de esa página y genera los enlaces de navegación.

## Preguntas técnicas para practicar

**¿Qué diferencia hay entre proyecto y app?**
El proyecto contiene la configuración general y las rutas principales. Cada app resuelve una sección: Inicio, Nosotros, Sucursales o Contacto. Se registran en `INSTALLED_APPS`.

**¿Qué es un modelo?**
Una clase de Python que describe los datos. `Producto` hereda de `models.Model`. Django crea una tabla mediante migraciones. `objects.all()` obtiene un QuerySet; no es una lista HTML.

**¿Qué son las migraciones?**
Archivos que describen la estructura y sus cambios. `makemigrations` genera esos archivos y `migrate` aplica los cambios en la base de datos. No son lo mismo que crear registros.

**¿Para qué sirven created y updated?**
`created` usa `auto_now_add=True`: se registra al crear. `updated` usa `auto_now=True`: se actualiza al guardar. No se editan manualmente en el administrador.

**¿Por qué ordenar antes de paginar?**
Para que la base de datos entregue un orden definido. En este proyecto se usa el ID. Cada página recibe una parte del QuerySet.

**¿Qué ocurre con un parámetro de página incorrecto?**
`get_page()` devuelve la primera página si el valor no es un número. Para un número fuera del rango devuelve la última, sin lanzar una página de error.

**¿Qué debe coincidir entre vista y template?**
La clave del contexto. Aquí se envía `{"page_obj": page_obj}` y el template utiliza `page_obj`. El nombre se puede cambiar si se cambia en ambos sitios.

**¿Qué diferencia hay entre static y media?**
`static` contiene CSS, JavaScript y fotografías fijas del sitio. Se usa `{% load static %}` y `{% static 'app/archivo' %}`. `media` contiene imágenes asociadas a registros del modelo y subidas desde el administrador; su ruta se guarda en `ImageField`.

**¿Cómo se comparte el diseño?**
La plantilla base define menú, estilos y pie. Las páginas usan `{% extends 'inicio/base.html' %}` y completan bloques. Las rutas se generan con `{% url %}`, evitando enlaces a archivos HTML sueltos.

**¿Cómo se ve la persistencia?**
Al guardar un producto en el administrador cambia `db.sqlite3`. La siguiente consulta de Inicio obtiene el dato nuevo. Los cambios siguen existiendo después de reiniciar el servidor. El comando de inicio no repone registros borrados.

**¿Cómo funciona Contacto?**
GET muestra un `ModelForm`. POST valida nombre, teléfono/correo, sucursal y mensaje. Si todo es válido, `form.save()` crea el registro y se redirige para evitar repetirlo al actualizar. Si falla, aparecen los errores junto a los campos. CSRF protege el envío. Los mensajes se consultan en el administrador.

## Demostración sugerida

1. Mostrar las cuatro secciones y su menú.
2. Mostrar los cinco registros de la primera página y los cinco de la segunda.
3. Entrar a `/admin/` con las credenciales de la pauta.
4. Editar un producto y mostrar el cambio en Inicio.
5. Mostrar la página 3, donde comienzan las cervezas importadas, y la última página: hay 54 productos y 11 páginas.
6. Crear un registro desde el administrador, comprobar que aparece y eliminar solo ese registro de prueba.
7. Mostrar el modelo, las migraciones, la vista y el template de paginación.
8. Enviar un mensaje de ejemplo en Contacto y comprobar que aparece en el administrador.

## Ubicación del código principal

- `misreinas/settings.py`: apps, base de datos, idioma, zona horaria, static y media.
- `misreinas/urls.py`: cuatro secciones, administrador y media local.
- `inicio/models.py`: los seis atributos requeridos y los campos precio y unidad del prototipo.
- `inicio/views.py`: consulta, orden, Paginator, GET y contexto.
- `inicio/templates/inicio/inicio.html`: bucle del catálogo y enlaces.
- `inicio/admin.py`: registro del modelo, filtros, búsqueda y fechas de solo lectura.
- `contacto/forms.py`: validación del formulario.
- `contacto/views.py`: guardado y redirección.

## Extra opcional: carrito de demostración

La parte evaluada sigue siendo Django, el modelo administrable, la persistencia y la paginación. El carrito es una mejora visual de JavaScript, adicional a la pauta.

- precio es un entero positivo en pesos chilenos, opcional; unidad identifica la presentación de venta. Se agregan mediante la migración 0002 de inicio.
- La vista envía el catálogo con precio mediante json_script. Django escapa ese JSON y JavaScript usa textContent al mostrar nombres.
- localStorage conserva solo IDs, cantidades y local; no es una tabla de pedidos ni una confirmación de stock. Los nombres y precios se obtienen nuevamente del servidor al recargar.
- El total es la suma de precio por cantidad, con formato CLP. Las cantidades aceptan enteros de 1 a 99.
- Preparar el mensaje solo modifica un textarea local. No existe un envío a WhatsApp ni una operación de pago.
- El catálogo tiene 10 ejemplos iniciales y 44 cervezas con fotografías y precios de referencia de Líder. No confirma precios ni stock de Mis Reinas. Las imágenes se guardan localmente y todos los productos se pueden editar en el administrador.
- `importar_catalogo` valida las imágenes antes de crear registros y evita duplicarlos. La migración 0003 permite una descripción vacía en las fichas que solo muestran título, imagen y precio.

Código: inicio/static/inicio/js/carrito.js e inicio/static/inicio/css/carrito.css.
