# 🐍 P2E - Python to EXE Converter (v2.0)

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/Varun-SV/P2E)

**P2E** is a modern, modular tool for converting Python scripts into standalone executables. Built with a clean architecture and intuitive interfaces, it makes PyInstaller accessible to everyone.

🔗 **GitHub**: [https://github.com/Varun-SV/P2E](https://github.com/Varun-SV/P2E)

---

## 🎯 What's New in v2.0

P2E has been completely **reimagined** while keeping the essence of the original:

### ✨ Modern Architecture
- **Modular Design**: Clear separation of concerns with `core`, `cli`, `web`, and `utils` modules
- **Type Safety**: Full type hints throughout the codebase
- **Configuration Management**: YAML/JSON config file support
- **Better Error Handling**: Comprehensive validation and error messages

### 🚀 Multiple Interfaces
- **Modern CLI**: Rich, colorful command-line interface with progress bars
- **Web UI**: Clean, intuitive Streamlit-based web interface
- **Programmatic API**: Use P2E as a library in your own tools

### 🎨 Enhanced Features
- Configuration templates for common use cases
- Build history tracking
- Real-time build progress
- Example projects included
- Better proxy support
- Comprehensive logging

---

## 📁 Project Structure

```
P2E/
├── p2e/                      # Main package
│   ├── core/                 # Core conversion logic
│   │   ├── config.py         # Build configuration
│   │   └── converter.py      # PyInstaller wrapper
│   ├── cli/                  # Command-line interface
│   │   └── app.py            # CLI application
│   ├── web/                  # Web interface
│   │   └── app.py            # Streamlit web app
│   ├── utils/                # Utilities
│   │   ├── logger.py         # Logging utilities
│   │   └── validators.py     # Validation functions
│   └── templates/            # Configuration templates
│       ├── basic_config.yaml
│       └── gui_app_config.yaml
├── examples/                 # Example scripts
│   ├── simple_example.py     # Console app example
│   └── gui_example.py        # GUI app example
├── python_code/              # Legacy code (v1.0)
│   ├── p2e.py                # Original Tkinter GUI
│   └── streamlit_app.py      # Original Streamlit app
├── tests/                    # Test suite
├── run_cli.py                # CLI entry point
├── run_web.py                # Web UI entry point
├── requirements.txt          # Dependencies
└── README.md                 # You are here!
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Varun-SV/P2E.git
cd P2E

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

### Option 1: Command-Line Interface (Recommended)

```bash
# Build a script with default settings
p2e build script.py

# Customize the build
p2e build script.py --name MyApp --windowed --icon app.ico

# Use a configuration file
p2e build script.py --config config.yaml

# See all options
p2e build --help
```

### Option 2: Web Interface

```bash
# Start the web interface
python run_web.py

# Or use streamlit directly
streamlit run p2e/web/app.py
```

Then open your browser to the URL shown (typically http://localhost:8501)

### Option 3: Programmatic Usage

```python
from pathlib import Path
from p2e import BuildConfig, PyConverter

# Create configuration
config = BuildConfig(
    script_path=Path("my_script.py"),
    exe_name="MyApp",
    one_file=True,
    console_mode=False,
    icon_path=Path("icon.ico")
)

# Build the executable
converter = PyConverter(config)
success = converter.build()

if success:
    print(f"Built: {converter.get_output_path()}")
```

---

## 💡 Features

### Core Features (Preserved from v1.0)
✅ Easy conversion of `.py` files to `.exe`  
✅ Support for additional files and folders  
✅ PyInstaller options: `--onefile`, `--windowed`, `--icon`, etc.  
✅ Hidden imports management  
✅ Proxy support for restricted networks  
✅ Settings save/load functionality  
✅ Real-time progress and logging  

### New Features (v2.0)
🎯 **Modular Architecture**: Clean, maintainable codebase  
🎯 **Modern CLI**: Rich terminal interface with colors and progress bars  
🎯 **Config Files**: YAML/JSON configuration support  
🎯 **Templates**: Pre-configured templates for common scenarios  
🎯 **Better Validation**: Comprehensive error checking  
🎯 **Build History**: Track your builds in the web interface  
🎯 **Examples**: Included example scripts to get started  
🎯 **Type Safety**: Full type hints for better IDE support  

---

## 📖 Usage Examples

### Example 1: Simple Console App

```bash
# Build a console application
p2e build examples/simple_example.py --name HelloApp
```

### Example 2: GUI Application

```bash
# Build a windowed GUI app (no console)
p2e build examples/gui_example.py --name MyGUI --windowed --icon p2e.ico
```

### Example 3: Using Configuration File

Create `config.yaml`:
```yaml
script_path: "my_app.py"
exe_name: "MyApp"
one_file: true
console_mode: false
icon_path: "icon.ico"
hidden_imports:
  - "pandas"
  - "numpy"
additional_files:
  - ["data.csv", "data.csv"]
```

Then build:
```bash
p2e build my_app.py --config config.yaml
```

### Example 4: Advanced CLI Options

```bash
# Build with all the bells and whistles
p2e build script.py \
    --name AdvancedApp \
    --output ./dist \
    --windowed \
    --icon app.ico \
    --add-file data.json:data.json \
    --add-folder assets:assets \
    --hidden-import requests \
    --hidden-import PIL \
    --proxy http://proxy:8080 \
    --clean
```

---

## 🔧 Configuration

### Configuration File Format

P2E supports both YAML and JSON configuration files. Here's a complete example:

```yaml
# Build configuration
script_path: "app.py"
output_dir: "./dist"
exe_name: "MyApplication"

# Build mode
one_file: true
console_mode: false
windowed: true
clean_build: true

# Icon
icon_path: "resources/icon.ico"

# Additional resources
additional_files:
  - ["config.json", "config.json"]
  - ["data.db", "data.db"]

additional_folders:
  - ["assets/", "assets/"]
  - ["templates/", "templates/"]

# Hidden imports
hidden_imports:
  - "numpy"
  - "pandas"
  - "requests"
  - "PIL"

# Network
use_proxy: false
proxy_url: null

# Advanced
upx_compress: false
strip_symbols: false
extra_args: []
```

### Saving/Loading Configurations

```bash
# Save current settings to a config file
p2e save-config my_script.py myconfig.yaml

# View a configuration file
p2e show-config myconfig.yaml

# Use a configuration file for building
p2e build script.py --config myconfig.yaml
```

---

## 🎓 CLI Reference

### Main Commands

```bash
p2e --help              # Show help
p2e --version           # Show version
p2e info                # Display information about P2E
p2e build SCRIPT        # Build an executable
p2e save-config         # Save a configuration
p2e show-config         # Display a configuration
```

### Build Options

```bash
-o, --output PATH       # Output directory
-n, --name TEXT         # Executable name
--onefile / --onedir    # Build mode (default: onefile)
--console / --windowed  # Window mode (default: console)
-i, --icon PATH         # Icon file (.ico)
--clean / --no-clean    # Clean build artifacts (default: clean)
--add-file SRC:DST      # Add a file (can use multiple times)
--add-folder SRC:DST    # Add a folder (can use multiple times)
--hidden-import MODULE  # Add hidden import (can use multiple times)
--proxy URL             # Proxy URL for pip installs
--config PATH           # Load configuration from file
```

---

## 🌐 Web Interface Guide

The web interface provides an intuitive GUI for building executables:

1. **Upload** your Python script
2. **Configure** build settings (name, mode, icon, etc.)
3. **Add** any additional files or dependencies
4. **Build** and download your executable
5. **Track** your build history

Features:
- Drag-and-drop file upload
- Real-time build progress
- Build history tracking
- Configuration save/load
- Detailed build logs

---

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=p2e
```

### Code Quality

```bash
# Format code
black p2e/

# Type checking
mypy p2e/

# Linting
pylint p2e/
```

---

## 🔄 Migration from v1.0

If you're upgrading from P2E v1.0, here's what changed:

### What's Preserved
- All core PyInstaller functionality
- Basic build options (onefile, windowed, icon, etc.)
- Additional files and folders support
- Hidden imports
- Proxy support

### What's New
- Modern CLI with `p2e` command
- Configuration file support
- Better project structure
- Type hints throughout
- More examples and templates

### Legacy Support
The old scripts are still available in `python_code/` for backward compatibility:
- `python_code/p2e.py` - Original Tkinter GUI
- `python_code/streamlit_app.py` - Original Streamlit app

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙌 Credits

**Created with ❤️ by [Varun S V](https://github.com/Varun-SV)**

Reimagined and modernized while preserving the essence of the original tool.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📮 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Varun-SV/P2E/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Varun-SV/P2E/discussions)
- 📧 **Email**: Open an issue for support

---

> **"Turn your Python ideas into standalone applications - now with style!"** ✨
