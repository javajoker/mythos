/* map.js — 自研 SVG 世界視圖（太平洋中心，equirectangular）
 * 投影規則與渲染器同源：顯示經度 = lon < lon_wrap_below(-25) ? lon + 360 : lon。
 * 圖層：basemap（海岸線/地貌塊）→ chains（山經鏈）→ points（框架書點）→ 注記/現代點。
 * 交互：拖拽平移、滾輪/雙指縮放、點選回調、懸停提示。
 */
const SHJMap = (() => {
  const NS = 'http://www.w3.org/2000/svg';
  const W = 1440; // 畫布寬；高依窗口緯度範圍等比
  const CN_NUM = { '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12 };
  const CHAIN_BOOK = { '西': '02', '中': '05', '北': '03', '東': '04', '南': '01' };

  function el(tag, attrs) {
    const e = document.createElementNS(NS, tag);
    for (const k in (attrs || {})) e.setAttribute(k, attrs[k]);
    return e;
  }

  async function create(container, opts) {
    const [base, chains, points] = await Promise.all([
      Store.basemap(), Store.mapChains(), Store.mapPoints(),
    ]);
    return build(container, base, chains.chains, points, opts || {});
  }

  function build(container, base, chains, points, opts) {
    const win = base.window; // {lon0,lon1,lat0,lat1}
    const wrapBelow = base.lon_wrap_below;
    const H = Math.round(W * (win.lat1 - win.lat0) / (win.lon1 - win.lon0));

    function project(lon, lat) {
      const d = lon < wrapBelow ? lon + 360 : lon;
      return [(d - win.lon0) / (win.lon1 - win.lon0) * W,
              (win.lat1 - lat) / (win.lat1 - win.lat0) * H];
    }

    container.classList.add('map-wrap');
    const oldSvg = container.querySelector('svg');
    if (oldSvg) oldSvg.remove();
    const oldTip = container.querySelector('.map-tooltip');
    if (oldTip) oldTip.remove();
    const oldLoading = container.querySelector('.map-loading');
    if (oldLoading) oldLoading.remove();
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': '山海經現實映射世界地圖（太平洋中心）' });
    const vp = el('g', { id: 'shj-viewport' });
    svg.appendChild(vp);

    const layers = {
      grid: el('g', {}), basemap: el('g', {}), chains: el('g', {}), points: el('g', {}),
      annotations: el('g', {}), modern: el('g', {}),
    };
    vp.appendChild(layers.grid);
    vp.appendChild(layers.basemap);
    vp.appendChild(layers.annotations);
    vp.appendChild(layers.chains);
    vp.appendChild(layers.points);
    vp.appendChild(layers.modern);

    // ── 經緯網格（世界坐標，隨圖平移；標籤恆定字號）──
    for (let lon = Math.ceil(win.lon0 / 30) * 30; lon < win.lon1; lon += 30) {
      const [x1, y1] = project(lon, win.lat0), [x2, y2] = project(lon, win.lat1);
      layers.grid.appendChild(el('line', { x1, y1, x2, y2, stroke: '#d9d2c0', 'stroke-width': 0.8 }));
      const trueLon = lon > 180 ? lon - 360 : lon;
      const t = el('text', { x: x1 + 3, y: y1 - 6, 'font-size': 9, fill: '#999', class: 'shj-label' });
      t.dataset.fs = 9;
      t.textContent = `${Math.abs(trueLon)}°${trueLon < 0 ? 'W' : 'E'}`;
      layers.grid.appendChild(t);
    }
    for (let lat = Math.ceil(win.lat0 / 10) * 10; lat < win.lat1; lat += 10) {
      const [x1, y1] = project(win.lon0, lat), [x2, y2] = project(win.lon1, lat);
      layers.grid.appendChild(el('line', { x1, y1, x2, y2, stroke: '#d9d2c0', 'stroke-width': 0.8 }));
      const t = el('text', { x: x1 + 3, y: y1 - 4, 'font-size': 9, fill: '#999', class: 'shj-label' });
      t.dataset.fs = 9;
      t.textContent = `${Math.abs(lat)}°${lat < 0 ? 'S' : 'N'}`;
      layers.grid.appendChild(t);
    }

    // ── 底圖 ──
    for (const item of base.basemap) {
      if (item[0] === 'line') {
        const [, pts, color, width, name, labelPos] = item;
        const d = pts.map((p, i) => {
          const [x, y] = project(p[0], p[1]);
          return (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1);
        }).join(' ');
        layers.basemap.appendChild(el('path', {
          d, fill: 'none', stroke: color, 'stroke-width': width || 1.2, 'stroke-linejoin': 'round',
        }));
        if (name && labelPos) {
          const [x, y] = project(labelPos[0], labelPos[1]);
          const t = el('text', { x, y, 'font-size': 11, class: 'shj-label' });
          t.dataset.fs = 11;
          t.textContent = name;
          layers.annotations.appendChild(t);
        }
      } else if (item[0] === 'blob') {
        const [, lon, lat, rx, ry, color, name] = item;
        const [x, y] = project(lon, lat);
        const sx = rx / (win.lon1 - win.lon0) * W;
        const sy = ry / (win.lat1 - win.lat0) * H;
        layers.basemap.appendChild(el('ellipse', {
          cx: x, cy: y, rx: sx, ry: sy, fill: color, opacity: 0.55, stroke: '#b8ad93', 'stroke-width': 0.6,
        }));
        if (name) {
          const t = el('text', { x, y, 'font-size': 10, 'text-anchor': 'middle', class: 'shj-label' });
          t.dataset.fs = 10;
          t.textContent = name;
          layers.annotations.appendChild(t);
        }
      }
    }

    // ── 底圖注記 ──
    for (const [text, lon, lat, color] of (base.annotations || [])) {
      const [x, y] = project(lon, lat);
      const t = el('text', { x, y, 'font-size': 10.5, fill: color || '#666', class: 'shj-label' });
      t.dataset.fs = 10.5;
      t.textContent = text;
      layers.annotations.appendChild(t);
    }

    // ── 山經鏈 ──
    for (const c of chains) {
      const g = el('g', {});
      const pts = c.points.map(p => project(p.lon, p.lat));
      const d = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
      g.appendChild(el('path', {
        d, fill: 'none', stroke: c.color, 'stroke-width': 2, opacity: 0.85, 'stroke-linejoin': 'round',
      }));
      c.points.forEach((p, i) => {
        const [x, y] = pts[i];
        const dot = el('circle', {
          cx: x, cy: y, r: 3, fill: '#fff', stroke: c.color, 'stroke-width': 1.6,
          'pointer-events': 'none', class: 'shj-icon', 'data-base': 3,
        });
        g.appendChild(dot);
        if (c.anchor_index === i) { // 錨站：雙圈
          g.appendChild(el('circle', {
            cx: x, cy: y, r: 6, fill: 'none', stroke: c.color, 'stroke-width': 1.4, 'pointer-events': 'none',
            class: 'shj-icon', 'data-base': 6,
          }));
        }
        // 透明擴大熱區，便於點選
        const hit = el('circle', {
          cx: x, cy: y, r: 9, fill: 'rgba(0,0,0,0)',
          class: 'shj-station shj-icon', 'data-base': 9, 'data-chain': c.label, 'data-name': p.n, 'data-idx': i,
        });
        hit.appendChild(el('title', {})).textContent = `${c.label} ${p.n}`;
        g.appendChild(hit);
      });
      if (c.label_pos) {
        const [x, y] = project(c.label_pos[0], c.label_pos[1]);
        const t = el('text', { x, y, 'font-size': 12, fill: c.color, class: 'shj-label shj-chain-label' });
        t.dataset.fs = 12;
        t.textContent = `${c.label}｜${c.short || ''}`;
        g.appendChild(t);
      }
      layers.chains.appendChild(g);
    }

    // ── 框架書點 ──
    points.forEach((p, idx) => {
      const [x, y] = project(p.lon, p.lat);
      const r = (p.size || 3.5) + 0.5;
      let node;
      if (p.status === 'pending_anchor') { // 紅虛框
        node = el('rect', {
          x: x - r, y: y - r, width: r * 2, height: r * 2,
          fill: 'rgba(192,57,43,0.12)', stroke: '#c0392b', 'stroke-width': 1.2, 'stroke-dasharray': '3,2',
          class: 'shj-icon-rect', 'data-cx': x, 'data-cy': y, 'data-base': r,
        });
      } else {
        node = el('circle', { cx: x, cy: y, r, fill: p.color, opacity: 0.9, stroke: '#fff', 'stroke-width': 0.8,
          class: 'shj-icon', 'data-base': r });
      }
      node.setAttribute('pointer-events', 'none');
      layers.points.appendChild(node);
      const hit = el('circle', {
        cx: x, cy: y, r: Math.max(r + 4, 9), fill: 'rgba(0,0,0,0)',
        class: 'shj-point shj-icon', 'data-base': Math.max(r + 4, 9), 'data-idx': idx, 'data-name': p.name,
      });
      hit.appendChild(el('title', {})).textContent = p.note || p.name;
      layers.points.appendChild(hit);
    });

    // ── 現代參照點 ──
    for (const [name, lon, lat] of (base.modern || [])) {
      const [x, y] = project(lon, lat);
      layers.modern.appendChild(el('circle', { cx: x, cy: y, r: 2.4, fill: '#7f8c8d', stroke: '#fff', 'stroke-width': 0.6, class: 'shj-icon', 'data-base': 2.4 }));
      const t = el('text', { x: x + 4, y: y - 3, 'font-size': 9.5, class: 'shj-label' });
      t.dataset.fs = 9.5;
      t.textContent = name;
      layers.modern.appendChild(t);
    }

    // ── 提示條 ──
    const tip = document.createElement('div');
    tip.className = 'map-tooltip';
    container.appendChild(tip);

    // ── pan / zoom ──
    let scale = 1, tx = 0, ty = 0;
    const pointers = new Map();
    let pinchDist = 0, moved = false;

    const labelEls = [];
    const iconEls = [];
    const iconRects = [];
    // 比例尺（屏幕固定疊加層）
    const scaleBar = document.createElement('div');
    scaleBar.className = 'map-scalebar';
    container.appendChild(scaleBar);
    const latMid = (win.lat0 + win.lat1) / 2;
    const kmPerDeg = 111.3 * Math.cos(latMid * Math.PI / 180);
    function updateScaleBar() {
      const r = svg.getBoundingClientRect();
      const pxPerDeg = (r.width / W) * scale;
      const pxPerKm = pxPerDeg / kmPerDeg;
      const seg = [25, 50, 100, 200, 500, 1000, 2000, 4000].find(k => k * pxPerKm >= 60 && k * pxPerKm <= 220) || 1000;
      scaleBar.innerHTML = `<div class="bar" style="width:${(seg * pxPerKm).toFixed(0)}px"></div><span>${seg} km</span>`;
    }
    function apply() {
      vp.setAttribute('transform', `translate(${tx},${ty}) scale(${scale})`);
      for (const t of labelEls) t.style.fontSize = (parseFloat(t.dataset.fs) / scale) + 'px';
      for (const c of iconEls) c.setAttribute('r', parseFloat(c.dataset.base) / scale);
      for (const rc of iconRects) {
        const b = parseFloat(rc.dataset.base) / scale, cx = parseFloat(rc.dataset.cx), cy = parseFloat(rc.dataset.cy);
        rc.setAttribute('x', cx - b); rc.setAttribute('y', cy - b);
        rc.setAttribute('width', b * 2); rc.setAttribute('height', b * 2);
      }
      updateScaleBar();
    }
    // 延遲收集（渲染完成後一次性抓取）
    setTimeout(() => {
      labelEls.push(...vp.querySelectorAll('.shj-label'));
      iconEls.push(...vp.querySelectorAll('.shj-icon'));
      iconRects.push(...vp.querySelectorAll('.shj-icon-rect'));
      updateScaleBar();
    }, 0);
    function toWorld(cx, cy) {
      const r = svg.getBoundingClientRect();
      return {
        x: (cx - r.left) / r.width * W,
        y: (cy - r.top) / r.height * H,
      };
    }
    function zoomAt(cx, cy, factor) {
      const p = toWorld(cx, cy);
      const ns = Math.min(24, Math.max(0.7, scale * factor));
      const k = ns / scale;
      tx = p.x - (p.x - tx) * k;
      ty = p.y - (p.y - ty) * k;
      scale = ns;
      apply();
    }

    window.addEventListener('resize', updateScaleBar);

    svg.addEventListener('wheel', e => {
      e.preventDefault();
      zoomAt(e.clientX, e.clientY, e.deltaY < 0 ? 1.18 : 1 / 1.18);
    }, { passive: false });

    svg.addEventListener('pointerdown', e => {
      svg.setPointerCapture(e.pointerId);
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      moved = false;
      if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        pinchDist = Math.hypot(a.x - b.x, a.y - b.y);
      }
      svg.classList.add('dragging');
    });
    svg.addEventListener('pointermove', e => {
      // 懸停提示
      const t = e.target;
      if (t.classList && (t.classList.contains('shj-point') || t.classList.contains('shj-station'))) {
        tip.style.display = 'block';
        tip.textContent = t.querySelector('title') ? t.querySelector('title').textContent : '';
        const cr = container.getBoundingClientRect();
        tip.style.left = Math.min(e.clientX - cr.left + 12, cr.width - 240) + 'px';
        tip.style.top = (e.clientY - cr.top + 14) + 'px';
      } else {
        tip.style.display = 'none';
      }
      if (!pointers.has(e.pointerId)) return;
      const prev = pointers.get(e.pointerId);
      const dx = e.clientX - prev.x, dy = e.clientY - prev.y;
      pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
      if (pointers.size === 1) {
        const r = svg.getBoundingClientRect();
        tx += dx / r.width * W;
        ty += dy / r.height * H;
        apply();
      } else if (pointers.size === 2) {
        const [a, b] = [...pointers.values()];
        const nd = Math.hypot(a.x - b.x, a.y - b.y);
        if (pinchDist > 0 && nd > 0) {
          zoomAt((a.x + b.x) / 2, (a.y + b.y) / 2, nd / pinchDist);
        }
        pinchDist = nd;
      }
    });
    function endPointer(e) {
      pointers.delete(e.pointerId);
      if (pointers.size === 0) svg.classList.remove('dragging');
    }
    svg.addEventListener('pointerup', endPointer);
    svg.addEventListener('pointercancel', endPointer);

    // 點選（區分拖拽）：就近拾取——在屏幕 14px 閾值內找最近的站點/點位
    const hitTargets = []; // {x, y, sel}（世界坐標）
    for (const c of chains) {
      c.points.forEach((p, i) => {
        const [x, y] = project(p.lon, p.lat);
        hitTargets.push({
          x, y,
          sel: {
            kind: 'station', chain: c.label,
            book: CHAIN_BOOK[c.label[0]] || null,
            sub: CN_NUM[c.label.slice(1)] || null,
            name: p.n, anchor: c.anchor_index === i,
          },
        });
      });
    }
    points.forEach(p => {
      const [x, y] = project(p.lon, p.lat);
      hitTargets.push({ x, y, sel: { kind: 'point', point: p } });
    });
    svg.addEventListener('click', e => {
      if (moved || !opts.onSelect) return;
      const p = toWorld(e.clientX, e.clientY);
      const wx = (p.x - tx) / scale, wy = (p.y - ty) / scale;
      const r = svg.getBoundingClientRect();
      const thresh = 14 / (r.width / W) / scale; // 屏幕 14px → 世界單位
      let best = null, bestD = thresh;
      for (const h of hitTargets) {
        const d = Math.hypot(h.x - wx, h.y - wy);
        if (d < bestD) { bestD = d; best = h; }
      }
      if (best) opts.onSelect(best.sel);
    });

    container.appendChild(svg);
    apply();

    return {
      svg,
      setLayer(name, on) { layers[name].style.display = on ? '' : 'none'; },
      layers: Object.keys(layers),
      reset() { scale = 1; tx = 0; ty = 0; apply(); },
    };
  }

  return { create };
})();
