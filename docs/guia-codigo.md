# Guía del código de Mis Reinas

## Cómo llega una oferta al navegador

Django recibe la URL en `misreinas/urls.py`. El prefijo `/ofertas/` se delega a `ofertas/urls.py`, y su vista reúne el catálogo. `select_related` obtiene la sucursal en la misma consulta y `prefetch_related` reúne las categorías sin repetir una consulta por tarjeta. Los filtros se aplican antes de crear el paginador, por lo que el número de resultados corresponde a la selección y no al catálogo completo.

Las plantillas de `ofertas/templates/` presentan esos objetos. Django escapa los nombres y las descripciones al imprimirlos. JavaScript no es necesario para consultar esta versión HTML del catálogo.

## Cómo funciona la API

`api/urls.py` agrupa las rutas JSON. `api/views.py` valida parámetros, consulta los mismos modelos y selecciona expresamente los campos publicados. `serialize_offer` define el contrato: precio decimal como cadena, imagen opcional, sucursal y categorías. La API no entrega contraseñas, sesiones o una representación automática de todas las columnas.

Los errores se mantienen en JSON para que el cliente pueda tratarlos sin intentar interpretar una página HTML. El decorador `json_get` permite consultar y rechaza escrituras. La edición sigue protegida en Django Admin.

`ofertas/static/ofertas/js/api.js` consume el endpoint. Cancela una búsqueda anterior y comprueba qué solicitud es la más reciente, evitando que una respuesta lenta reemplace la búsqueda actual. Construye las tarjetas con textContent, así que el texto recibido no se ejecuta como HTML.

## Qué representan las relaciones

`Sucursal` identifica el local de una oferta. La relación es muchos a uno: varias ofertas pueden pertenecer a una sucursal. La eliminación está protegida mientras existan ofertas relacionadas. `Categoria` clasifica el catálogo mediante una relación muchos a muchos: una oferta puede llevar varias etiquetas y una etiqueta puede aparecer en varias ofertas.

El precio permite null porque un importe desconocido no significa que el producto sea gratis. Las fechas automáticas registran altas y guardados, no prueban cuándo se publicó una promoción en una red social.

## Qué hace el formulario de contacto

`contact/forms.py` valida nombre, correo, teléfono opcional, sucursal, asunto y mensaje. El selector de sucursal utiliza registros existentes; manipular el identificador desde el navegador no lo convierte en una opción válida. El teléfono se normaliza al formato chileno admitido por el ejercicio. `contact/views.py` conserva los errores para que la persona pueda corregirlos. Un envío válido muestra una confirmación que declara el alcance de demostración.

No hay envío de correo ni tabla de mensajes. Incorporarlos sería un cambio funcional adicional que requiere definir destino, permisos, retención y protección contra abuso.

## Qué se debe conservar al migrar

El historial mantiene la transferencia del modelo Oferta desde core a ofertas antes de eliminar la tabla antigua. Las migraciones usan modelos históricos para no depender de la definición actual del código. Las imágenes se referencian por su ruta y no se copian en cada cambio del esquema. No borres migraciones antiguas para resolver un error sin revisar las bases que ya las aplicaron.

## Cómo demostrar el proyecto

1. Crear un entorno nuevo, aplicar migraciones y ejecutar seed_demo.
2. Mostrar catálogo, categorías, filtro por sucursal y paginación.
3. Abrir el explorador de API y comparar los mismos productos con la respuesta JSON.
4. Mostrar una búsqueda sin resultados y un parámetro inválido.
5. Enviar un contacto incorrecto y explicar la validación del servidor y CSRF.
6. Ejecutar las pruebas y explicar qué comportamiento protege cada caso.
