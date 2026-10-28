/* kg.js — 「關係圖譜」頁：按實體瀏覽知識圖譜裏的關係與屬性
 * 進頁顯示類型總覽；搜尋／篩選選中一個實體後，展示它的關係網（出邊入邊按關係類型分組）
 * 與屬性（按 predicate 分組）。實體間跳轉用 pushState，不重載整頁。
 */

/* 關係類型的大白話翻譯與一句話說明 */
const KG_REL_NAMES = {
  rises_at: '發源於', flows_into: '流入', produces: '出產', inhabits: '棲息於',
  worships: '祭祀', located_in: '位於', connected_to: '與……相連', adjacent_to: '與……相鄰',
  same_entity_as: '是同一個', reused_from_shanjing: '沿用山經定位', motif_of: '同一傳說母題',
  genealogy: '譜系', anchored_to: '依附於', related_to: '相關', same_as: '等同',
  invented_by: '始創',
};
const KG_REL_DESC = {
  rises_at: '河水從哪座山發源',
  flows_into: '河水最後流進哪裏',
  produces: '這座山、這片水域出產什麼',
  inhabits: '什麼人、什麼動物住在這裏',
  worships: '祭祀哪座山、哪位神',
  located_in: '位於哪個地方之內',
  connected_to: '兩地山水相連',
  adjacent_to: '兩地緊挨着',
  same_entity_as: '不同名字其實是同一個',
  reused_from_shanjing: '海經沿用《山經》的定位',
  motif_of: '屬於同一個傳說母題',
  genealogy: '譜系上的承繼關係',
  anchored_to: '定位上依附於某座山某條河',
  related_to: '有其他關聯',
  same_as: '認定等同',
  invented_by: '傳說中由誰始創',
};
const KG_LAYER_NAMES = { textual: '原文所述', interpretive: '研究推斷' };

async function bootKg() {
  const main = document.getElementById('kg-main');
  main.innerHTML = '<p class="notice">正在載入關係圖譜（資料較大，請稍候）…</p>';
  let g;
  try { g = await Store.graph(); }
  catch (err) { main.innerHTML = `<p class="notice">載入失敗：${App.esc(err.message)}</p>`; return; }

  const nodes = g.nodes;
  const byId = Object.fromEntries(nodes.map(n => [n.id, n]));

  /* 出邊／入邊索引與度數（關係多的排前面，方便挑有意思的看） */
  const outEdges = {}, inEdges = {};
  g.edges.forEach(e => {
    (outEdges[e.src] = outEdges[e.src] || []).push(e);
    (inEdges[e.dst] = inEdges[e.dst] || []).push(e);
  });
  const degree = id => (outEdges[id] || []).length + (inEdges[id] || []).length;

  const typeCounts = {};
  nodes.forEach(n => { typeCounts[n.type] = (typeCounts[n.type] || 0) + 1; });
  const relCounts = {};
  g.edges.forEach(e => { relCounts[e.type] = (relCounts[e.type] || 0) + 1; });

  const state = { q: '', type: '', book: '' };

  main.innerHTML = `
    <h1>關係圖譜</h1>
    <p class="muted">這一頁看的是事物之間的關係：哪條河發源於哪座山、哪座山出產什麼、誰住在哪裏……
    共 ${nodes.length.toLocaleString()} 個事物、${g.edges.length.toLocaleString()} 條關係。
    先用搜尋或篩選挑一個事物，就能看到它的關係網和全部屬性。</p>
    <div class="kg-controls">
      <input id="kg-search" class="search-box" type="search"
        placeholder="搜尋事物名稱（按 / 快速聚焦）——試試「赤水」「九尾狐」「女媧」">
      <select id="kg-type" aria-label="按類別篩選">
        <option value="">全部類別</option>
        ${Object.keys(App.TYPE_NAMES).filter(t => typeCounts[t]).map(t =>
          `<option value="${t}">${App.TYPE_NAMES[t]}（${typeCounts[t]}）</option>`).join('')}
      </select>
      <select id="kg-book" aria-label="按卷篩選">
        <option value="">全部卷</option>
        ${Object.keys(App.BOOKS).sort().map(no =>
          `<option value="${no}">卷${no} · ${App.BOOKS[no].name}</option>`).join('')}
      </select>
    </div>
    <div id="kg-body"></div>`;

  const body = document.getElementById('kg-body');
  const search = document.getElementById('kg-search');
  const typeSel = document.getElementById('kg-type');
  const bookSel = document.getElementById('kg-book');

  /* ── 工具 ─────────────────────────────── */
  function entrySource(entryId) {
    const parts = String(entryId || '').split('-');
    const b = App.BOOKS[parts[1]];
    if (!b) return { label: entryId || '', book: parts[1] || '', anchor: entryId || '' };
    const sub = +parts[2], idx = parseInt(parts[3], 10);
    return {
      label: `《${b.name}》· ${App.subName(parts[1], sub)}第 ${idx} 段`,
      book: parts[1], anchor: entryId,
    };
  }
  function readingOf(n) {
    const a = n.attrs.find(x => x.predicate === 'era.candidate');
    if (!a) return '';
    const v = a.value;
    return typeof v === 'string' ? v : (v.name || '');
  }
  function relName(t) { return KG_REL_NAMES[t] || t; }
  function layerBadge(layer) {
    const label = KG_LAYER_NAMES[layer];
    if (!label) return '';
    return `<span class="badge ${layer === 'textual' ? 'anchor' : 'review'}">${label}</span>`;
  }
  function nodeLink(id) {
    const n = byId[id];
    if (!n) return `<span class="mono">${App.esc(id)}</span>`;
    return `<a href="kg.html?id=${encodeURIComponent(id)}">${App.esc(n.name)}</a>` +
      ` <span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>`;
  }

  /* 屬性值渲染：字串直接顯示；物件按鍵逐行（白話字段名）；
   * era.candidate 若帶 primary/rival 鍵，主讀法與其他讀法分開展示 */
  const ROLE_NAMES = {
    primary: '主讀法', rival: '其他讀法', identification: '身份認定',
    framework_reference: '框架參照', initialization: '初始記錄',
  };
  function valHtml(v, skipKeys) {
    if (v == null) return '<span class="muted">（沒有記錄）</span>';
    if (typeof v === 'string') return App.esc(v);
    if (typeof v === 'number' || typeof v === 'boolean') return App.esc(String(v));
    if (Array.isArray(v)) {
      if (!v.length) return '<span class="muted">（無）</span>';
      return '<ul class="kv-list">' + v.map(x => '<li>' + valHtml(x) + '</li>').join('') + '</ul>';
    }
    return Object.entries(v)
      .filter(([k]) => !skipKeys || !skipKeys.includes(k))
      .map(([k, val]) => {
        const shown = k === 'role' && typeof val === 'string' && ROLE_NAMES[val] ? ROLE_NAMES[val] : val;
        return `<div class="kv"><b>${App.esc(App.ATTR_KEY_NAMES[k] || k)}：</b>${valHtml(shown)}</div>`;
      }).join('');
  }
  function eraCandidateHtml(v) {
    if (v && typeof v === 'object' && !Array.isArray(v) && (v.primary || v.rival)) {
      let h = `<div class="kv"><b>主讀法：</b>${valHtml(v.primary)}</div>`;
      if (v.rival) h += `<div class="kv"><b>其他讀法：</b>${valHtml(v.rival)}</div>`;
      Object.entries(v).forEach(([k, val]) => {
        if (k === 'primary' || k === 'rival') return;
        h += `<div class="kv"><b>${App.esc(App.ATTR_KEY_NAMES[k] || k)}：</b>${valHtml(val)}</div>`;
      });
      return h;
    }
    return valHtml(v, ['primary', 'rival'].includes(v.role) ? ['role'] : null);
  }
  function attrValueHtml(a) {
    return a.predicate === 'era.candidate' ? eraCandidateHtml(a.value) : valHtml(a.value);
  }
  function attrCardHtml(a) {
    return `<div class="kg-attr">
      <div class="kg-attr-meta">${App.confBadge(a.confidence)}
        <span class="badge">${App.esc(App.KIND_NAMES[a.kind] || a.kind)}</span></div>
      <div>${attrValueHtml(a)}</div>
    </div>`;
  }
  /* era.candidate 組內再按 role 分：主讀法／其他讀法／其餘 */
  function eraCandidateGroupHtml(attrs) {
    const prim = attrs.filter(a => a.value && a.value.role === 'primary');
    const riv = attrs.filter(a => a.value && a.value.role === 'rival');
    const rest = attrs.filter(a => !prim.includes(a) && !riv.includes(a));
    let h = '';
    if (prim.length) h += `<h5 class="kg-role-head">主讀法（${prim.length}）</h5>` + prim.map(attrCardHtml).join('');
    if (riv.length) h += `<h5 class="kg-role-head">其他讀法（${riv.length}）</h5>` + riv.map(attrCardHtml).join('');
    if (rest.length) {
      h += (prim.length || riv.length ? `<h5 class="kg-role-head">其他記錄（${rest.length}）</h5>` : '') +
        rest.map(attrCardHtml).join('');
    }
    return h;
  }

  /* ── 類型總覽（進頁默認）────────────────── */
  function renderOverview() {
    body.innerHTML = `
      <h2 class="sub-head">各類事物統計</h2>
      <div class="kg-stats">` +
      Object.keys(App.TYPE_NAMES).filter(t => typeCounts[t]).map(t => `
        <div class="kg-stat" data-pick-type="${t}" tabindex="0" role="button">
          <div class="num">${typeCounts[t].toLocaleString()}</div>
          <div class="lbl">${App.TYPE_NAMES[t]}</div>
        </div>`).join('') + `</div>
      <h2 class="sub-head">各種關係統計</h2>
      <table class="attr-table"><thead><tr><th>關係</th><th>意思</th><th>條數</th></tr></thead><tbody>` +
      Object.keys(KG_REL_NAMES).filter(t => relCounts[t]).sort((a, b) => relCounts[b] - relCounts[a]).map(t =>
        `<tr><td><strong>${relName(t)}</strong></td><td>${App.esc(KG_REL_DESC[t] || '')}</td>
         <td>${relCounts[t].toLocaleString()}</td></tr>`).join('') +
      `</tbody></table>
      <p class="muted">點上方類別方塊，或用搜尋框，挑一個事物開始看它的關係網。</p>`;
    body.querySelectorAll('[data-pick-type]').forEach(el => {
      const pick = () => {
        state.type = el.dataset.pickType;
        typeSel.value = state.type;
        renderList();
      };
      el.addEventListener('click', pick);
      el.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); pick(); } });
    });
  }

  /* ── 搜尋／篩選結果列表（分頁式：最多 60 項）── */
  function match(n) {
    if (state.type && n.type !== state.type) return false;
    if (state.book && String(n.entry).split('-')[1] !== state.book) return false;
    if (!state.q) return true;
    const q = state.q.toLowerCase();
    if (n.name.toLowerCase().includes(q)) return true;
    return readingOf(n).toLowerCase().includes(q);
  }
  function renderList() {
    const filtering = state.q || state.type || state.book;
    if (!filtering) { renderOverview(); return; }
    const hits = nodes.filter(match).sort((a, b) => degree(b.id) - degree(a.id));
    const cap = 60;
    body.innerHTML =
      `<p class="muted">共 ${hits.length} 項（按關係多少排序）${hits.length > cap ? `，只顯示前 ${cap} 項，請再縮小範圍` : ''}。</p>` +
      hits.slice(0, cap).map(n => {
        const src = entrySource(n.entry);
        return `<div class="entity-row">
          <a class="nm" href="kg.html?id=${encodeURIComponent(n.id)}">${App.esc(n.name)}</a>
          <span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
          <span class="badge region">關係 ${degree(n.id)} 條</span>
          <span class="rd">${App.esc(readingOf(n)).slice(0, 80)}</span>
          <a href="book.html?book=${src.book}#${App.esc(src.anchor)}">${App.esc(App.BOOKS[src.book] ? `《${App.BOOKS[src.book].name}》` : src.label)}</a>
        </div>`;
      }).join('');
  }

  /* ── 單個實體：關係網＋屬性 ─────────────── */
  function edgeLine(e, out) {
    const otherId = out ? e.dst : e.src;
    const src = entrySource(e.entry);
    const srcLink = src.book && App.BOOKS[src.book]
      ? `<a href="book.html?book=${src.book}#${App.esc(src.anchor)}">${App.esc(src.label)}</a>`
      : App.esc(src.label);
    return `<li>${out ? '→' : '←'} ${nodeLink(otherId)}
      ${e.bearing ? `<span class="muted">（方位：${App.esc(e.bearing)}）</span>` : ''}
      ${layerBadge(e.layer)}
      <span class="muted">出自 ${srcLink}</span></li>`;
  }
  function relGroupHtml(title, edges, out) {
    const groups = {};
    edges.forEach(e => { (groups[e.type] = groups[e.type] || []).push(e); });
    const types = Object.keys(groups).sort((a, b) => groups[b].length - groups[a].length);
    return `<h2 class="sub-head">${title}（共 ${edges.length} 條）</h2>` +
      (edges.length ? types.map(t => `
        <div class="kg-rel-group"><h4>${relName(t)}（${groups[t].length}）</h4>
        <ul>${groups[t].map(e => edgeLine(e, out)).join('')}</ul></div>`).join('')
      : '<p class="muted">（沒有）</p>');
  }
  function renderEntity(id) {
    const n = byId[id];
    if (!n) {
      body.innerHTML = `<p class="notice">找不到這個事物，它可能已被更名或合併。</p>`;
      return;
    }
    const src = entrySource(n.entry);
    const out = outEdges[id] || [], inc = inEdges[id] || [];

    let h = `<p><a href="kg.html" class="kg-back">← 返回關係圖譜總覽</a></p>
      <h1>${App.esc(n.name)}</h1>
      <p><span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
      <span class="badge ${n.status === 'active' ? 'ok' : 'pending'}">${n.status === 'active' ? '位置較有把握' : '位置待定'}</span></p>
      <p>出處：${src.book && App.BOOKS[src.book]
        ? `<a href="book.html?book=${src.book}#${App.esc(src.anchor)}">${App.esc(src.label)}</a>`
        : App.esc(src.label)}
      　·　<a href="entity.html?id=${encodeURIComponent(id)}">看它的古今對應詳情 →</a></p>`;

    h += relGroupHtml('它指向別的事物', out, true);
    h += relGroupHtml('別的事物指向它', inc, false);

    /* 屬性按 predicate 分組 */
    const byPred = {};
    n.attrs.forEach(a => { (byPred[a.predicate] = byPred[a.predicate] || []).push(a); });
    const preds = Object.keys(byPred).sort((a, b) => byPred[b].length - byPred[a].length);
    h += `<h2 class="sub-head">屬性（共 ${n.attrs.length} 項，按類別分組）</h2>` +
      (preds.length ? preds.map(p => `
        <div class="kg-rel-group"><h4>${App.esc(App.PREDICATE_NAMES[p] || p)}（${byPred[p].length}）</h4>` +
        (p === 'era.candidate' ? eraCandidateGroupHtml(byPred[p]) : byPred[p].map(attrCardHtml).join('')) +
        '</div>').join('')
      : '<p class="muted">（沒有屬性記錄）</p>');

    body.innerHTML = h;
  }

  /* ── 路由與跳轉 ────────────────────────── */
  function route() {
    const id = new URLSearchParams(location.search).get('id');
    if (id) renderEntity(id);
    else renderList();
  }
  main.addEventListener('click', ev => {
    const a = ev.target.closest && ev.target.closest('a[href^="kg.html"]');
    if (!a) return;
    ev.preventDefault();
    history.pushState(null, '', a.getAttribute('href'));
    route();
    window.scrollTo(0, 0);
  });
  window.addEventListener('popstate', route);

  function leaveEntity() {
    if (new URLSearchParams(location.search).get('id')) history.pushState(null, '', 'kg.html');
  }
  search.addEventListener('input', () => {
    state.q = search.value.trim();
    leaveEntity();
    renderList();
  });
  typeSel.addEventListener('change', () => { state.type = typeSel.value; leaveEntity(); renderList(); });
  bookSel.addEventListener('change', () => { state.book = bookSel.value; leaveEntity(); renderList(); });
  document.addEventListener('keydown', ev => {
    if (ev.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) {
      ev.preventDefault(); search.focus();
    }
  });

  route();
}
