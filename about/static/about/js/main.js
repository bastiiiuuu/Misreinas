// Este archivo controla el DOM del frontend; la consulta y persistencia de Sucursales se realizan en Django.
document.addEventListener('DOMContentLoaded', () => { // Espera al evento que indica que el navegador terminó de construir el DOM; el callback no necesita parámetros.
  initNavToggle(); // Inicializa el botón del menú después de que sus elementos HTML puedan encontrarse.
  initContactForm(); // Inicializa la validación de demostración; la función comprueba primero que exista el formulario.
}); // Cierra el callback y su registro; la inicialización ocurre cuando se dispara DOMContentLoaded.

/* ---------- Menú hamburguesa ---------- */
function initNavToggle() { // Agrupa el comportamiento del menú; no recibe parámetros porque busca los elementos por sus id del HTML.
  const toggle = document.getElementById('navToggle'); // Guarda la referencia al botón; const impide reasignar la variable, aunque permite cambiar el elemento.
  const menu = document.getElementById('navMenu'); // Guarda la lista de enlaces que se expandirá o contraerá.
  if (!toggle || !menu) return; // Sale si falta algún elemento, evitando intentar registrar eventos sobre null.

  toggle.addEventListener('click', () => { // Registra un callback que se ejecutará cuando el usuario pulse el botón del menú.
    const isOpen = menu.classList.toggle('is-open'); // Añade o retira la clase CSS y obtiene un booleano que indica si quedó presente.
    toggle.setAttribute('aria-expanded', String(isOpen)); // Convierte el booleano en texto para comunicar el estado a lectores de pantalla.
  }); // Cierra el callback del botón; la clase CSS define la presentación visual del menú abierto.

  // Cierra el menú al elegir una opción, para que no cubra el contenido en pantallas pequeñas.
  menu.querySelectorAll('a').forEach((link) => { // Obtiene los enlaces del menú y entrega cada elemento al parámetro link del callback.
    link.addEventListener('click', () => { // Cada enlace recibe un callback que se ejecuta al seleccionarlo.
      menu.classList.remove('is-open'); // Retira la clase de apertura antes de navegar a la sección elegida.
      toggle.setAttribute('aria-expanded', 'false'); // Sincroniza el estado accesible del botón con el menú que se acaba de cerrar.
    }); // Cierra el callback del enlace actual.
  }); // Cierra el recorrido; cada enlace queda asociado a su manejador de cierre.
} // Cierra initNavToggle; declarar la función no la ejecuta por sí solo.

/* ---------- Validación del formulario de contacto ---------- */
function initContactForm() { // Agrupa la demostración del formulario; no implementa envío HTTP, correo ni persistencia en BD.
  const form = document.getElementById('contactForm'); // Busca el formulario por el id que declara contact/contacto.html.
  if (!form) return; // En Inicio, Nosotros y Sucursales no existe este formulario, por lo que se termina sin errores.

  const feedback = document.getElementById('formFeedback'); // Conserva la referencia al aviso de validación que ya existe en el HTML.

  const rules = { // Asocia cada name del formulario a un objeto con su función de validación y su mensaje de error.
    nombre: { // La clave nombre coincide con el atributo name del input de nombre completo.
      validate: (value) => value.trim().length >= 3, // value es el texto del campo; trim elimina espacios de los extremos y exige tres caracteres restantes.
      message: 'Ingresa tu nombre completo (mínimo 3 caracteres).' // Define la explicación que se mostrará si la función validate devuelve false.
    }, // Cierra la regla de nombre y separa la siguiente propiedad del objeto rules.
    contacto: { // La clave contacto corresponde al input que acepta un teléfono o correo de contacto.
      validate: (value) => isValidPhoneOrEmail(value.trim()), // Envía el texto sin espacios exteriores a la función que comprueba ambos formatos.
      message: 'Ingresa un teléfono válido (+56 9 ...) o un correo válido.' // Indica al usuario qué tipo de dato se admite en este campo.
    }, // Cierra la regla de contacto.
    sucursal: { // La clave sucursal identifica el select del formulario.
      validate: (value) => value !== '', // Rechaza el valor vacío de la opción inicial para exigir que se seleccione un local.
      message: 'Selecciona la sucursal con la que quieres contactarte.' // Explica por qué la opción inicial no sirve como selección.
    }, // Cierra la regla de sucursal.
    mensaje: { // La clave mensaje corresponde al textarea del formulario.
      validate: (value) => value.trim().length >= 10, // Exige al menos diez caracteres después de quitar espacios exteriores.
      message: 'Cuéntanos un poco más (mínimo 10 caracteres).' // Explica el mínimo requerido por esta demostración de validación.
    } // Cierra la última regla; no hace falta una coma porque no sigue otra propiedad.
  }; // Cierra el objeto de reglas y la asignación a la constante rules.

  // Retira errores al editar un campo para permitir que el usuario corrija su contenido.
  Object.keys(rules).forEach((name) => { // Recorre los nombres de las reglas; name contiene una clave distinta en cada iteración.
    const field = form.elements[name]; // Localiza el control cuyo atributo name coincide con la clave de la regla.
    if (!field) return; // Si ese control no existe, omite esta iteración sin interrumpir el resto del recorrido.
    field.addEventListener('input', () => clearFieldError(field)); // Retira el error al escribir, reutilizando la función que limpia su presentación.
    field.addEventListener('change', () => clearFieldError(field)); // Retira también el error al cambiar una selección o confirmar otro control.
  }); // Cierra el recorrido y el registro de eventos de edición de los campos.

  form.addEventListener('submit', (event) => { // event es el objeto del evento de envío; permite cancelar la acción predeterminada del navegador.
    event.preventDefault(); // Cancela el envío HTML para ejecutar esta demostración en la misma página; no envía datos a Django.
    feedback.classList.remove('is-visible'); // Oculta el aviso de un intento anterior antes de comprobar de nuevo los campos.

    let isFormValid = true; // let permite cambiar esta bandera cuando alguna regla detecte un dato inválido.

    Object.entries(rules).forEach(([name, rule]) => { // Obtiene pares de clave y valor; la desestructuración separa el nombre del campo y su objeto de regla.
      const field = form.elements[name]; // Recupera el control del formulario asociado a esta regla.
      if (!field) return; // Omite un control inexistente para que el callback no acceda a una propiedad de null o undefined.
      const valid = rule.validate(field.value); // Ejecuta la función de validación con el valor actual del control y conserva su booleano.
      if (!valid) { // Entra cuando el contenido no cumple la condición de esta regla.
        isFormValid = false; // Marca el formulario completo como inválido sin dejar de revisar los otros campos.
        showFieldError(field, rule.message); // Entrega el control y su explicación a la función que destaca y muestra el error.
      } else { // Se ejecuta cuando la regla del campo actual devuelve true.
        clearFieldError(field); // Quita cualquier error anterior que ya se haya corregido.
      } // Cierra la alternativa de validación del campo actual.
    }); // Termina la evaluación de todas las reglas, sin detenerse en el primer error.

    if (!isFormValid) { // Si al menos una regla falló, no se muestra el aviso de validación correcta.
      const firstInvalid = form.querySelector('.has-error input, .has-error select, .has-error textarea'); // Busca el primer control de los contenedores marcados con error.
      if (firstInvalid) firstInvalid.focus(); // Lleva el foco al primer control inválido para facilitar su corrección con teclado.
      return; // Termina este callback de submit antes de limpiar el formulario o presentar el aviso correcto.
    } // Cierra el caso de formulario inválido.

    // La validación correcta es una demostración frontend; aquí no se usa fetch ni se almacena un mensaje.
    feedback.classList.add('is-visible'); // Activa la clase que muestra el aviso de demostración del HTML.
    form.reset(); // Devuelve los controles a sus valores iniciales después de terminar la validación de demostración.
    feedback.scrollIntoView({ behavior: 'smooth', block: 'center' }); // Desplaza la vista suavemente para que el aviso quede cerca del centro visible.
  }); // Cierra el callback de submit y su asociación al formulario.
} // Cierra initContactForm y deja sus eventos registrados cuando se ejecuta la función.

function showFieldError(field, message) { // field es el control inválido y message es el texto que explica el problema al usuario.
  const wrapper = field.closest('.field'); // Busca el contenedor de campo más cercano para agrupar control, etiqueta y espacio de error.
  if (!wrapper) return; // Sale si no hay contenedor, evitando modificar clases de un elemento inexistente.
  wrapper.classList.add('has-error'); // Activa la clase que cambia el borde del control según el CSS del frontend.
  const errorEl = wrapper.querySelector('.field__error'); // Encuentra el elemento reservado para escribir el mensaje de este campo.
  if (errorEl) errorEl.textContent = message; // Escribe texto, sin interpretar etiquetas HTML, únicamente cuando existe el elemento de error.
} // Cierra la función de presentación del error de un campo.

function clearFieldError(field) { // Recibe el control cuyo mensaje y presentación de error deben retirarse.
  const wrapper = field.closest('.field'); // Encuentra el mismo contenedor que utiliza showFieldError para mantener ambos comportamientos coherentes.
  if (!wrapper) return; // Si el control no pertenece a un contenedor conocido, termina sin modificar el DOM.
  wrapper.classList.remove('has-error'); // Retira la clase que resalta el borde como inválido.
  const errorEl = wrapper.querySelector('.field__error'); // Busca el espacio de error dentro del contenedor actual.
  if (errorEl) errorEl.textContent = ''; // Vacía el mensaje anterior mediante textContent, sin sustituir la estructura HTML del campo.
} // Cierra la función que restaura la presentación normal de un campo.

function isValidPhoneOrEmail(value) { // value es la cadena ya recortada; devuelve un booleano para la regla de contacto.
  if (!value) return false; // Rechaza un texto vacío antes de comprobar las expresiones regulares.
  const phonePattern = /^(\+?56)?[\s-]?9?[\s-]?\d{4}[\s-]?\d{4}$/; // Patrón básico: prefijo 56 y 9 opcionales, grupos de cuatro dígitos y separadores; ^ y $ exigen coincidencia de toda la cadena.
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Patrón básico de correo: texto sin espacios, arroba, dominio y punto; no verifica que la dirección exista.
  return phonePattern.test(value) || emailPattern.test(value); // Acepta si coincide cualquiera de los dos formatos; || evita evaluar el segundo cuando el primero ya es true.
} // Cierra la comprobación de formato, que es validación de presentación y no validación de un backend de contacto.
