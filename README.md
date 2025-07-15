# 🐍 P2E - Python to EXE GUI

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**P2E** is a beginner-friendly GUI tool built with **Tkinter** that helps you convert your Python scripts into standalone Windows `.exe` files using **PyInstaller** — with zero command-line knowledge required.

🔗 **GitHub Repo**: [https://github.com/Varun-SV/P2E](https://github.com/Varun-SV/P2E)

---

## 📁 Folder Structure

```

P2E/
│   README.md                <- You're here!
│
├───python\_code/
│   └───p2e.py               <- Main GUI application script
│
├───streamlit\_version/      <- Future/alternative Streamlit-based web version (optional)
│   ├───lib/
│   └───web-pages/
│
└───windows\_exe/
└───p2e.exe              <- Precompiled executable for Windows (run this if you don’t want to use Python)

```

---

## 💡 Features

✅ Easy GUI to package `.py` files into `.exe`  
✅ Add extra files and folders with destination paths  
✅ Toggle PyInstaller options like:
- `--onefile`
- `--windowed`
- `--icon`
- `--hidden-import`
- `--clean`

✅ Proxy support for restricted networks  
✅ Save and load settings using `.json`  
✅ Real-time progress and log viewer

---

## 🚀 Get Started

### 🖥️ Option 1: Use Pre-Built EXE (No Python Needed)

Just run the file:
```

windows\_exe/p2e.exe

````

---

### 🐍 Option 2: Run From Source

#### Requirements

- Python 3.7+
- Tkinter (included in standard Python)
- Internet access (to auto-install PyInstaller if not installed)

#### Clone and Run

```bash
git clone https://github.com/Varun-SV/P2E.git
cd P2E/python_code
python p2e.py
````

---

## 🔧 How to Use

1. **Select your Python script** (`*.py`)
2. **Choose output folder** for the compiled EXE
3. **Set executable name and icon (optional)**
4. **Add any extra files or folders** to include in the EXE
5. **Configure advanced options** like proxy or hidden imports
6. **Save settings** for reuse or **load** existing config
7. Click **Start Compilation** 🚀

---

## 🧪 Example Use Case

* Script: `your_app.py`
* Icon: `app.ico`
* Output: `dist/`
* Extra folder: `assets/ -> assets/`
* Hidden imports: `numpy`, `matplotlib`

---

## 📦 Output

Depending on your settings, the resulting `.exe` will be saved inside your selected **output directory**, either as a single file (`--onefile`) or in a folder (`--onedir`).

---

## 📄 License

This project is licensed under the **MIT License**.
Feel free to fork, modify, and use it in your own projects.

---

## 🙌 Credits

Created with ❤️ by [Varun S V](https://github.com/Varun-SV)
Inspired by the need for a cleaner GUI for PyInstaller workflows.

---

> “Turn your Python ideas into Windows apps without touching the terminal.”
