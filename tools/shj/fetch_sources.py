"""Re-fetch the three public-domain witnesses of 山海經 from zh.wikisource.org (reproducibility).

  wikisource-base : 山海經/<書名>              raw wikitext (punctuated, with 郭注 and 異文 templates)
  sbck-chenghua   : 山海經 (四部叢刊本)/卷第N    rendered text of 明成化庚寅(1470)刊本 photo-reprint, 郭璞傳
  skqs            : 山海經 (四庫全書本)/卷NN     raw wikitext of 四庫全書 (1781) transcription

Usage: python3 -I tools/shj/fetch_sources.py   (writes into reference/shanhaijing/sources/)
"""
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reference/shanhaijing/sources"
UA = {"User-Agent": "mythos-research/0.1 (open research project)"}
BOOKS = ["南山經", "西山經", "北山經", "東山經", "中山經", "海外南經", "海外西經", "海外北經", "海外東經",
         "海內南經", "海內西經", "海內北經", "海內東經", "大荒東經", "大荒南經", "大荒西經", "大荒北經", "海內經"]
NUMS = "一 二 三 四 五 六 七 八 九 十 十一 十二 十三 十四 十五 十六 十七 十八".split()


def get(url: str) -> bytes:
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA)).read()


def raw(title: str) -> str:
    return get("https://zh.wikisource.org/w/index.php?action=raw&title=" + urllib.parse.quote(title)).decode()


def rendered_text(title: str) -> str:
    data = json.loads(get("https://zh.wikisource.org/w/api.php?action=parse&format=json&prop=text"
                          "&variant=zh-hant&page=" + urllib.parse.quote(title)))
    return html_to_text(data["parse"]["text"]["*"])


def html_to_text(h: str) -> str:
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<br\s*/?>|</p>|</div>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h)).replace("​", "")
    t = re.sub(r"\.mw-parser-output[^\n〈]*?(?=〈|$)", "", t, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", t).strip() + "\n"


def main():
    base = OUT / "wikisource-base"; base.mkdir(parents=True, exist_ok=True)
    (base / "index.wiki").write_text(raw("山海經"))
    for i, b in enumerate(BOOKS + ["郭璞序"], 1):
        (base / f"{i:02d}-{b}.wiki").write_text(raw(f"山海經/{b}"))
    sbck = OUT / "sbck-chenghua"; sbck.mkdir(parents=True, exist_ok=True)
    (sbck / "00-序.txt").write_text(rendered_text("山海經 (四部叢刊本)/序"))
    for i, n in enumerate(NUMS, 1):
        (sbck / f"{i:02d}.txt").write_text(rendered_text(f"山海經 (四部叢刊本)/卷第{n}"))
    skqs = OUT / "skqs"; skqs.mkdir(parents=True, exist_ok=True)
    for i in range(1, 19):
        (skqs / f"{i:02d}.wiki").write_text(raw(f"山海經 (四庫全書本)/卷{i:02d}"))


if __name__ == "__main__":
    main()
