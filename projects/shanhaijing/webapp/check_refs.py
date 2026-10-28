#!/usr/bin/env python3
"""check_refs.py — 核對 webapp 前端引用的 data/images/maps 文件都存在，且無外部依賴。

用法：python3 check_refs.py（在 webapp/ 目錄內運行）
退出碼 0 = 全部通過。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

errors = []
warnings = []


def check(path, why):
    if not os.path.isfile(path):
        errors.append(f"缺失 {path}（{why}）")


# 1. data/*.json 與 file:// 回退 .js
for name in ["entries", "graph", "map-chains", "map-points", "basemap", "adjudications", "manifest", "timelapse"]:
    check(f"data/{name}.json", "Store.load")
    check(f"data/{name}.js", "file:// 回退")

# 2. entries.json 引用的圖片
entries = json.load(open("data/entries.json", encoding="utf-8"))
srcs = set()
for e in entries:
    for im in e["images"]:
        srcs.add(im["src"])
    for m in re.finditer(r"!\[[^\]]*\]\(([^)\s]+)\)", e["reading_md"]):
        srcs.add(m.group(1))
for src in sorted(srcs):
    # 地圖引用在前端被重寫為 maps/；此處按同一規則核對
    src = re.sub(r"^(\.\./)*data/derived/era/adaptation/", "maps/", src)
    check(src, "entries.json 配圖")
    if not src.startswith(("images/", "maps/")):
        warnings.append(f"配圖不在 images/ 或 maps/ 下：{src}")

# 3. reading_md 裡的地圖鏈接（前端會把 ../../data/derived/era/adaptation/ 重寫為 maps/）
for e in entries:
    for m in re.finditer(r"\]\((\.\./)*data/derived/era/adaptation/([^)\s]+)\)", e["reading_md"]):
        check(f"maps/{m.group(2)}", f"{e['id']} 地圖鏈接")

# 4. app.js 中 BOOKS 引用的地圖
appjs = open("js/app.js", encoding="utf-8").read()
for m in sorted(set(re.findall(r"'((?:book\d+|[a-z0-9-]+-map|[a-z]+-overview)\.svg)'", appjs))):
    check(f"maps/{m}", "app.js BOOKS.maps")

# 5. HTML 引用的本地資源 + 外部依賴掃描
for html in sorted(f for f in os.listdir(".") if f.endswith(".html")):
    text = open(html, encoding="utf-8").read()
    for m in re.findall(r'(?:src|href)="([^"#]+)"', text):
        if m.startswith(("http://", "https://", "//", "mailto:")):
            errors.append(f"{html} 引用外部資源：{m}")
        elif not m.startswith(("data:", "#")) and ":" not in m.split("/")[0]:
            if not re.search(r"\?\w+=", m) and not m.endswith(".html"):
                check(m.split("?")[0], f"{html} 引用")

# 6. JS 中不得有外部 URL（除註釋說明）
for js in ["js/app.js", "js/map.js", "js/store.js", "js/kg.js"]:
    text = open(js, encoding="utf-8").read()
    for m in re.findall(r'["\'](https?://[^"\']+)["\']', text):
        if m == "http://www.w3.org/2000/svg":  # SVG 命名空間常量，非網絡請求
            continue
        errors.append(f"{js} 引用外部資源：{m}")

for w in warnings:
    print("WARN:", w)
if errors:
    print(f"\n{len(errors)} 個錯誤：")
    for e in errors:
        print("FAIL:", e)
    sys.exit(1)
print(f"OK：所有引用文件存在；無外部依賴（警告 {len(warnings)} 條）。")
