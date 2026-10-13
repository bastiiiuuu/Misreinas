"""Configuración de desarrollo local de Misreinas; cada decisión se explica en línea."""
from pathlib import Path  # Construye rutas de archivos portables entre Windows, Linux y macOS.

BASE_DIR = Path(__file__).resolve().parent.parent  # Resuelve el directorio que contiene manage.py, sin depender del directorio de la terminal.
SECRET_KEY = "django-insecure-misreinas-evaluacion-ii-solo-desarrollo-local"  # Clave de firma exclusivamente para esta entrega local; en producción debe venir del entorno.
DEBUG = True  # Activa diagnósticos y el servicio local de static/media durante el desarrollo.
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]"]  # Autoriza los nombres habituales del servidor local y la dirección IPv6 de loopback.

INSTALLED_APPS = [  # Registra las apps para descubrir modelos, Admin, migraciones, templates y archivos static.
    "django.contrib.admin",  # Proporciona el panel administrativo para cargar las sucursales.
    "django.contrib.auth",  # Proporciona usuarios, contraseñas con hash y permisos del superusuario.
    "django.contrib.contenttypes",  # Identifica modelos para relacionarlos con permisos y registros del Admin.
    "django.contrib.sessions",  # Conserva el inicio de sesión entre solicitudes HTTP mediante sesiones.
    "django.contrib.messages",  # Muestra avisos del Admin, como la confirmación al guardar un registro.
    "django.contrib.staticfiles",  # Descubre CSS, JS e imágenes de las carpetas static de las apps.
    "core.apps.CoreConfig",  # Registra Inicio y permite descubrir Oferta, su Admin, migraciones, templates y recursos static propios.
    "about.apps.AboutConfig",  # Registra la app independiente de Nosotros.
    "contact.apps.ContactConfig",  # Registra la app independiente de Contacto.
    "sucursales.apps.SucursalesConfig",  # Registra la app dinámica y habilita el descubrimiento de su modelo.
]  # Termina la lista de apps; conserva también las seis apps incluidas por Django.

MIDDLEWARE = [  # Define las capas que procesan cada solicitud, en este orden de entrada.
    "django.middleware.security.SecurityMiddleware",  # Añade protecciones y cabeceras generales de seguridad.
    "django.contrib.sessions.middleware.SessionMiddleware",  # Añade request.session antes de procesar autenticación.
    "django.middleware.common.CommonMiddleware",  # Maneja comportamientos comunes, como completar la barra final de URLs.
    "django.middleware.csrf.CsrfViewMiddleware",  # Comprueba el token CSRF en solicitudes que pueden modificar datos, incluido el Admin.
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Añade request.user a partir de la sesión ya disponible.
    "django.contrib.messages.middleware.MessageMiddleware",  # Permite mostrar mensajes temporales apoyándose en las capas anteriores.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Restringe que otra página incruste el sitio en un frame.
]  # Cierra las capas; Django procesa las respuestas en orden inverso.

ROOT_URLCONF = "misreinas.urls"  # Indica el módulo de rutas usando el nombre exacto de la carpeta misreinas.
TEMPLATES = [  # Permite configurar uno o varios motores de plantillas; aquí usamos solamente el de Django.
    {  # Abre la configuración de ese motor de plantillas.
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Interpreta etiquetas como url, static, for e if.
        "DIRS": [],  # No necesitamos una carpeta global porque cada app posee sus propios templates.
        "APP_DIRS": True,  # Busca en app/templates/ de todas las apps registradas.
        "OPTIONS": {  # Agrupa las opciones adicionales del motor.
            "context_processors": [  # Inyecta datos comunes en el contexto de render().
                "django.template.context_processors.request",  # Hace disponible request en los templates.
                "django.contrib.auth.context_processors.auth",  # Expone user y permisos para las plantillas del Admin.
                "django.contrib.messages.context_processors.messages",  # Expone los avisos generados por el sistema de mensajes.
            ],  # Cierra los procesadores de contexto.
        },  # Cierra las opciones adicionales.
    },  # Cierra el único motor configurado.
]  # Cierra la lista de motores.
WSGI_APPLICATION = "misreinas.wsgi.application"  # Señala la aplicación callable WSGI dentro del paquete existente en minúsculas.
ASGI_APPLICATION = "misreinas.asgi.application"  # Señala la aplicación callable ASGI dentro del mismo paquete.

DATABASES = {  # Define las conexiones de base de datos del ORM.
    "default": {  # Es el alias que Django utiliza cuando no se solicita otra conexión.
        "ENGINE": "django.db.backends.sqlite3",  # SQLite evita instalar otro servidor para rendir la evaluación local.
        "NAME": BASE_DIR / "db.sqlite3",  # Guarda la base de datos como archivo al lado de manage.py.
    },  # Cierra la conexión principal.
}  # Cierra la configuración de bases de datos.

AUTH_PASSWORD_VALIDATORS = [  # Conserva las comprobaciones de contraseña del proyecto estándar.
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # Evita claves demasiado parecidas a datos del usuario.
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # Comprueba la longitud mínima configurada por Django.
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # Detecta contraseñas presentes en su lista de claves comunes.
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # Rechaza claves compuestas exclusivamente por números.
]  # Cierra los validadores usados por los formularios de contraseña de Django.

LANGUAGE_CODE = "es-cl"  # Traduce la interfaz de Django al español de Chile cuando hay traducciones disponibles.
TIME_ZONE = "America/Santiago"  # Usa la capitalización oficial de la zona IANA para mostrar fechas locales en el Admin.
USE_I18N = True  # Activa el sistema de traducciones de Django.
USE_TZ = True  # Usa fechas con zona horaria; normalmente se almacenan en UTC y se muestran en la zona configurada.
STATIC_URL = "/static/"  # Prefijo público de CSS, JS e imágenes que forman parte del frontend.
MEDIA_URL = "/media/"  # Prefijo público de los archivos subidos desde el Admin; termina con una barra.
MEDIA_ROOT = BASE_DIR / "media"  # Directorio físico donde el almacenamiento local guarda las imágenes de ImageField.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Crea automáticamente una clave primaria id de 64 bits cuando no la declaramos.
