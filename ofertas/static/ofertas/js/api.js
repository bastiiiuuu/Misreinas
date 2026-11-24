/**
 * Cada búsqueda reemplaza la petición anterior para que una respuesta lenta no
 * sobrescriba el filtro más reciente. El catálogo se construye con nodos de texto:
 * nombres y descripciones de la API no se interpretan como HTML.
 */
const form = document.querySelector('#api-search');
const status = document.querySelector('#status');
const results = document.querySelector('#results');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
let controller;
let requestNumber = 0;
let links = {};

function element(tag, text) {
  const node = document.createElement(tag);
  node.textContent = text;
  return node;
}

async function load(url) {
  controller?.abort();
  controller = new AbortController();
  const current = ++requestNumber;
  const timer = setTimeout(() => controller.abort(), 8000);
  status.textContent = 'Consultando catálogo…';
  results.setAttribute('aria-busy', 'true');
  previous.disabled = next.disabled = true;
  try {
    const response = await fetch(url, { signal: controller.signal, headers: { Accept: 'application/json' } });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error ?? 'No se pudo consultar el catálogo.');
    if (current !== requestNumber) return;
    results.replaceChildren();
    for (const item of data.results) {
      const card = document.createElement('article');
      card.append(element('h2', item.nombre), element('p', item.descripcion), element('strong', item.precio_clp === null ? 'Consultar precio' : new Intl.NumberFormat('es-CL', { style:'currency',currency:'CLP' }).format(Number(item.precio_clp))), element('p', item.sucursal.nombre));
      results.append(card);
    }
    links = data;
    previous.disabled = !data.previous;
    next.disabled = !data.next;
    document.querySelector('#page').textContent = `Página ${data.page} de ${data.pages}`;
    document.querySelector('#json').textContent = JSON.stringify(data, null, 2);
    status.textContent = data.count ? `${data.count} productos encontrados.` : 'No hay productos para esta búsqueda.';
  } catch (error) {
    if (current !== requestNumber) return;
    results.replaceChildren();
    document.querySelector('#json').textContent = '';
    document.querySelector('#page').textContent = '';
    status.textContent = error.name === 'AbortError' ? 'La consulta tardó demasiado. Intenta buscar de nuevo.' : error.message;
  } finally {
    clearTimeout(timer);
    if (current === requestNumber) results.removeAttribute('aria-busy');
  }
}
form.addEventListener('submit', event => {
  event.preventDefault();
  const url = new URL(form.dataset.endpoint, location.origin);
  url.searchParams.set('q', new FormData(form).get('q'));
  load(url);
});
previous.addEventListener('click', () => { if (links.previous) load(links.previous); });
next.addEventListener('click', () => { if (links.next) load(links.next); });
load(form.dataset.endpoint);
