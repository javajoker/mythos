/* app.js — 共享 UI（頁首/頁腳、markdown 渲染、詳情卡、徽章）＋ 各頁 boot */
const App = (() => {

  /* ── 卷次元數據 ─────────────────────────── */
  const FAMILY = {
    west:   { name: '西', color: '#6c3483' },
    center: { name: '中', color: '#c0392b' },
    north:  { name: '北', color: '#a07d1e' },
    east:   { name: '東', color: '#1e8449' },
    south:  { name: '南', color: '#2e86c1' },
  };
  const BOOKS = {
    '01': { name: '南山經',   fam: 'south',  maps: ['nanshan-overview.svg', 'nanci1-map.svg', 'nanci2-map.svg', 'nanci3-map.svg'] },
    '02': { name: '西山經',   fam: 'west',   maps: ['xishan-overview.svg', 'xici1-map.svg', 'xici2-map.svg', 'xici3-map.svg', 'xici4-map.svg'] },
    '03': { name: '北山經',   fam: 'north',  maps: ['beishan-overview.svg', 'beici1-map.svg', 'beici2-map.svg', 'beici3-map.svg'] },
    '04': { name: '東山經',   fam: 'east',   maps: ['dongshan-overview.svg', 'dongci1-map.svg', 'dongci2-map.svg', 'dongci3-map.svg', 'dongci4-map.svg'] },
    '05': { name: '中山經',   fam: 'center', maps: ['zhongshan-overview.svg', 'wuzang-overview.svg',
            'zhongci1-map.svg', 'zhongci2-map.svg', 'zhongci3-map.svg', 'zhongci4-map.svg', 'zhongci5-map.svg', 'zhongci6-map.svg',
            'zhongci7-map.svg', 'zhongci8-map.svg', 'zhongci9-map.svg', 'zhongci10-map.svg', 'zhongci11-map.svg', 'zhongci12-map.svg'] },
    '06': { name: '海外南經', fam: null, maps: ['book06-map.svg'] },
    '07': { name: '海外西經', fam: null, maps: ['book07-map.svg'] },
    '08': { name: '海外北經', fam: null, maps: ['book08-map.svg'] },
    '09': { name: '海外東經', fam: null, maps: ['book09-map.svg'] },
    '10': { name: '海內南經', fam: null, maps: ['book10-map.svg'] },
    '11': { name: '海內西經', fam: null, maps: ['book11-map.svg'] },
    '12': { name: '海內北經', fam: null, maps: ['book12-map.svg'] },
    '13': { name: '海內東經', fam: null, maps: ['book13-map.svg'] },
    '14': { name: '大荒東經', fam: null, maps: ['book14-map.svg'] },
    '15': { name: '大荒南經', fam: null, maps: ['book15-map.svg'] },
    '16': { name: '大荒西經', fam: null, maps: ['book16-map.svg'] },
    '17': { name: '大荒北經', fam: null, maps: ['book17-map.svg'] },
    '18': { name: '海內經',   fam: null, maps: ['book18-map.svg'] },
  };
  const CN = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三'];
  const SHAN_PREFIX = { '01': '南', '02': '西', '03': '北', '04': '東', '05': '中' };
  function subName(book, sub) {
    if (SHAN_PREFIX[book]) {
      if (book === '05' && sub === 13) return '卷末總結（禹曰）';
      return sub === 1 ? SHAN_PREFIX[book] + '山經之首' : SHAN_PREFIX[book] + '次' + CN[sub] + '經';
    }
    return '全卷';
  }

  const TYPE_NAMES = {
    MTN: '山體', WAT: '水體', LND: '地標', POL: '族群／邦國', PER: '人物／神格',
    CRE: '動物', PLA: '植物', MIN: '礦物／資源', OBJ: '物件', AST: '天象',
    CLIM: '氣象／兆象', DOC: '文獻',
  };
  const EDGE_NAMES = {
    rises_at: '發源於', flows_into: '注於', connected_to: '相連', adjacent_to: '相鄰',
    located_in: '位於', related_to: '關聯', motif_of: '母題', produces: '出產',
    inhabits: '棲息', same_entity_as: '同一實體', invented_by: '始創',
  };
  const ATTR_KEY_NAMES = {
    role: '角色', name: '候選', fit: '契合', entity_attr: '屬性', station_ref: '站點',
    region: '區域', kind: '類別', conflicts: '衝突', unknowns: '未知', modern_name: '現代名',
    period_state: '時代狀態', present_state: '現今狀態', evolution_logic: '演化邏輯',
    disposition: '處置', original_kind: '原類別', anchor: '錨', candidate: '候選',
    coordinates: '坐標', symbolism: '賦義', trigger: '觸發原文', reading: '讀法',
    status: '狀態', book: '卷', entry: '條目', components: '組成', historical_scenarios: '歷史情景',
    static_fit: '靜態契合', grid_0385: '網格',
  };

  /* ── 工具 ──────────────────────────────── */
  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function confBadge(c) {
    switch (c) {
      case 'high': case 'high_within_hypothesis':
        return '<span class="badge good">很可靠</span>';
      case 'medium': case 'medium_high': case 'low_medium':
        return '<span class="badge ok">較可靠</span>';
      case 'low': case 'very_low': case 'framework':
        return '<span class="badge dir">方向性</span>';
      case 'myth_layer':
        return '<span class="badge myth">神話層</span>';
      default:
        return '<span class="badge na">待考</span>';
    }
  }
  function pointStatusBadge(status) {
    if (status === 'mapped') return '<span class="badge anchor">復用錨定</span>';
    if (status === 'region') return '<span class="badge region">區域方向</span>';
    return '<span class="badge pending">待定錨</span>';
  }

  /* ── 迷你 markdown 渲染（僅支持本地數據用到的語法）──── */
  function rewriteUrl(url) {
    // 導出數據中的地圖引用指向源倉庫路徑；webapp 內統一落在 maps/
    return url.replace(/^(\.\.\/)*data\/derived\/era\/adaptation\//, 'maps/');
  }
  function mdInline(s) {
    let h = esc(s);
    h = h.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, (m, alt, src) =>
      `<img loading="lazy" src="${esc(rewriteUrl(src))}" alt="${alt}">`);
    h = h.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, t, url) =>
      `<a href="${esc(rewriteUrl(url))}" target="_blank" rel="noopener">${t}</a>`);
    h = h.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    h = h.replace(/`([^`]+)`/g, '<code>$1</code>');
    return h;
  }
  function md(src) {
    const lines = String(src || '').replace(/\r/g, '').split('\n');
    const out = [];
    let i = 0;
    const para = [];
    const flushPara = () => {
      if (para.length) { out.push('<p>' + para.map(mdInline).join('<br>') + '</p>'); para.length = 0; }
    };
    while (i < lines.length) {
      const ln = lines[i];
      if (/^\s*$/.test(ln)) { flushPara(); i++; continue; }
      let m;
      if ((m = ln.match(/^(#{1,6})\s+(.*)/))) {
        flushPara();
        out.push(`<h${m[1].length}>${mdInline(m[2])}</h${m[1].length}>`); i++; continue;
      }
      if (/^---+\s*$/.test(ln)) { flushPara(); out.push('<hr>'); i++; continue;
      }
      if (/^>\s?/.test(ln)) {
        flushPara();
        const q = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) { q.push(lines[i].replace(/^>\s?/, '')); i++; }
        out.push('<blockquote>' + q.map(mdInline).join('<br>') + '</blockquote>'); continue;
      }
      if (/^[-*]\s+/.test(ln)) {
        flushPara();
        const items = [];
        while (i < lines.length && /^[-*]\s+/.test(lines[i])) { items.push(lines[i].replace(/^[-*]\s+/, '')); i++; }
        out.push('<ul>' + items.map(t => '<li>' + mdInline(t) + '</li>').join('') + '</ul>'); continue;
      }
      if (/^\d+\.\s+/.test(ln)) {
        flushPara();
        const items = [];
        while (i < lines.length && /^\d+\.\s+/.test(lines[i])) { items.push(lines[i].replace(/^\d+\.\s+/, '')); i++; }
        out.push('<ol>' + items.map(t => '<li>' + mdInline(t) + '</li>').join('') + '</ol>'); continue;
      }
      if (/^\|/.test(ln) && i + 1 < lines.length && /^\|[\s:|-]+\|/.test(lines[i + 1])) {
        flushPara();
        const rows = [ln];
        i += 2;
        while (i < lines.length && /^\|/.test(lines[i])) { rows.push(lines[i]); i++; }
        const cell = r => r.replace(/^\||\|$/g, '').split('|').map(c => c.trim());
        const head = cell(rows[0]);
        out.push('<table><thead><tr>' + head.map(c => '<th>' + mdInline(c) + '</th>').join('') + '</tr></thead><tbody>' +
          rows.slice(1).map(r => '<tr>' + cell(r).map(c => '<td>' + mdInline(c) + '</td>').join('') + '</tr>').join('') +
          '</tbody></table>');
        continue;
      }
      para.push(ln); i++;
    }
    flushPara();
    return out.join('\n');
  }

  /* ── 條目詳情卡 ─────────────────────────── */
  function entryCard(e) {
    const b = BOOKS[e.book] || { name: e.book };
    let h = `<h3>${esc(e.title)}</h3>
      <div class="detail-meta"><span class="mono">${esc(e.id)}</span> ·
      <a href="book.html?book=${e.book}#${esc(e.id)}">${esc(b.name)}</a>
      <span class="badge review">競爭假說 proposed_pending_review</span></div>`;
    if (/借名/.test(e.reading_md)) {
      h += `<div class="borrowed-warning">借名警示：本條目涉及後世同名／借名討論——後世地名沿襲不得反推為定位證據。</div>`;
    }
    if (/神話層|神话层/.test(e.reading_md)) {
      h += `<div class="myth-note">本條目涉及神話層內容，與地理層分開呈現，不作現實定位。</div>`;
    }
    h += `<div class="entry-body">${md(e.reading_md)}</div>`;
    if (e.unresolved && e.unresolved.length) {
      h += `<details class="unresolved"><summary>未決 ${e.unresolved.length} 項</summary><ul>` +
        e.unresolved.map(u => '<li>' + esc(u) + '</li>').join('') + '</ul></details>';
    }
    return h;
  }
  function pointCard(p, entry) {
    let h = `<h3>${esc(p.name)}</h3>
      <div class="detail-meta">${pointStatusBadge(p.status)}</div>`;
    if (entry) return h + entryCardBody(entry);
    h += `<p>${esc(p.note || '')}</p><p class="muted">此點位暫未關聯條目；狀態見上方徽章（待定錨／區域方向均為方向性假說）。</p>`;
    return h;
  }
  function entryCardBody(e) {
    // 供 pointCard 複用：去掉重複標題
    const div = document.createElement('div');
    div.innerHTML = entryCard(e);
    div.querySelector('h3').remove();
    return div.innerHTML;
  }

  /* ── 詳情側欄 ──────────────────────────── */
  let cardEl = null;
  function openDetail(html) {
    if (!cardEl) {
      cardEl = document.createElement('aside');
      cardEl.className = 'detail-card';
      cardEl.setAttribute('role', 'dialog');
      document.body.appendChild(cardEl);
    }
    cardEl.innerHTML = '<button class="detail-close" aria-label="關閉">關閉 ✕</button>' + html;
    cardEl.querySelector('.detail-close').onclick = closeDetail;
    cardEl.scrollTop = 0;
    cardEl.classList.add('open');
  }
  function closeDetail() { if (cardEl) cardEl.classList.remove('open'); }

  /* ── lightbox ──────────────────────────── */
  function lightbox(src, alt) {
    const lb = document.createElement('div');
    lb.className = 'lightbox';
    lb.innerHTML = `<img src="${esc(src)}" alt="${esc(alt || '')}"><div class="cap">${esc(alt || '')}</div>`;
    lb.onclick = () => lb.remove();
    document.addEventListener('keydown', function onk(ev) {
      if (ev.key === 'Escape') { lb.remove(); document.removeEventListener('keydown', onk); }
    });
    document.body.appendChild(lb);
  }
  document.addEventListener('click', e => {
    if (e.target.matches && e.target.matches('.entry-body img, .book-maps img')) {
      lightbox(e.target.getAttribute('src'), e.target.getAttribute('alt'));
    }
  });

  /* ── 頁首頁腳 ──────────────────────────── */
  function chrome(active) {
    const nav = [
      ['index.html', '世界地圖'], ['book.html', '卷目錄'], ['entities.html', '實體庫'],
      ['adjudications.html', '裁決與發現'], ['review.html', '覆核中心'], ['about.html', '關於'],
    ];
    const header = document.querySelector('.site-header');
    if (header) {
      header.innerHTML =
        `<div class="site-title"><a href="index.html">山海經現實映射</a><span class="sub">時代窗口 4000–1000 BCE</span></div>
         <nav class="site-nav">` +
        nav.map(([h, t]) => `<a href="${h}"${h === active ? ' class="active"' : ''}>${t}</a>`).join('') + '</nav>';
    }
    const footer = document.querySelector('.site-footer');
    if (footer) {
      footer.innerHTML =
        `<div class="honesty">全部對應為競爭假說（proposed_pending_review）；時代窗口 4000–1000 BCE</div>
         <div>《山海經》時代假想推理研究 · 純靜態站 · 無追蹤 · 離線可用</div>`;
    }
  }

  return {
    BOOKS, FAMILY, TYPE_NAMES, EDGE_NAMES, ATTR_KEY_NAMES, CN,
    esc, md, mdInline, confBadge, pointStatusBadge,
    entryCard, pointCard, openDetail, closeDetail, chrome, subName, lightbox,
  };
})();

/* ═══════════════ 頁面 boot ═══════════════ */

document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.page;
  App.chrome(page === 'index' ? 'index.html'
    : page === 'book' ? 'book.html'
    : page === 'entities' || page === 'entity' ? 'entities.html'
    : page === 'adjudications' ? 'adjudications.html'
    : page === 'review' ? 'review.html'
    : page === 'about' ? 'about.html' : '');
  if (page === 'index') bootIndex();
  else if (page === 'book') bootBook();
  else if (page === 'entities') bootEntities();
  else if (page === 'entity') bootEntity();
  else if (page === 'review') bootReview();
  else if (page === 'adjudications') bootAdjudications();
  else if (page === 'about') bootAbout();
});

/* ── 首頁：世界地圖 ─────────────────────── */
async function bootIndex() {
  const container = document.getElementById('map');
  const loading = document.createElement('div');
  loading.className = 'map-loading';
  loading.textContent = '地圖數據加載中…';
  container.appendChild(loading);

  let entries = null, byId = null;
  Store.entries().then(list => {
    entries = list;
    byId = Object.fromEntries(list.map(e => [e.id, e]));
  }).catch(err => console.error(err));

  function findStationEntry(book, sub, name) {
    if (!entries || !book || !sub) return null;
    const base = name.replace(/（[一二三四五六七八九十]+）$/, '');
    return entries.find(e =>
      e.book === book && +e.id.split('-')[2] === sub &&
      (e.title.includes(base) || e.original.includes(base))) || null;
  }

  function onSelect(sel) {
    if (sel.kind === 'station') {
      const e = findStationEntry(sel.book, sel.sub, sel.name);
      if (e) { App.openDetail(App.entryCard(e)); return; }
      App.openDetail(`<h3>${App.esc(sel.chain)}｜${App.esc(sel.name)}</h3>
        <div class="detail-meta">${sel.anchor ? '<span class="badge anchor">錨站</span>' : ''}
        <span class="badge review">競爭假說 proposed_pending_review</span></div>
        <p class="muted">山經里程鏈站點；未匹配到對應條目（可能為同名複站或里程點）。坐標為擬合值，全部定位均為競爭假說。</p>`);
    } else {
      const p = sel.point;
      const e = p.entry && byId ? byId[p.entry] : null;
      App.openDetail(App.pointCard(p, e));
    }
  }

  try {
    const map = await SHJMap.create(container, { onSelect });
    loading.remove();
    document.querySelectorAll('[data-layer]').forEach(cb => {
      cb.addEventListener('change', () => map.setLayer(cb.dataset.layer, cb.checked));
    });
    const resetBtn = document.getElementById('map-reset');
    if (resetBtn) resetBtn.onclick = () => map.reset();
  } catch (err) {
    loading.textContent = '地圖加載失敗：' + err.message;
  }
}

/* ── 卷頁 ──────────────────────────────── */
async function bootBook() {
  const main = document.getElementById('book-main');
  const q = new URLSearchParams(location.search);
  const bookNo = q.get('book');
  let entries;
  try { entries = await Store.entries(); }
  catch (err) { main.innerHTML = `<p class="notice">數據加載失敗：${App.esc(err.message)}</p>`; return; }

  if (!bookNo) { // 18 卷目錄
    const counts = {};
    entries.forEach(e => { counts[e.book] = (counts[e.book] || 0) + 1; });
    main.innerHTML = '<h1>卷目錄（18 卷）</h1><div class="book-grid">' +
      Object.keys(App.BOOKS).sort().map(no => {
        const b = App.BOOKS[no];
        const color = b.fam ? App.FAMILY[b.fam].color : '#7d6608';
        return `<div class="book-tile" style="border-top-color:${color}">
          <h3><a href="book.html?book=${no}">卷${no} · ${b.name}</a></h3>
          <div class="cnt">${counts[no] || 0} 條目${b.fam ? ' · 五藏山經（' + App.FAMILY[b.fam].name + '）' : ' · 框架書'}</div>
        </div>`;
      }).join('') + '</div>';
    return;
  }

  const b = App.BOOKS[bookNo];
  if (!b) { main.innerHTML = '<p class="notice">未知卷號。</p>'; return; }
  const list = entries.filter(e => e.book === bookNo);
  const subs = {};
  list.forEach(e => {
    const s = +e.id.split('-')[2];
    (subs[s] = subs[s] || []).push(e);
  });

  let h = `<h1>卷${bookNo} · ${b.name}</h1>
    <p class="muted">本卷 ${list.length} 條目 · <span class="badge review">全部為競爭假說 proposed_pending_review</span></p>`;

  // 卷導覽：子經/分組概覽
  h += '<h2 class="sub-head">本卷導覽</h2><ul>' +
    Object.keys(subs).sort((a, b) => a - b).map(s =>
      `<li><strong>${App.subName(bookNo, +s)}</strong>（${subs[s].length} 條）——首條：${App.esc(subs[s][0].title)}</li>`
    ).join('') + '</ul>';

  // 本卷地圖
  if (b.maps && b.maps.length) {
    h += '<h2 class="sub-head">本卷地圖</h2><div class="book-maps">' +
      b.maps.map(m => `<img loading="lazy" src="maps/${m}" alt="${b.name} 地圖 ${m}">`).join('') + '</div>';
  }

  // 條目列表
  h += '<h2 class="sub-head">條目</h2>';
  for (const s of Object.keys(subs).sort((x, y) => x - y)) {
    if (Object.keys(subs).length > 1) h += `<h3>${App.subName(bookNo, +s)}</h3>`;
    h += '<ul class="entry-list">' + subs[s].map(e => `
      <li id="${App.esc(e.id)}">
        <div class="entry-row" data-eid="${App.esc(e.id)}" tabindex="0">
          <span class="eid">${App.esc(e.id)}</span>
          <span>${App.esc(e.title)}</span>
          ${e.unresolved.length ? `<span class="cnt-badge">未決 ${e.unresolved.length}</span>` : ''}
        </div>
        <div class="entry-detail" hidden></div>
      </li>`).join('') + '</ul>';
  }
  main.innerHTML = h;

  const byId = Object.fromEntries(list.map(e => [e.id, e]));
  function toggle(row, open) {
    const li = row.closest('li');
    const det = li.querySelector('.entry-detail');
    const willOpen = open !== undefined ? open : det.hidden;
    if (willOpen && det.hidden) {
      det.innerHTML = App.entryCard(byId[row.dataset.eid]);
      det.hidden = false;
      if (open !== undefined) li.scrollIntoView({ block: 'start', behavior: 'smooth' });
    } else if (!willOpen) {
      det.hidden = true;
    }
  }
  main.querySelectorAll('.entry-row').forEach(row => {
    row.addEventListener('click', () => toggle(row));
    row.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); toggle(row); } });
  });
  // hash 定位
  if (location.hash) {
    const id = location.hash.slice(1);
    const row = main.querySelector(`[data-eid="${CSS.escape(id)}"]`);
    if (row) toggle(row, true);
  }
  // ←→ 同卷上/下條目
  document.addEventListener('keydown', ev => {
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return;
    if (/INPUT|TEXTAREA/.test(document.activeElement.tagName)) return;
    const rows = [...main.querySelectorAll('.entry-row')];
    const cur = rows.findIndex(r => !r.closest('li').querySelector('.entry-detail').hidden);
    const next = ev.key === 'ArrowRight' ? (cur < 0 ? 0 : Math.min(cur + 1, rows.length - 1))
                                         : (cur < 0 ? 0 : Math.max(cur - 1, 0));
    toggle(rows[next], true);
  });
}

/* ── 實體庫 ─────────────────────────────── */
async function bootEntities() {
  const main = document.getElementById('entities-main');
  main.innerHTML = '<p class="notice">實體庫加載中（graph.json 約 3.7 MB，僅本頁加載）…</p>';
  let g;
  try { g = await Store.graph(); }
  catch (err) { main.innerHTML = `<p class="notice">加載失敗：${App.esc(err.message)}</p>`; return; }

  const nodes = g.nodes;
  const counts = {};
  nodes.forEach(n => { counts[n.type] = (counts[n.type] || 0) + 1; });

  function readingOf(n) {
    const a = n.attrs.find(a => a.predicate === 'era.candidate');
    if (a) {
      const v = a.value;
      return { text: typeof v === 'string' ? v : (v.name || ''), conf: a.confidence };
    }
    return { text: '', conf: null };
  }

  const state = { type: null, q: '', mode: 'list' };

  main.innerHTML = `
    <h1>實體庫</h1>
    <p class="muted">KG 節點 ${nodes.length} 個 · 邊 ${g.edges.length} 條 · 屬性全部為 proposed（競爭假說）。</p>
    <div class="entities-layout">
      <div>
        <div class="type-tree">
          <strong>類型</strong>
          <ul>
            <li><a data-type="">全部（${nodes.length}）</a></li>
            ${Object.keys(App.TYPE_NAMES).filter(t => counts[t]).map(t =>
              `<li><a data-type="${t}">${App.TYPE_NAMES[t]}（${counts[t]}）</a></li>`).join('')}
          </ul>
          <strong>視圖</strong>
          <ul>
            <li><a data-mode="list">列表</a></li>
            <li><a data-mode="agg">類名聚合（同名多實例）</a></li>
          </ul>
        </div>
      </div>
      <div>
        <input id="entity-search" class="search-box" type="search"
          placeholder="搜索名稱／讀法（按 / 聚焦）——試試「赤水」「九尾狐」「鹽池」「極光」">
        <div id="entity-results"></div>
      </div>
    </div>`;

  const results = document.getElementById('entity-results');
  const search = document.getElementById('entity-search');

  function match(n) {
    if (state.type && n.type !== state.type) return false;
    if (!state.q) return true;
    const q = state.q.toLowerCase();
    if (n.name.toLowerCase().includes(q)) return true;
    return n.attrs.some(a => JSON.stringify(a.value).toLowerCase().includes(q));
  }

  function rowHtml(n) {
    const r = readingOf(n);
    return `<div class="entity-row">
      <a class="nm" href="entity.html?id=${encodeURIComponent(n.id)}">${App.esc(n.name)}</a>
      <span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
      ${App.confBadge(r.conf)}
      <span class="rd">${App.esc(r.text).slice(0, 90)}</span>
      <a class="mono" href="book.html?book=${n.entry.split('-')[1]}#${App.esc(n.entry)}">${App.esc(n.entry)}</a>
    </div>`;
  }

  function render() {
    if (state.mode === 'agg') { renderAgg(); return; }
    const hits = nodes.filter(match);
    const cap = 300;
    results.innerHTML =
      `<p class="muted">${hits.length} 個實體${hits.length > cap ? `（僅顯示前 ${cap}，請用搜索縮小範圍）` : ''}</p>` +
      hits.slice(0, cap).map(rowHtml).join('');
  }

  function renderAgg() {
    const groups = {};
    nodes.filter(match).forEach(n => { (groups[n.name] = groups[n.name] || []).push(n); });
    const multi = Object.entries(groups).filter(([, v]) => v.length > 1)
      .sort((a, b) => b[1].length - a[1].length);
    results.innerHTML =
      `<p class="muted">同名多實例類名 ${multi.length} 組——同一經名在不同時代/地域的多個現實候選實例聚合一頁（參見 ADJ-005 類名討論）。</p>` +
      multi.slice(0, 120).map(([name, inst]) => `
        <div class="agg-block"><h3>${App.esc(name)}（${inst.length} 實例）</h3>` +
        inst.map(n => {
          const r = readingOf(n);
          return `<div class="entity-row">
            <a class="mono" href="entity.html?id=${encodeURIComponent(n.id)}">${App.esc(n.id)}</a>
            <span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
            ${App.confBadge(r.conf)}
            <span class="rd">${App.esc(r.text).slice(0, 80)}</span>
            <a class="mono" href="book.html?book=${n.entry.split('-')[1]}#${App.esc(n.entry)}">${App.esc(n.entry)}</a>
          </div>`;
        }).join('') + '</div>').join('');
  }

  main.querySelectorAll('[data-type]').forEach(a => a.addEventListener('click', () => {
    state.type = a.dataset.type || null;
    main.querySelectorAll('[data-type]').forEach(x => x.classList.toggle('active', x === a));
    render();
  }));
  main.querySelectorAll('[data-mode]').forEach(a => a.addEventListener('click', () => {
    state.mode = a.dataset.mode;
    main.querySelectorAll('[data-mode]').forEach(x => x.classList.toggle('active', x === a));
    render();
  }));
  search.addEventListener('input', () => { state.q = search.value.trim(); render(); });
  document.addEventListener('keydown', ev => {
    if (ev.key === '/' && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) {
      ev.preventDefault(); search.focus();
    }
  });
  main.querySelector('[data-type=""]').classList.add('active');
  main.querySelector('[data-mode="list"]').classList.add('active');
  render();
}

/* ── 實體詳情 ───────────────────────────── */
/* ── 覆核中心 ──────────────────────────── */
async function bootReview() {
  const main = document.getElementById('review-main');
  const NAMES = { accepted: '採納', contested: '存疑', rejected: '否決' };
  function render() {
    const q = Object.values(Store.reviewQueue());
    main.innerHTML = `<h1>覆核中心</h1>
      <p class="muted">在實體頁對候選屬性點「採納／存疑／否決」後在此匯出覆核包（JSONL），
      放入倉庫後執行 <span class="mono">python3 tools/shj/apply_review.py &lt;文件&gt;</span> 回寫 KG（status: accepted/contested/rejected）。</p>
      <p>隊列中：<strong>${q.length}</strong> 條</p>
      ${q.length ? `<table class="attr-table"><thead><tr><th>屬性 ID</th><th>決定</th><th>日期</th></tr></thead><tbody>` +
        q.map(a => `<tr><td class="mono">${App.esc(a.attribute_id)}</td><td>${NAMES[a.decision] || a.decision}</td><td>${App.esc(a.date)}</td></tr>`).join('') +
        '</tbody></table>' : '<p class="muted">（空——到實體庫逐條覆核）</p>'}
      <p style="margin-top:14px">
        <button id="rev-export" class="rev-btn on" ${q.length ? '' : 'disabled'}>導出覆核包（review-actions.jsonl）</button>
        <button id="rev-clear" class="rev-btn" ${q.length ? '' : 'disabled'}>清空隊列</button></p>`;
    const ex = document.getElementById('rev-export');
    if (ex) ex.onclick = () => {
      const blob = new Blob([Store.reviewExport()], { type: 'application/jsonl' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'review-actions.jsonl';
      a.click();
    };
    const cl = document.getElementById('rev-clear');
    if (cl) cl.onclick = () => { Store.reviewClear(); render(); };
  }
  render();
}

async function bootEntity() {
  const main = document.getElementById('entity-main');
  const id = new URLSearchParams(location.search).get('id');
  if (!id) { main.innerHTML = '<p class="notice">缺少 id 參數。</p>'; return; }
  main.innerHTML = '<p class="notice">實體庫加載中（graph.json 約 3.7 MB）…</p>';
  let g;
  try { g = await Store.graph(); }
  catch (err) { main.innerHTML = `<p class="notice">加載失敗：${App.esc(err.message)}</p>`; return; }

  const byId = Object.fromEntries(g.nodes.map(n => [n.id, n]));
  const n = byId[id];
  if (!n) { main.innerHTML = `<p class="notice">未找到實體 <span class="mono">${App.esc(id)}</span>。</p>`; return; }

  const allText = JSON.stringify(n.attrs);
  const borrowed = allText.includes('借名');
  const myth = n.attrs.some(a => a.confidence === 'myth_layer') ||
    n.attrs.some(a => a.predicate === 'era.state' && /myth/.test(String(a.value)));

  let h = `<h1>${App.esc(n.name)}</h1>
    <p><span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
    <span class="mono">${App.esc(n.id)}</span>
    <span class="badge ${n.status === 'active' ? 'ok' : 'pending'}">${n.status === 'active' ? '已錨定' : '待定錨 pending_anchor'}</span>
    <span class="badge review">競爭假說 proposed_pending_review</span></p>
    <p>出處條目：<a href="book.html?book=${n.entry.split('-')[1]}#${App.esc(n.entry)}">${App.esc(n.entry)}（卷${n.entry.split('-')[1]}）</a></p>`;
  if (borrowed) {
    h += `<div class="borrowed-warning">借名警示：本實體的候選/賦義涉及後世同名或借名——後世沿襲不得反推為定位證據。</div>`;
  }
  if (myth) {
    h += `<div class="myth-note">神話層內容：與地理層分開呈現，不作現實定位。</div>`;
  }

  // 同名實例聚合
  const same = g.nodes.filter(x => x.name === n.name && x.id !== n.id);
  if (same.length) {
    h += `<h2 class="sub-head">同名類名實例（${same.length + 1}）</h2><ul>` +
      [n, ...same].map(x =>
        `<li><a href="entity.html?id=${encodeURIComponent(x.id)}" class="mono">${App.esc(x.id)}</a>
         （出處 <a href="book.html?book=${x.entry.split('-')[1]}#${App.esc(x.entry)}">${App.esc(x.entry)}</a>）</li>`
      ).join('') + '</ul>';
  }

  // 屬性表
  h += `<h2 class="sub-head">屬性（${n.attrs.length}）</h2>
    <table class="attr-table"><thead><tr><th>謂詞</th><th>值</th><th>類型</th><th>置信度</th><th>覆核</th></tr></thead><tbody>` +
    n.attrs.map(a => {
      let v;
      if (typeof a.value === 'string') v = App.esc(a.value);
      else v = Object.entries(a.value).map(([k, val]) =>
        `<div class="kv"><b>${App.esc(App.ATTR_KEY_NAMES[k] || k)}：</b>${App.esc(typeof val === 'string' ? val : JSON.stringify(val, null, 0))}</div>`).join('');
      const cur = (Store.reviewQueue()[a.id] || {}).decision || '';
      const btn = d => `<button class="rev-btn${cur === d ? ' on' : ''}" data-attr="${App.esc(a.id)}" data-dec="${d}">${{ accepted: '採納', contested: '存疑', rejected: '否決' }[d]}</button>`;
      return `<tr><td class="mono">${App.esc(a.predicate)}</td><td>${v}</td>
        <td>${App.esc(a.kind)}</td><td>${App.confBadge(a.confidence)}</td>
        <td class="rev-cell">${btn('accepted')}${btn('contested')}${btn('rejected')}</td></tr>`;
    }).join('') + '</tbody></table>';

  // 關係邊
  const rel = g.edges.filter(e => e.src === id || e.dst === id);
  if (rel.length) {
    h += `<h2 class="sub-head">關係（${rel.length}）</h2><ul>` +
      rel.map(e => {
        const out = e.src === id;
        const other = byId[out ? e.dst : e.src];
        const label = App.EDGE_NAMES[e.type] || e.type;
        const otherHtml = other
          ? `<a href="entity.html?id=${encodeURIComponent(other.id)}">${App.esc(other.name)}</a>`
          : `<span class="mono">${App.esc(out ? e.dst : e.src)}</span>`;
        return `<li>${out ? '→' : '←'} ${label} ${otherHtml}
          <span class="muted">（${e.layer}／${e.status} · 出處
          <a href="book.html?book=${e.entry.split('-')[1]}#${App.esc(e.entry)}">${App.esc(e.entry)}</a>）</span></li>`;
      }).join('') + '</ul>';
  }
  main.innerHTML = h;
  main.querySelectorAll('.rev-btn').forEach(b => b.addEventListener('click', () => {
    Store.reviewSet(b.dataset.attr, b.dataset.dec);
    main.querySelectorAll(`.rev-btn[data-attr="${b.dataset.attr}"]`).forEach(x => x.classList.toggle('on', x.dataset.dec === b.dataset.dec));
  }));
}

/* ── 裁決與發現 ─────────────────────────── */
async function bootAdjudications() {
  const main = document.getElementById('adj-main');
  let list;
  try { list = await Store.adjudications(); }
  catch (err) { main.innerHTML = `<p class="notice">加載失敗：${App.esc(err.message)}</p>`; return; }
  main.innerHTML = `<h1>裁決與發現（ADJ / F 系列）</h1>
    <p class="muted">共 ${list.length} 份。源文件位於倉庫 <span class="mono">projects/shanhaijing/findings/</span>（此處為內嵌全文渲染，可離線閱讀）。</p>` +
    list.map(a => `
      <details class="adj-item">
        <summary><strong>${App.esc(a.title)}</strong> <span class="file">${App.esc(a.file)}</span></summary>
        <div class="adj-body">${App.md(a.content || '')}</div>
      </details>`).join('');
}

/* ── 關於 ──────────────────────────────── */
async function bootAbout() {
  const el = document.getElementById('about-stats');
  if (!el) return;
  try {
    const m = await Store.manifest();
    el.innerHTML = `<ul>
      <li>KG 節點 ${m.graph.nodes.toLocaleString()} · 邊 ${m.graph.edges.toLocaleString()} · 屬性 ${m.graph.attributes.toLocaleString()}</li>
      <li>條目 ${m.entries.sections} · 地圖 ${m.maps} 張 · 實拍配圖 ${m.images} 張 · 裁決/發現 ${m.adjudications} 份</li>
    </ul>`;
  } catch (e) { el.textContent = ''; }
}
