"""Tests for validators."""

from pathlib import Path
import pytest

from p2e.utils.validators import validate_python_file, validate_icon_file


def test_validate_python_file_valid(tmp_path):
    """Test validating a valid Python file."""
    py_file = tmp_path / "test.py"
    py_file.write_text("print('hello')")
    
    is_valid, error = validate_python_file(py_file)
    
    assert is_valid is True
    assert error == ""


def test_validate_python_file_not_exists(tmp_path):
    """Test validating non-existent file."""
    py_file = tmp_path / "nonexistent.py"
    
    is_valid, error = validate_python_file(py_file)
    
    assert is_valid is False
    assert "not found" in error.lower()


def test_validate_python_file_not_py(tmp_path):
    """Test validating non-Python file."""
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("text")
    
    is_valid, error = validate_python_file(txt_file)
    
    assert is_valid is False
    assert "not a python file" in error.lower()


def test_validate_python_file_empty(tmp_path):
    """Test validating empty Python file."""
    py_file = tmp_path / "empty.py"
    py_file.write_text("")
    
    is_valid, error = validate_python_file(py_file)
    
    assert is_valid is False
    assert "empty" in error.lower()


def test_validate_icon_file_valid(tmp_path):
    """Test validating a valid icon file."""
    ico_file = tmp_path / "icon.ico"
    ico_file.write_bytes(b"fake icon data")
    
    is_valid, error = validate_icon_file(ico_file)
    
    assert is_valid is True
    assert error == ""


def test_validate_icon_file_not_exists(tmp_path):
    """Test validating non-existent icon file."""
    ico_file = tmp_path / "nonexistent.ico"
    
    is_valid, error = validate_icon_file(ico_file)
    
    assert is_valid is False
    assert "not found" in error.lower()


def test_validate_icon_file_not_ico(tmp_path):
    """Test validating non-ico file."""
    png_file = tmp_path / "image.png"
    png_file.write_bytes(b"fake png data")
    
    is_valid, error = validate_icon_file(png_file)
    
    assert is_valid is False
    assert "not an .ico file" in error.lower()
