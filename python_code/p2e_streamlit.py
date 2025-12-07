import streamlit as st
import os
import subprocess
import shutil
import tempfile
import zipfile
from pathlib import Path

# --- Page Config ---
st.set_page_config(page_title="PyInstaller Cloud GUI", layout="wide")

st.title("📦 PyInstaller Cloud GUI")
st.markdown("""
Convert Python scripts to standalone executables. 
**Note:** Since this app runs on a Linux server, the **Cloud Build** will generate a **Linux Binary**. 
To get a Windows `.exe`, use the **Command Generator** tab and run it locally.
""")

# --- Helper Functions ---

def save_uploaded_file(uploaded_file, target_dir):
    try:
        path = os.path.join(target_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return path
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return None

def zip_directory(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

# --- Sidebar Configuration ---
st.sidebar.header("Configuration")

# Main Script Upload
uploaded_script = st.sidebar.file_uploader("Upload Python Script (.py)", type=["py"])

# General Options
st.sidebar.subheader("Build Options")
one_file = st.sidebar.checkbox("One File (--onefile)", value=True)
console_mode = st.sidebar.checkbox("Console Mode (--console)", value=True, help="Show terminal window when running")
clean_build = st.sidebar.checkbox("Clean Build (--clean)", value=True)

# Icon Upload
uploaded_icon = st.sidebar.file_uploader("Icon (.ico or .png for Linux)", type=["ico", "png"])

# Advanced Options
with st.sidebar.expander("Advanced Options"):
    exe_name = st.text_input("Executable Name (Optional)")
    hidden_imports = st.text_area("Hidden Imports (comma separated)", placeholder="pandas,numpy")
    add_data_files = st.file_uploader("Additional Data Files", accept_multiple_files=True)

# --- Main Logic ---

if uploaded_script:
    # Create Tabs
    tab1, tab2 = st.tabs(["☁️ Cloud Build (Linux)", "💻 Local Command (Windows/Mac)"])

    # --- TAB 1: CLOUD BUILD ---
    with tab1:
        st.info("This will compile the script on the current server (Linux).")
        
        if st.button("Start Cloud Compilation", type="primary"):
            # Create a temporary directory for the build process
            with tempfile.TemporaryDirectory() as temp_dir:
                status_text = st.empty()
                progress_bar = st.progress(0)

                # 1. Setup Environment
                status_text.text("Setting up environment...")
                work_dir = os.path.join(temp_dir, "work")
                dist_dir = os.path.join(temp_dir, "dist")
                os.makedirs(work_dir, exist_ok=True)
                
                # Save Script
                script_path = save_uploaded_file(uploaded_script, work_dir)
                script_name = uploaded_script.name
                
                # Save Icon if exists
                icon_path = None
                if uploaded_icon:
                    icon_path = save_uploaded_file(uploaded_icon, work_dir)

                # Save Additional Files
                data_args = []
                if add_data_files:
                    for f in add_data_files:
                        f_path = save_uploaded_file(f, work_dir)
                        # On Linux separator is :, on Windows ;
                        # We use . because files are in root of work_dir
                        data_args.append(f"--add-data={f.name}:.") 

                progress_bar.progress(25)

                # 2. Build Command
                status_text.text("Building PyInstaller command...")
                
                cmd = ["pyinstaller", script_path]
                
                if one_file:
                    cmd.append("--onefile")
                else:
                    cmd.append("--onedir")
                
                if not console_mode:
                    cmd.append("--noconsole") # In Linux "windowed" is noconsole
                
                if clean_build:
                    cmd.append("--clean")

                if exe_name:
                    cmd.extend(["--name", exe_name])
                
                if icon_path:
                    cmd.extend(["--icon", icon_path])

                # Hidden Imports
                if hidden_imports:
                    imports = [x.strip() for x in hidden_imports.split(",") if x.strip()]
                    for imp in imports:
                        cmd.extend(["--hidden-import", imp])
                
                # Add Data
                cmd.extend(data_args)

                # Set Output Dirs
                cmd.extend(["--distpath", dist_dir])
                cmd.extend(["--workpath", os.path.join(temp_dir, "build")])
                cmd.extend(["--specpath", work_dir])

                progress_bar.progress(50)

                # 3. Execute
                status_text.text("Running PyInstaller... (This may take a minute)")
                
                # Display command for debug
                st.code(" ".join(cmd), language="bash")

                try:
                    process = subprocess.run(
                        cmd, 
                        capture_output=True, 
                        text=True, 
                        cwd=work_dir
                    )

                    if process.returncode == 0:
                        progress_bar.progress(90)
                        status_text.text("Compressing output...")
                        
                        # Zip the result
                        zip_output_path = os.path.join(temp_dir, "output.zip")
                        zip_directory(dist_dir, zip_output_path)
                        
                        progress_bar.progress(100)
                        status_text.success("Compilation Successful!")
                        
                        # Show logs in expander
                        with st.expander("View Build Logs"):
                            st.text(process.stdout)
                        
                        # Download Button
                        with open(zip_output_path, "rb") as fp:
                            st.download_button(
                                label="⬇️ Download Build (Linux Binary)",
                                data=fp,
                                file_name=f"{exe_name if exe_name else 'app'}_linux.zip",
                                mime="application/zip"
                            )
                    else:
                        st.error("Compilation Failed")
                        st.error(process.stderr)
                        with st.expander("View Output Logs"):
                            st.text(process.stdout)
                
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    # --- TAB 2: COMMAND GENERATOR ---
    with tab2:
        st.info("Use this to generate a command to run on your local Windows machine.")
        
        st.subheader("Your Local Configuration")
        
        # Windows-specific inputs
        win_icon_path = st.text_input("Local Path to Icon (e.g., C:\\Users\\Icon.ico)", value="icon.ico" if uploaded_icon else "")
        win_script_path = st.text_input("Local Path to Script", value=uploaded_script.name)
        
        # Build the command string
        cmd_parts = ["pyinstaller", f'"{win_script_path}"']
        
        if one_file:
            cmd_parts.append("--onefile")
        else:
            cmd_parts.append("--onedir")
            
        if not console_mode:
            cmd_parts.append("--noconsole")
            
        if clean_build:
            cmd_parts.append("--clean")
            
        if exe_name:
            cmd_parts.append(f'--name "{exe_name}"')
            
        if win_icon_path:
            cmd_parts.append(f'--icon "{win_icon_path}"')
            
        if hidden_imports:
            imports = [x.strip() for x in hidden_imports.split(",") if x.strip()]
            for imp in imports:
                cmd_parts.append(f'--hidden-import "{imp}"')

        if add_data_files:
            for f in add_data_files:
                # Windows separator ;
                cmd_parts.append(f'--add-data "{f.name};."')

        full_command = " ".join(cmd_parts)
        
        st.markdown("### Copy and paste this into your Command Prompt / PowerShell:")
        st.code(full_command, language="powershell")
        
        st.warning("Make sure you have `pip install pyinstaller` executed on your machine first.")

else:
    st.info("👈 Please upload a Python script in the sidebar to begin.")
