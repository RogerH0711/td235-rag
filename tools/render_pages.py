"""把說明書掃描 PDF 轉成 OCR 用的圖片。

用法：.venv/Scripts/python tools/render_pages.py [--pages 9,13]

說明書版面（逐頁看過）：
- 偶數頁：德文內文＋插圖（Fig. 1–11 都印在偶數頁）
- 奇數頁 3–11：左欄英文、右欄法文；p13：橫跨整頁的英文規格表
- p1 封面、p15 封底、p2 三語目錄＋德文致詞

每個 PDF 只有第 1 頁有內容；第 2 頁之後若不是空白會印出警告。
輸出到 ocr/pages/：
    pNN_full.png  整頁（校對用，所有頁）
    pNN_en.png    英文欄（OCR 用，只有英文頁）
"""
import argparse
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "source_pdf"
OUT_DIR = ROOT / "ocr" / "pages"

DPI = 300
ENGLISH_PAGES = {3, 5, 7, 9, 11, 13}
FULL_WIDTH_PAGES = {13}  # Technical Data 是橫跨整頁的表格
BLANK_DARK_RATIO = 0.001  # 深色像素比例低於這個值視為空白頁
GUTTER_RANGE = (0.40, 0.62)  # 欄間空白只會出現在頁面中段
GUTTER_NOISE = 2  # 一欄裡容許的深色像素數（掃描雜點）
CONTENT_BOTTOM = 0.95  # 頁碼印在最下面約 3% 的位置，不送進 OCR
TRIM_MARGIN = 10  # 裁掉四周空白後保留的邊界（pt）


def gray_pixmap(page, dpi):
    return page.get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY, alpha=False)


def dark_ratio(page):
    """低解析度灰階渲染，計算深色像素比例。"""
    samples = gray_pixmap(page, 50).samples
    return sum(1 for b in samples if b < 128) / len(samples)


def find_gutter(page):
    """找左右兩欄之間最寬的直向空白帶，回傳 (中點占頁寬比例, 空白帶寬度比例)。

    固定從 50% 裁切不可靠：p7 的英文行尾延伸到約 50.1%。
    """
    pix = gray_pixmap(page, 100)
    w, h, stride, s = pix.width, pix.height, pix.stride, pix.samples
    x0, x1 = int(w * GUTTER_RANGE[0]), int(w * GUTTER_RANGE[1])
    dark = [0] * (x1 - x0)
    for y in range(h):
        row = s[y * stride + x0 : y * stride + x1]
        for i, b in enumerate(row):
            if b < 128:
                dark[i] += 1
    best_start, best_len, start = 0, 0, None
    for i, count in enumerate(dark + [GUTTER_NOISE + 1]):  # 結尾哨兵，收掉最後一段
        if count <= GUTTER_NOISE:
            start = i if start is None else start
        elif start is not None:
            if i - start > best_len:
                best_start, best_len = start, i - start
            start = None
    if best_len == 0:
        raise ValueError("找不到欄間空白")
    return (x0 + best_start + best_len / 2) / w, best_len / w


def trim_to_content(page, clip):
    """把 clip 縮到有字的範圍（四周留 TRIM_MARGIN）。

    Ollama 送進模型的 token 數和像素數成正比（每 1024 像素約 1 個 token），
    p13 整頁 300 dpi 約 8500 token，超過 num_ctx 8192；裁掉空白後才放得下。
    """
    clip = clip & pymupdf.Rect(clip.x0, clip.y0, clip.x1, page.rect.y0 + page.rect.height * CONTENT_BOTTOM)
    dpi = 100
    pix = page.get_pixmap(dpi=dpi, clip=clip, colorspace=pymupdf.csGRAY, alpha=False)
    w, h, stride, s = pix.width, pix.height, pix.stride, pix.samples
    rows, cols = [0] * h, [0] * w
    for y in range(h):
        for x, b in enumerate(s[y * stride : y * stride + w]):
            if b < 128:
                rows[y] += 1
                cols[x] += 1
    ys = [y for y, c in enumerate(rows) if c > GUTTER_NOISE]
    xs = [x for x, c in enumerate(cols) if c > GUTTER_NOISE]
    if not ys or not xs:
        raise ValueError("裁切範圍內沒有內容")
    pt = 72 / dpi  # 像素 → pt
    box = pymupdf.Rect(clip.x0 + xs[0] * pt, clip.y0 + ys[0] * pt,
                       clip.x0 + (xs[-1] + 1) * pt, clip.y0 + (ys[-1] + 1) * pt)
    margin = pymupdf.Rect(-TRIM_MARGIN, -TRIM_MARGIN, TRIM_MARGIN, TRIM_MARGIN)
    return (box + margin) & clip


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", help="只處理這些頁，例如 9,13")
    args = ap.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    pdfs = sorted(SRC_DIR.glob("*.pdf"), key=lambda p: int(p.stem))
    if args.pages:
        wanted = {int(n) for n in args.pages.split(",")}
        pdfs = [p for p in pdfs if int(p.stem) in wanted]

    for pdf in pdfs:
        n = int(pdf.stem)
        doc = pymupdf.open(pdf)
        extra = [i + 1 for i in range(1, doc.page_count) if dark_ratio(doc[i]) > BLANK_DARK_RATIO]
        if extra:
            print(f"⚠ p{n}: 第 {extra} 頁不是空白，請人工確認")
        page = doc[0]
        if page.get_text().strip():
            print(f"⚠ p{n}: 有文字層，可以考慮直接抽文字")
        page.get_pixmap(dpi=DPI).save(OUT_DIR / f"p{n:02d}_full.png")
        if n not in ENGLISH_PAGES:
            print(f"p{n}: 非英文頁，只輸出整頁圖")
            continue
        rect = page.rect
        if n in FULL_WIDTH_PAGES:
            clip, note = rect, "整頁"
        else:
            split, gap = find_gutter(page)
            clip = pymupdf.Rect(rect.x0, rect.y0, rect.x0 + rect.width * split, rect.y1)
            note = f"左欄裁在 {split:.1%}（欄間空白寬 {gap:.1%}）"
        clip = trim_to_content(page, clip)
        pix = page.get_pixmap(dpi=DPI, clip=clip)
        pix.save(OUT_DIR / f"p{n:02d}_en.png")
        print(f"p{n}: 英文頁，{note}，去空白後 {pix.width}x{pix.height}"
              f"（約 {pix.width * pix.height / 1024:.0f} 個圖片 token）")


if __name__ == "__main__":
    main()
