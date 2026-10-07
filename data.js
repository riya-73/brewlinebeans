/* API-backed data adapter. The original demo dataset is preserved in data.static.js as a fallback. */
(function () {
  const base = window.BREWLINE_API_BASE || (window.location.protocol === 'file:' ? 'http://localhost:8000' : window.location.origin);
  function get(path) {
    const request = new XMLHttpRequest();
    request.open('GET', base + path, false);
    try { request.send(); } catch (_) { return null; }
    if (request.status >= 200 && request.status < 300) return JSON.parse(request.responseText);
    return null;
  }
  const apiInventory = get('/api/inventory');
  const apiMenu = get('/api/menu');
  const apiSuppliers = get('/api/suppliers');
  const apiPurchases = get('/api/purchases');
  if (!apiInventory || !apiMenu || !apiSuppliers || !apiPurchases) {
    document.write('<script src="data.static.js"><\\/script>');
    return;
  }
  const inventoryById = Object.fromEntries(apiInventory.map(i => [i.id, i]));
  window.inventory = apiInventory.map(i => ({ id: `ing-${i.id}`, name: i.name, currentStock: Number(i.current_stock), reorderLevel: Number(i.reorder_level), unit: i.unit }));
  window.statusFor = item => {
    const ratio = item.currentStock / item.reorderLevel;
    if (item.currentStock < item.reorderLevel * 0.6) return 'Critical';
    if (ratio < 1) return 'Low Stock';
    return 'Healthy';
  };
  const placeholder = 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><rect width="100%" height="100%" fill="#ead8bb"/><text x="50%" y="50%" text-anchor="middle" fill="#5c3d2e" font-size="28">Brewline</text></svg>');
  window.menuItems = apiMenu.map(item => ({ id: `m-${item.id}`, apiId: item.id, name: item.name, description: item.description, price: Number(item.price), category: item.category, image: placeholder, available: true, ingredients: item.ingredients }));
  window.suppliers = apiSuppliers.map(s => ({ id: `s-${s.id}`, apiId: s.id, name: s.name, ingredient: inventoryById[s.ingredient_id]?.name || `Ingredient ${s.ingredient_id}`, pricePerUnit: Number(s.price_per_unit), unit: inventoryById[s.ingredient_id]?.unit || '', leadTimeDays: s.lead_time_days, qualityScore: Number(s.quality_score), reliability: Number(s.reliability) }));
  window.purchases = apiPurchases.map(p => ({ id: p.order_number, date: p.ordered_on, ingredient: inventoryById[p.ingredient_id]?.name || `Ingredient ${p.ingredient_id}`, supplier: `Supplier ${p.supplier_id}`, quantity: Number(p.quantity), unit: '', totalCost: Number(p.quantity) * Number(p.unit_price) }));
})();
