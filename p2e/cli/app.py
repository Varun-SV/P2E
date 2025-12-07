"""
Modern CLI for P2E using Click and Rich.
"""

import sys
from pathlib import Path
from typing import Optional, List

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich import box

from p2e.core.config import BuildConfig
from p2e.core.converter import PyConverter
from p2e import __version__

console = Console()


@click.group()
@click.version_option(version=__version__)
def cli():
    """🐍 P2E - Python to EXE Converter
    
    Convert Python scripts to standalone executables with ease.
    """
    pass


@cli.command()
@click.argument('script', type=click.Path(exists=True, path_type=Path))
@click.option('-o', '--output', type=click.Path(path_type=Path), help='Output directory')
@click.option('-n', '--name', help='Executable name')
@click.option('--onefile/--onedir', default=True, help='Build as single file or directory')
@click.option('--console/--windowed', default=True, help='Console or windowed mode')
@click.option('-i', '--icon', type=click.Path(exists=True, path_type=Path), help='Icon file (.ico)')
@click.option('--clean/--no-clean', default=True, help='Clean build artifacts')
@click.option('--add-file', multiple=True, help='Add file (format: src:dst)')
@click.option('--add-folder', multiple=True, help='Add folder (format: src:dst)')
@click.option('--hidden-import', multiple=True, help='Hidden import module')
@click.option('--proxy', help='Proxy URL for pip installs')
@click.option('--config', type=click.Path(exists=True, path_type=Path), help='Load config from file')
def build(
    script: Path,
    output: Optional[Path],
    name: Optional[str],
    onefile: bool,
    console: bool,
    icon: Optional[Path],
    clean: bool,
    add_file: tuple,
    add_folder: tuple,
    hidden_import: tuple,
    proxy: Optional[str],
    config: Optional[Path]
):
    """Build a Python script into an executable."""
    
    try:
        # Load config from file if provided
        if config:
            console.print(f"[cyan]Loading config from {config}...[/cyan]")
            if config.suffix == '.json':
                build_config = BuildConfig.from_json(config)
            elif config.suffix in ['.yaml', '.yml']:
                build_config = BuildConfig.from_yaml(config)
            else:
                console.print("[red]Config file must be .json or .yaml[/red]")
                sys.exit(1)
            # Override with CLI arguments
            build_config.script_path = script
            if output:
                build_config.output_dir = output
            if name:
                build_config.exe_name = name
        else:
            # Parse additional files and folders
            additional_files = []
            for file_spec in add_file:
                if ':' in file_spec:
                    src, dst = file_spec.split(':', 1)
                    additional_files.append((src, dst))
                else:
                    console.print(f"[yellow]Warning: Invalid file spec '{file_spec}', should be 'src:dst'[/yellow]")
            
            additional_folders = []
            for folder_spec in add_folder:
                if ':' in folder_spec:
                    src, dst = folder_spec.split(':', 1)
                    additional_folders.append((src, dst))
                else:
                    console.print(f"[yellow]Warning: Invalid folder spec '{folder_spec}', should be 'src:dst'[/yellow]")
            
            # Create build config
            build_config = BuildConfig(
                script_path=script,
                output_dir=output,
                exe_name=name,
                one_file=onefile,
                console_mode=console,
                icon_path=icon,
                clean_build=clean,
                additional_files=additional_files,
                additional_folders=additional_folders,
                hidden_imports=list(hidden_import),
                use_proxy=bool(proxy),
                proxy_url=proxy
            )
        
        # Display build configuration
        display_config(build_config)
        
        # Create converter with rich logging
        logs = []
        
        def log_callback(message: str):
            logs.append(message)
            console.print(f"  {message}")
        
        converter = PyConverter(build_config, log_callback=log_callback)
        
        # Build
        console.print("\n[bold cyan]Starting build...[/bold cyan]")
        success = converter.build(realtime_output=True)
        
        if success:
            console.print("\n[bold green]✓ Build completed successfully![/bold green]")
            output_path = converter.get_output_path()
            if output_path:
                console.print(f"[green]Executable: {output_path}[/green]")
        else:
            console.print("\n[bold red]✗ Build failed![/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument('script', type=click.Path(exists=True, path_type=Path))
@click.argument('output', type=click.Path(path_type=Path))
@click.option('-f', '--format', type=click.Choice(['json', 'yaml']), default='json', help='Config format')
def save_config(script: Path, output: Path, format: str):
    """Save a build configuration to a file."""
    
    try:
        # Create a basic config
        config = BuildConfig(script_path=script)
        
        # Save based on format
        if format == 'json':
            if not output.suffix:
                output = output.with_suffix('.json')
            config.save_json(output)
        else:
            if not output.suffix:
                output = output.with_suffix('.yaml')
            config.save_yaml(output)
        
        console.print(f"[green]✓ Configuration saved to {output}[/green]")
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@cli.command()
@click.argument('config_file', type=click.Path(exists=True, path_type=Path))
def show_config(config_file: Path):
    """Display a configuration file."""
    
    try:
        # Load config
        if config_file.suffix == '.json':
            config = BuildConfig.from_json(config_file)
        elif config_file.suffix in ['.yaml', '.yml']:
            config = BuildConfig.from_yaml(config_file)
        else:
            console.print("[red]Config file must be .json or .yaml[/red]")
            sys.exit(1)
        
        display_config(config)
        
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


def display_config(config: BuildConfig):
    """Display build configuration in a nice table."""
    table = Table(title="Build Configuration", box=box.ROUNDED)
    table.add_column("Setting", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    
    table.add_row("Script", str(config.script_path))
    table.add_row("Output Dir", str(config.output_dir))
    table.add_row("Executable Name", config.exe_name)
    table.add_row("One File", "Yes" if config.one_file else "No")
    table.add_row("Console Mode", "Yes" if config.console_mode else "No")
    
    if config.icon_path:
        table.add_row("Icon", str(config.icon_path))
    
    if config.additional_files:
        table.add_row("Additional Files", str(len(config.additional_files)))
    
    if config.additional_folders:
        table.add_row("Additional Folders", str(len(config.additional_folders)))
    
    if config.hidden_imports:
        table.add_row("Hidden Imports", ", ".join(config.hidden_imports))
    
    console.print(table)


@cli.command()
def info():
    """Display information about P2E."""
    
    info_text = f"""
[bold cyan]P2E - Python to EXE Converter[/bold cyan]
Version: {__version__}

A modern, modular tool for converting Python scripts to standalone executables.

[bold]Features:[/bold]
  • 🎯 Modular architecture with clean separation of concerns
  • 🖥️  Modern CLI with rich formatting
  • 🌐 Web interface for non-technical users
  • ⚙️  Comprehensive PyInstaller options
  • 📦 Configuration file support (JSON/YAML)
  • 🔒 Proxy support for restricted networks
  • 📝 Real-time build progress tracking

[bold]Usage:[/bold]
  p2e build script.py              # Build with defaults
  p2e build script.py -n MyApp     # Custom name
  p2e build script.py --windowed   # No console window
  p2e build script.py --config config.json  # Use config file

[bold]More info:[/bold]
  Repository: https://github.com/Varun-SV/P2E
  Documentation: Run 'p2e --help' for more commands
    """
    
    console.print(Panel(info_text, border_style="cyan"))


if __name__ == '__main__':
    cli()
