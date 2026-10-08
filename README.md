# Mis Reinas — Evaluación II

Integrante: **Bastian Acuna**. Proyecto individual de Desarrollo Backend con Django.

El sitio original se integró en Django conservando sus cuatro secciones, su diseño y sus fotografías. Inicio contiene un catálogo administrable de productos y servicios: los 10 ejemplos iniciales y 44 cervezas de referencia del catálogo público de Líder. El formulario de contacto guarda los mensajes en la base de datos y permite revisarlos en el administrador.

## Inicio rápido en Windows

1. Extraer completamente el ZIP en una carpeta.
2. Tener instalado Python 3.12 o superior. El proyecto fue verificado con Python 3.13 y Django 6.1.
3. Abrir **Iniciar Mis Reinas.cmd** con doble clic. La primera vez se crea el entorno `.venv` y se instalan las dependencias; requiere internet para esa instalación.
4. Abrir **http://127.0.0.1:8001/**.

El ZIP incluye la base de datos con 54 registros y sus imágenes. Las fotos y los estilos son locales: una vez instaladas las dependencias, el sitio funciona sin servicios externos.

Administrador: **http://127.0.0.1:8001/admin/**. Usuario: **root**. Contraseña: **rootroot**. Son las credenciales locales exigidas por la pauta de evaluación.

Para detener el servidor, presionar `Ctrl+C` en su ventana. Si ya hay un servidor en el puerto 8001, utilizar esa instancia o detenerla antes de abrir otra.

## Instalación manual

Desde la carpeta que contiene `manage.py`, en PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8001
```

Si se comienza sin la base de datos incluida, ejecutar también:

```powershell
.\.venv\Scripts\python.exe manage.py preparar_demo
```

El comando `preparar_demo` agrega las ofertas iniciales que falten y crea `root` solo si no existe. No sobrescribe los textos o contraseñas ya modificados. No se ejecuta automáticamente al iniciar el servidor, por lo que los productos eliminados desde el administrador no reaparecen.

## Organización

| App | Ruta | Responsabilidad |
| --- | --- | --- |
| `inicio` | `/` | Inicio y catálogo dinámico, modelo Producto y administrador |
| `nosotros` | `/nosotros/` | Historia, escudo y valores |
| `sucursales` | `/sucursales/` | Los tres locales existentes, direcciones y servicios |
| `contacto` | `/contacto/` | Formulario con validación, guardado y administrador de mensajes |

Cada app tiene su `apps.py`, `urls.py`, `views.py`, templates y recursos estáticos con un nombre propio. `inicio/templates/inicio/base.html` reúne el encabezado, menú y pie compartidos. `misreinas/` contiene la configuración general.

Los archivos del frontend previo se conservan en `referencia_frontend/` como referencia; la versión evaluable se ejecuta con `manage.py`.

## Modelo evaluado

`inicio/models.py` define **Producto**, con ocho atributos explícitos: `nombre`, `descripcion`, `categoria`, `imagen`, `created`, `updated`, `precio` y `unidad`, además del ID automático. Los dos últimos se agregaron para el carrito de demostración. El campo de imagen usa Pillow. Las migraciones se encuentran en `inicio/migrations/`.

El catálogo contiene 10 productos genéricos iniciales, con ilustraciones y precios ficticios, y 44 cervezas importadas con fotos y precios de referencia en CLP. Se muestran **5 registros por página**, con orden estable por ID y enlaces a primera, anterior, siguiente y última página. Con 54 registros hay 11 páginas; los productos importados empiezan en la página 3. La descripción es opcional mediante la migración 0003 para permitir fichas con título, foto y precio.

Para demostrar la persistencia: entrar al administrador, editar una descripción, guardar y actualizar Inicio. Crear, cambiar o eliminar productos afecta el catálogo y la cantidad de páginas automáticamente. La base de datos es `db.sqlite3`; las imágenes subidas están en `media/`.

Los mensajes de contacto se almacenan localmente y se ven en el panel. El formulario no envía correos ni WhatsApp.

## Comprobaciones

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
```

Las pruebas usan una base temporal y cubren páginas, paginación, imágenes, administración del catálogo, persistencia, validación de contacto y CSRF. No alteran los datos de la entrega.

## Entrega

El archivo **Acuna.zip** contiene una carpeta `Acuna/` con el proyecto, `integrantes.txt`, la base de datos, imágenes, migraciones, dependencias y esta guía. El entorno virtual, Git y archivos temporales se excluyen: se recrea el entorno en el equipo donde se presente.

Leer **GUIA_DEFENSA.md** para preparar la explicación técnica del proyecto.

## Datos de los locales

Direcciones y contactos revisados en las páginas de Facebook proporcionadas por el usuario el 8 de octubre de 2026:

| Local | Dirección publicada | Teléfono publicado | Facebook |
| --- | --- | --- | --- |
| Almacén Mis Reinas | Los Delfines 1850, Los Lobos Viejos, Talcahuano | +56 9 5672 6971 | https://www.facebook.com/almacenmisreinas |
| Minimarket Mis Reinas | Avenida Los Lobos 1836, Talcahuano, Chile | +56 9 5672 6971 | https://www.facebook.com/profile.php?id=61594394111365 |
| Botillería Mis Reinas | Avenida Los Lobos 813, Concepción, Chile | +56 9 5672 6971 (confirmado por el usuario) | https://www.facebook.com/profile.php?id=61570976522580 |

Almacén publica también el correo caterinvenegas.s@hotmail.com. Los botones de teléfono, WhatsApp, correo y Facebook abren esos canales externos; el formulario del sitio sigue guardando mensajes localmente. El minimarket se corrigió de 1838 a 1836 y la botillería usa su nombre publicado. Los horarios anteriores no se verificaron en estas fichas y se sustituyeron por una indicación para consultarlos en cada página. La carpeta referencia_frontend conserva el contenido histórico sin estas correcciones.

## Carrito de demostración

El usuario confirmó que +56 9 5672 6971 es el teléfono de los tres locales.

El carrito es una función adicional al alcance de la evaluación: permite agregar productos, cambiar cantidades de 1 a 99, quitar o vaciar y elegir un local. Conserva únicamente IDs, cantidades y local en localStorage, sin enviar datos. Al cambiar de página o recargar, los nombres y precios se consultan nuevamente desde Django. Los productos eliminados o sin precio se descartan al recargar. Un navegador que bloquee almacenamiento permite usarlo en la página actual y muestra un aviso.

El botón **Preparar pedido para WhatsApp (demo)** muestra un mensaje local con cantidades, subtotales, total y local. No abre WhatsApp ni tiene una ruta de envío: no crea pedidos, no reserva stock, no cobra y no almacena pedidos en la base de datos. Los enlaces de WhatsApp de Contacto y Sucursales siguen siendo canales reales de consulta, independientes del prototipo.

Los diez productos iniciales conservan sus precios ficticios e ilustraciones genéricas. Las 44 cervezas tienen precios de referencia observados en Líder el 8 de octubre de 2026, que no representan precios ni existencias confirmados de Mis Reinas. Todos se pueden modificar desde el administrador; dejar el precio vacío muestra “Consultar precio” y deshabilita su compra de ejemplo. Las imágenes originales de los locales se mantienen en las otras secciones. El script herramientas/generar_ilustraciones.py permite regenerar las ilustraciones con Pillow.

Para demostrarlo: agregar pan y leche en la primera página, pasar a la segunda y agregar una bebida, ajustar cantidades, elegir un local y preparar la vista previa. Comprobar que no cambia a WhatsApp y que no aparece ningún pedido en el administrador. Vaciar el carrito al terminar.

## Catálogo importado de referencia

`inicio/data/catalogo_lider.csv` conserva los 44 registros de origen, sus precios, URLs de producto e imagen y fechas de captura. Se añadieron las marcas LOA y Kross a dos títulos iguales después de comprobar sus fichas para distinguirlos. Las fotos se descargaron y validaron con Pillow; quedan en `media/productos/lider-*.jpg` (o su formato original), sin depender del CDN al mostrar el sitio. Dos fotos usan la ampliación publicada de 768 × 768; las otras, el mayor candidato de la categoría, de 580 × 580.

Para volver a agregar los productos que falten, con conexión a Internet:

```powershell
.\.venv\Scripts\python.exe manage.py importar_catalogo
```

El comando valida el CSV y todas las imágenes antes de guardar los registros. Conserva productos existentes y ediciones hechas desde el administrador. No se ejecuta al iniciar el servidor. Los productos importados son bebidas del prototipo, sin descripción comercial añadida ni publicación en una tienda externa.
