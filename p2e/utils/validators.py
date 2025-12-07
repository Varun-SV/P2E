"""Validation utilities for P2E."""

from pathlib import Path
from typing import Tuple


def validate_python_file(path: Path) -> Tuple[bool, str]:
    """
    Validate a Python file.
    
    Args:
        path: Path to Python file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path.exists():
        return False, f"File not found: {path}"
    
    if not path.is_file():
        return False, f"Not a file: {path}"
    
    if path.suffix.lower() != ".py":
        return False, f"Not a Python file: {path}"
    
    if path.stat().st_size == 0:
        return False, f"File is empty: {path}"
    
    return True, ""


def validate_icon_file(path: Path) -> Tuple[bool, str]:
    """
    Validate an icon file.
    
    Args:
        path: Path to icon file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path.exists():
        return False, f"Icon file not found: {path}"
    
    if not path.is_file():
        return False, f"Not a file: {path}"
    
    if path.suffix.lower() != ".ico":
        return False, f"Not an .ico file: {path}"
    
    return True, ""
