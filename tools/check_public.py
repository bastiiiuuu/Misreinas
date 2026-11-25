"""Comprueba todas las rutas estáticas, filtros y la ausencia de datos privados."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re
ROOT=Path(__file__).resolve().parents[1]/'public-build'
errors=[];pages=list(ROOT.rglob('*.html'))
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag=='form':errors.append(f'{page}: formulario no compatible con edición estática')
        for attribute in ['href','src']:
            value=values.get(attribute,'');url=urlsplit(value)
            if not url.path or url.scheme or url.netloc:continue
            if not url.path.startswith('/Misreinas/'):
                errors.append(f'{page}: ruta sin prefijo {value}');continue
            target=ROOT/unquote(url.path.removeprefix('/Misreinas/'))
            if target.is_dir():target=target/'index.html'
            if not target.is_file():errors.append(f'{page}: enlace roto {value}')
            if url.query:errors.append(f'{page}: filtro dinámico sin exportar {value}')
for page in pages:
    text=page.read_text(encoding='utf-8');Links().feed(text)
    if re.search(r'DEMO|demostraci[oó]n|csrfmiddlewaretoken|/admin/|explorar-api',text,re.I):errors.append(f'{page}: contenido no destinado al público')
for file in ROOT.rglob('*'):
    if file.suffix in {'.sqlite3','.py','.env'}:errors.append(f'Archivo privado o de servidor en salida: {file}')
first=(ROOT/'ofertas/index.html').read_text(encoding='utf-8')
second=(ROOT/'ofertas/pagina/2/index.html').read_text(encoding='utf-8')
if first.count('class="card offer-card"')!=5 or second.count('class="card offer-card"')!=5:errors.append('La paginación debe repartir los diez productos en dos páginas.')
if errors:raise SystemExit('\n'.join(errors))
print(f'{len(pages)} páginas: enlaces, filtros, paginación y salida pública verificados.')
