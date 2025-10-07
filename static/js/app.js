// ---- CSRF from cookie ----
function getCookie(name) {
  const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return m ? m.pop() : '';
}
const CSRF = getCookie('csrftoken');
const jsonHeaders = { 'Content-Type': 'application/json', 'X-CSRFToken': CSRF };

// ---- Shortcuts to toasts ----
const toastOk = (m) => window.showToast?.({ title: 'Success', message: m, type: 'success' });
const toastErr = (m) => window.showToast?.({ title: 'Error', message: m, type: 'error' });

// ---- Elements ----
const listEl   = document.getElementById('product-list');
const loadEl   = document.getElementById('state-loading');
const emptyEl  = document.getElementById('state-empty');
const errEl    = document.getElementById('state-error');

const btnRefresh = document.getElementById('btn-refresh');
const btnOpenCreate = document.getElementById('btn-open-create');

const modalForm = document.getElementById('modal-form');
const modalTitle = document.getElementById('modal-title');
const form = document.getElementById('product-form');

const f = {
  id: document.getElementById('field-id'),
  name: document.getElementById('field-name'),
  price: document.getElementById('field-price'),
  category: document.getElementById('field-category'),
  size: document.getElementById('field-size'),
  stock: document.getElementById('field-stock'),
  thumb: document.getElementById('field-thumb'),
  desc: document.getElementById('field-desc'),
  featured: document.getElementById('field-featured'),
  sale: document.getElementById('field-sale'),
};

const modalConfirm = document.getElementById('modal-confirm');
const confirmNo = document.getElementById('confirm-no');
const confirmYes = document.getElementById('confirm-yes');
let pendingDeleteId = null;

function show(el, flag) { if (el) el.classList.toggle('hidden', !flag); }

// ---- API calls ----
async function apiList() {
  const r = await fetch('/ajax/products/');
  if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
  const j = await r.json();
  if (!j.ok) throw new Error(j.error || 'Failed to load');
  return j.data;
}

async function apiGet(id) {
  const r = await fetch(`/ajax/product/${id}/`);
  const j = await r.json();
  if (!j.ok) throw new Error(j.error || 'Failed to fetch item');
  return j.data;
}

async function apiCreate(body) {
  const r = await fetch('/ajax/product/create/', { method: 'POST', headers: jsonHeaders, body: JSON.stringify(body) });
  const j = await r.json();
  if (!j.ok) throw new Error(j.error || 'Create failed');
  return j.data;
}

async function apiUpdate(id, body) {
  const r = await fetch(`/ajax/product/${id}/update/`, { method: 'POST', headers: jsonHeaders, body: JSON.stringify(body) });
  const j = await r.json();
  if (!j.ok) throw new Error(j.error || 'Update failed');
  return j.data;
}

async function apiDelete(id) {
  const r = await fetch(`/ajax/product/${id}/delete/`, { method: 'POST', headers: jsonHeaders });
  const j = await r.json();
  if (!j.ok) throw new Error(j.error || 'Delete failed');
  return true;
}

// ---- Render list ----
function render(products) {
  listEl.innerHTML = '';
  products.forEach(p => {
    const li = document.createElement('li');
    li.className = 'rounded-xl border p-4 bg-white shadow-sm flex flex-col gap-2';
    li.innerHTML = `
      <div class="flex items-start justify-between gap-3">
        <div>
          <div class="font-semibold">${p.name}</div>
          <div class="text-sm text-slate-600">ID #${p.id} • ${p.category || 'Uncategorized'} • Size ${p.size}</div>
        </div>
        <img src="${p.thumbnail || ''}" alt="" class="h-12 w-12 object-cover rounded ${p.thumbnail ? '' : 'hidden'}">
      </div>
      <div class="text-sm text-slate-700">Rp ${Number(p.price).toLocaleString('id-ID')} • Stock ${p.stock} (${p.stock_status})</div>
      <div class="text-sm">${p.description || ''}</div>
      <div class="mt-2 flex gap-2">
        <button data-edit="${p.id}" class="rounded bg-slate-800 text-white px-3 py-1.5">Edit</button>
        <button data-delete="${p.id}" class="rounded bg-rose-600 text-white px-3 py-1.5">Delete</button>
      </div>
    `;
    listEl.appendChild(li);
  });
}

// ---- Load flow ----
async function load() {
  if (!listEl) return; // not on the list page
  show(loadEl, true); show(emptyEl, false); show(errEl, false);
  try {
    const items = await apiList();
    render(items);
    show(emptyEl, items.length === 0);
  } catch (e) {
    if (errEl) errEl.textContent = e.message || 'Request failed';
    show(errEl, true);
  } finally {
    show(loadEl, false);
  }
}

// ---- Open create modal ----
btnOpenCreate?.addEventListener('click', () => {
  if (!modalForm) return;
  modalTitle.textContent = 'Create Product';
  f.id.value = '';
  f.name.value = ''; f.price.value = ''; f.category.value = '';
  f.size.value = 'M'; f.stock.value = '0'; f.thumb.value = ''; f.desc.value = '';
  f.featured.checked = false; f.sale.checked = false;
  modalForm.showModal();
});

// ---- Click handlers on list (edit/delete) ----
listEl?.addEventListener('click', async (e) => {
  const id = e.target.getAttribute('data-edit');
  const del = e.target.getAttribute('data-delete');

  if (id) {
    try {
      const p = await apiGet(id);
      modalTitle.textContent = 'Update Product';
      f.id.value = p.id; f.name.value = p.name; f.price.value = p.price;
      f.category.value = p.category || ''; f.size.value = p.size; f.stock.value = p.stock;
      f.thumb.value = p.thumbnail || ''; f.desc.value = p.description || '';
      f.featured.checked = !!p.is_featured; f.sale.checked = !!p.for_sale;
      modalForm.showModal();
    } catch (err) { toastErr(err.message); }
  }

  if (del) {
    pendingDeleteId = del;
    modalConfirm?.showModal();
  }
});

// ---- Save (create/update) ----
form?.addEventListener('submit', async (ev) => {
  ev.preventDefault();
  const body = {
    name: f.name.value.trim(),
    price: Number(f.price.value || 0),
    category: f.category.value.trim(),
    size: f.size.value,
    stock: Number(f.stock.value || 0),
    thumbnail: f.thumb.value.trim(),
    description: f.desc.value.trim(),
    is_featured: !!f.featured.checked,
    for_sale: !!f.sale.checked,
  };
  const id = f.id.value;

  try {
    if (id) {
      await apiUpdate(id, body);
      toastOk('Product updated');
    } else {
      await apiCreate(body);
      toastOk('Product created');
    }
    modalForm.close();
    await load();
  } catch (e) { toastErr(e.message); }
});

// ---- Confirm delete ----
confirmNo?.addEventListener('click', () => modalConfirm.close());
confirmYes?.addEventListener('click', async () => {
  try {
    await apiDelete(pendingDeleteId);
    modalConfirm.close();
    toastOk('Product deleted');
    await load();
  } catch (e) { toastErr(e.message); }
});

// ---- Refresh button ----
btnRefresh?.addEventListener('click', load);

// ---- Initial load ----
if (listEl) load();

// --- Auth modals and AJAX ---
const modalLogin = document.getElementById('modal-login');
const modalRegister = document.getElementById('modal-register');

document.getElementById('btn-open-login')?.addEventListener('click', () => modalLogin.showModal());
document.getElementById('btn-open-register')?.addEventListener('click', () => modalRegister.showModal());

document.getElementById('btn-login-submit')?.addEventListener('click', async (e) => {
  e.preventDefault();
  try {
    const r = await fetch('/api/auth/login/', {
      method: 'POST', headers: jsonHeaders,
      body: JSON.stringify({
        username: document.getElementById('login-username').value.trim(),
        password: document.getElementById('login-password').value
      })
    });
    const j = await r.json();
    if (!j.ok) throw new Error(j.error || 'Login failed');
    modalLogin.close();
    window.showToast({ title: 'Success', message: 'Logged in', type: 'success' });
    // optional: refresh list after login (if currently on products page)
    if (typeof load === 'function') load();
  } catch (err) {
    window.showToast({ title: 'Error', message: err.message, type: 'error' });
  }
});

document.getElementById('btn-register-submit')?.addEventListener('click', async (e) => {
  e.preventDefault();
  try {
    const r = await fetch('/api/auth/register/', {
      method: 'POST', headers: jsonHeaders,
      body: JSON.stringify({
        username: document.getElementById('reg-username').value.trim(),
        password: document.getElementById('reg-password').value
      })
    });
    const j = await r.json();
    if (!j.ok) throw new Error(j.error || 'Register failed');
    modalRegister.close();
    window.showToast({ title: 'Success', message: 'Registered', type: 'success' });
    modalLogin?.showModal(); // prompt user to log in
  } catch (err) {
    window.showToast({ title: 'Error', message: err.message, type: 'error' });
  }
});

document.getElementById('btn-ajax-logout')?.addEventListener('click', async () => {
  try {
    const r = await fetch('/api/auth/logout/', { method: 'POST', headers: { 'X-CSRFToken': CSRF } });
    const j = await r.json();
    if (!j.ok) throw new Error(j.error || 'Logout failed');
    window.showToast({ title: 'Success', message: 'Logged out', type: 'success' });
    // optional: clear list UI if you want to hide products post-logout
    // listEl && (listEl.innerHTML = '');
  } catch (err) {
    window.showToast({ title: 'Error', message: err.message, type: 'error' });
  }
});
