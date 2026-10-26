/* store.js — 數據加載與緩存
 * 優先 fetch('data/<name>.json')；file:// 協議下 fetch 被瀏覽器攔截時，
 * 回退到 <script src="data/<name>.js">（同名包裝檔，賦值到 window.SHJ_DATA[name]）。
 * entries.json 首屏加載；graph.json 僅實體頁加載。
 */
const Store = (() => {
  const cache = {};

  function loadViaScript(name) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = 'data/' + name + '.js';
      s.onload = () => {
        if (window.SHJ_DATA && window.SHJ_DATA[name] !== undefined) {
          resolve(window.SHJ_DATA[name]);
        } else {
          reject(new Error('data/' + name + '.js 已加載但未找到數據'));
        }
      };
      s.onerror = () => reject(new Error(
        '無法載入 data/' + name + '.json。若使用 file:// 打開，需要同名 .js 包裝檔；' +
        '建議在 webapp/ 目錄運行 python3 -m http.server 後用瀏覽器訪問。'));
      document.head.appendChild(s);
    });
  }

  function load(name) {
    if (!cache[name]) {
      cache[name] = fetch('data/' + name + '.json')
        .then(r => {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .catch(err => {
          if (location.protocol === 'file:') return loadViaScript(name);
          throw err;
        });
    }
    return cache[name];
  }

  return {
    load,
    entries: () => load('entries'),
    graph: () => load('graph'),
    mapChains: () => load('map-chains'),
    mapPoints: () => load('map-points'),
    basemap: () => load('basemap'),
    adjudications: () => load('adjudications'),
    manifest: () => load('manifest'),
  };
})();
