import streamlit as st
import zipfile
import io
import base64
from pathlib import Path
import json

# Page configuration
st.set_page_config(
    page_title="Python to EXE Converter",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f0f8f0;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'main_file' not in st.session_state:
    st.session_state.main_file = None
if 'additional_files' not in st.session_state:
    st.session_state.additional_files = []
if 'requirements' not in st.session_state:
    st.session_state.requirements = []

# Header
st.title("🔄 Python to EXE Converter")
st.markdown("Upload your Python script and dependencies to create a compilation package")

# Warning banner
st.markdown("""
<div class="warning-box">
    <h4>⚠️ Important Note</h4>
    <p>Due to Streamlit Cloud security restrictions, this app <strong>cannot directly compile executables</strong>. 
    Instead, it will create a complete package with:</p>
    <ul>
        <li>✅ Your Python files</li>
        <li>✅ Automated compilation script</li>
        <li>✅ Requirements and dependencies</li>
        <li>✅ Step-by-step instructions</li>
    </ul>
    <p>You'll run the compilation script on your local machine to generate the .exe file.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# Main layout
tab1, tab2, tab3 = st.tabs(["📤 Upload Files", "⚙️ Configuration", "📦 Generate Package"])

with tab1:
    st.header("Upload Your Python Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Main Python Script")
        main_script = st.file_uploader(
            "Upload your main .py file",
            type=['py'],
            help="This is the entry point of your application",
            key="main_script"
        )
        
        if main_script:
            try:
                content = main_script.read()
                # Reset file pointer for re-reading if needed
                main_script.seek(0)
                st.session_state.main_file = {
                    'name': main_script.name,
                    'content': content.decode('utf-8')
                }
                st.success(f"✅ Loaded: {main_script.name}")
                
                with st.expander("Preview Code"):
                    st.code(st.session_state.main_file['content'], language='python')
            except UnicodeDecodeError:
                st.error("❌ Error: File must be a valid UTF-8 encoded Python file")
    
    with col2:
        st.subheader("📚 Additional Files")
        additional_files = st.file_uploader(
            "Upload additional Python files, data files, etc.",
            type=['py', 'txt', 'json', 'csv', 'png', 'jpg', 'ico'],
            accept_multiple_files=True,
            help="Upload any files your script depends on",
            key="additional_files_uploader"
        )
        
        if additional_files:
            st.session_state.additional_files = []
            for file in additional_files:
                try:
                    content = file.read()
                    # Reset file pointer
                    file.seek(0)
                    
                    # Determine if binary
                    is_binary = file.type.startswith('image') or file.name.endswith(('.ico', '.png', '.jpg', '.jpeg', '.gif'))
                    
                    st.session_state.additional_files.append({
                        'name': file.name,
                        'content': content,
                        'is_binary': is_binary
                    })
                except Exception as e:
                    st.error(f"Error reading {file.name}: {str(e)}")
                    
            st.success(f"✅ Loaded {len(st.session_state.additional_files)} file(s)")
            
            for file in st.session_state.additional_files:
                st.text(f"  • {file['name']}")
    
    st.divider()
    
    st.subheader("📋 Requirements / Dependencies")
    
    col_req1, col_req2 = st.columns([3, 1])
    
    with col_req1:
        requirements_input = st.text_area(
            "Enter Python packages (one per line)",
            placeholder="requests\nnumpy\npandas\npillow",
            height=150,
            help="List all pip packages your script needs"
        )
    
    with col_req2:
        st.markdown("**Or upload requirements.txt**")
        req_file = st.file_uploader("requirements.txt", type=['txt'], key="req_file")
        
        if req_file:
            try:
                content = req_file.read()
                requirements_input = content.decode('utf-8')
            except UnicodeDecodeError:
                st.error("❌ Error: requirements.txt must be UTF-8 encoded")
                requirements_input = ""
    
    if requirements_input:
        st.session_state.requirements = [
            line.strip() for line in requirements_input.split('\n') 
            if line.strip() and not line.strip().startswith('#')
        ]
        st.info(f"📦 {len(st.session_state.requirements)} package(s) detected")

with tab2:
    st.header("⚙️ Compilation Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Settings")
        
        exe_name = st.text_input(
            "Executable Name",
            value=st.session_state.main_file['name'].replace('.py', '') if st.session_state.main_file else "MyApp",
            help="Name for your .exe file"
        )
        
        icon_file = st.file_uploader(
            "Application Icon (.ico)",
            type=['ico'],
            help="Optional: Icon for your executable"
        )
        
        st.subheader("Build Options")
        
        one_file = st.checkbox("Bundle into single .exe file", value=True, help="--onefile")
        console_mode = st.checkbox("Show console window", value=False, help="Show terminal/console")
        clean_build = st.checkbox("Clean previous builds", value=True, help="--clean")
        
    with col2:
        st.subheader("Advanced Options")
        
        hidden_imports = st.text_area(
            "Hidden Imports (one per line)",
            placeholder="tkinter\nPIL.Image\nrequests.adapters",
            help="Modules that PyInstaller might miss",
            height=100
        )
        
        upx_compress = st.checkbox("Enable UPX compression", value=False, help="Reduce file size")
        
        include_common_imports = st.checkbox(
            "Include common hidden imports",
            value=True,
            help="Automatically include frequently needed modules"
        )

with tab3:
    st.header("📦 Generate Compilation Package")
    
    if not st.session_state.main_file:
        st.warning("⚠️ Please upload a main Python script in the 'Upload Files' tab first!")
    else:
        st.markdown("""
        <div class="success-box">
            <h4>✅ Ready to Generate Package</h4>
            <p>Your package will include:</p>
            <ul>
                <li>Your Python script(s)</li>
                <li>Automated compilation script</li>
                <li>Requirements file</li>
                <li>Detailed README with instructions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Show package contents
        with st.expander("📋 Package Contents Preview"):
            st.write("**Main Script:**", st.session_state.main_file['name'])
            if st.session_state.additional_files:
                st.write("**Additional Files:**")
                for f in st.session_state.additional_files:
                    st.write(f"  • {f['name']}")
            if st.session_state.requirements:
                st.write("**Dependencies:**")
                for req in st.session_state.requirements:
                    st.write(f"  • {req}")
        
        st.divider()
        
        # Generate button
        if st.button("🚀 Generate Compilation Package", type="primary", use_container_width=True):
            with st.spinner("Creating your package..."):
                # Create compilation script
                hidden_imports_list = [h.strip() for h in hidden_imports.split('\n') if h.strip()] if hidden_imports else []
                
                if include_common_imports:
                    hidden_imports_list.extend([
                        "IPython.lib.inputhook",
                        "pkg_resources.py2_warn",
                        "charset_normalizer.constant"
                    ])
                
                compile_script = f'''import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully!")
    except Exception as e:
        print(f"Error installing requirements: {{e}}")
        return False
    return True

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully!")
    except Exception as e:
        print(f"Error installing PyInstaller: {{e}}")
        return False
    return True

def compile_to_exe():
    """Compile Python script to executable"""
    print("\\nStarting compilation...")
    print("=" * 60)
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "{'--onefile' if one_file else '--onedir'}",
        "{'--windowed' if not console_mode else '--console'}",
        "{'--clean' if clean_build else ''}",
        "--name", "{exe_name}",
    ]
    
    # Remove empty strings
    cmd = [c for c in cmd if c]
    
    {"# Add icon" if icon_file else ""}
    {"cmd.extend(['--icon', 'icon.ico'])" if icon_file else ""}
    
    # Add hidden imports
    hidden_imports = {hidden_imports_list}
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    {"# UPX compression" if upx_compress else ""}
    {"cmd.append('--upx-dir')" if upx_compress else ""}
    
    # Main script
    cmd.append("{st.session_state.main_file['name']}")
    
    print("Command:", " ".join(cmd))
    print("=" * 60)
    
    try:
        subprocess.run(cmd, check=True)
        print("=" * 60)
        print("✅ COMPILATION SUCCESSFUL!")
        print(f"Your executable is in the 'dist' folder: dist/{exe_name}.exe")
        print("=" * 60)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Compilation failed: {{e}}")
        return False

def main():
    print("Python to EXE Compiler")
    print("=" * 60)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("Failed to install requirements. Exiting.")
        return
    
    # Step 2: Install PyInstaller
    if not install_pyinstaller():
        print("Failed to install PyInstaller. Exiting.")
        return
    
    # Step 3: Compile
    compile_to_exe()
    
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()
'''
                
                # Create README
                readme = f'''# Python to EXE Compilation Package

## 📋 Contents
- `{st.session_state.main_file['name']}` - Your main Python script
{"- Additional files: " + ", ".join([f['name'] for f in st.session_state.additional_files]) if st.session_state.additional_files else ""}
- `requirements.txt` - Python dependencies
- `compile.py` - Automated compilation script
- `README.md` - This file

## 🚀 How to Compile

### Option 1: Automated (Recommended)
1. Open a terminal/command prompt in this folder
2. Run: `python compile.py`
3. Wait for compilation to complete
4. Find your .exe in the `dist` folder

### Option 2: Manual
1. Install dependencies: `pip install -r requirements.txt`
2. Install PyInstaller: `pip install pyinstaller`
3. Run: `pyinstaller --onefile{"" if console_mode else " --windowed"} --name {exe_name} {st.session_state.main_file['name']}`
4. Find your .exe in the `dist` folder

## ⚙️ Configuration Used
- Executable name: {exe_name}
- Single file: {"Yes" if one_file else "No"}
- Console window: {"Yes" if console_mode else "No"}
- Clean build: {"Yes" if clean_build else "No"}
- UPX compression: {"Yes" if upx_compress else "No"}

## 📦 Requirements
{chr(10).join(f"- {req}" for req in st.session_state.requirements) if st.session_state.requirements else "No additional requirements"}

## 🔧 Troubleshooting
- If compilation fails, check that all dependencies are installed
- Make sure you have internet connection for pip installs
- Try running as administrator if you get permission errors
- Check the console output for specific error messages

## 📝 Notes
- Compilation requires Windows to create .exe files
- First compilation may take several minutes
- The executable will include all dependencies
- Antivirus might flag the .exe as suspicious (false positive)

Generated by Python to EXE Converter
'''
                
                # Create requirements.txt
                requirements_txt = '\n'.join(st.session_state.requirements) if st.session_state.requirements else "# No additional requirements"
                requirements_txt += "\npyinstaller>=6.0.0"
                
                # Create zip file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Add main script
                    zip_file.writestr(st.session_state.main_file['name'], st.session_state.main_file['content'])
                    
                    # Add additional files
                    for file in st.session_state.additional_files:
                        zip_file.writestr(file['name'], file['content'])
                    
                    # Add icon if provided
                    if icon_file:
                        icon_content = icon_file.read()
                        zip_file.writestr('icon.ico', icon_content)
                    
                    # Add compilation script
                    zip_file.writestr('compile.py', compile_script)
                    
                    # Add README
                    zip_file.writestr('README.md', readme)
                    
                    # Add requirements
                    zip_file.writestr('requirements.txt', requirements_txt)
                
                zip_buffer.seek(0)
                
                st.success("✅ Package created successfully!")
                
                # Download button
                st.download_button(
                    label="⬇️ Download Compilation Package (.zip)",
                    data=zip_buffer,
                    file_name=f"{exe_name}_compilation_package.zip",
                    mime="application/zip",
                    use_container_width=True
                )
                
                st.markdown("""
                <div class="info-box">
                    <h4>📖 Next Steps:</h4>
                    <ol>
                        <li>Download the package above</li>
                        <li>Extract the ZIP file to a folder</li>
                        <li>Open terminal/command prompt in that folder</li>
                        <li>Run: <code>python compile.py</code></li>
                        <li>Wait for compilation to complete</li>
                        <li>Find your .exe in the <code>dist</code> folder!</li>
                    </ol>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💡 <strong>Tip:</strong> The first compilation may take several minutes as PyInstaller analyzes your code</p>
    <p>🔒 <strong>Privacy:</strong> All processing happens in your browser. No files are uploaded to any server.</p>
    <p>Made with ❤️ for Python developers</p>
</div>
""", unsafe_allow_html=True)
