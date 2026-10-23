# 交接文件

最後更新：2026-10-22（Mac，Claude Code）。下一個工作階段先讀 `CLAUDE.md`，再讀這份。

## 一、目前進度

| 步驟 | 狀態 |
|---|---|
| 6.1 OCR | ✅ Roger 確認 OCR 文字正確（2026-10-23）。說明書本身印錯的 5 處已在母本校正（內文改成校正後寫法＋「[校對註] 已校正」）；▼ 在英、德文版都只有圖示，依操作順序推斷為 UP（註記標「推斷」） |
| 6.2 `make_docs.py` | ✅ 11 篇 TXT＋`td235-docs.zip`（已上 Drive，檔案 ID `1I6bknLAUu3dU6QvowY6LuZOwqRO3SXin`）。`ocr/annotations_zh.md` 的中文標題與練習問題 **Roger 已確認**（2026-10-22） |
| 6.3 `RAG01.ipynb` | ✅ 在 Colab T4（學校帳號）整份跑過，老師的檢查全部通過 |
| `rag-data.zip` | ✅ 內文加〔校正〕〔推斷〕標記後重建：28,364 bytes，sha256 `9c62dfef…`。已上 Drive（檔案 ID `1_-jACKgzovK9Pmrdkmq1jNG23Fs_c258`），不登入下載確認相同 |
| 6.4 `RAG02.ipynb` | ✅ Colab 網頁「全部執行」跑通（真的呼叫 Groq）。**繳交用的 Colab 連結**：`https://colab.research.google.com/drive/1xaXf3ZbpQBZZU-ZBNK1ZhHHMU-V8RCOw?usp=sharing`（Drive 檔案 ID `1xaXf3ZbpQBZZU-ZBNK1ZhHHMU-V8RCOw`；不登入可下載，已確認內容和 repo 的 `RAG02.ipynb` 相同、輸出沒有金鑰） |
| 7.1 人設 | ✅ 2026-10-23 定案並在網頁實測（開場白、語氣、口頭禪都有出現）。實測發現模型沒照規則 9 說明「原文印的值」和「推斷」，還編了「圖示向上」→ 規則 9 改寫後再測，問題仍在 → Roger 選 (A) 在內文加〔校正〕〔推斷〕標記、重建（10/23 15.07 重測）：「圖示向上」和旋鈕混淆都消失，但模型仍不主動說原文印錯／是推斷 |
| 8.1／8.2 | ✅ RAG01 第 13.1～13.3 節，練習問題確認後在 T4 正式重跑：A top-1 22/29、top-3 27/29；B（加中文標題）較差 → 維持 A；有答案和離題分數重疊，門檻維持 0.62（`docs/retrieval-eval.md` 最後一節）。13.3 的 `NO_ANSWER_QUESTIONS` Roger 已確認 |
| 8.3～8.5 | ✅ 都在 RAG02：8.5 在第 12 節；8.3（Gradio 勾選並排純 LLM）、8.4（門檻 0.62）在新增的第 15.1 節＋第 16 節。Colab 網頁實測：門檻擋下「藍牙」✅；勾選對照並排 ✅（純 LLM 編出「220 V ±10%」，和說明書的 100–240 V 矛盾） |
| 截圖（第 10 節） | 節點 1～8 全部 ✅（節點 2、3 是 10/23 18.41～19.01）；7.3 各類問題 ✅（10/23 14.29～14.32 六張） |
| git | `8798a15` 已 push；人設與校正的改動**還沒 commit** |

## 二、等 Roger 處理的

1. **寫「我的理解」**：`docs/ai-usage-log.md` 共 13 筆。寫法與每筆的提示見 2026-10-23 Claude 的說明（之後會整理進繳交說明）
2. **針壓／▼**：(A) 已完成並重測（Drive 上兩個檔案已驗證是新版）。Roger 決定**不**再由程式附上標記；繳交說明把「模型不主動說原文印錯／是推斷」寫成已知限制（完整文件裡看得到標記）
3. 繳交說明 `docs/submission.md`：初稿已完成，Roger 已補主題原因與「我的理解」
4. **RAG02 第 18 節加了 `STOP_DEMO` 開關**（10/23：「全部執行」原本會跑到 `demo.close()` 把 Gradio 關掉）✅ 已上傳並驗證：「重新啟動並執行全部」後啟動格 [20]、第 18 節 [21]，Gradio 仍能回答。這次就是用**另一個 Google 帳號**測的（唯讀連結、自己設 `Groq` secret），助教視角的最終驗證已完成
5. 以後本機改了 RAG02，就到 Drive 用「管理版本 → 上傳新版本」更新（**先關掉 Colab 分頁**），連結不變；在 Colab 網頁上改的內容要下載回 repo

## 三、下一步（Claude）

1. Roger 更新 Colab 上的 RAG02 後：不登入下載，確認和 repo 相同、輸出沒有金鑰
2. ✅ 繳交說明初稿 `docs/submission.md`
3. 8.6 多輪對話、8.7 第二知識來源都是選做，**要先問 Roger**（目前建議先不做）

**重建規則**：母本或 `annotations_zh.md` 有改 → 跑 `make_docs.py` → zip 的 sha256 有變，就到 Drive 用「管理版本 → 上傳新版本」覆蓋（檔案 ID 不變）→ 從 RAG01 第 7 節起重建 → 新的 `rag-data.zip` 也用同樣方式更新到 Drive。

## 四、環境

### Mac（目前主要的工作機器）

- repo 在 `~/code/td235-rag`，`origin` 是 `https://github.com/RogerH0711/td235-rag.git`，可以直接 push
- `tools/make_docs.py` 只用標準函式庫：`python3 tools/make_docs.py`
  - ⚠ Mac 的 zlib 和 ROG 不同，**內容沒變也會壓出不同位元組的 `td235-docs.zip`**。跑完先看 `git status`：只有 zip 變、`docs_txt/` 沒變，就用 `git checkout -- td235-docs.zip` 還原，Drive 上那份才不用重傳
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
