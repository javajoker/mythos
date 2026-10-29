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
    MTN: '山', WAT: '河流與水域', LND: '地標', POL: '族群與邦國', PER: '人物與神靈',
    CRE: '動物', PLA: '植物', MIN: '礦物與資源', OBJ: '器物', AST: '天象',
    CLIM: '氣象與徵兆', DOC: '文獻',
  };
  const EDGE_NAMES = {
    rises_at: '發源於', flows_into: '流入', connected_to: '相連', adjacent_to: '相鄰',
    located_in: '位於', related_to: '相關', motif_of: '相關的故事母題', produces: '出產',
    inhabits: '棲息於', same_entity_as: '同一事物', invented_by: '始創',
  };
  const PREDICATE_NAMES = {
    'era.candidate': '對應的現實對象',
    'era.state': '古今狀態對照',
    'associative.symbolism': '象徵與聯想',
    'deductive.utility': '用途推斷',
  };
  const KIND_NAMES = {
    semantic_fit: '古今對應', associative: '聯想', deductive: '推斷',
  };
  const ATTR_KEY_NAMES = {
    role: '角色', name: '名稱', fit: '吻合之處', entity_attr: '屬性', station_ref: '路線站點',
    region: '所在區域', kind: '類別', conflicts: '不合之處', unknowns: '仍不清楚', modern_name: '今天的名字',
    period_state: '當時的狀態', present_state: '今天的狀態', evolution_logic: '演變過程',
    disposition: '處理方式', original_kind: '原本的類別', anchor: '定位點', candidate: '候選對象',
    coordinates: '坐標', symbolism: '象徵意義', trigger: '相關原文', reading: '解讀',
    status: '狀態', book: '卷', entry: '段落', components: '組成', historical_scenarios: '歷史情景',
    static_fit: '靜態吻合度', grid_0385: '推算網格',
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
        return '<span class="badge dir">大致方向</span>';
      case 'myth_layer':
        return '<span class="badge myth">神話故事</span>';
      default:
        return '<span class="badge na">還在研究</span>';
    }
  }
  function pointStatusBadge(status) {
    if (status === 'mapped') return '<span class="badge anchor">位置較有把握</span>';
    if (status === 'region') return '<span class="badge region">大致區域</span>';
    return '<span class="badge pending">位置待定</span>';
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
      <div class="detail-meta"><a href="book.html?book=${e.book}#${esc(e.id)}">出自《${esc(b.name)}》</a>
      <span class="badge review">研究假說 · 尚待覆核</span></div>`;
    if (/借名/.test(e.reading_md)) {
      h += `<div class="borrowed-warning">提醒：這一條涉及「借名」問題——後世沿用了同樣的地名，不能拿後來的同名地名反推古書裏的位置。</div>`;
    }
    if (/神話層|神话层/.test(e.reading_md)) {
      h += `<div class="myth-note">這一條屬於神話故事，與地理記錄分開呈現，不做現實定位。</div>`;
    }
    h += `<div class="entry-body">${md(e.reading_md)}</div>`;
    if (e.unresolved && e.unresolved.length) {
      h += `<details class="unresolved"><summary>還沒有答案的 ${e.unresolved.length} 個問題</summary><ul>` +
        e.unresolved.map(u => '<li>' + esc(u) + '</li>').join('') + '</ul></details>';
    }
    return h;
  }
  function pointCard(p, entry) {
    let h = `<h3>${esc(p.name)}</h3>
      <div class="detail-meta">${pointStatusBadge(p.status)}</div>`;
    if (entry) return h + entryCardBody(entry);
    h += `<p>${esc(p.note || '')}</p><p class="muted">這個地點暫時沒有對應到書中的具體段落；上方標籤表示把握程度，「位置待定」「大致區域」都只是初步推測。</p>`;
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
      ['index.html', '世界地圖'], ['book.html', '分卷閱讀'], ['entities.html', '收錄的事物'],
      ['kg.html', '關係圖譜'], ['timelapse.html', '時光地圖'],
      ['adjudications.html', '研究檔案'], ['review.html', '覆核工具（研究者用）'], ['about.html', '關於本站'],
    ];
    const header = document.querySelector('.site-header');
    if (header) {
      header.innerHTML =
        `<div class="site-title"><a href="index.html">山海經現實映射</a><span class="sub">約三四千年前的世界，對照到今天</span></div>
         <nav class="site-nav">` +
        nav.map(([h, t]) => `<a href="${h}"${h === active ? ' class="active"' : ''}>${t}</a>`).join('') + '</nav>';
    }
    const footer = document.querySelector('.site-footer');
    if (footer) {
      footer.innerHTML =
        `<div class="honesty">本站所有古今對應都是研究中的假說，不是定論；對照的年代大約在距今六千年到三千年之間</div>
         <div>《山海經》古今對照研究 · 純靜態站 · 無賬號、無追蹤 · 斷網也能用</div>`;
    }
  }

  return {
    BOOKS, FAMILY, TYPE_NAMES, EDGE_NAMES, ATTR_KEY_NAMES, PREDICATE_NAMES, KIND_NAMES, CN,
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
    : page === 'kg' ? 'kg.html'
    : page === 'timelapse' ? 'timelapse.html'
    : page === 'adjudications' ? 'adjudications.html'
    : page === 'review' ? 'review.html'
    : page === 'about' ? 'about.html' : '');
  if (page === 'index') bootIndex();
  else if (page === 'book') bootBook();
  else if (page === 'entities') bootEntities();
  else if (page === 'entity') bootEntity();
  else if (page === 'kg') bootKg();
  else if (page === 'timelapse') bootTimelapse();
  else if (page === 'review') bootReview();
  else if (page === 'adjudications') bootAdjudications();
  else if (page === 'about') bootAbout();
});

/* ── 首頁：世界地圖 ─────────────────────── */
async function bootIndex() {
  const container = document.getElementById('map');
  const loading = document.createElement('div');
  loading.className = 'map-loading';
  loading.textContent = '地圖資料載入中…';
  container.appendChild(loading);

  // 首次訪客引導條（看過就不再顯示）
  const hint = document.getElementById('map-hint');
  if (hint) {
    try { if (localStorage.getItem('shj-hint-seen')) hint.hidden = true; } catch {}
    hint.addEventListener('click', () => {
      hint.hidden = true;
      try { localStorage.setItem('shj-hint-seen', '1'); } catch {}
    });
  }

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
        <div class="detail-meta">${sel.anchor ? '<span class="badge anchor">關鍵站點</span>' : ''}
        <span class="badge review">研究假說 · 尚待覆核</span></div>
        <p class="muted">這是《山經》記山路線上的一個站點，沒有找到對應的書中段落（可能是重名站或純里程點）。地圖上的位置是推算出來的，所有定位都只是研究假說。</p>`);
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
    loading.textContent = '地圖載入失敗：' + err.message;
  }
}

/* ── 時光地圖：古今變遷 ─────────────────── */
async function bootTimelapse() {
  const container = document.getElementById('map');
  const loading = document.createElement('div');
  loading.className = 'map-loading';
  loading.textContent = '地圖資料載入中…';
  container.appendChild(loading);

  const slider = document.getElementById('tl-slider');
  const ticks = document.getElementById('tl-ticks');
  const desc = document.getElementById('tl-desc');

  function entryLink(entryId) {
    const m = String(entryId || '').match(/SHJ-(\d{2})-\d+-\d{3}/);
    if (!m) return '';
    const b = App.BOOKS[m[1]];
    if (!b) return '';
    return `<a href="book.html?book=${m[1]}#${App.esc(m[0])}">出自《${App.esc(b.name)}》</a>`;
  }

  function onSelect(sel) {
    if (sel.kind === 'water') {
      const f = sel.f;
      const PERIOD_STATE = {
        water: '仍是水體', marsh: '已縮成沼澤', shrunk: '大幅縮小但還在', gone: '今天已消失',
      };
      const rows = ['wet', 'book', 'now'].map(pid => {
        const p = { wet: '濕潤期', book: '成書時代', now: '今天' }[pid];
        const sh = f.shapes[pid] || {};
        return `<tr><td>${p}</td><td>${PERIOD_STATE[sh.state || 'water']}</td></tr>`;
      }).join('');
      App.openDetail(`<h3>${App.esc(f.name)}</h3>
        <div class="detail-meta">${entryLink(f.entry)}
        <span class="badge review">研究假說 · 尚待覆核</span></div>
        <p><strong>對應：</strong>${App.esc(f.reading)}</p>
        <table class="attr-table"><thead><tr><th>時期</th><th>狀態</th></tr></thead><tbody>${rows}</tbody></table>
        <p>${App.esc(f.note)}</p>`);
    } else {
      const s = sel.s;
      const nowTxt = s.now ? '今天仍有殘存（橙色範圍）' : '今天已在當地徹底消失';
      App.openDetail(`<h3>${App.esc(s.name)}</h3>
        <div class="detail-meta">${entryLink(s.entry)}
        <span class="badge review">研究假說 · 尚待覆核</span></div>
        <p><strong>分布變化：</strong>${nowTxt}</p>
        <p>${App.esc(s.note)}</p>`);
    }
  }

  let tlData = null;
  function showPeriod(id) {
    if (!tlData) return;
    const p = tlData.periods.find(x => x.id === id);
    if (p) desc.innerHTML = `<strong>${App.esc(p.label)}</strong>（${App.esc(p.span)}）——${App.esc(p.desc)}`;
    slider.value = tlData.periods.findIndex(x => x.id === id);
    ticks.querySelectorAll('.tl-tick').forEach(tk =>
      tk.classList.toggle('on', tlData.periods[+tk.dataset.i].id === id));
  }

  try {
    tlData = await Store.timelapse();
    const map = await SHJTimelapse.create(container, { onSelect, onPeriod: showPeriod });
    loading.remove();

    ticks.innerHTML = tlData.periods.map((p, i) =>
      `<span class="tl-tick" data-i="${i}">${App.esc(p.label)}</span>`).join('');
    ticks.querySelectorAll('.tl-tick').forEach(tk => {
      tk.addEventListener('click', () => map.setPeriod(tlData.periods[+tk.dataset.i].id));
    });
    slider.addEventListener('input', () => map.setPeriod(tlData.periods[+slider.value].id));

    document.querySelectorAll('[data-layer]').forEach(cb => {
      cb.addEventListener('change', () => map.setLayer(cb.dataset.layer, cb.checked));
    });
    const resetBtn = document.getElementById('map-reset');
    if (resetBtn) resetBtn.onclick = () => map.reset();
    showPeriod('book'); // 首期說明（onPeriod 建構期觸發時 tlData 尚未就緒，此處補一次）
  } catch (err) {
    loading.textContent = '地圖載入失敗：' + err.message;
  }
}

/* ── 卷頁 ──────────────────────────────── */
async function bootBook() {
  const main = document.getElementById('book-main');
  const q = new URLSearchParams(location.search);
  const bookNo = q.get('book');
  let entries;
  try { entries = await Store.entries(); }
  catch (err) { main.innerHTML = `<p class="notice">資料載入失敗：${App.esc(err.message)}</p>`; return; }

  if (!bookNo) { // 18 卷目錄
    const counts = {};
    entries.forEach(e => { counts[e.book] = (counts[e.book] || 0) + 1; });
    main.innerHTML = '<h1>分卷閱讀（共 18 卷）</h1><div class="book-grid">' +
      Object.keys(App.BOOKS).sort().map(no => {
        const b = App.BOOKS[no];
        const color = b.fam ? App.FAMILY[b.fam].color : '#7d6608';
        return `<div class="book-tile" style="border-top-color:${color}">
          <h3><a href="book.html?book=${no}">卷${no} · ${b.name}</a></h3>
          <div class="cnt">${counts[no] || 0} 段 · ${b.fam ? '「五藏山經」' : '海經與大荒經'}</div>
        </div>`;
      }).join('') + '</div>';
    return;
  }

  const b = App.BOOKS[bookNo];
  if (!b) { main.innerHTML = '<p class="notice">沒有這一卷。</p>'; return; }
  const list = entries.filter(e => e.book === bookNo);
  const subs = {};
  list.forEach(e => {
    const s = +e.id.split('-')[2];
    (subs[s] = subs[s] || []).push(e);
  });

  let h = `<h1>卷${bookNo} · ${b.name}</h1>
    <p class="muted">本卷共 ${list.length} 段 · <span class="badge review">以下古今對應均為研究假說</span></p>`;

  // 卷導覽：子經/分組概覽
  h += '<h2 class="sub-head">本卷分段</h2><ul>' +
    Object.keys(subs).sort((a, b) => a - b).map(s =>
      `<li><strong>${App.subName(bookNo, +s)}</strong>（${subs[s].length} 段）——第一段：${App.esc(subs[s][0].title)}</li>`
    ).join('') + '</ul>';

  // 本卷地圖
  if (b.maps && b.maps.length) {
    h += '<h2 class="sub-head">本卷地圖</h2><div class="book-maps">' +
      b.maps.map(m => `<img loading="lazy" src="maps/${m}" alt="${b.name} 地圖 ${m}">`).join('') + '</div>';
  }

  // 條目列表
  h += '<h2 class="sub-head">逐段閱讀</h2>';
  for (const s of Object.keys(subs).sort((x, y) => x - y)) {
    if (Object.keys(subs).length > 1) h += `<h3>${App.subName(bookNo, +s)}</h3>`;
    h += '<ul class="entry-list">' + subs[s].map((e, i) => `
      <li id="${App.esc(e.id)}">
        <div class="entry-row" data-eid="${App.esc(e.id)}" tabindex="0">
          <span class="eid">第${i + 1}段</span>
          <span>${App.esc(e.title)}</span>
          ${e.unresolved.length ? `<span class="cnt-badge">還有 ${e.unresolved.length} 個待解問題</span>` : ''}
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

/* ── 收錄的事物 ─────────────────────────── */
async function bootEntities() {
  const main = document.getElementById('entities-main');
  main.innerHTML = '<p class="notice">正在載入收錄的事物（資料較大，請稍候）…</p>';
  let g;
  try { g = await Store.graph(); }
  catch (err) { main.innerHTML = `<p class="notice">載入失敗：${App.esc(err.message)}</p>`; return; }

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

  function entrySource(entryId) {
    const parts = entryId.split('-');
    const b = App.BOOKS[parts[1]];
    return b ? `《${b.name}》` : entryId;
  }

  const state = { type: null, q: '', mode: 'list' };

  main.innerHTML = `
    <h1>收錄的事物</h1>
    <p class="muted">《山海經》裏提到的山、河、動植物、礦物、族群等，共 ${nodes.length} 項，另有 ${g.edges.length} 條相互關聯。每一項都標了我們認為它對應到今天什麼，以及有多大把握——全部還在研究之中。</p>
    <div class="entities-layout">
      <div>
        <div class="type-tree">
          <strong>按類別瀏覽</strong>
          <ul>
            <li><a data-type="">全部（${nodes.length}）</a></li>
            ${Object.keys(App.TYPE_NAMES).filter(t => counts[t]).map(t =>
              `<li><a data-type="${t}">${App.TYPE_NAMES[t]}（${counts[t]}）</a></li>`).join('')}
          </ul>
          <strong>瀏覽方式</strong>
          <ul>
            <li><a data-mode="list">逐條列出</a></li>
            <li><a data-mode="agg">同名事物歸併</a></li>
          </ul>
        </div>
      </div>
      <div>
        <input id="entity-search" class="search-box" type="search"
          placeholder="搜尋名稱或說明（按 / 快速聚焦）——試試「赤水」「九尾狐」「鹽池」「極光」">
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
      <a href="book.html?book=${n.entry.split('-')[1]}#${App.esc(n.entry)}">${App.esc(entrySource(n.entry))}</a>
    </div>`;
  }

  function render() {
    if (state.mode === 'agg') { renderAgg(); return; }
    const hits = nodes.filter(match);
    const cap = 300;
    results.innerHTML =
      `<p class="muted">共 ${hits.length} 項${hits.length > cap ? `（只顯示前 ${cap} 項，請用搜尋縮小範圍）` : ''}</p>` +
      hits.slice(0, cap).map(rowHtml).join('');
  }

  function renderAgg() {
    const groups = {};
    nodes.filter(match).forEach(n => { (groups[n.name] = groups[n.name] || []).push(n); });
    const multi = Object.entries(groups).filter(([, v]) => v.length > 1)
      .sort((a, b) => b[1].length - a[1].length);
    results.innerHTML =
      `<p class="muted">書中同樣的名字，在不同地方可能指不同的事物。這裏把同名的 ${multi.length} 組歸在一起，方便對照。</p>` +
      multi.slice(0, 120).map(([name, inst]) => `
        <div class="agg-block"><h3>${App.esc(name)}（共 ${inst.length} 處）</h3>` +
        inst.map(n => {
          const r = readingOf(n);
          return `<div class="entity-row">
            <a class="nm" href="entity.html?id=${encodeURIComponent(n.id)}">${App.esc(entrySource(n.entry))}</a>
            <span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
            ${App.confBadge(r.conf)}
            <span class="rd">${App.esc(r.text).slice(0, 80)}</span>
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

/* ── 事物詳情 ───────────────────────────── */
/* ── 覆核工具（研究者用）─────────────────── */
async function bootReview() {
  const main = document.getElementById('review-main');
  const NAMES = { accepted: '採納', contested: '存疑', rejected: '否決' };
  function render() {
    const q = Object.values(Store.reviewQueue());
    main.innerHTML = `<h1>覆核工具（研究者用）</h1>
      <p class="notice">這是給研究者使用的頁面，一般讀者可以略過。</p>
      <p class="muted">在實體頁對候選屬性點「採納／存疑／否決」後在此匯出覆核包（JSONL），
      放入倉庫後執行 <span class="mono">python3 tools/shj/apply_review.py &lt;文件&gt;</span> 回寫 KG（status: accepted/contested/rejected）。</p>
      <p>隊列中：<strong>${q.length}</strong> 條</p>
      ${q.length ? `<table class="attr-table"><thead><tr><th>屬性 ID</th><th>決定</th><th>日期</th></tr></thead><tbody>` +
        q.map(a => `<tr><td class="mono">${App.esc(a.attribute_id)}</td><td>${NAMES[a.decision] || a.decision}</td><td>${App.esc(a.date)}</td></tr>`).join('') +
        '</tbody></table>' : '<p class="muted">（空——到「收錄的事物」逐條覆核）</p>'}
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
  if (!id) { main.innerHTML = '<p class="notice">網址缺少 id 參數。</p>'; return; }
  main.innerHTML = '<p class="notice">正在載入收錄的事物（資料較大，請稍候）…</p>';
  let g;
  try { g = await Store.graph(); }
  catch (err) { main.innerHTML = `<p class="notice">載入失敗：${App.esc(err.message)}</p>`; return; }

  const byId = Object.fromEntries(g.nodes.map(n => [n.id, n]));
  const n = byId[id];
  if (!n) { main.innerHTML = '<p class="notice">找不到這個事物，它可能已被更名或合併。</p>'; return; }

  function entrySource(entryId) {
    const parts = entryId.split('-');
    const b = App.BOOKS[parts[1]];
    if (!b) return { label: entryId, book: parts[1], anchor: entryId };
    const sub = +parts[2], idx = parseInt(parts[3], 10);
    return {
      label: `《${b.name}》· ${App.subName(parts[1], sub)}第 ${idx} 段`,
      book: parts[1], anchor: entryId,
    };
  }

  const allText = JSON.stringify(n.attrs);
  const borrowed = allText.includes('借名');
  const myth = n.attrs.some(a => a.confidence === 'myth_layer') ||
    n.attrs.some(a => a.predicate === 'era.state' && /myth/.test(String(a.value)));

  const src = entrySource(n.entry);
  let h = `<h1>${App.esc(n.name)}</h1>
    <p><span class="badge">${App.TYPE_NAMES[n.type] || n.type}</span>
    <span class="badge ${n.status === 'active' ? 'ok' : 'pending'}">${n.status === 'active' ? '位置較有把握' : '位置待定'}</span>
    <span class="badge review">研究假說 · 尚待覆核</span></p>
    <p>出處：<a href="book.html?book=${src.book}#${App.esc(src.anchor)}">${App.esc(src.label)}</a></p>`;
  if (borrowed) {
    h += `<div class="borrowed-warning">提醒：這個事物的對應涉及「借名」問題——後世沿用了同樣的名字，不能拿後來的同名地名反推古書裏的位置。</div>`;
  }
  if (myth) {
    h += `<div class="myth-note">這個事物屬於神話故事，與地理記錄分開呈現，不做現實定位。</div>`;
  }

  // 同名實例聚合
  const same = g.nodes.filter(x => x.name === n.name && x.id !== n.id);
  if (same.length) {
    h += `<h2 class="sub-head">書中同名的事物（共 ${same.length + 1} 個）</h2><ul>` +
      [n, ...same].map(x => {
        const s = entrySource(x.entry);
        return `<li><a href="entity.html?id=${encodeURIComponent(x.id)}">${App.esc(s.label)}</a></li>`;
      }).join('') + '</ul>';
  }

  // 屬性表
  h += `<h2 class="sub-head">詳細屬性（${n.attrs.length} 項）</h2>
    <table class="attr-table"><thead><tr><th>項目</th><th>內容</th><th>性質</th><th>把握程度</th><th>覆核（研究者用）</th></tr></thead><tbody>` +
    n.attrs.map(a => {
      let v;
      if (typeof a.value === 'string') v = App.esc(a.value);
      else v = Object.entries(a.value).map(([k, val]) =>
        `<div class="kv"><b>${App.esc(App.ATTR_KEY_NAMES[k] || k)}：</b>${App.esc(typeof val === 'string' ? val : JSON.stringify(val, null, 0))}</div>`).join('');
      const cur = (Store.reviewQueue()[a.id] || {}).decision || '';
      const btn = d => `<button class="rev-btn${cur === d ? ' on' : ''}" data-attr="${App.esc(a.id)}" data-dec="${d}">${{ accepted: '採納', contested: '存疑', rejected: '否決' }[d]}</button>`;
      return `<tr><td>${App.esc(App.PREDICATE_NAMES[a.predicate] || a.predicate)}</td><td>${v}</td>
        <td>${App.esc(App.KIND_NAMES[a.kind] || a.kind)}</td><td>${App.confBadge(a.confidence)}</td>
        <td class="rev-cell">${btn('accepted')}${btn('contested')}${btn('rejected')}</td></tr>`;
    }).join('') + '</tbody></table>';

  // 關係邊
  const rel = g.edges.filter(e => e.src === id || e.dst === id);
  if (rel.length) {
    h += `<h2 class="sub-head">它與其他事物的關係（${rel.length} 條）</h2><ul>` +
      rel.map(e => {
        const out = e.src === id;
        const other = byId[out ? e.dst : e.src];
        const label = App.EDGE_NAMES[e.type] || e.type;
        const otherHtml = other
          ? `<a href="entity.html?id=${encodeURIComponent(other.id)}">${App.esc(other.name)}</a>`
          : `<span class="mono">${App.esc(out ? e.dst : e.src)}</span>`;
        const s = entrySource(e.entry);
        return `<li>${out ? '→' : '←'} ${label} ${otherHtml}
          <span class="muted">（出自 <a href="book.html?book=${s.book}#${App.esc(s.anchor)}">${App.esc(s.label)}</a>）</span></li>`;
      }).join('') + '</ul>';
  }
  main.innerHTML = h;
  main.querySelectorAll('.rev-btn').forEach(b => b.addEventListener('click', () => {
    Store.reviewSet(b.dataset.attr, b.dataset.dec);
    main.querySelectorAll(`.rev-btn[data-attr="${b.dataset.attr}"]`).forEach(x => x.classList.toggle('on', x.dataset.dec === b.dataset.dec));
  }));
}

/* ── 研究檔案 ───────────────────────────── */
async function bootAdjudications() {
  const main = document.getElementById('adj-main');
  let list;
  try { list = await Store.adjudications(); }
  catch (err) { main.innerHTML = `<p class="notice">載入失敗：${App.esc(err.message)}</p>`; return; }
  main.innerHTML = `<h1>研究檔案</h1>
    <p class="muted">我們做判斷時留下的討論記錄，共 ${list.length} 份——哪些對應為什麼這樣定、哪些爭議還沒有結論，都在這裏（偏研究者向，可離線閱讀）。</p>` +
    list.map(a => `
      <details class="adj-item">
        <summary><strong>${App.esc(a.title)}</strong> <span class="file">${App.esc(a.file)}</span></summary>
        <div class="adj-body">${App.md(a.content || '')}</div>
      </details>`).join('');
}

/* ── 關於本站 ────────────────────────────── */
async function bootAbout() {
  const el = document.getElementById('about-stats');
  if (!el) return;
  try {
    const m = await Store.manifest();
    el.innerHTML = `<ul>
      <li>收錄事物 ${m.graph.nodes.toLocaleString()} 項 · 事物之間的關聯 ${m.graph.edges.toLocaleString()} 條 · 屬性記錄 ${m.graph.attributes.toLocaleString()} 條</li>
      <li>白話分段 ${m.entries.sections} 段 · 地圖 ${m.maps} 張 · 實地照片 ${m.images} 張 · 研究檔案 ${m.adjudications} 份</li>
    </ul>`;
  } catch (e) { el.textContent = ''; }
}
