"""母本 → 老師 RAG01 格式的「一節一檔」TXT → td235-docs.zip

用法：.venv/Scripts/python tools/make_docs.py

- 讀 ocr/td235_manual_en.md，依 `## ` 章節切成一節一檔，寫到 docs_txt/（會先清掉舊的 .txt）
- 太短的章節（英文字數少於 MIN_WORDS）併到同頁相鄰章節：優先併進前一節，該頁沒有前一節就併進下一節
- 中文標題與【檢索練習問題】讀自 ocr/annotations_zh.md（由 Roger 撰寫或確認）
- 相關圖從內文的「Fig. N」找出，附上圖所在的頁碼（圖都印在偶數德文頁）
- 最後打包成 td235-docs.zip（檔案放在 zip 根目錄，時間戳固定，內容不變時 sha256 也不變）
"""
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "ocr" / "td235_manual_en.md"
ANNOTATIONS = ROOT / "ocr" / "annotations_zh.md"
OUT_DIR = ROOT / "docs_txt"
ZIP_PATH = ROOT / "td235-docs.zip"

MIN_WORDS = 30
MAX_WORDS = 1000  # 粗略上限；EmbeddingGemma 2 的 2048 tokens 由 RAG01 第 9 節精確檢查
NOTE_PREFIX = "[校對註]"
FIGURE_PAGES = {1: 4, 2: 4, 3: 4, 4: 4, 5: 6, 6: 6, 7: 8, 8: 8, 9: 8, 10: 10, 11: 10}
DOC_TYPE = "Thorens TD 235 原廠操作說明書英文原文（OCR 後人工校對）"
SOURCE = "Thorens TD 235 Operating Instructions, p.{page}"
ZIP_DATE = (1980, 1, 1, 0, 0, 0)

PAGE_RE = re.compile(r"^<!-- page: (\d+) -->$")
HEADING_RE = re.compile(r"^## (.+)$")
FIG_RE = re.compile(r"\bFig\.\s*(\d+)", re.IGNORECASE)


def read_sections(text):
    """回傳 [{"title", "page", "body"}]。檔頭說明等 HTML 註解不收，頁碼標記保留。"""
    text = re.sub(r"<!--(?! page: \d+ -->).*?-->", "", text, flags=re.S)
    sections, page = [], None
    for line in text.splitlines():
        if m := PAGE_RE.match(line):
            page = int(m.group(1))
        elif m := HEADING_RE.match(line):
            if page is None:
                raise ValueError(f"章節「{m.group(1)}」前面沒有頁碼標記")
            sections.append({"title": m.group(1).strip(), "page": page, "lines": []})
        elif sections:
            sections[-1]["lines"].append(line)
        elif line.strip():
            raise ValueError(f"第一個章節之前有內文：{line!r}")
    for s in sections:
        s["body"] = "\n".join(s.pop("lines")).strip()
        if not s["body"]:
            raise ValueError(f"p{s['page']}「{s['title']}」沒有內文")
    return sections


def english_words(body):
    """校對註不是原文，不算字數。"""
    return sum(len(line.split()) for line in body.splitlines() if not line.startswith(NOTE_PREFIX))


def merge_short(sections):
    """回傳 [[section, ...], ...]，每個內層清單是一篇文件。"""
    docs, pending = [], []
    for s in sections:
        short = english_words(s["body"]) < MIN_WORDS
        if pending and pending[0]["page"] != s["page"]:
            raise ValueError(f"p{pending[0]['page']}「{pending[0]['title']}」太短，但同頁沒有下一節可以併")
        if short and not pending and docs and docs[-1][-1]["page"] == s["page"]:
            docs[-1].append(s)
        elif short:
            pending.append(s)
        else:
            docs.append(pending + [s])
            pending = []
    if pending:
        raise ValueError(f"p{pending[0]['page']}「{pending[0]['title']}」太短，但後面沒有章節可以併")
    return docs


def read_annotations(text):
    """回傳 {英文標題: {"title_zh", "confirmed", "questions"}}。"""
    result = {}
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        title, _, rest = block.partition("\n")
        zh = re.search(r"^中文標題[：:][ \t]*(.*)$", rest, flags=re.M)
        confirmed = re.search(r"^確認[：:][ \t]*(.*)$", rest, flags=re.M)
        result[title.strip()] = {
            "title_zh": zh.group(1).strip() if zh else "",
            "confirmed": bool(confirmed) and confirmed.group(1).strip() == "是",
            "questions": [l[2:].strip() for l in rest.splitlines() if l.startswith("- ") and l[2:].strip()],
        }
    return result


def snake_case(title):
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")


def render_doc(group, note):
    page = group[0]["page"]
    title = " / ".join(s["title"] for s in group)
    if len(group) == 1:
        body = group[0]["body"]
    else:  # 併起來的章節保留各自的小標題
        body = "\n\n".join(f"{s['title']}\n{s['body']}" for s in group)
    figures = sorted({int(n) for n in FIG_RE.findall(body)})
    unknown = [n for n in figures if n not in FIGURE_PAGES]
    if unknown:
        raise ValueError(f"「{title}」提到不認識的圖號：{unknown}")
    figure_text = ", ".join(f"Fig. {n} (p.{FIGURE_PAGES[n]})" for n in figures)
    text = (
        f"標題：{title}\n"
        f"中文標題：{note['title_zh']}\n"
        f"頁碼：{page}\n"
        f"相關圖：{figure_text}\n"
        f"資料類型：{DOC_TYPE}\n"
        f"來源：{SOURCE.format(page=page)}\n"
        f"\n【內容】\n{body}\n"
        f"\n【檢索練習問題】\n" + "\n".join(note["questions"]) + "\n"
    )
    return title, text, figures


def main():
    sections = read_sections(MASTER.read_text(encoding="utf-8"))
    groups = merge_short(sections)
    annotations = read_annotations(ANNOTATIONS.read_text(encoding="utf-8"))

    titles = [" / ".join(s["title"] for s in g) for g in groups]
    missing = [t for t in titles if t not in annotations]
    extra = [t for t in annotations if t not in titles]
    if missing or extra:
        raise ValueError(f"annotations_zh.md 的標題對不上。缺少：{missing}；多出：{extra}")
    for t in titles:
        if not annotations[t]["title_zh"] or not annotations[t]["questions"]:
            raise ValueError(f"「{t}」缺少中文標題或檢索練習問題")

    OUT_DIR.mkdir(exist_ok=True)
    for old in OUT_DIR.glob("*.txt"):
        old.unlink()
    unconfirmed = []
    print(f"{'檔名':<52}{'頁':>3}{'字數':>6}  相關圖")
    for number, group in enumerate(groups, start=1):
        title, text, figures = render_doc(group, annotations[titles[number - 1]])
        words = sum(english_words(s["body"]) for s in group)
        if words > MAX_WORDS:
            raise ValueError(f"「{title}」有 {words} 字，請依段落拆開")
        if "�" in text:
            raise ValueError(f"「{title}」含有替代字元 \\ufffd")
        name = f"{number:02d}_{snake_case(title)}.txt"
        (OUT_DIR / name).write_text(text, encoding="utf-8", newline="\n")
        if not annotations[title]["confirmed"]:
            unconfirmed.append(title)
        merged = "（併入：" + "、".join(s["title"] for s in group[1:]) + "）" if len(group) > 1 else ""
        print(f"{name:<52}{group[0]['page']:>3}{words:>6}  {', '.join(map(str, figures)) or '-'}{merged}")

    paths = sorted(OUT_DIR.glob("*.txt"))
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            info = zipfile.ZipInfo(path.name, date_time=ZIP_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    with zipfile.ZipFile(ZIP_PATH) as archive:
        assert archive.testzip() is None
        for name in archive.namelist():
            archive.read(name).decode("utf-8")  # 不是 UTF-8 會直接報錯
    print(f"\n共 {len(paths)} 篇，已打包 {ZIP_PATH.name}（{ZIP_PATH.stat().st_size:,} bytes）")
    if unconfirmed:
        print(f"⚠ 還有 {len(unconfirmed)} 篇的中文標題／檢索練習問題是 AI 初稿、尚未確認：")
        for t in unconfirmed:
            print("  -", t)


if __name__ == "__main__":
    main()
