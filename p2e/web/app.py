"""
Modern Streamlit web interface for P2E.
"""

import datetime
import re
import streamlit as st
import tempfile
import shutil
from pathlib import Path
from typing import List, Tuple

from p2e.core.config import BuildConfig
from p2e.core.converter import PyConverter
from p2e import __version__


def create_app():
    """Create and configure the Streamlit app."""
    
    # Page configuration
    st.set_page_config(
        page_title="P2E - Python to EXE",
        page_icon="🐍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 1rem 2rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 0.75rem;
            border: none;
            font-size: 1.1rem;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .success-box {
            padding: 1rem;
            border-radius: 8px;
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .error-box {
            padding: 1rem;
            border-radius: 8px;
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'build_history' not in st.session_state:
        st.session_state.build_history = []
    
    # Header
    st.title("🐍 P2E - Python to EXE Converter")
    st.markdown(f"**Version {__version__}** | Modern tool for building Python executables")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Load/Save config
        st.subheader("Config Management")
        config_file = st.file_uploader("Load Config", type=['json', 'yaml', 'yml'])
        
        if config_file:
            try:
                with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix=config_file.name) as tmp:
                    tmp.write(config_file.getvalue())
                    tmp_path = Path(tmp.name)
                
                if config_file.name.endswith('.json'):
                    loaded_config = BuildConfig.from_json(tmp_path)
                else:
                    loaded_config = BuildConfig.from_yaml(tmp_path)
                
                st.success("✓ Config loaded!")
                st.session_state.loaded_config = loaded_config
                tmp_path.unlink()
            except Exception as e:
                st.error(f"Failed to load config: {e}")
        
        st.divider()
        
        # About
        st.subheader("ℹ️ About")
        st.info("""
        **P2E** helps you convert Python scripts into standalone executables.
        
        Features:
        - 🎯 Easy-to-use interface
        - ⚙️ Advanced PyInstaller options
        - 📦 Include additional files
        - 🔒 Proxy support
        - 💾 Save/Load configurations
        """)
    
    # Main content
    tabs = st.tabs(["📝 Build", "📚 Advanced", "📊 History"])
    
    with tabs[0]:
        build_tab()
    
    with tabs[1]:
        advanced_tab()
    
    with tabs[2]:
        history_tab()


def build_tab():
    """Main build interface."""
    st.header("Build Executable")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Source")
        
        # Main script upload
        main_script = st.file_uploader(
            "Main Python Script",
            type=['py'],
            key="main_script",
            help="The main .py file to convert"
        )
        
        if main_script:
            st.success(f"✓ Loaded: {main_script.name}")
        
        # Output settings
        st.subheader("🎯 Output Settings")
        
        exe_name = st.text_input(
            "Executable Name",
            value=main_script.name.replace('.py', '') if main_script else "MyApp",
            help="Name for the output executable"
        )
        
        # Build options
        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            one_file = st.checkbox("Single File", value=True, help="Bundle everything into one file")
            console_mode = st.checkbox("Show Console", value=True, help="Keep console window visible")
        with col_opt2:
            clean_build = st.checkbox("Clean Build", value=True, help="Remove build artifacts")
            use_icon = st.checkbox("Use Icon", value=False)
        
        icon_file = None
        if use_icon:
            icon_file = st.file_uploader("Icon File (.ico)", type=['ico'])
    
    with col2:
        st.subheader("📦 Additional Resources")
        
        # Additional files
        additional_files = st.file_uploader(
            "Additional Files",
            accept_multiple_files=True,
            help="Include extra files (data, images, etc.)"
        )
        
        if additional_files:
            st.success(f"✓ {len(additional_files)} file(s) selected")
        
        # Hidden imports
        st.subheader("🔧 Hidden Imports")
        hidden_imports_text = st.text_area(
            "Module Names (one per line)",
            placeholder="numpy\npandas\nrequests",
            help="Modules that PyInstaller might miss"
        )
        
        # Proxy settings
        st.subheader("🌐 Network")
        use_proxy = st.checkbox("Use Proxy")
        proxy_url = None
        if use_proxy:
            proxy_url = st.text_input("Proxy URL", value="http://proxy:8080")
    
    st.divider()
    
    # Build button
    if st.button("🚀 BUILD EXECUTABLE", type="primary"):
        if not main_script:
            st.error("❌ Please upload a Python script first!")
        else:
            build_executable(
                main_script=main_script,
                exe_name=exe_name,
                one_file=one_file,
                console_mode=console_mode,
                clean_build=clean_build,
                icon_file=icon_file,
                additional_files=additional_files or [],
                hidden_imports_text=hidden_imports_text,
                use_proxy=use_proxy,
                proxy_url=proxy_url
            )


def advanced_tab():
    """Advanced options tab."""
    st.header("Advanced Options")
    
    st.info("🚧 Advanced features coming soon!")
    
    st.subheader("Planned Features")
    st.markdown("""
    - ✨ Custom PyInstaller arguments
    - ✨ Multiple script bundling
    - ✨ Virtual environment integration
    - ✨ Build templates
    - ✨ Automated testing
    - ✨ Code signing support
    """)


def history_tab():
    """Build history tab."""
    st.header("Build History")
    
    if not st.session_state.build_history:
        st.info("No builds yet. Create your first build in the Build tab!")
    else:
        for i, build in enumerate(reversed(st.session_state.build_history)):
            with st.expander(f"{build['name']} - {build['timestamp']}"):
                st.write(f"**Status:** {build['status']}")
                st.write(f"**Output:** {build.get('output', 'N/A')}")
                if build.get('logs'):
                    st.code(build['logs'][-10:], language='text')


def build_executable(
    main_script,
    exe_name: str,
    one_file: bool,
    console_mode: bool,
    clean_build: bool,
    icon_file,
    additional_files: List,
    hidden_imports_text: str,
    use_proxy: bool,
    proxy_url: str
):
    """Execute the build process."""
    
    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    log_placeholder = st.empty()
    
    logs = []
    
    def log(message: str):
        logs.append(message)
        with log_placeholder.container():
            st.code("\n".join(logs[-20:]), language='text')
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Save main script
            status_placeholder.info("📝 Preparing build environment...")
            progress_bar.progress(10)
            
            script_path = temp_path / main_script.name
            with open(script_path, 'wb') as f:
                f.write(main_script.getvalue())
            log(f"✓ Saved main script: {main_script.name}")
            
            # Save icon if provided
            icon_path = None
            if icon_file:
                icon_path = temp_path / icon_file.name
                with open(icon_path, 'wb') as f:
                    f.write(icon_file.getvalue())
                log(f"✓ Saved icon: {icon_file.name}")
            
            # Save additional files
            add_files_list = []
            for add_file in additional_files:
                file_path = temp_path / add_file.name
                with open(file_path, 'wb') as f:
                    f.write(add_file.getvalue())
                add_files_list.append((str(file_path), add_file.name))
                log(f"✓ Saved additional file: {add_file.name}")
            
            # Parse hidden imports with validation
            hidden_imports = []
            for line in hidden_imports_text.split('\n'):
                module = line.strip()
                if module and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$', module):
                    hidden_imports.append(module)
                elif module:
                    log(f"⚠ Warning: Invalid module name '{module}', skipping")
            
            progress_bar.progress(30)
            
            # Create build config
            config = BuildConfig(
                script_path=script_path,
                output_dir=temp_path / "dist",
                exe_name=exe_name,
                one_file=one_file,
                console_mode=console_mode,
                clean_build=clean_build,
                icon_path=icon_path,
                additional_files=add_files_list,
                hidden_imports=hidden_imports,
                use_proxy=use_proxy,
                proxy_url=proxy_url if use_proxy else None
            )
            
            log(f"✓ Configuration created")
            log(f"  - Executable: {exe_name}")
            log(f"  - Mode: {'Single File' if one_file else 'Directory'}")
            log(f"  - Console: {'Yes' if console_mode else 'No'}")
            
            # Create converter
            status_placeholder.info("🔨 Building executable...")
            progress_bar.progress(50)
            
            converter = PyConverter(config, log_callback=log)
            
            # Build
            success = converter.build(realtime_output=True)
            
            progress_bar.progress(90)
            
            if success:
                status_placeholder.success("✅ Build completed successfully!")
                progress_bar.progress(100)
                
                # Get output file
                output_path = converter.get_output_path()
                
                if output_path and output_path.exists():
                    # Offer download
                    with open(output_path, 'rb') as f:
                        st.download_button(
                            label=f"⬇️ Download {output_path.name}",
                            data=f,
                            file_name=output_path.name,
                            mime="application/octet-stream"
                        )
                    
                    # Add to history
                    st.session_state.build_history.append({
                        'name': exe_name,
                        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'Success',
                        'output': str(output_path.name),
                        'logs': logs
                    })
                else:
                    st.warning("⚠️ Build succeeded but output file not found")
            else:
                status_placeholder.error("❌ Build failed!")
                progress_bar.progress(0)
                
                # Add to history
                st.session_state.build_history.append({
                    'name': exe_name,
                    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'Failed',
                    'logs': logs
                })
    
    except Exception as e:
        status_placeholder.error(f"❌ Error: {e}")
        log(f"✗ Error: {e}")
        progress_bar.progress(0)


if __name__ == '__main__':
    create_app()
