"""
Core conversion logic for P2E.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Callable, List
from enum import Enum

from p2e.core.config import BuildConfig


class BuildStatus(Enum):
    """Build status enumeration."""
    IDLE = "idle"
    CHECKING_DEPS = "checking_dependencies"
    INSTALLING_DEPS = "installing_dependencies"
    BUILDING = "building"
    CLEANING = "cleaning"
    COMPLETE = "complete"
    FAILED = "failed"


class PyConverter:
    """Main converter class for building Python executables."""
    
    def __init__(self, config: BuildConfig, log_callback: Optional[Callable[[str], None]] = None):
        """
        Initialize converter.
        
        Args:
            config: Build configuration
            log_callback: Optional callback for logging messages
        """
        self.config = config
        self.log_callback = log_callback or print
        self.status = BuildStatus.IDLE
        self.process: Optional[subprocess.Popen] = None
    
    def log(self, message: str) -> None:
        """Log a message."""
        if self.log_callback:
            self.log_callback(message)
    
    def check_pyinstaller(self) -> bool:
        """Check if PyInstaller is installed."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", "pyinstaller"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except Exception as e:
            self.log(f"Error checking PyInstaller: {e}")
            return False
    
    def install_pyinstaller(self) -> bool:
        """Install PyInstaller."""
        try:
            self.status = BuildStatus.INSTALLING_DEPS
            self.log("Installing PyInstaller...")
            
            cmd = [sys.executable, "-m", "pip", "install", "pyinstaller"]
            
            if self.config.use_proxy and self.config.proxy_url:
                cmd.extend(["--proxy", self.config.proxy_url])
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            if result.returncode == 0:
                self.log("PyInstaller installed successfully")
                return True
            else:
                self.log(f"Failed to install PyInstaller: {result.stderr}")
                return False
        except Exception as e:
            self.log(f"Error installing PyInstaller: {e}")
            return False
    
    def build_command(self) -> List[str]:
        """Build PyInstaller command."""
        cmd = [sys.executable, "-m", "PyInstaller"]
        
        # Basic options
        if self.config.one_file:
            cmd.append("--onefile")
        else:
            cmd.append("--onedir")
        
        if self.config.windowed or not self.config.console_mode:
            cmd.append("--windowed")
        
        if self.config.clean_build:
            cmd.append("--clean")
        
        # Output settings
        cmd.extend(["--distpath", str(self.config.output_dir)])
        cmd.extend(["--name", self.config.exe_name])
        
        # Icon
        if self.config.icon_path and self.config.icon_path.exists():
            cmd.extend(["--icon", str(self.config.icon_path)])
        
        # UPX compression
        if self.config.upx_compress:
            cmd.append("--upx-dir")
        
        # Strip symbols
        if self.config.strip_symbols:
            cmd.append("--strip")
        
        # Additional files
        for src, dst in self.config.additional_files:
            cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
        
        # Additional folders
        for src, dst in self.config.additional_folders:
            cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
        
        # Hidden imports
        for import_name in self.config.hidden_imports:
            cmd.extend(["--hidden-import", import_name])
        
        # Extra arguments
        if self.config.extra_args:
            cmd.extend(self.config.extra_args)
        
        # Script file (must be last)
        cmd.append(str(self.config.script_path))
        
        return cmd
    
    def build(self, realtime_output: bool = True) -> bool:
        """
        Build the executable.
        
        Args:
            realtime_output: Whether to show output in real-time
            
        Returns:
            True if build succeeded, False otherwise
        """
        try:
            # Validate configuration
            self.config.validate()
            
            # Check PyInstaller
            self.status = BuildStatus.CHECKING_DEPS
            self.log("Checking PyInstaller installation...")
            
            if not self.check_pyinstaller():
                self.log("PyInstaller not found")
                if not self.install_pyinstaller():
                    self.status = BuildStatus.FAILED
                    return False
            else:
                self.log("PyInstaller is installed")
            
            # Build command
            self.status = BuildStatus.BUILDING
            cmd = self.build_command()
            
            self.log(f"Building executable: {self.config.exe_name}")
            self.log(f"Command: {' '.join(cmd)}")
            
            # Change to script directory
            original_dir = Path.cwd()
            script_dir = self.config.script_path.parent
            os.chdir(script_dir)
            
            try:
                if realtime_output:
                    # Run with real-time output
                    self.process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        universal_newlines=True
                    )
                    
                    for line in iter(self.process.stdout.readline, ''):
                        if line:
                            self.log(line.rstrip())
                    
                    self.process.wait()
                    returncode = self.process.returncode
                else:
                    # Run without real-time output
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        check=False
                    )
                    self.log(result.stdout)
                    if result.stderr:
                        self.log(result.stderr)
                    returncode = result.returncode
                
                if returncode != 0:
                    self.log(f"Build failed with return code {returncode}")
                    self.status = BuildStatus.FAILED
                    return False
                
            finally:
                os.chdir(original_dir)
            
            # Clean up build artifacts
            if self.config.clean_build:
                self.cleanup_build_artifacts(script_dir)
            
            # Verify output
            output_path = self.get_output_path()
            if output_path and output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                self.log(f"✓ Executable created: {output_path}")
                self.log(f"✓ Size: {size_mb:.2f} MB")
                self.status = BuildStatus.COMPLETE
                return True
            else:
                self.log("⚠ Warning: Expected output not found")
                self.status = BuildStatus.FAILED
                return False
                
        except Exception as e:
            self.log(f"✗ Build error: {e}")
            self.status = BuildStatus.FAILED
            return False
    
    def cleanup_build_artifacts(self, script_dir: Path) -> None:
        """Clean up build artifacts."""
        self.status = BuildStatus.CLEANING
        self.log("Cleaning build artifacts...")
        
        # Remove build directory
        build_dir = script_dir / "build"
        if build_dir.exists():
            try:
                shutil.rmtree(build_dir)
                self.log(f"Removed: {build_dir}")
            except Exception as e:
                self.log(f"Warning: Could not remove build dir: {e}")
        
        # Remove spec file
        spec_file = script_dir / f"{self.config.exe_name}.spec"
        if spec_file.exists():
            try:
                spec_file.unlink()
                self.log(f"Removed: {spec_file}")
            except Exception as e:
                self.log(f"Warning: Could not remove spec file: {e}")
    
    def get_output_path(self) -> Optional[Path]:
        """Get the expected output path."""
        if self.config.one_file:
            # For Windows, add .exe extension
            if sys.platform == "win32":
                return self.config.output_dir / f"{self.config.exe_name}.exe"
            else:
                return self.config.output_dir / self.config.exe_name
        else:
            # For onedir builds, the executable is in a subfolder
            if sys.platform == "win32":
                return self.config.output_dir / self.config.exe_name / f"{self.config.exe_name}.exe"
            else:
                return self.config.output_dir / self.config.exe_name / self.config.exe_name
    
    def stop(self) -> None:
        """Stop the build process."""
        if self.process and self.process.poll() is None:
            self.log("Stopping build process...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.log("Build process stopped")
