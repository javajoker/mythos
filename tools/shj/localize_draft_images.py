#!/usr/bin/env python3
"""Download draft-v2 images via local proxy and rewrite markdown URLs to local files.

Usage: python3 tools/shj/localize_draft_images.py
"""
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path

DRAFT = Path(__file__).resolve().parents[2] / "projects/shanhaijing/deliverables/draft-v2"
IMGDIR = DRAFT / "images"
PROXY = "http://127.0.0.1:8889"
CT_EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/gif": ".gif", "image/webp": ".webp"}


def fname_for(url):
    path = urllib.parse.urlparse(url).path
    base = urllib.parse.unquote(path.rsplit("/", 1)[-1])
    base = re.sub(r"[^\w.\-]+", "_", base).strip("_")[:80] or "image"
    return base


def main():
    urls = set()
    for md in DRAFT.glob("book-*.md"):
        urls.update(re.findall(r"https://[^)\s]+", md.read_text(encoding="utf-8")))
    urls = sorted(urls)
    print(f"{len(urls)} unique image URLs")
    ok, failed, mapping = 0, [], {}
    used = set()
    for i, url in enumerate(urls):
        base = fname_for(url)
        name = base
        k = 1
        while name in used:
            stem, dot, ext = base.rpartition(".")
            name = f"{stem}_{k}.{ext}" if dot else f"{base}_{k}"
            k += 1
        used.add(name)
        dest = IMGDIR / name
        r = subprocess.run(["curl", "-sL", "-x", PROXY, "-m", "90", "-o", str(dest), url],
                           capture_output=True, text=True)
        # verify
        if dest.exists() and dest.stat().st_size > 1000:
            head = dest.read_bytes()[:12]
            is_img = (head[:3] == b"\xff\xd8\xff" or head[:8] == b"\x89PNG\r\n\x1a\n"
                      or head[:4] == b"GIF8" or head[:4] == b"RIFF")
            if is_img:
                ok += 1
                mapping[url] = f"images/{name}"
                print(f"[{i+1}/{len(urls)}] OK {name} ({dest.stat().st_size//1024} KB)")
                continue
        failed.append(url)
        print(f"[{i+1}/{len(urls)}] FAIL {url[:100]}", file=sys.stderr)
        if dest.exists():
            dest.unlink()
    # rewrite
    for md in DRAFT.glob("book-*.md"):
        s = md.read_text(encoding="utf-8")
        for url, local in mapping.items():
            s = s.replace(url, local)
        md.write_text(s, encoding="utf-8")
    print(f"downloaded {ok}/{len(urls)}; failed {len(failed)}")
    if failed:
        print("FAILED:")
        for u in failed:
            print(" ", u)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
