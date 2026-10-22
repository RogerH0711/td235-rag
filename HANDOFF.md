# 交接文件

最後更新：2026-10-22（ROG，Claude Code 透過 Mac SSH 連入）。下一個工作階段先讀 `CLAUDE.md`，再讀這份。

## 一、目前進度

| 步驟 | 狀態 |
|---|---|
| 6.1 OCR | ✅ 6 頁英文頁 OCR 完成，Claude 已初校。母本 `ocr/td235_manual_en.md` **待 Roger 校對確認** |
| 6.2 `make_docs.py` | ✅ 產出 11 篇 TXT＋`td235-docs.zip`。中文標題與檢索練習問題是 AI 初稿，**待 Roger 確認**（`ocr/annotations_zh.md`） |
| `td235-docs.zip` 上 Drive | ✅ 檔案 ID `1I6bknLAUu3dU6QvowY6LuZOwqRO3SXin`。已實測不用登入就能直接下載，sha256 `b7534c5e…`，和本機相同 |
| 6.3 `RAG01.ipynb` | ✅ 已寫好，`DOCS_ZIP_URL` 已填。本機在假模組下跑過第 2～7 節。**模型、FAISS、匯出還沒在 Colab 上跑過** |
| `rag-data.zip` | ❌ 還沒產生 |
| 6.4 `RAG02.ipynb` | ❌ 還沒開始 |
| 7.1 人設 | ❌ 由 Roger 決定 |
| 8 加分功能 | ❌ 還沒開始 |
| 截圖（第 10 節） | 節點 1 ✅；節點 2、3 待截（Roger 說之後再截） |
| git | 已 commit 在 `main`，**還沒 push**，GitHub 上也還沒有 repo（見第四節） |

## 二、等 Roger 處理的

1. **校對母本** `ocr/td235_manual_en.md`，和 `ocr/pages/pNN_full.png` 並排看（圖只在 ROG 上，見第四節）。重點：5 則 `[校對註]` 的文字（AI 擬的）、p7 對照表、p13 的 22 行規格。確認後把檔頭的「Roger 確認：待確認」改成日期。
2. **確認 `ocr/annotations_zh.md`**：練習問題要寫成自己真的會問的話，它們是檢索評估的測試題。改完把「確認：待確認」改成「是」，再跑 `python3 tools/make_docs.py`。
3. **push 到 GitHub**：照第四節的指令操作。
4. **Colab CLI 用學校帳號登入**：照第四節操作，登入要本人在瀏覽器完成。
5. 截圖節點 2、3；決定人設（7.1）。

## 三、下一步（Claude）

1. 用 Colab CLI（學校帳號）跑 `RAG01.ipynb`，GPU 用 T4，配不到就用 CPU（11 篇用 CPU 也夠快）。
   - ⚠ 最後一格的 `files.download()` 要靠瀏覽器前端，用 CLI 的 `colab exec` 執行很可能沒有作用。這點還沒驗證。替代做法：用 `colab ls`／`colab download` 從 VM 取回 `rag-data.zip`（它在 `/tmp/rag_index_*_download/` 底下），或改用 Colab 網頁執行。
   - 先讀 `colab skill`，內建說明寫得很完整。用完一定要 `colab stop -s <名稱>`。
2. Roger 把 `rag-data.zip` 上傳到 Drive（分享：知道連結的任何人）→ 填進 RAG02 的 `RAG_ZIP_URL`，用 `urllib` 實測可以直接下載。
3. 照 `CLAUDE.md` 6.4 改寫 `RAG02.ipynb`。做法和 RAG01 一樣：用一次性腳本從 `reference/` 轉出來，只改指定的 cell，清掉輸出，再用假模組在本機跑不需要模型的 cell。
4. 第 8 節加分功能，從 8.1 檢索評估、8.2 跨語言實驗做起。

**重建規則**：母本或 `annotations_zh.md` 有改 → 跑 `make_docs.py` → zip 的 sha256 有變，就到 Drive 用「管理版本 → 上傳新版本」覆蓋（檔案 ID 不變）→ 從 RAG01 第 7 節起重建 → 新的 `rag-data.zip` 也用同樣方式更新到 Drive。

## 四、環境

### push 到 GitHub（Roger 在 Mac 上執行）

ROG 的 SSH 工作階段不能 push：Windows 認證管理員（wincredman）在 SSH 底下讀不到，ROG 上也沒有 GitHub 的 SSH key。改成從 Mac push：

1. 在 GitHub 網頁建立**空的 private repo** `td235-rag`（不要勾 README、.gitignore、license）
2. 在 Mac 上執行（`rog` 換成你 ssh 用的主機名稱）：
   ```bash
   cd ~/code
   scp rog:td235-rag.bundle .
   git clone td235-rag.bundle td235-rag
   cd td235-rag
   git remote set-url origin https://github.com/RogerH0711/td235-rag.git
   git push -u origin main
   ```
3. ROG 上的 repo 已經設好 `origin` 指向同一個網址。之後回到 ROG 桌面（不是透過 SSH）就能直接 `git pull`

### Mac（之後主要在這裡工作）

- `tools/make_docs.py` 只用到 Python 標準函式庫，直接 `python3 tools/make_docs.py` 就能跑
- `tools/render_pages.py` 和 OCR 只有重跑 OCR 時才需要。原始 PDF（`source_pdf/`）和頁面圖（`ocr/pages/`）沒進 git，只在 ROG 上；要在 Mac 校對看原圖，要從 ROG 複製過去：`scp -r rog:TAICA/RAG/ocr/pages ~/code/td235-rag/ocr/`
- **Colab CLI**（Google 的 `google-colab-cli`，ROG 上裝的是 0.7.4 版）：
  ```bash
  uv tool install google-colab-cli      # 或 pip install google-colab-cli
  colab --help                          # 以實際輸出為準
  ```
  - 預設登入方式的說法不一致：0.7.4 版的 `--help` 寫預設是 `oauth2`，README 和內建 SKILL.md 寫 `adc`。ROG 上**沒有** `~/.colab-cli-oauth-config.json`，卻已經有登入 token（`~/.config/colab-cli/token.json`），推測 CLI 內建了預設的 OAuth client。Mac 上裝好後，直接執行 `colab sessions`，依實際跳出的流程登入
  - 登入時**選學校帳號 `f74146115@gs.ncku.edu.tw`**。token 和任何 OAuth 設定檔都**不要放進 repo**
  - 確認身分：`colab whoami`（隱藏的除錯指令，會印出目前登入的信箱）
  - 學校帳號是 Google Workspace for Education，可能被管理員關掉 Colab，或配不到 GPU。`colab new -s rag01 --gpu T4` 回 400 的話，就去掉 `--gpu`，改用 CPU
  - 也可以改用 ADC 登入（`gcloud auth application-default login --scopes=openid,https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/colaboratory`），詳見 `colab skill`

### ROG（家裡的 Windows，RTX 3070）

- Colab CLI 在 **WSL Ubuntu** 裡（`/home/roger/.local/bin/colab`），用 uv tool 安裝。登入的是**個人 Pro 帳號**；這個專案要用學校帳號
- OCR：Ollama 0.40.6（Windows 原生），模型 `qwen3-vl:4b-instruct`。pdf2md 在 `C:\Users\USER\GitHubCode\code\python\pdf2md`
- `.venv`（Python 3.14：pymupdf、pillow、pandas），只有 ROG 有
- Windows 上用 `python -I` 會忽略 `PYTHONIOENCODING`，中文輸出要改用 `-X utf8`

## 五、已經定案的決定（細節在 `CLAUDE.md` 和 `docs/ai-usage-log.md`）

- OCR：pdf2md＋`qwen3-vl:4b-instruct`、300 dpi、自動裁出英文欄並去掉空白、`--ctx 8192`
- 原文本身的錯誤：**照原文照錄＋`[校對註]`**（Roger 選的），校對註會一起送進 RAG 文字
- 短章節（英文字數 < 30）併到同頁相鄰章節，共 11 篇
- 「相關圖」寫成 `Fig. 7 (p.8)`，附上圖實際所在的德文頁
- `extract_rag_text()` 沿用老師原版；目前 embedding 只用英文（8.2 的 A 方案），要不要加中文標題由實驗數據決定
- 兩個 zip 都放 Google Drive；更新一律用「管理版本」，保持檔案 ID 不變
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
| `docs/ai-usage-log.md` | 註三 AI 使用紀錄（「我的理解」欄留給 Roger 填） |
