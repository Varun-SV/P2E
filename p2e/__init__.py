"""
P2E - Python to EXE Converter
A modern, modular tool for converting Python scripts to executables.
"""

__version__ = "2.0.0"
__author__ = "Varun S V"
__license__ = "MIT"

from p2e.core.converter import PyConverter
from p2e.core.config import BuildConfig

__all__ = ["PyConverter", "BuildConfig"]
