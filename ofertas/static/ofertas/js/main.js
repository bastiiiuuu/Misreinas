/**
 * La navegación mantiene aria-expanded sincronizado con el menú visible y se
 * cierra al elegir un enlace. No intercepta los formularios POST del servidor:
 * la validación y la protección CSRF permanecen a cargo de Django.
 */
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('navMenu');

  if (!toggle || !menu) return;

  toggle.addEventListener('click', () => {
    const abierto = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(abierto));
  });

  menu.querySelectorAll('a').forEach((enlace) => {
    enlace.addEventListener('click', () => {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
});
