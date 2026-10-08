
document.addEventListener('DOMContentLoaded', () => {
  initNavToggle();
  initContactForm();
});

/* ---------- Menú hamburguesa ---------- */
function initNavToggle() {
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('navMenu');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  // Cierra el menú al elegir una opción (útil en mobile)
  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ---------- Validación del formulario de contacto ---------- */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  const feedback = document.getElementById('formFeedback');

  const rules = {
    nombre: {
      validate: (value) => value.trim().length >= 3,
      message: 'Ingresa tu nombre completo (mínimo 3 caracteres).'
    },
    contacto: {
      validate: (value) => isValidPhoneOrEmail(value.trim()),
      message: 'Ingresa un teléfono válido (+56 9 ...) o un correo válido.'
    },
    sucursal: {
      validate: (value) => value !== '',
      message: 'Selecciona la sucursal con la que quieres contactarte.'
    },
    mensaje: {
      validate: (value) => value.trim().length >= 10,
      message: 'Cuéntanos un poco más (mínimo 10 caracteres).'
    }
  };

  // Oculta el error apenas el campo cambia, para no ser intrusivo
  Object.keys(rules).forEach((name) => {
    const field = form.elements[name];
    if (!field) return;
    field.addEventListener('input', () => clearFieldError(field));
    field.addEventListener('change', () => clearFieldError(field));
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    feedback.classList.remove('is-visible');

    let isFormValid = true;

    Object.entries(rules).forEach(([name, rule]) => {
      const field = form.elements[name];
      if (!field) return;
      const valid = rule.validate(field.value);
      if (!valid) {
        isFormValid = false;
        showFieldError(field, rule.message);
      } else {
        clearFieldError(field);
      }
    });

    if (!isFormValid) {
      const firstInvalid = form.querySelector('.has-error input, .has-error select, .has-error textarea');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    // Sin backend por ahora: confirmación en pantalla sin recargar la página.
    feedback.classList.add('is-visible');
    form.reset();
    feedback.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}

function showFieldError(field, message) {
  const wrapper = field.closest('.field');
  if (!wrapper) return;
  wrapper.classList.add('has-error');
  const errorEl = wrapper.querySelector('.field__error');
  if (errorEl) errorEl.textContent = message;
}

function clearFieldError(field) {
  const wrapper = field.closest('.field');
  if (!wrapper) return;
  wrapper.classList.remove('has-error');
  const errorEl = wrapper.querySelector('.field__error');
  if (errorEl) errorEl.textContent = '';
}

function isValidPhoneOrEmail(value) {
  if (!value) return false;
  const phonePattern = /^(\+?56)?[\s-]?9?[\s-]?\d{4}[\s-]?\d{4}$/;
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return phonePattern.test(value) || emailPattern.test(value);
}
