"""Publica páginas de Django como HTML estático, sin backend ni datos de autenticación."""
from pathlib import Path
import argparse,os,sys,secrets,json,re,shutil,html
from urllib.parse import urlsplit,parse_qs,quote
from tempfile import TemporaryDirectory
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
PREFIX='/Misreinas/'

def offer_path(category=None,branch=None,page=1):
    path='ofertas/'
    if category:path+='categoria/'+quote(str(category),safe='')+'/'
    if branch:path+='local/'+str(branch)+'/'
    if int(page)>1:path+='pagina/'+str(page)+'/'
    return path

def build(output):
    if output.exists():
        if output.resolve().parent!=ROOT or output.name!='public-build':
            raise SystemExit('La salida debe ser public-build dentro del repositorio.')
        shutil.rmtree(output)
    output.mkdir(parents=True)
    data=json.loads((ROOT/'public_site/catalog.json').read_text(encoding='utf-8'))
    # La exportación utiliza una base temporal nueva. Nunca abre la base habitual.
    with TemporaryDirectory(prefix='misreinas-public-') as temporary:
        os.environ['DJANGO_SETTINGS_MODULE']='misreinas.settings'
        os.environ['DJANGO_DB_PATH']=':memory:'
        os.environ['DJANGO_SECRET_KEY']=secrets.token_urlsafe(50)
        os.environ['DJANGO_DEBUG']='1'
        import django
        django.setup()
        from django.core.management import call_command
        from django.core.paginator import Paginator
        from django.template.loader import render_to_string
        from django.test import RequestFactory
        from django.db import connection
        from django.contrib.staticfiles.finders import find
        from ofertas.models import Oferta
        from sucursales.models import Sucursal
        from categorias.models import Categoria
        from contact.forms import ContactoForm
        from PIL import Image
        call_command('migrate',verbosity=0,interactive=False)
        if str(connection.settings_dict['NAME']) != ':memory:':
            raise SystemExit('La base de exportación debe ser temporal en memoria.')
        # La migración inicial carga categorías; se reemplazan solo en esta base efímera.
        Categoria.objects.all().delete()
        for model,table in [(Sucursal,'sucursales_sucursal'),(Categoria,'categorias_categoria'),(Oferta,'ofertas_oferta'),(Oferta.categorias.through,'ofertas_oferta_categorias')]:
            model.objects.bulk_create([model(**row) for row in data[table]])
        branches=Sucursal.objects.order_by('-created','-pk')
        categories=Categoria.objects.all()
        common={'locales_del_negocio':branches,'total_locales':branches.count()}
        media={}
        for file in (ROOT/'public_site/media').rglob('*'):
            if not file.is_file():continue
            relative=file.relative_to(ROOT/'public_site/media')
            destination=Path('media')/relative.with_suffix('.webp')
            target=output/destination;target.parent.mkdir(parents=True,exist_ok=True)
            with Image.open(file) as image:
                image=image.convert('RGB');image.thumbnail((1600,1600));image.save(target,quality=87)
            media['/media/'+relative.as_posix()]=PREFIX+destination.as_posix()
        logo=ROOT/'public_site/logo.jpg'
        if logo.exists():shutil.copy2(logo,output/'logo.jpg')
        hero=ROOT/'public_site/hero.jpg'
        if hero.exists():
            with Image.open(hero) as image:
                image=image.convert('RGB');image.thumbnail((1800,1800));image.save(output/'hero.webp',quality=87)
        static=set();paths=[]
        def rewrite(match):
            name,value=match.group(1),html.unescape(match.group(2))
            if value=='https://i.postimg.cc/MGhw2NCr/logo.jpg' and logo.exists():value=PREFIX+'logo.jpg'
            elif value.startswith('/'):
                url=urlsplit(value)
                if url.path.startswith('/static/'):
                    static.add(url.path.removeprefix('/static/'));value=PREFIX+value.lstrip('/')
                elif url.path.startswith('/media/'):value=media.get(url.path,value)
                elif url.path=='/ofertas/':
                    query=parse_qs(url.query);value=PREFIX+offer_path(query.get('categoria',[None])[0],query.get('sucursal',[None])[0],query.get('page',[1])[0])+('#'+url.fragment if url.fragment else '')
                else:value=PREFIX+value.lstrip('/')
            return f'{name}="{html.escape(value,quote=True)}"'
        def publish(path,template,context):
            request=RequestFactory().get('/'+path)
            text=render_to_string(template,{**common,**context},request=request)
            text=re.sub(r'<p class="container"><a href="/ofertas/explorar-api/">.*?</a></p>','',text,flags=re.S)
            if path=='contacto/':
                # La edición estática utiliza canales públicos; no simula el envío de un POST.
                text=re.sub(r'<div class="form-card">.*?<aside class="info-card">','<div class="form-card"><h2>Contacta con nuestros locales</h2><p>Utiliza los canales publicados para consultar por productos y disponibilidad.</p><a class="btn btn-primary" href="https://www.facebook.com/almacenmisreinas">Consultar en Facebook</a></div><aside class="info-card">',text,flags=re.S)
                text=text.replace('Escríbenos por el formulario, WhatsApp o correo.','Consulta por los canales de contacto publicados.')
                text=text.replace('Escríbenos por WhatsApp, correo o el formulario en línea.','Consulta por los canales de contacto publicados.')
            text=text.replace('Ofertas de nuestras sucursales','Catálogo de nuestras sucursales')
            text=text.replace('Selecciona una etiqueta o un local para encontrar una promoción.','Selecciona una categoría o un local para explorar sus productos.')
            text=text.replace('Proyecto académico de Desarrollo Backend.','Proyecto académico de Desarrollo Backend. Confirma precios y disponibilidad con el local.')
            text=re.sub(r'\b(href|src)="([^"]*)"',rewrite,text)
            canonical='https://bastiiiuuu.github.io'+PREFIX+('ofertas/' if path.startswith('ofertas/') else path)
            text=text.replace('</head>',f'<link rel="canonical" href="{canonical}"><meta name="theme-color" content="#14120f"></head>')
            if re.search(r'demo|demostraci[oó]n|csrfmiddlewaretoken|/admin/|explorar-api',text,re.I):raise SystemExit('La página exportada contiene texto o rutas no destinados a la publicación: '+path)
            target=output/path/'index.html' if not path.endswith('.html') else output/path
            target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text,encoding='utf-8');paths.append(path)
        for path,template,context in [('', 'core/index.html',{}),('nosotros/','about/nosotros.html',{}),('sucursales/','sucursales/sucursales.html',{'sucursales':branches}),('contacto/','contact/contacto.html',{'form':ContactoForm()}),('404.html','core/404.html',{})]:publish(path,template,context)
        for category in [None,*categories]:
            for branch in [None,*branches]:
                offers=Oferta.objects.select_related('sucursal').prefetch_related('categorias').order_by('-created','-pk')
                if category:offers=offers.filter(categorias=category)
                if branch:offers=offers.filter(sucursal=branch)
                paginator=Paginator(offers,5)
                for page in range(1,paginator.num_pages+1):
                    publish(offer_path(category.slug if category else None,branch.pk if branch else None,page),'ofertas/ofertas.html',{'page_obj':paginator.page(page),'categorias':categories,'sucursales_filtro':branches,'categoria_actual':category,'sucursal_actual':branch,'filtro_query':('&'.join(([f'categoria={category.slug}'] if category else [])+([f'sucursal={branch.pk}'] if branch else [])))})
        # Solo se copian recursos referenciados por las páginas públicas, nunca el Admin.
        for relative in static:
            source=find(relative)
            if not source:raise SystemExit('Falta recurso estático: '+relative)
            destination=output/'static'/relative;destination.parent.mkdir(parents=True,exist_ok=True)
            if destination.suffix=='.css' and hero.exists():
                css=Path(source).read_text(encoding='utf-8').replace('https://i.postimg.cc/9f42kCnn/segundo-M2.jpg',PREFIX+'hero.webp')
                destination.write_text(css,encoding='utf-8')
            else:shutil.copy2(source,destination)
        connection.close()
    (output/'.nojekyll').touch()
    (output/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://bastiiiuuu.github.io/Misreinas/sitemap.xml\n',encoding='utf-8')
    urls=['','nosotros/','ofertas/','sucursales/','contacto/']
    (output/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://bastiiiuuu.github.io/Misreinas/'+p+'</loc></url>' for p in urls)+'</urlset>',encoding='utf-8')
    print(f'Publicadas {len(paths)} páginas estáticas con filtros y paginación.')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'public-build');args=parser.parse_args();build(args.output.resolve())
