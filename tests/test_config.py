"""Tests for BuildConfig."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml

from p2e.core.config import BuildConfig


def test_build_config_defaults(tmp_path):
    """Test BuildConfig with defaults."""
    script = tmp_path / "test.py"
    script.write_text("print('hello')")
    
    config = BuildConfig(script_path=script)
    
    assert config.script_path == script
    assert config.exe_name == "test"
    assert config.output_dir == tmp_path / "dist"
    assert config.one_file is True
    assert config.console_mode is True


def test_build_config_validation(tmp_path):
    """Test BuildConfig validation."""
    # Non-existent script should raise error
    with pytest.raises(ValueError, match="Script file not found"):
        config = BuildConfig(script_path=Path("nonexistent.py"))
        config.validate()
    
    # Non-Python file should raise error
    non_py = tmp_path / "test.txt"
    non_py.write_text("text")
    with pytest.raises(ValueError, match="Script must be a .py file"):
        config = BuildConfig(script_path=non_py)
        config.validate()


def test_build_config_to_dict(tmp_path):
    """Test converting config to dictionary."""
    script = tmp_path / "test.py"
    script.write_text("print('hello')")
    
    config = BuildConfig(
        script_path=script,
        exe_name="MyApp",
        one_file=False,
        console_mode=False
    )
    
    data = config.to_dict()
    
    assert isinstance(data, dict)
    assert data['exe_name'] == "MyApp"
    assert data['one_file'] is False
    assert data['console_mode'] is False
    assert isinstance(data['script_path'], str)


def test_build_config_from_dict(tmp_path):
    """Test loading config from dictionary."""
    script = tmp_path / "test.py"
    script.write_text("print('hello')")
    
    data = {
        'script_path': str(script),
        'exe_name': 'TestApp',
        'one_file': False,
        'console_mode': True,
        'hidden_imports': ['numpy', 'pandas']
    }
    
    config = BuildConfig.from_dict(data)
    
    assert config.script_path == script
    assert config.exe_name == 'TestApp'
    assert config.one_file is False
    assert config.console_mode is True
    assert 'numpy' in config.hidden_imports
    assert 'pandas' in config.hidden_imports


def test_build_config_save_load_json(tmp_path):
    """Test saving and loading JSON config."""
    script = tmp_path / "test.py"
    script.write_text("print('hello')")
    
    config = BuildConfig(
        script_path=script,
        exe_name="MyApp",
        one_file=False,
        hidden_imports=['requests']
    )
    
    config_file = tmp_path / "config.json"
    config.save_json(config_file)
    
    assert config_file.exists()
    
    loaded_config = BuildConfig.from_json(config_file)
    
    assert loaded_config.exe_name == "MyApp"
    assert loaded_config.one_file is False
    assert 'requests' in loaded_config.hidden_imports


def test_build_config_save_load_yaml(tmp_path):
    """Test saving and loading YAML config."""
    script = tmp_path / "test.py"
    script.write_text("print('hello')")
    
    config = BuildConfig(
        script_path=script,
        exe_name="MyYamlApp",
        console_mode=False,
        hidden_imports=['pandas', 'numpy']
    )
    
    config_file = tmp_path / "config.yaml"
    config.save_yaml(config_file)
    
    assert config_file.exists()
    
    loaded_config = BuildConfig.from_yaml(config_file)
    
    assert loaded_config.exe_name == "MyYamlApp"
    assert loaded_config.console_mode is False
    assert 'pandas' in loaded_config.hidden_imports
    assert 'numpy' in loaded_config.hidden_imports


def test_build_config_windowed_mode(tmp_path):
    """Test windowed mode overrides console mode."""
    script = tmp_path / "test.py"
    script.write_text("print('hello')")
    
    config = BuildConfig(
        script_path=script,
        windowed=True
    )
    
    # windowed=True should set console_mode=False
    assert config.windowed is True
    assert config.console_mode is False
