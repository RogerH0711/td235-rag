# 交接文件

最後更新：2026-10-22（Mac，Claude Code）。下一個工作階段先讀 `CLAUDE.md`，再讀這份。

## 一、目前進度

| 步驟 | 狀態 |
|---|---|
| 6.1 OCR | ✅ 6 頁英文頁 OCR 完成，Claude 已初校。母本 `ocr/td235_manual_en.md` **待 Roger 校對確認** |
| 6.2 `make_docs.py` | ✅ 11 篇 TXT＋`td235-docs.zip`（已上 Drive，檔案 ID `1I6bknLAUu3dU6QvowY6LuZOwqRO3SXin`）。中文標題與練習問題是 AI 初稿，**待 Roger 確認**（`ocr/annotations_zh.md`） |
| 6.3 `RAG01.ipynb` | ✅ 在 Colab T4（學校帳號）整份跑過，老師的檢查全部通過 |
| `rag-data.zip` | ✅ 28,322 bytes，sha256 `df8650a0…`。已上 Drive，檔案 ID `1_-jACKgzovK9Pmrdkmq1jNG23Fs_c258`；用 `urllib`、不登入實測可下載，sha256 和本機相同 |
| 6.4 `RAG02.ipynb` | ✅ Roger 在 Colab 網頁「全部執行」跑通到 Gradio（真的呼叫 Groq），已重跑一次確認粗體、圖所在頁、少補步驟有改善。之後新增 `normalize_citations()`（模型堅持寫【doc_009】），**這版還沒在 Colab 上跑** |
| 7.1 人設 | ❌ `RAG02.ipynb` 第 9 節的 `PERSONA` 是暫時的中性句子，由 Roger 撰寫 |
| 8.1／8.2 | 🔶 初步數據在 `docs/retrieval-eval.md`（用的是待確認的練習問題）。**還沒寫成 RAG01 的新增 cell** |
| 8.3～8.5 | 8.5（頁碼與圖號提示）已併進 RAG02 第 12 節；8.3、8.4 還沒做 |
| 截圖（第 10 節） | 節點 1、4、6 ✅；節點 2、3 待截；節點 8 等修正後重跑再截 |
| git | `main` 已 push 到 GitHub。本次的改動**還沒 commit** |

## 二、等 Roger 處理的

1. **Colab 上的 RAG02 要更新成最新版**：Drive 的 Colab Notebooks 裡對 `RAG02.ipynb` 按右鍵 →「檔案資訊 → 管理版本 → 上傳新版本」（**先關掉 Colab 分頁**，不然自動儲存可能把舊版存回去）。可以等 8.3／8.4 改完再一起更新。重跑後看狀態列是否不再誤報「回答未附文件編號」，截圖當節點 8 的「修正後」。以後在 Colab 網頁上改的內容要下載回 repo
2. **寫人設**（7.1）：取代 RAG02 第 9 節的 `PERSONA`。需要的話 Claude 可以提 2～3 個方向。定稿 prompt 時一起處理：模型仍會在結尾加「請參考官方維修手冊」（規則 3 已寫明不要，它還是寫；見 `docs/ai-usage-log.md`）
3. **校對母本**、**確認 `ocr/annotations_zh.md`**（同上次）。練習問題是檢索評估的測試題，定稿後要重跑評估
4. 截圖節點 2、3

## 三、下一步（Claude）

1. **8.1／8.2 寫成 RAG01 的新增 cell**（第 13 節後，標「🔧 新增」）：練習問題 → top-1／top-3 命中率表；A/B 另建暫時索引比較，不影響匯出的索引。練習問題定稿後在 T4 上重跑，結果更新到 `docs/retrieval-eval.md`
2. **8.4 門檻**：初步數據顯示說明書沒寫但跟唱盤有關的問題（轉速、清潔）分數和有答案的題目一樣高，門檻只能擋明顯離題的問題。設計和說明要照這個事實寫（見 `docs/retrieval-eval.md`）
3. **8.3**：純 LLM／RAG 對照搬進 Gradio
4. 每次改完 RAG02，用測試版在 CLI 上跑一次（做法見第四節）

**重建規則**：母本或 `annotations_zh.md` 有改 → 跑 `make_docs.py` → zip 的 sha256 有變，就到 Drive 用「管理版本 → 上傳新版本」覆蓋（檔案 ID 不變）→ 從 RAG01 第 7 節起重建 → 新的 `rag-data.zip` 也用同樣方式更新到 Drive。

## 四、環境

### Mac（目前主要的工作機器）

- repo 在 `~/code/td235-rag`，`origin` 是 `https://github.com/RogerH0711/td235-rag.git`，可以直接 push
- `tools/make_docs.py` 只用標準函式庫：`python3 tools/make_docs.py`
- 本機 python.org 版的 `python3` 沒裝 CA 憑證，`urllib` 連 HTTPS 會 `CERTIFICATE_VERIFY_FAILED`。測下載網址改用 macOS 內建的 `/usr/bin/python3`（或 `curl -sSL`）
- **Colab CLI**：`google-colab-cli` 0.7.5（uv tool），已用學校帳號 `f74146115@gs.ncku.edu.tw` 登入（`colab whoami` 確認；token 在 `~/.config/colab-cli/`，不進 repo）
  - 學校帳號配得到 T4：`colab new -s rag01 --gpu T4`
  - `colab exec -s <名稱> -f X.ipynb --timeout 900`：預設 timeout 只有 30 秒，裝套件和下載模型會超過，一定要加 `--timeout`
  - **CLI 讀不到 Colab Secrets**：`userdata.get()` 會等瀏覽器前端回應然後逾時。需要 `Groq` 的部分只能在 Colab 網頁上跑
  - `files.download()` 在 CLI 下沒有作用；改用 `colab download -s <名稱> <VM 路徑> <本機路徑>`。RAG01 的輸出在 VM 的 `/tmp/rag_index_*_download/rag-data.zip`
  - RAG02 測試版的做法：`colab upload` 把 `rag-data.zip` 傳到 `/content/`，`RAG_ZIP_URL` 換成 `file:///content/rag-data.zip`（`urllib` 支援 `file://`）、Groq 那格換成假 client、刪掉 `demo.launch()` 和 `demo.close()` 兩格
  - 用完一定要 `colab stop -s <名稱>`，再用 `colab sessions` 確認沒有殘留
- 原始 PDF（`source_pdf/`）和頁面圖（`ocr/pages/`）只在 ROG 上；要在 Mac 校對看原圖：`scp -r rog:TAICA/RAG/ocr/pages ~/code/td235-rag/ocr/`

### ROG（家裡的 Windows，RTX 3070）

- 透過 SSH 連入時不能 push（讀不到 Windows 認證管理員、沒有 GitHub SSH key），要在 ROG 桌面或 Mac push
- Colab CLI 在 **WSL Ubuntu** 裡，登入的是**個人 Pro 帳號**；這個專案要用學校帳號
- OCR：Ollama 0.40.6（Windows 原生），模型 `qwen3-vl:4b-instruct`。pdf2md 在 `C:\Users\USER\GitHubCode\code\python\pdf2md`
- `.venv`（Python 3.14：pymupdf、pillow、pandas），只有 ROG 有
- Windows 上用 `python -I` 會忽略 `PYTHONIOENCODING`，中文輸出要改用 `-X utf8`

## 五、已經定案的決定（細節在 `CLAUDE.md` 和 `docs/ai-usage-log.md`）

- OCR：pdf2md＋`qwen3-vl:4b-instruct`、300 dpi、自動裁出英文欄並去掉空白、`--ctx 8192`
- 原文本身的錯誤：**照原文照錄＋`[校對註]`**（Roger 選的），校對註會一起送進 RAG 文字；RAG02 的規則第 9 條告訴模型校對註不是原廠內容
- 短章節（英文字數 < 30）併到同頁相鄰章節，共 11 篇
- 「相關圖」寫成 `Fig. 7 (p.8)`，附上圖實際所在的德文頁
- `extract_rag_text()` 沿用老師原版，embedding 只用英文（8.2 的 A 方案）。初步實驗 B（加中文標題）沒有比較好，練習問題定稿後重跑再定案
- 兩個 zip 都放 Google Drive；更新一律用「管理版本」，保持檔案 ID 不變
- RAG02 的 notebook 設定用 CPU（助教不需要 GPU 配額；查詢只算一個問題的向量，CPU 夠快）
- git：`.gitattributes` 讓文字檔一律用 LF（Windows、macOS 之間同步用）

## 六、檔案地圖

| 路徑 | 內容 |
|---|---|
| `ocr/td235_manual_en.md` | 英文母本（含 `[校對註]`） |
| `ocr/annotations_zh.md` | 中文標題、檢索練習問題（待確認） |
| `ocr/raw/`、`ocr/trial/` | 未校對的 OCR 原始輸出、p9 試跑的三種設定 |
| `tools/render_pages.py` | PDF → 300 dpi 圖，裁英文欄（需要 pymupdf＋`source_pdf/`） |
| `tools/make_docs.py` | 母本 → `docs_txt/` 11 篇 → `td235-docs.zip` |
| `RAG01.ipynb` | 建庫 notebook（老師 RAG_01 改寫） |
| `RAG01_output.ipynb` | CLI 執行 RAG01 的結果（含輸出，沒進 git） |
| `rag-data.zip` | RAG01 的輸出（沒進 git，要上 Drive） |
| `RAG02.ipynb` | 問答 notebook（老師 RAG_02 改寫） |
| `docs/ai-usage-log.md` | 註三 AI 使用紀錄（「我的理解」欄留給 Roger 填） |
| `docs/retrieval-eval.md` | 檢索實驗紀錄（8.1／8.2／8.4） |
