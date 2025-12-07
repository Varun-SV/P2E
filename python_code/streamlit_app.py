import streamlit as st
import os
import shutil
import tempfile
import subprocess
import sys
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Python to EXE Converter",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .upload-box {
        border: 2px dashed #4CAF50;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f0f8f0;
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
        width: 100%;
    }
    .stButton>button:hover { background-color: #45a049; }
    .console-output {
        background-color: #0e1117;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        padding: 1rem;
        border-radius: 5px;
        height: 300px;
        overflow-y: scroll;
        border: 1px solid #333;
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
st.title("⚡ Python to EXE Builder")
st.markdown("Upload your Python script and get a standalone executable.")

st.divider()

# Main layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Upload Files")
    
    st.subheader("🎯 Main Script")
    main_script = st.file_uploader(
        "Upload your main .py file",
        type=['py'],
        key="main_script"
    )
    
    if main_script:
        st.session_state.main_file = {
            'name': main_script.name,
            'content': main_script.getvalue()
        }
        st.success(f"Loaded: {main_script.name}")

    st.subheader("📚 Dependencies / Assets")
    additional_files = st.file_uploader(
        "Upload additional .py files, images, data, or config files",
        accept_multiple_files=True,
        key="additional_files_uploader"
    )
    
    if additional_files:
        st.session_state.additional_files = []
        for file in additional_files:
            st.session_state.additional_files.append({
                'name': file.name,
                'content': file.getvalue()
            })
        st.success(f"Loaded {len(additional_files)} additional file(s)")

    st.subheader("📦 Requirements")
    req_text = st.text_area(
        "Enter pip packages (one per line)", 
        placeholder="pandas\nrequests",
        height=100
    )
    if req_text:
        st.session_state.requirements = [line.strip() for line in req_text.split('\n') if line.strip()]

with col2:
    st.header("2. Configuration & Build")
    
    exe_name = st.text_input(
        "Output Name",
        value=st.session_state.main_file['name'].replace('.py', '') if st.session_state.main_file else "MyApp"
    )
    
    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        one_file = st.checkbox("One File (Bundle everything)", value=True)
        console_mode = st.checkbox("Show Console", value=True, help="Keep checked for CLI apps, uncheck for GUIs")
    with col_opt2:
        install_reqs = st.checkbox("Install Requirements first", value=True, help="Attempts to pip install packages before building")
        clean_build = st.checkbox("Clean Build", value=True)

    st.divider()

    if st.button("🚀 BUILD EXECUTABLE"):
        if not st.session_state.main_file:
            st.error("Please upload a main Python file first.")
        else:
            # Create a temporary directory for the build process
            with tempfile.TemporaryDirectory() as temp_dir:
                status_container = st.empty()
                log_container = st.empty()
                logs = []

                def log(message):
                    logs.append(message)
                    log_container.code("\n".join(logs), language="bash")

                try:
                    status_container.info("Preparing environment...")
                    
                    # 1. Save Main File
                    main_path = os.path.join(temp_dir, st.session_state.main_file['name'])
                    with open(main_path, 'wb') as f:
                        f.write(st.session_state.main_file['content'])
                    log(f"Saved {st.session_state.main_file['name']}")

                    # 2. Save Additional Files
                    for f_data in st.session_state.additional_files:
                        f_path = os.path.join(temp_dir, f_data['name'])
                        with open(f_path, 'wb') as f:
                            f.write(f_data['content'])
                        log(f"Saved {f_data['name']}")

                    # 3. Install Requirements
                    if install_reqs and st.session_state.requirements:
                        status_container.info("Installing dependencies...")
                        log("--- Installing Dependencies ---")
                        # Write req file
                        req_path = os.path.join(temp_dir, "requirements.txt")
                        with open(req_path, "w") as f:
                            f.write("\n".join(st.session_state.requirements))
                        
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_path])
                        log("Dependencies installed.")

                    # Ensure PyInstaller is installed
                    try:
                        import PyInstaller
                    except ImportError:
                        log("Installing PyInstaller...")
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

                    # 4. Build Command
                    status_container.info("Compiling... This may take a minute.")
                    log("--- Starting PyInstaller ---")
                    
                    cmd = [
                        sys.executable, "-m", "PyInstaller",
                        "--noconfirm",
                        "--distpath", os.path.join(temp_dir, "dist"),
                        "--workpath", os.path.join(temp_dir, "build"),
                        "--specpath", temp_dir,
                        "--name", exe_name,
                    ]

                    if one_file:
                        cmd.append("--onefile")
                    else:
                        cmd.append("--onedir")
                    
                    if not console_mode:
                        cmd.append("--noconsole")
                    
                    if clean_build:
                        cmd.append("--clean")

                    # Add data files (simple approach: add all additional files as data)
                    # Note: complex folder structures require more logic, assuming flat for now or user zips
                    sep = ';' if sys.platform.startswith('win') else ':'
                    for f_data in st.session_state.additional_files:
                        # Format: source_file;dest_folder
                        cmd.extend(['--add-data', f"{os.path.join(temp_dir, f_data['name'])}{sep}."])

                    cmd.append(main_path)

                    log(f"Running: {' '.join(cmd)}")

                    # Run PyInstaller
                    process = subprocess.run(
                        cmd, 
                        capture_output=True, 
                        text=True,
                        cwd=temp_dir
                    )

                    if process.returncode != 0:
                        log("ERROR:")
                        log(process.stderr)
                        status_container.error("Compilation failed. Check logs.")
                    else:
                        log("COMPILATION SUCCESSFUL")
                        status_container.success("Build Complete!")
                        
                        # locate output
                        dist_folder = os.path.join(temp_dir, "dist")
                        
                        output_file = None
                        output_filename = ""
                        
                        if one_file:
                            # Search for the file (handling .exe extension difference)
                            for f in os.listdir(dist_folder):
                                if f.startswith(exe_name):
                                    output_file = os.path.join(dist_folder, f)
                                    output_filename = f
                                    break
                        else:
                            # Zip the folder if it's not onefile
                            output_filename = f"{exe_name}.zip"
                            output_file = os.path.join(temp_dir, output_filename)
                            shutil.make_archive(output_file.replace('.zip', ''), 'zip', os.path.join(dist_folder, exe_name))

                        if output_file and os.path.exists(output_file):
                            with open(output_file, "rb") as file:
                                btn = st.download_button(
                                    label=f"⬇️ DOWNLOAD {output_filename}",
                                    data=file,
                                    file_name=output_filename,
                                    mime="application/octet-stream",
                                    type="primary"
                                )
                        else:
                            status_container.error("Could not locate output file.")

                except Exception as e:
                    status_container.error(f"An error occurred: {str(e)}")
                    log(str(e))

# Footer
st.divider()
st.caption("Note: The operating system of the generated executable matches the server OS (Windows -> .exe, Linux -> binary).")
