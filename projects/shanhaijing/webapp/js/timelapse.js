/* timelapse.js — 時光地圖：古水體與物種分布的古今變遷
 * 自研 SVG 世界視圖（投影規則與 map.js 同源：顯示經度 = lon < lon_wrap_below ? lon + 360 : lon）。
 * 圖層：basemap → waters（隨時間軸變化）→ chains（淡色參考）→ species（當時/現今對照）→ modern。
 * 交互：時間軸三段切換、圖層開關、拖拽平移、滾輪/雙指縮放、點選詳情卡、懸停提示。
 */
const SHJTimelapse = (() => {
  const NS = 'http://www.w3.org/2000/svg';
  const W = 1440;

  function el(tag, attrs) {
    const e = document.createElementNS(NS, tag);
    for (const k in (attrs || {})) e.setAttribute(k, attrs[k]);
    return e;
  }

  async function create(container, opts) {
    const [base, chains, tl] = await Promise.all([
      Store.basemap(), Store.mapChains(), Store.timelapse(),
    ]);
    return build(container, base, chains.chains, tl, opts || {});
  }

  function build(container, base, chains, tl, opts) {
    const win = base.window;
    const wrapBelow = base.lon_wrap_below;
    const H = Math.round(W * (win.lat1 - win.lat0) / (win.lon1 - win.lon0));
    function project(lon, lat) {
      const d = lon < wrapBelow ? lon + 360 : lon;
      return [(d - win.lon0) / (win.lon1 - win.lon0) * W,
              (win.lat1 - lat) / (win.lat1 - win.lat0) * H];
    }

    container.classList.add('map-wrap');
    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': '山海經古今變遷時光地圖' });
    const vp = el('g', { id: 'shj-viewport' });
    svg.appendChild(vp);
    const gridOv = el('g', { 'pointer-events': 'none' });
    svg.appendChild(gridOv);

    const layers = {
      basemap: el('g', {}), waters: el('g', {}), chains: el('g', {}),
      species: el('g', {}), modern: el('g', {}),
    };
    vp.appendChild(layers.basemap);
    vp.appendChild(layers.waters);
    vp.appendChild(layers.chains);
    vp.appendChild(layers.species);
    vp.appendChild(layers.modern);

    // ── 底圖（僅海岸線/地貌，不放注記以免干擾）──
    for (const item of base.basemap) {
      if (item[0] === 'line') {
        const [, pts, color, width, name, labelPos] = item;
        const d = pts.map((p, i) => {
          const [x, y] = project(p[0], p[1]);
          return (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1);
        }).join(' ');
        layers.basemap.appendChild(el('path', {
          d, fill: 'none', stroke: color, 'stroke-width': width || 1.2, 'stroke-linejoin': 'round',
          'vector-effect': 'non-scaling-stroke', opacity: 0.7,
        }));
        if (name && labelPos) {
          const [x, y] = project(labelPos[0], labelPos[1]);
          const t = el('text', { x, y, 'font-size': 10, class: 'shj-label', opacity: 0.65 });
          t.dataset.fs = 10;
          t.textContent = name;
          layers.basemap.appendChild(t);
        }
      } else if (item[0] === 'blob') {
        const [, lon, lat, rx, ry, color, name] = item;
        const [x, y] = project(lon, lat);
        const sx = rx / (win.lon1 - win.lon0) * W;
        const sy = ry / (win.lat1 - win.lat0) * H;
        layers.basemap.appendChild(el('ellipse', {
          cx: x, cy: y, rx: sx, ry: sy, fill: color, opacity: 0.4, stroke: '#b8ad93', 'stroke-width': 0.6,
        }));
        if (name) {
          const t = el('text', { x, y, 'font-size': 9.5, 'text-anchor': 'middle', class: 'shj-label', opacity: 0.6 });
          t.dataset.fs = 9.5;
          t.textContent = name;
          layers.basemap.appendChild(t);
        }
      }
    }

    // ── 山經鏈（淡色參考，可關）──
    for (const c of chains) {
      const pts = c.points.map(p => project(p.lon, p.lat));
      const d = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
      layers.chains.appendChild(el('path', {
        d, fill: 'none', stroke: c.color, 'stroke-width': 1.4, opacity: 0.28, 'stroke-linejoin': 'round',
        'vector-effect': 'non-scaling-stroke',
      }));
    }

    // ── 現代參照點 ──
    for (const [name, lon, lat] of (base.modern || [])) {
      const [x, y] = project(lon, lat);
      layers.modern.appendChild(el('circle', { cx: x, cy: y, r: 2.4, fill: '#7f8c8d', stroke: '#fff', 'stroke-width': 0.6, class: 'shj-icon', 'data-base': 2.4, 'vector-effect': 'non-scaling-stroke' }));
      const t = el('text', { x: x + 4, y: y - 3, 'font-size': 9.5, class: 'shj-label' });
      t.dataset.fs = 9.5;
      t.textContent = name;
      layers.modern.appendChild(t);
    }

    // ── 古水體（隨時期變化；每期重建）──
    const WATER_STYLE = {
      water:  { fill: '#2e86c1', opacity: 0.5 },
      marsh:  { fill: '#7fa05a', opacity: 0.5 },
      shrunk: { fill: '#2e86c1', opacity: 0.55 },
    };
    const hitTargets = [];

    function drawWaters(periodId) {
      layers.waters.innerHTML = '';
      for (const f of tl.waters) {
        const sh = f.shapes[periodId] || {};
        const [cx, cy] = project(f.lon, f.lat);
        const g = el('g', {});
        const gone = sh.state === 'gone';
        const rx = sh.rx || 1.2, ry = sh.ry || 0.8;
        const sx = rx / (win.lon1 - win.lon0) * W;
        const sy = ry / (win.lat1 - win.lat0) * H;
        if (gone) {
          g.appendChild(el('ellipse', {
            cx, cy, rx: sx, ry: sy, fill: 'rgba(0,0,0,0.03)',
            stroke: '#a05a2c', 'stroke-width': 1.3, 'stroke-dasharray': '4,3',
            'vector-effect': 'non-scaling-stroke', class: 'shj-gone-outline',
          }));
          const t = el('text', { x: cx, y: cy, 'font-size': 9, 'text-anchor': 'middle', fill: '#a05a2c', class: 'shj-label' });
          t.dataset.fs = 9;
          t.textContent = '已消失';
          g.appendChild(t);
        } else {
          const st = WATER_STYLE[sh.state || 'water'];
          g.appendChild(el('ellipse', { cx, cy, rx: sx, ry: sy, fill: st.fill, opacity: st.opacity, stroke: '#1a5276', 'stroke-width': 0.7, 'vector-effect': 'non-scaling-stroke' }));
          if (f.label) {
            const t = el('text', { x: cx, y: cy, 'font-size': 10.5, 'text-anchor': 'middle', fill: '#154360', class: 'shj-label' });
            t.dataset.fs = 10.5;
            t.textContent = f.name;
            g.appendChild(t);
          }
        }
        layers.waters.appendChild(g);
        const hit = el('circle', {
          cx, cy, r: Math.max(sx, 9), fill: 'rgba(0,0,0,0)',
          class: 'shj-hit shj-icon', 'data-base': Math.max(sx, 9),
          'data-tip': `${f.name}｜${f.reading}`, style: 'cursor:pointer',
        });
        layers.waters.appendChild(hit);
        hitTargets.push({ x: cx, y: cy, sel: { kind: 'water', f } });
      }
    }

    // ── 物種分布對照（當時 vs 現今；隨時期調整強調）──
    function drawSpecies(periodId) {
      layers.species.innerHTML = '';
      const nowEra = periodId === 'now';
      for (const s of tl.species) {
        const g = el('g', {});
        const [tx0, ty0] = project(s.then.lon, s.then.lat);
        const tsx = s.then.rx / (win.lon1 - win.lon0) * W;
        const tsy = s.then.ry / (win.lat1 - win.lat0) * H;
        // 當時分布：現在時期降為虛線殘跡，其餘時期實色
        g.appendChild(el('ellipse', {
          cx: tx0, cy: ty0, rx: tsx, ry: tsy,
          fill: nowEra ? 'rgba(30,132,73,0.06)' : '#1e8449', 'fill-opacity': nowEra ? 1 : 0.28,
          stroke: '#1e8449', 'stroke-width': 1.2,
          'stroke-dasharray': nowEra ? '5,3' : 'none', 'vector-effect': 'non-scaling-stroke',
        }));
        const lt = el('text', { x: tx0, y: ty0 - tsy - 3, 'font-size': 10, 'text-anchor': 'middle', fill: '#145a32', class: 'shj-label' });
        lt.dataset.fs = 10;
        lt.textContent = s.name;
        g.appendChild(lt);
        let nowPt = null;
        if (s.now) {
          const [nx, ny] = project(s.now.lon, s.now.lat);
          nowPt = [nx, ny];
          const nsx = s.now.rx / (win.lon1 - win.lon0) * W;
          const nsy = s.now.ry / (win.lat1 - win.lat0) * H;
          // 連線（遷徙方向）
          g.appendChild(el('line', {
            x1: tx0, y1: ty0, x2: nx, y2: ny, stroke: '#b9770e', 'stroke-width': 1,
            'stroke-dasharray': '4,3', opacity: 0.7, 'vector-effect': 'non-scaling-stroke',
          }));
          g.appendChild(el('ellipse', {
            cx: nx, cy: ny, rx: nsx, ry: nsy,
            fill: '#e67e22', 'fill-opacity': nowEra ? 0.55 : 0.35,
            stroke: '#b9770e', 'stroke-width': 1.2, 'vector-effect': 'non-scaling-stroke',
          }));
          const nt = el('text', { x: nx, y: ny + nsy + 11, 'font-size': 9, 'text-anchor': 'middle', fill: '#9c640c', class: 'shj-label' });
          nt.dataset.fs = 9;
          nt.textContent = '現今殘存';
          g.appendChild(nt);
        } else {
          // 區域滅絕：中心打 ✕
          const x1 = tx0 - tsx * 0.25, x2 = tx0 + tsx * 0.25, y1 = ty0 - tsy * 0.35, y2 = ty0 + tsy * 0.35;
          g.appendChild(el('line', { x1, y1, x2, y2, stroke: '#c0392b', 'stroke-width': 2, 'vector-effect': 'non-scaling-stroke' }));
          g.appendChild(el('line', { x1, y1: y2, x2, y2: y1, stroke: '#c0392b', 'stroke-width': 2, 'vector-effect': 'non-scaling-stroke' }));
        }
        layers.species.appendChild(g);
        const mkHit = (hx, hy, hr) => {
          const hit = el('circle', {
            cx: hx, cy: hy, r: hr, fill: 'rgba(0,0,0,0)',
            class: 'shj-hit shj-icon', 'data-base': hr,
            'data-tip': `${s.name}｜點選看古今分布變化`, style: 'cursor:pointer',
          });
          layers.species.appendChild(hit);
        };
        mkHit(tx0, ty0, Math.max(tsx, 10));
        hitTargets.push({ x: tx0, y: ty0, sel: { kind: 'species', s } });
        if (nowPt) {
          mkHit(nowPt[0], nowPt[1], Math.max(s.now.rx / (win.lon1 - win.lon0) * W, 10));
          hitTargets.push({ x: nowPt[0], y: nowPt[1], sel: { kind: 'species', s } });
        }
      }
    }

    // ── 提示條 ──
    const tip = document.createElement('div');
    tip.className = 'map-tooltip';
    container.appendChild(tip);

    // ── pan / zoom（與 map.js 同模式）──
    let scale = 1, tx = 0, ty = 0;
    const pointers = new Map();
    let pinchDist = 0, moved = false;
    const labelEls = [];
    const iconEls = [];

    const scaleBar = document.createElement('div');
    scaleBar.className = 'map-scalebar';
    container.appendChild(scaleBar);
    const latMid = (win.lat0 + win.lat1) / 2;
    const kmPerDeg = 111.3 * Math.cos(latMid * Math.PI / 180);
    function updateScaleBar() {
      const { s: cssScale } = viewMetrics();
      const pxPerDeg = cssScale * (W / (win.lon1 - win.lon0)) * scale;
      const pxPerKm = pxPerDeg / kmPerDeg;
      const seg = [25, 50, 100, 200, 500, 1000, 2000, 4000].find(k => k * pxPerKm >= 60 && k * pxPerKm <= 220) || 1000;
      scaleBar.innerHTML = `<div class="bar" style="width:${(seg * pxPerKm).toFixed(0)}px"></div><span>${seg} km</span>`;
    }
    function drawGrid() {
      const { s: cssScale } = viewMetrics();
      const wx0 = (0 - tx) / scale, wx1 = (W - tx) / scale;
      const wy0 = (0 - ty) / scale, wy1 = (H - ty) / scale;
      const dLon0 = wx0 / W * (win.lon1 - win.lon0) + win.lon0;
      const dLon1 = wx1 / W * (win.lon1 - win.lon0) + win.lon0;
      const latTop = win.lat1 - wy0 / H * (win.lat1 - win.lat0);
      const latBot = win.lat1 - wy1 / H * (win.lat1 - win.lat0);
      const pxPerLon = W / (win.lon1 - win.lon0) * scale * cssScale;
      const pxPerLat = H / (win.lat1 - win.lat0) * scale * cssScale;
      const lonStep = [1, 2, 5, 10, 15, 30, 45].find(st => st * pxPerLon >= 70) || 45;
      const latStep = [1, 2, 5, 10, 15, 30].find(st => st * pxPerLat >= 60) || 30;
      gridOv.innerHTML = '';
      for (let d = Math.ceil(dLon0 / lonStep) * lonStep; d <= dLon1; d += lonStep) {
        const wx = (d - win.lon0) / (win.lon1 - win.lon0) * W;
        const sx = wx * scale + tx;
        if (sx < -5 || sx > W + 5) continue;
        gridOv.appendChild(el('line', { x1: sx, y1: 0, x2: sx, y2: H, stroke: '#c9c2b0', 'stroke-width': 0.8 }));
        const trueLon = d > 180 ? d - 360 : d;
        const t = el('text', { x: sx + 3, y: H - 8, 'font-size': 9, fill: '#999' });
        t.textContent = `${Math.abs(trueLon)}°${trueLon < 0 ? 'W' : 'E'}`;
        gridOv.appendChild(t);
      }
      for (let lat = Math.ceil(latBot / latStep) * latStep; lat <= latTop; lat += latStep) {
        const wy = (win.lat1 - lat) / (win.lat1 - win.lat0) * H;
        const sy = wy * scale + ty;
        if (sy < -5 || sy > H + 5) continue;
        gridOv.appendChild(el('line', { x1: 0, y1: sy, x2: W, y2: sy, stroke: '#c9c2b0', 'stroke-width': 0.8 }));
        const t = el('text', { x: 4, y: sy - 3, 'font-size': 9, fill: '#999' });
        t.textContent = `${Math.abs(lat)}°${lat < 0 ? 'S' : 'N'}`;
        gridOv.appendChild(t);
      }
    }
    function collect() {
      labelEls.length = 0; iconEls.length = 0;
      labelEls.push(...vp.querySelectorAll('.shj-label'));
      iconEls.push(...vp.querySelectorAll('.shj-icon'));
    }
    function apply() {
      vp.setAttribute('transform', `translate(${tx},${ty}) scale(${scale})`);
      for (const t of labelEls) t.style.fontSize = (parseFloat(t.dataset.fs) / scale) + 'px';
      for (const c of iconEls) c.setAttribute('r', parseFloat(c.dataset.base) / scale);
      updateScaleBar();
      drawGrid();
    }
    function viewMetrics() {
      const r = svg.getBoundingClientRect();
      const s = Math.min(r.width / W, r.height / H);
      return { r, s, ox: (r.width - W * s) / 2, oy: (r.height - H * s) / 2 };
    }
    function toWorld(cx, cy) {
      const { r, s, ox, oy } = viewMetrics();
      return { x: (cx - r.left - ox) / s, y: (cy - r.top - oy) / s };
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
      const t = e.target;
      if (t.classList && t.classList.contains('shj-hit')) {
        tip.style.display = 'block';
        tip.textContent = t.dataset.tip || '';
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
        if (pinchDist > 0 && nd > 0) zoomAt((a.x + b.x) / 2, (a.y + b.y) / 2, nd / pinchDist);
        pinchDist = nd;
      }
    });
    function endPointer(e) {
      pointers.delete(e.pointerId);
      if (pointers.size === 0) svg.classList.remove('dragging');
    }
    svg.addEventListener('pointerup', endPointer);
    svg.addEventListener('pointercancel', endPointer);

    // 點選：就近拾取
    svg.addEventListener('click', e => {
      if (moved || !opts.onSelect) return;
      const p = toWorld(e.clientX, e.clientY);
      const wx = (p.x - tx) / scale, wy = (p.y - ty) / scale;
      const { s: cssScale } = viewMetrics();
      const thresh = 14 / cssScale / scale;
      let best = null, bestD = thresh;
      for (const h of hitTargets) {
        if (h.sel.kind === 'water' && !layerOn.waters) continue;
        if (h.sel.kind === 'species' && !layerOn.species) continue;
        const d = Math.hypot(h.x - wx, h.y - wy);
        if (d < bestD) { bestD = d; best = h; }
      }
      if (best) opts.onSelect(best.sel);
    });

    container.appendChild(svg);

    // ── 圖層開關與時期切換 ──
    const layerOn = { waters: true, species: true };
    let periodId = tl.periods[1].id; // 預設：成書時代

    function renderPeriod() {
      hitTargets.length = 0;
      if (layerOn.waters) drawWaters(periodId);
      else layers.waters.innerHTML = '';
      if (layerOn.species) drawSpecies(periodId);
      else layers.species.innerHTML = '';
      collect();
      apply();
      if (opts.onPeriod) opts.onPeriod(periodId);
    }
    renderPeriod();

    return {
      svg,
      periods: tl.periods,
      get period() { return periodId; },
      setPeriod(id) { if (id !== periodId) { periodId = id; renderPeriod(); } },
      setLayer(name, on) {
        if (name === 'waters' || name === 'species') { layerOn[name] = on; renderPeriod(); }
        else layers[name].style.display = on ? '' : 'none';
      },
      reset() { scale = 1; tx = 0; ty = 0; apply(); },
    };
  }

  return { create };
})();
