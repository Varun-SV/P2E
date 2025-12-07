# 🚀 P2E Quick Start Guide

Get started with P2E in 5 minutes!

## Installation

```bash
# Clone the repository
git clone https://github.com/Varun-SV/P2E.git
cd P2E

# Install dependencies
pip install -r requirements.txt

# Or install as a package
pip install -e .
```

## Quick Examples

### 1. Build with CLI (Recommended)

```bash
# Build with defaults
p2e build examples/simple_example.py

# Build a GUI app (no console window)
p2e build examples/gui_example.py --name MyGUI --windowed

# Build with custom settings
p2e build script.py \
    --name MyApp \
    --output ./dist \
    --windowed \
    --icon app.ico \
    --hidden-import numpy
```

### 2. Use Configuration Files

**Create a config file:**
```bash
# Save default config for your script
p2e save-config examples/simple_example.py myconfig.yaml --format yaml
```

**Edit the config (myconfig.yaml):**
```yaml
script_path: examples/simple_example.py
exe_name: MyApp
one_file: true
console_mode: false
hidden_imports:
  - requests
  - pandas
```

**Build using config:**
```bash
p2e build examples/simple_example.py --config myconfig.yaml
```

### 3. Web Interface

```bash
# Start the web UI
python run_web.py

# Or with streamlit
streamlit run p2e/web/app.py
```

Then:
1. Upload your Python script
2. Configure build settings
3. Click "Build"
4. Download your executable!

### 4. Use as a Python Library

```python
from pathlib import Path
from p2e import BuildConfig, PyConverter

# Create configuration
config = BuildConfig(
    script_path=Path("my_script.py"),
    exe_name="MyApp",
    one_file=True,
    console_mode=False,
    icon_path=Path("icon.ico"),
    hidden_imports=["numpy", "pandas"]
)

# Build
converter = PyConverter(config)
if converter.build():
    print(f"Success! Executable: {converter.get_output_path()}")
else:
    print("Build failed!")
```

## Common Use Cases

### Console Application

```bash
p2e build script.py --name MyConsoleApp
```

### GUI Application (Tkinter, PyQt, etc.)

```bash
p2e build gui_app.py --name MyGUI --windowed --icon app.ico
```

### Application with Dependencies

```bash
p2e build app.py \
    --hidden-import pandas \
    --hidden-import numpy \
    --hidden-import matplotlib
```

### Application with Data Files

```bash
p2e build app.py \
    --add-file config.json:config.json \
    --add-file data.db:data.db \
    --add-folder assets:assets
```

### Behind Corporate Proxy

```bash
p2e build script.py --proxy http://proxy.company.com:8080
```

## Configuration Templates

Use built-in templates:

```bash
# Copy basic template
cp p2e/templates/basic_config.yaml my_config.yaml

# Copy GUI template
cp p2e/templates/gui_app_config.yaml my_gui_config.yaml

# Edit and use
p2e build script.py --config my_config.yaml
```

## Tips & Tricks

### 1. Check Configuration Before Building

```bash
# Preview what will be built
p2e show-config myconfig.yaml
```

### 2. Test with Example Scripts

```bash
# Try with the included examples
p2e build examples/simple_example.py
p2e build examples/gui_example.py --windowed
```

### 3. Save Your Favorite Settings

```bash
# Save your working configuration
p2e save-config script.py my-favorite-config.yaml

# Reuse it later
p2e build another_script.py --config my-favorite-config.yaml
```

### 4. Debug Build Issues

If build fails:
1. Check the console output for PyInstaller errors
2. Try adding missing imports with `--hidden-import`
3. Make sure all data files are included with `--add-file`
4. Test the script works before building

### 5. Get Help Anytime

```bash
p2e --help              # General help
p2e build --help        # Build command help
p2e info                # About P2E
```

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [CHANGELOG.md](CHANGELOG.md) for version history
- Browse [examples/](examples/) for more examples
- Explore [p2e/templates/](p2e/templates/) for config templates

## Troubleshooting

**Problem: "Command not found: p2e"**
```bash
# Use python to run directly
python run_cli.py build script.py

# Or install the package
pip install -e .
```

**Problem: Build fails with missing modules**
```bash
# Add the missing module as hidden import
p2e build script.py --hidden-import missing_module
```

**Problem: Executable is too large**
```bash
# Try with UPX compression (if available)
# Or use --onedir instead of --onefile for smaller initial size
p2e build script.py --onedir
```

## Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Varun-SV/P2E/issues)
- 📖 **Docs**: [README.md](README.md)
- 💡 **Examples**: [examples/](examples/)

---

Happy building! 🎉
