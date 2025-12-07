"""
Configuration management for P2E builds.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import yaml


@dataclass
class BuildConfig:
    """Configuration for building an executable."""

    # Required fields
    script_path: Path

    # Output settings
    output_dir: Optional[Path] = None
    exe_name: Optional[str] = None

    # PyInstaller options
    one_file: bool = True
    console_mode: bool = True
    windowed: bool = False
    clean_build: bool = True

    # Advanced options
    icon_path: Optional[Path] = None
    upx_compress: bool = False
    strip_symbols: bool = False

    # Additional resources
    additional_files: List[tuple[str, str]] = field(default_factory=list)
    additional_folders: List[tuple[str, str]] = field(default_factory=list)
    hidden_imports: List[str] = field(default_factory=list)

    # Network settings
    use_proxy: bool = False
    proxy_url: Optional[str] = None

    # Advanced PyInstaller args
    extra_args: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate and normalize configuration."""
        # Convert string paths to Path objects
        if isinstance(self.script_path, str):
            self.script_path = Path(self.script_path)
        if self.output_dir and isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)
        if self.icon_path and isinstance(self.icon_path, str):
            self.icon_path = Path(self.icon_path)

        # Set defaults
        if not self.output_dir:
            self.output_dir = self.script_path.parent / "dist"
        if not self.exe_name:
            self.exe_name = self.script_path.stem

        # Ensure windowed is opposite of console_mode
        if self.windowed:
            self.console_mode = False

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.script_path.exists():
            raise ValueError(f"Script file not found: {self.script_path}")
        if self.script_path.suffix != ".py":
            raise ValueError(f"Script must be a .py file: {self.script_path}")
        if self.icon_path and not self.icon_path.exists():
            raise ValueError(f"Icon file not found: {self.icon_path}")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        data = asdict(self)
        # Convert Path objects to strings
        for key, value in data.items():
            if isinstance(value, Path):
                data[key] = str(value)
        return data

    def save_json(self, path: Path) -> None:
        """Save configuration to JSON file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)

    def save_yaml(self, path: Path) -> None:
        """Save configuration to YAML file."""
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BuildConfig':
        """Load configuration from dictionary."""
        # Convert string paths back to Path objects
        if 'script_path' in data:
            data['script_path'] = Path(data['script_path'])
        if 'output_dir' in data and data['output_dir']:
            data['output_dir'] = Path(data['output_dir'])
        if 'icon_path' in data and data['icon_path']:
            data['icon_path'] = Path(data['icon_path'])
        return cls(**data)

    @classmethod
    def from_json(cls, path: Path) -> 'BuildConfig':
        """Load configuration from JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_yaml(cls, path: Path) -> 'BuildConfig':
        """Load configuration from YAML file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)
