[繁體中文](README.md) | [English](README_en.md)

# nowrite · Handwriting Generator

Turn typed text into natural-looking **handwriting images and PDFs**. Redesigned UI (Apple liquid‑glass × Tesla white‑minimal), Traditional‑Chinese‑first with 繁／简／EN switching, plus **offline desktop apps** for macOS and Windows.

Repository: <https://github.com/Miiduoa/nowrite>

> Want a quick look at the UI? Open `redesign-preview.html` in a browser — the top‑right toggle switches Auto / Light / Dark.

---

## ✨ Features

- **Text → handwriting**: render typed text into handwriting‑style images, multi‑page supported.
- **Custom fonts**: upload a `.ttf` for your own handwriting style.
- **Backgrounds**: upload a background image, or just give a width/height and lined paper is generated automatically.
- **Fine‑grained controls**: margins, font size, line/word spacing, stroke jitter & rotation, ink depth, strike‑through marks.
- **Import text**: type directly, or upload `.txt / .pdf / .docx` to extract content.
- **Live preview & batch export**: generate a full set of images (zipped) or export a PDF.
- **UI**: liquid‑glass + white minimal, auto light/dark, 繁／简／EN language switch.
- **Offline desktop**: the app bundles the backend — no network required to generate.

---

## 🚀 Get the desktop app (offline, recommended)

Easiest: download a prebuilt installer from this repo's **Actions** (or **Releases**):

- macOS: `手寫生成-x.y.z-arm64.dmg`
- Windows: `手寫生成-x.y.z-setup.exe`

Or build it yourself (see [`DESKTOP_BUILD.md`](DESKTOP_BUILD.md)):

- **macOS one‑click**: `bash build-dmg.command`
- **Build mac + win in the cloud**: run `bash push-to-github.command` to push, then GitHub Actions builds both — download from the Actions tab.

> The app is unsigned (personal use): on macOS right‑click → Open the first time; on Windows click "More info → Run anyway".

---

## 🧑‍💻 Local development (web)

Requirements: Node.js 18+, Python 3.10–3.12.

**Backend**

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
# requirements.txt is UTF-16; convert to UTF-8 first
python -c "open('req.txt','w',encoding='utf-8').write(open('requirements.txt',encoding='utf-16').read())"
pip install -r req.txt
python run_server.py                                   # http://127.0.0.1:5005
```

**Frontend**

```bash
cd frontend
npm install
npm run serve                                          # http://localhost:8080 (/api proxied to 5005)
```

---

## 🐳 Self‑host (Docker, advanced)

The repo ships `dockerfile.frontend` and `dockerfile.backend`; build the images and deploy (backend on `5005`, frontend on `80`).
Note: the root `docker-compose.yml` pulls upstream public images by default — to deploy *this* project, build the images from source instead.

---

## 🏗️ Tech stack

- **Frontend**: Vue 3, Vue Router, Vuex, vue-i18n, Bootstrap 5, SweetAlert2, axios
- **Backend**: FastAPI, Uvicorn, [handright], Pillow, OpenCV, scikit-learn, PyMuPDF, python-docx, PyPDF2; task state in **SQLite**
- **Desktop**: Electron + electron-builder; backend bundled as a **PyInstaller** sidecar
- **CI**: GitHub Actions builds macOS / Windows installers

---

## 📁 Project structure

```
frontend/                     Vue 3 frontend (redesigned UI, i18n 繁/简/EN)
backend/                      FastAPI backend (rendering, file extraction, SQLite tasks)
  run_server.py               entry point for the offline desktop backend
desktop/                      Electron shell & packaging (mac dmg / win nsis)
ttf_files/                    bundled fonts
.github/workflows/build.yml   CI: build macOS + Windows
build-dmg.command             macOS one-click build
push-to-github.command        push & overwrite the GitHub repo
DESKTOP_BUILD.md              detailed desktop / CI build guide
```

---

## ⚙️ How the backend works

Submit a task → write to SQLite → return a `task_id` immediately → a background worker renders in a queue (concurrency limited by a semaphore) → the client gets progress/results via **WebSocket or polling**. In the desktop app, the frontend's `/api` calls automatically target the bundled backend at `127.0.0.1:5005`.

---

## 📄 License & credits

Released under the **MIT** License (see [`LICENSE`](LICENSE)).

The UI redesign (Apple liquid‑glass × Tesla minimal), Traditional‑Chinese localization, and offline desktop packaging were done in this project. Core handwriting rendering uses the open‑source **handright** library, and this work is derived from the open‑source **handwriting-web** project (MIT, © Liuweiqing).

[handright]: https://github.com/Gsllchb/Handright
