/* Prototipo local: no hay peticiones de red ni enlace de envío a WhatsApp. */
(() => {
  'use strict';
  const data = document.getElementById('catalogo-carrito');
  if (!data) return;

  const products = new Map(JSON.parse(data.textContent).map(product => [String(product.id), product]));
  const key = 'misreinas-demo-cart-v1';
  const cart = new Map();
  const money = new Intl.NumberFormat('es-CL', {style: 'currency', currency: 'CLP', maximumFractionDigits: 0});
  const list = document.getElementById('cart-items');
  const branch = document.getElementById('cart-branch');
  const status = document.getElementById('cart-status');
  const empty = document.getElementById('cart-empty');
  const clear = document.getElementById('cart-clear');
  const preview = document.getElementById('cart-preview');
  const panel = document.getElementById('pedido-preview-panel');
  const message = document.getElementById('pedido-preview');

  function element(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }

  function storageUnavailable() {
    document.getElementById('cart-storage-note').hidden = false;
  }

  // Solo se recuperan IDs vigentes y cantidades enteras entre 1 y 99.
  // Los precios y los nombres siempre vienen del catálogo actual de Django.
  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved && Array.isArray(saved.items)) {
      for (const item of saved.items) {
        if (!item || typeof item !== 'object') continue;
        const id = String(item.id);
        if (products.has(id) && Number.isInteger(item.quantity) && item.quantity >= 1 && item.quantity <= 99) {
          cart.set(id, item.quantity);
        }
      }
      if (Array.from(branch.options).some(option => option.value === saved.branch)) branch.value = saved.branch;
    }
  } catch (error) {
    if (error.name !== 'SyntaxError') storageUnavailable();
  }

  function save() {
    try {
      localStorage.setItem(key, JSON.stringify({
        items: Array.from(cart, ([id, quantity]) => ({id, quantity})),
        branch: branch.value,
      }));
    } catch {
      storageUnavailable();
    }
  }

  function total() {
    return Array.from(cart, ([id, quantity]) => products.get(id).precio * quantity).reduce((sum, value) => sum + value, 0);
  }

  function previewText() {
    const lines = [
      'PEDIDO DE DEMOSTRACIÓN — NO ENVIADO',
      'Mis Reinas',
      `Local: ${branch.selectedOptions[0].textContent}`,
      'Teléfono de referencia: +56 9 5672 6971',
      '',
      ...Array.from(cart, ([id, quantity]) => {
        const product = products.get(id);
        return `${quantity} × ${product.nombre} (${product.unidad}) · ${money.format(product.precio)} c/u = ${money.format(product.precio * quantity)}`;
      }),
      '',
      `TOTAL DE EJEMPLO: ${money.format(total())}`,
      '',
      'Precios de referencia. Sin pago, reserva ni confirmación de stock.',
      'Este prototipo no envía mensajes ni genera pedidos reales.',
    ];
    return lines.join('\n');
  }

  function render() {
    list.replaceChildren();
    for (const [id, quantity] of cart) {
      const product = products.get(id);
      const row = element('li', undefined, 'cart-item');
      const description = element('div', undefined, 'cart-item__description');
      description.append(element('h4', product.nombre), element('p', `${money.format(product.precio)} / ${product.unidad}`));
      const controls = element('div', undefined, 'cart-item__controls');
      const minus = element('button', '−', 'quantity-button');
      const plus = element('button', '+', 'quantity-button');
      for (const [button, action, label, disabled] of [
        [minus, 'minus', `Disminuir cantidad de ${product.nombre}`, quantity === 1],
        [plus, 'plus', `Aumentar cantidad de ${product.nombre}`, quantity === 99],
      ]) {
        button.type = 'button';
        button.dataset.id = id;
        button.dataset.action = action;
        button.setAttribute('aria-label', label);
        button.disabled = disabled;
      }
      const input = element('input');
      input.type = 'number';
      input.min = '1';
      input.max = '99';
      input.step = '1';
      input.value = String(quantity);
      input.dataset.id = id;
      input.setAttribute('aria-label', `Cantidad de ${product.nombre}`);
      const remove = element('button', 'Quitar', 'cart-text-button');
      remove.type = 'button';
      remove.dataset.id = id;
      remove.dataset.action = 'remove';
      remove.setAttribute('aria-label', `Quitar ${product.nombre} del carrito`);
      controls.append(minus, input, plus, remove);
      row.append(description, element('strong', money.format(quantity * product.precio), 'cart-item__subtotal'), controls);
      list.append(row);
    }
    empty.hidden = cart.size > 0;
    clear.disabled = cart.size === 0;
    preview.disabled = cart.size === 0;
    document.getElementById('cart-count').textContent = String(Array.from(cart.values()).reduce((sum, qty) => sum + qty, 0));
    document.getElementById('cart-total').textContent = money.format(total());
    document.querySelectorAll('.add-to-cart').forEach(button => {
      const quantity = cart.get(button.dataset.productId) || 0;
      button.disabled = !products.has(button.dataset.productId) || quantity === 99;
      button.textContent = quantity === 99 ? 'Límite de 99 unidades' : 'Agregar al carrito';
    });
    if (cart.size === 0 || !branch.value) {
      panel.hidden = true;
      message.value = '';
    } else if (!panel.hidden) {
      message.value = previewText();
    }
  }

  document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', () => {
      const id = button.dataset.productId;
      if (!products.has(id)) return;
      const quantity = cart.get(id) || 0;
      if (quantity >= 99) return;
      cart.set(id, quantity + 1);
      save();
      render();
      status.textContent = `${products.get(id).nombre} agregado. Cantidad: ${quantity + 1}.`;
    });
  });

  list.addEventListener('click', event => {
    const button = event.target.closest('button[data-action]');
    if (!button || !list.contains(button)) return;
    const id = button.dataset.id;
    if (!cart.has(id)) return;
    const quantity = cart.get(id);
    if (button.dataset.action === 'remove') cart.delete(id);
    if (button.dataset.action === 'minus' && quantity > 1) cart.set(id, quantity - 1);
    if (button.dataset.action === 'plus' && quantity < 99) cart.set(id, quantity + 1);
    save();
    render();
    status.textContent = button.dataset.action === 'remove' ? `${products.get(id).nombre} quitado del carrito.` : 'Cantidad actualizada.';
    const next = list.querySelector(`button[data-id="${id}"][data-action="${button.dataset.action}"]:not(:disabled)`) || list.querySelector(`input[data-id="${id}"]`) || clear;
    if (!next.disabled) next.focus({preventScroll: true});
  });

  // Actualiza al escribir sin recrear el campo enfocado ni perder el cursor.
  list.addEventListener('input', event => {
    const input = event.target.closest('input[data-id]');
    if (!input || !cart.has(input.dataset.id)) return;
    const quantity = Number(input.value);
    if (!Number.isInteger(quantity) || quantity < 1 || quantity > 99) {
      input.setAttribute('aria-invalid', 'true');
      preview.disabled = true;
      panel.hidden = true;
      status.textContent = 'La cantidad debe ser un número entero entre 1 y 99.';
      return;
    }
    input.removeAttribute('aria-invalid');
    cart.set(input.dataset.id, quantity);
    save();
    const row = input.closest('.cart-item');
    row.querySelector('.cart-item__subtotal').textContent = money.format(products.get(input.dataset.id).precio * quantity);
    row.querySelector('[data-action="minus"]').disabled = quantity === 1;
    row.querySelector('[data-action="plus"]').disabled = quantity === 99;
    document.getElementById('cart-count').textContent = String(Array.from(cart.values()).reduce((sum, qty) => sum + qty, 0));
    document.getElementById('cart-total').textContent = money.format(total());
    const add = document.querySelector(`.add-to-cart[data-product-id="${input.dataset.id}"]`);
    if (add) {
      add.disabled = quantity === 99;
      add.textContent = quantity === 99 ? 'Límite de 99 unidades' : 'Agregar al carrito';
    }
    preview.disabled = Boolean(list.querySelector('[aria-invalid="true"]'));
    if (!panel.hidden) message.value = previewText();
    status.textContent = 'Cantidad actualizada.';
  });

  list.addEventListener('change', event => {
    const input = event.target.closest('input[data-id]');
    if (!input || !cart.has(input.dataset.id)) return;
    const quantity = Number(input.value);
    if (!Number.isInteger(quantity) || quantity < 1 || quantity > 99) {
      input.value = String(cart.get(input.dataset.id));
      input.removeAttribute('aria-invalid');
      preview.disabled = Boolean(list.querySelector('[aria-invalid="true"]'));
      status.textContent = 'La cantidad debe ser un número entero entre 1 y 99.';
      return;
    }
    cart.set(input.dataset.id, quantity);
    save();
    render();
    list.querySelector(`input[data-id="${input.dataset.id}"]`).focus({preventScroll: true});
    status.textContent = 'Cantidad actualizada.';
  });

  branch.addEventListener('change', () => { save(); render(); status.textContent = ''; });
  clear.addEventListener('click', () => {
    cart.clear();
    save();
    render();
    status.textContent = 'Carrito vaciado.';
  });
  preview.addEventListener('click', () => {
    if (!cart.size) return;
    if (!branch.value) {
      status.textContent = 'Selecciona un local para preparar la vista previa.';
      branch.focus();
      return;
    }
    message.value = previewText();
    panel.hidden = false;
    document.getElementById('pedido-preview-title').focus();
    status.textContent = 'Vista previa preparada. No se ha enviado ningún pedido.';
  });
  document.getElementById('cart-preview-close').addEventListener('click', () => {
    panel.hidden = true;
    preview.focus({preventScroll: true});
  });
  save();
  render();
})();
