# Changelog

All notable changes to P2E will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-07

### 🎉 Complete Reimagining

P2E has been completely reimagined from the ground up while preserving the essence of what made it great. This is a major release with breaking changes in how you use P2E, but all core functionality has been preserved and enhanced.

### Added

#### New Architecture
- **Modular Design**: Clean separation into `core`, `cli`, `web`, and `utils` modules
- **Type Safety**: Full type hints throughout the entire codebase
- **Better Error Handling**: Comprehensive validation and error messages
- **Logging System**: Proper logging infrastructure with configurable levels

#### New CLI Interface
- **Modern CLI**: Built with Click and Rich for beautiful terminal output
- **Multiple Commands**: `build`, `save-config`, `show-config`, `info`
- **Rich Formatting**: Colored output, progress bars, and formatted tables
- **Configuration Files**: Full YAML and JSON support for build configurations

#### Enhanced Web Interface
- **Modern Design**: Clean, intuitive Streamlit-based UI
- **Tabbed Interface**: Organized into Build, Advanced, and History tabs
- **Build History**: Track all your builds with timestamps and status
- **Better UX**: Improved file uploads, progress tracking, and error messages

#### Configuration Management
- **YAML/JSON Support**: Save and load configurations in multiple formats
- **Configuration Templates**: Pre-built templates for common scenarios
- **Dataclass-based Config**: Type-safe configuration with `BuildConfig`
- **Config Validation**: Comprehensive validation before builds

#### Project Setup
- **Package Distribution**: Proper `setup.py` and `pyproject.toml`
- **Entry Points**: Install as a package with `pip install -e .`
- **Dependencies Management**: Clean requirements files
- **Examples**: Included example scripts for testing

#### Documentation
- **Comprehensive README**: Detailed documentation with examples
- **Configuration Guide**: Full guide for all configuration options
- **Migration Guide**: Help for users upgrading from v1.0
- **API Documentation**: Type hints serve as inline documentation

### Changed

#### Breaking Changes
- **Command-line usage changed**: Now uses `p2e build` instead of `python p2e.py`
- **Configuration format**: Old JSON format is different from new format
- **Project structure**: Files moved to new modular structure

#### Improvements
- **Code Organization**: Much cleaner and more maintainable codebase
- **Error Messages**: More helpful and specific error messages
- **Build Process**: More reliable with better progress tracking
- **Proxy Support**: Improved proxy handling

### Preserved

All core functionality from v1.0 has been preserved:
- ✅ PyInstaller integration
- ✅ Basic build options (onefile, windowed, icon)
- ✅ Additional files and folders support
- ✅ Hidden imports management
- ✅ Proxy support for pip installs
- ✅ Settings save/load (now with YAML/JSON)
- ✅ Real-time progress tracking
- ✅ GUI and web interfaces

### Backward Compatibility

The original v1.0 scripts are still available for backward compatibility:
- `python_code/p2e.py` - Original Tkinter GUI (works as before)
- `python_code/streamlit_app.py` - Original Streamlit app (works as before)

### Migration Guide

**From v1.0 to v2.0:**

1. **Install the package**: `pip install -e .`
2. **Use new CLI**: `p2e build script.py` instead of `python p2e.py`
3. **Update configs**: Convert old JSON configs to new format or use templates
4. **Try new features**: Explore configuration files and modern CLI

**Old way (v1.0):**
```bash
python python_code/p2e.py
```

**New way (v2.0):**
```bash
p2e build script.py --name MyApp --windowed
```

### Technical Details

#### New Dependencies
- `click>=8.0.0` - CLI framework
- `rich>=10.0.0` - Terminal formatting
- `PyYAML>=5.4.0` - YAML configuration support

#### Code Quality
- Full type hints with mypy compatibility
- Modular architecture following SOLID principles
- Comprehensive error handling
- Better separation of concerns

---

## [1.0.0] - Original Release

### Features
- Tkinter-based GUI for PyInstaller
- Basic PyInstaller options
- Additional files and folders support
- Hidden imports
- Proxy support
- Settings save/load (JSON)
- Streamlit web version

---

[2.0.0]: https://github.com/Varun-SV/P2E/releases/tag/v2.0.0
[1.0.0]: https://github.com/Varun-SV/P2E/releases/tag/v1.0.0
