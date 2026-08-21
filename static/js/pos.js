/* Fenix IT Mall – POS JavaScript
   Alpine.js store for cart management
*/

document.addEventListener('alpine:init', function () {
  Alpine.store('cart', {
    items: [],
    discountPct: 0,
    paymentMethod: 'cash',
    amountPaid: 0,
    customerId: '',

    get subtotal() {
      return this.items.reduce(function(sum, item) {
        return sum + (parseFloat(item.price) * parseInt(item.qty));
      }, 0);
    },
    get discountAmount() {
      return this.subtotal * (this.discountPct / 100);
    },
    get taxable() {
      return this.subtotal - this.discountAmount;
    },
    get gstAmount() {
      return this.taxable * 0.18;
    },
    get grandTotal() {
      return this.taxable + this.gstAmount;
    },
    get change() {
      return Math.max(0, parseFloat(this.amountPaid) - this.grandTotal);
    },

    addItem(product) {
      const existing = this.items.find(function(i) { return i.id === product.id; });
      if (existing) {
        if (existing.qty < existing.stock) {
          existing.qty++;
        } else {
          alert('Not enough stock for ' + existing.name);
        }
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          price: parseFloat(product.selling_price),
          qty: 1,
          stock: product.stock_quantity,
          code: product.product_code
        });
      }
    },

    removeItem(id) {
      this.items = this.items.filter(function(i) { return i.id !== id; });
    },

    updateQty(id, qty) {
      const item = this.items.find(function(i) { return i.id === id; });
      if (!item) return;
      qty = parseInt(qty);
      if (qty <= 0) {
        this.removeItem(id);
      } else if (qty > item.stock) {
        alert('Only ' + item.stock + ' in stock');
        item.qty = item.stock;
      } else {
        item.qty = qty;
      }
    },

    clear() {
      this.items = [];
      this.discountPct = 0;
      this.amountPaid = 0;
    },

    fmt(val) {
      return '₹' + parseFloat(val).toFixed(2);
    }
  });
});

// Barcode scanner listener
let barcodeBuffer = '';
let barcodeTimer = null;

document.addEventListener('keydown', function(e) {
  if (document.activeElement.tagName === 'INPUT' && document.activeElement.id !== 'barcode-input') return;
  if (e.key === 'Enter') {
    if (barcodeBuffer.length > 2) {
      searchByBarcode(barcodeBuffer);
    }
    barcodeBuffer = '';
    clearTimeout(barcodeTimer);
  } else if (e.key.length === 1) {
    barcodeBuffer += e.key;
    clearTimeout(barcodeTimer);
    barcodeTimer = setTimeout(function() { barcodeBuffer = ''; }, 100);
  }
});

function searchByBarcode(code) {
  fetch('/products/search/?barcode=' + encodeURIComponent(code))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.product) {
        Alpine.store('cart').addItem(data.product);
      } else {
        console.log('Product not found for barcode:', code);
      }
    })
    .catch(function(e) { console.error(e); });
}

function searchProducts(q) {
  if (!q || q.length < 2) return;
  fetch('/products/search/?q=' + encodeURIComponent(q))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      const resultsEl = document.getElementById('search-results');
      if (!resultsEl) return;
      resultsEl.innerHTML = '';
      (data.products || []).forEach(function(p) {
        const div = document.createElement('div');
        div.className = 'search-result-item';
        div.innerHTML = '<strong>' + p.name + '</strong> <span style="color:var(--accent-cyan)">₹' + p.selling_price + '</span> <span style="color:var(--text-muted);font-size:12px;">Stock: ' + p.stock_quantity + '</span>';
        div.onclick = function() {
          Alpine.store('cart').addItem(p);
          document.getElementById('product-search').value = '';
          resultsEl.innerHTML = '';
        };
        resultsEl.appendChild(div);
      });
    });
}
