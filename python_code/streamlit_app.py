import streamlit as st
import json
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="PyInstaller Command Generator",
    page_icon="📦",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    .code-box {
        background-color: #1e1e1e;
        color: #d4d4d4;
        padding: 1rem;
        border-radius: 0.5rem;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        overflow-x: auto;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'hidden_imports' not in st.session_state:
    st.session_state.hidden_imports = []
if 'additional_files' not in st.session_state:
    st.session_state.additional_files = []
if 'additional_folders' not in st.session_state:
    st.session_state.additional_folders = []

# Header
st.title("📦 PyInstaller Command Generator")
st.markdown("Create PyInstaller commands and compilation scripts for your Python projects")
st.divider()

# Main layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔧 Basic Configuration")
    
    script_name = st.text_input(
        "Python Script Path *",
        placeholder="script.py or /path/to/script.py",
        help="The main Python script to compile"
    )
    
    exe_name = st.text_input(
        "Executable Name",
        placeholder="MyApp (optional)",
        help="Name for the output executable"
    )
    
    output_dir = st.text_input(
        "Output Directory",
        value="./dist",
        help="Where to save the compiled executable"
    )
    
    icon_path = st.text_input(
        "Icon File (.ico)",
        placeholder="icon.ico (optional)",
        help="Path to icon file for Windows executable"
    )
    
    st.divider()
    
    st.subheader("⚙️ Build Options")
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        one_file = st.checkbox("Single File (--onefile)", value=True)
        clean_build = st.checkbox("Clean Build (--clean)", value=True)
    
    with col_opt2:
        console_mode = st.checkbox("Console Mode", value=False)
        upx_compress = st.checkbox("UPX Compression", value=False)
    
    st.divider()
    
    st.subheader("🌐 Proxy Settings")
    
    use_proxy = st.checkbox("Use Proxy")
    
    if use_proxy:
        proxy_url = st.text_input(
            "Proxy URL",
            value="http://proxy:port",
            help="HTTP proxy for pip installation"
        )
    else:
        proxy_url = ""

with col2:
    st.subheader("📚 Hidden Imports")
    
    new_import = st.text_input(
        "Add Hidden Import",
        placeholder="module.name",
        key="new_import_input"
    )
    
    col_add_import, col_clear_imports = st.columns([3, 1])
    
    with col_add_import:
        if st.button("➕ Add Import"):
            if new_import.strip() and new_import.strip() not in st.session_state.hidden_imports:
                st.session_state.hidden_imports.append(new_import.strip())
                st.rerun()
    
    with col_clear_imports:
        if st.button("🗑️ Clear All"):
            st.session_state.hidden_imports = []
            st.rerun()
    
    if st.session_state.hidden_imports:
        for idx, imp in enumerate(st.session_state.hidden_imports):
            col_imp, col_del = st.columns([4, 1])
            with col_imp:
                st.code(imp, language=None)
            with col_del:
                if st.button("❌", key=f"del_import_{idx}"):
                    st.session_state.hidden_imports.pop(idx)
                    st.rerun()
    
    st.divider()
    
    st.subheader("📄 Additional Files")
    
    file_source = st.text_input("File Source Path", key="file_source")
    file_dest = st.text_input("File Destination", key="file_dest")
    
    if st.button("➕ Add File"):
        if file_source.strip() and file_dest.strip():
            st.session_state.additional_files.append({
                'source': file_source.strip(),
                'dest': file_dest.strip()
            })
            st.rerun()
    
    if st.session_state.additional_files:
        for idx, file in enumerate(st.session_state.additional_files):
            col_file, col_del = st.columns([4, 1])
            with col_file:
                st.text(f"{file['source']} -> {file['dest']}")
            with col_del:
                if st.button("❌", key=f"del_file_{idx}"):
                    st.session_state.additional_files.pop(idx)
                    st.rerun()
    
    st.divider()
    
    st.subheader("📁 Additional Folders")
    
    folder_source = st.text_input("Folder Source Path", key="folder_source")
    folder_dest = st.text_input("Folder Destination", key="folder_dest")
    
    if st.button("➕ Add Folder"):
        if folder_source.strip() and folder_dest.strip():
            st.session_state.additional_folders.append({
                'source': folder_source.strip(),
                'dest': folder_dest.strip()
            })
            st.rerun()
    
    if st.session_state.additional_folders:
        for idx, folder in enumerate(st.session_state.additional_folders):
            col_folder, col_del = st.columns([4, 1])
            with col_folder:
                st.text(f"{folder['source']} -> {folder['dest']}")
            with col_del:
                if st.button("❌", key=f"del_folder_{idx}"):
                    st.session_state.additional_folders.pop(idx)
                    st.rerun()

# Generate command function
def generate_command(script_name, exe_name, output_dir, icon_path, one_file, 
                    console_mode, clean_build, upx_compress, hidden_imports, 
                    additional_files, additional_folders):
    if not script_name.strip():
        return ""
    
    cmd = "pyinstaller"
    
    if one_file:
        cmd += " --onefile"
    else:
        cmd += " --onedir"
    
    if not console_mode:
        cmd += " --windowed"
    
    if clean_build:
        cmd += " --clean"
    
    if output_dir.strip():
        cmd += f' --distpath "{output_dir}"'
    
    if exe_name.strip():
        cmd += f' --name "{exe_name}"'
    
    if icon_path.strip():
        cmd += f' --icon "{icon_path}"'
    
    if upx_compress:
        cmd += " --upx-dir"
    
    # Add additional files
    for file in additional_files:
        # Use semicolon for Windows, colon for Unix
        cmd += f' --add-data "{file["source"]};{file["dest"]}"'
    
    # Add additional folders
    for folder in additional_folders:
        cmd += f' --add-data "{folder["source"]};{folder["dest"]}"'
    
    # Add hidden imports
    for imp in hidden_imports:
        cmd += f" --hidden-import {imp}"
    
    cmd += f' "{script_name}"'
    
    return cmd

# Generate Python script function
def generate_python_script(command, use_proxy, proxy_url):
    proxy_param = f', "--proxy", "{proxy_url}"' if use_proxy and proxy_url else ''
    
    script = f'''import subprocess
import sys

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"{proxy_param}])
        print("PyInstaller installed successfully")

def compile_script():
    """Compile the Python script to executable"""
    install_pyinstaller()
    
    cmd = {command.split()}
    
    print("Running PyInstaller with command:")
    print(" ".join(cmd))
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print("-" * 60)
        print("Compilation completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {{e}}")
        return False

if __name__ == "__main__":
    compile_script()
'''
    return script

# Generate outputs
st.divider()
st.header("📋 Generated Output")

if script_name:
    command = generate_command(
        script_name, exe_name, output_dir, icon_path, one_file,
        console_mode, clean_build, upx_compress, st.session_state.hidden_imports,
        st.session_state.additional_files, st.session_state.additional_folders
    )
    
    python_script = generate_python_script(command, use_proxy, proxy_url if use_proxy else "")
    
    # Display command
    st.subheader("🖥️ Terminal Command")
    st.code(command, language="bash")
    
    col_copy1, col_info = st.columns([1, 3])
    with col_copy1:
        st.button("📋 Copy Command", key="copy_cmd", help="Click to select, then Ctrl+C to copy")
    
    st.divider()
    
    # Display Python script
    st.subheader("🐍 Python Compilation Script")
    st.code(python_script, language="python")
    
    # Download button
    st.download_button(
        label="⬇️ Download Python Script",
        data=python_script,
        file_name="compile_script.py",
        mime="text/x-python"
    )
    
    st.divider()
    
    # Instructions
    st.markdown("""
    <div class="info-box">
        <h4>📖 How to Use:</h4>
        <ol>
            <li><strong>Option 1:</strong> Copy the terminal command above and run it in your command prompt/terminal</li>
            <li><strong>Option 2:</strong> Download the Python script and run it: <code>python compile_script.py</code></li>
            <li>Your executable will be created in the output directory you specified</li>
        </ol>
        <p><strong>Note:</strong> Make sure PyInstaller is installed or the script will install it automatically.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Save/Load Settings
    st.divider()
    st.subheader("💾 Settings Management")
    
    col_save, col_load = st.columns(2)
    
    with col_save:
        st.markdown("**Save Current Configuration**")
        settings = {
            'script_name': script_name,
            'exe_name': exe_name,
            'output_dir': output_dir,
            'icon_path': icon_path,
            'one_file': one_file,
            'console_mode': console_mode,
            'clean_build': clean_build,
            'upx_compress': upx_compress,
            'use_proxy': use_proxy,
            'proxy_url': proxy_url if use_proxy else "",
            'hidden_imports': st.session_state.hidden_imports,
            'additional_files': st.session_state.additional_files,
            'additional_folders': st.session_state.additional_folders
        }
        
        settings_json = json.dumps(settings, indent=2)
        st.download_button(
            label="⬇️ Download Settings (JSON)",
            data=settings_json,
            file_name="pyinstaller_settings.json",
            mime="application/json"
        )
    
    with col_load:
        st.markdown("**Load Configuration**")
        uploaded_file = st.file_uploader("Upload Settings JSON", type=['json'])
        
        if uploaded_file is not None:
            try:
                loaded_settings = json.load(uploaded_file)
                if st.button("✅ Apply Loaded Settings"):
                    st.session_state.hidden_imports = loaded_settings.get('hidden_imports', [])
                    st.session_state.additional_files = loaded_settings.get('additional_files', [])
                    st.session_state.additional_folders = loaded_settings.get('additional_folders', [])
                    st.success("Settings loaded! Refresh the page to see changes.")
            except Exception as e:
                st.error(f"Error loading settings: {str(e)}")

else:
    st.info("👆 Enter a Python script path to generate the PyInstaller command")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 This tool generates PyInstaller commands - you'll need to run them on your local machine</p>
    <p>Made with ❤️ for Python developers</p>
</div>
""", unsafe_allow_html=True)
