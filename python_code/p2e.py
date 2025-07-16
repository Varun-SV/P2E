import os
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import sys

class PyInstallerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyInstaller GUI - Enhanced")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.file_path = tk.StringVar()
        self.proxy_url = tk.StringVar()
        self.use_proxy = tk.BooleanVar()
        self.output_dir = tk.StringVar()
        self.exe_name = tk.StringVar()
        self.icon_path = tk.StringVar()
        self.is_running = False
        self.one_file = tk.BooleanVar(value=True)
        self.console_mode = tk.BooleanVar(value=False)
        self.upx_compress = tk.BooleanVar(value=False)
        self.clean_build = tk.BooleanVar(value=True)
        
        # Lists for additional files and folders
        self.additional_files = []
        self.additional_folders = []
        self.hidden_imports = []
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Main tab
        self.main_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="Main")
        
        # Advanced tab
        self.advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_tab, text="Advanced")
        
        # Files & Folders tab
        self.files_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.files_tab, text="Files & Folders")
        
        self.setup_main_tab()
        self.setup_advanced_tab()
        self.setup_files_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 5))
        
    def setup_main_tab(self):
        main_frame = ttk.Frame(self.main_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # File selection
        ttk.Label(main_frame, text="Python Script:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path, width=50)
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.browse_button = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=1)
        
        # Output directory
        ttk.Label(main_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, width=50)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(output_frame, text="Browse", command=self.browse_output_dir).grid(row=0, column=1)
        
        # Executable name
        ttk.Label(main_frame, text="Executable Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.exe_entry = ttk.Entry(main_frame, textvariable=self.exe_name, width=50)
        self.exe_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Icon file
        ttk.Label(main_frame, text="Icon File (.ico):").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        icon_frame = ttk.Frame(main_frame)
        icon_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        icon_frame.columnconfigure(0, weight=1)
        
        self.icon_entry = ttk.Entry(icon_frame, textvariable=self.icon_path, width=50)
        self.icon_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(icon_frame, text="Browse", command=self.browse_icon).grid(row=0, column=1)
        
        # Build options
        options_frame = ttk.LabelFrame(main_frame, text="Build Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(options_frame, text="One File (--onefile)", variable=self.one_file).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(options_frame, text="Console Mode (--console)", variable=self.console_mode).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(options_frame, text="UPX Compression (--upx-dir)", variable=self.upx_compress).grid(row=1, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(options_frame, text="Clean Build", variable=self.clean_build).grid(row=1, column=1, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start Compilation", command=self.start_compilation)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_compilation, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="Clear Log", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Settings", command=self.load_settings).pack(side=tk.LEFT, padx=5)
        
        # Progress section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Log output
        log_frame = ttk.LabelFrame(progress_frame, text="Output Log", padding="5")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def setup_advanced_tab(self):
        advanced_frame = ttk.Frame(self.advanced_tab, padding="10")
        advanced_frame.pack(fill=tk.BOTH, expand=True)
        
        # Proxy configuration
        proxy_frame = ttk.LabelFrame(advanced_frame, text="Proxy Configuration", padding="10")
        proxy_frame.pack(fill=tk.X, pady=5)
        proxy_frame.columnconfigure(1, weight=1)
        
        self.proxy_check = ttk.Checkbutton(proxy_frame, text="Use Proxy", variable=self.use_proxy, command=self.toggle_proxy)
        self.proxy_check.grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(proxy_frame, text="Proxy URL:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.proxy_entry = ttk.Entry(proxy_frame, textvariable=self.proxy_url, width=50, state=tk.DISABLED)
        self.proxy_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=2, padx=(5, 0))
        
        # Set default proxy
        self.proxy_url.set("http://proxy")
        
        # Hidden imports
        imports_frame = ttk.LabelFrame(advanced_frame, text="Hidden Imports", padding="10")
        imports_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        imports_frame.columnconfigure(0, weight=1)
        imports_frame.rowconfigure(1, weight=1)
        
        import_entry_frame = ttk.Frame(imports_frame)
        import_entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        import_entry_frame.columnconfigure(0, weight=1)
        
        self.import_entry = ttk.Entry(import_entry_frame, width=50)
        self.import_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(import_entry_frame, text="Add Import", command=self.add_hidden_import).grid(row=0, column=1)
        
        # Hidden imports listbox
        list_frame = ttk.Frame(imports_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.imports_listbox = tk.Listbox(list_frame, height=8)
        self.imports_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        import_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.imports_listbox.yview)
        import_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.imports_listbox.config(yscrollcommand=import_scroll.set)
        
        ttk.Button(imports_frame, text="Remove Selected", command=self.remove_hidden_import).grid(row=2, column=0, pady=5)
        
    def setup_files_tab(self):
        files_frame = ttk.Frame(self.files_tab, padding="10")
        files_frame.pack(fill=tk.BOTH, expand=True)
        
        # Additional files section
        files_section = ttk.LabelFrame(files_frame, text="Additional Files", padding="10")
        files_section.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        files_section.columnconfigure(0, weight=1)
        files_section.rowconfigure(1, weight=1)
        
        file_buttons_frame = ttk.Frame(files_section)
        file_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(file_buttons_frame, text="Add File", command=self.add_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_buttons_frame, text="Remove Selected", command=self.remove_file).pack(side=tk.LEFT, padx=5)
        
        # Files listbox
        files_list_frame = ttk.Frame(files_section)
        files_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        files_list_frame.columnconfigure(0, weight=1)
        files_list_frame.rowconfigure(0, weight=1)
        
        self.files_listbox = tk.Listbox(files_list_frame, height=8)
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        files_scroll = ttk.Scrollbar(files_list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        files_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.files_listbox.config(yscrollcommand=files_scroll.set)
        
        # Additional folders section
        folders_section = ttk.LabelFrame(files_frame, text="Additional Folders", padding="10")
        folders_section.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        folders_section.columnconfigure(0, weight=1)
        folders_section.rowconfigure(1, weight=1)
        
        folder_buttons_frame = ttk.Frame(folders_section)
        folder_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(folder_buttons_frame, text="Add Folder", command=self.add_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(folder_buttons_frame, text="Remove Selected", command=self.remove_folder).pack(side=tk.LEFT, padx=5)
        
        # Folders listbox
        folders_list_frame = ttk.Frame(folders_section)
        folders_list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        folders_list_frame.columnconfigure(0, weight=1)
        folders_list_frame.rowconfigure(0, weight=1)
        
        self.folders_listbox = tk.Listbox(folders_list_frame, height=8)
        self.folders_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        folders_scroll = ttk.Scrollbar(folders_list_frame, orient=tk.VERTICAL, command=self.folders_listbox.yview)
        folders_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.folders_listbox.config(yscrollcommand=folders_scroll.set)
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python files", "*.py"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path.set(file_path)
            # Auto-set output directory and exe name
            if not self.output_dir.get():
                self.output_dir.set(os.path.dirname(file_path))
            if not self.exe_name.get():
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                self.exe_name.set(base_name)
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir.set(dir_path)
    
    def browse_icon(self):
        icon_path = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        if icon_path:
            self.icon_path.set(icon_path)
    
    def add_file(self):
        file_path = filedialog.askopenfilename(
            title="Select File to Include",
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            dest_path = filedialog.askstring("Destination Path", 
                                           f"Enter destination path for {os.path.basename(file_path)}:",
                                           initialvalue=os.path.basename(file_path))
            if dest_path:
                entry = f"{file_path} -> {dest_path}"
                self.additional_files.append((file_path, dest_path))
                self.files_listbox.insert(tk.END, entry)
    
    def remove_file(self):
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            self.files_listbox.delete(index)
            self.additional_files.pop(index)
    
    def add_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder to Include")
        if folder_path:
            dest_path = filedialog.askstring("Destination Path", 
                                           f"Enter destination path for {os.path.basename(folder_path)}:",
                                           initialvalue=os.path.basename(folder_path))
            if dest_path:
                entry = f"{folder_path} -> {dest_path}"
                self.additional_folders.append((folder_path, dest_path))
                self.folders_listbox.insert(tk.END, entry)
    
    def remove_folder(self):
        selection = self.folders_listbox.curselection()
        if selection:
            index = selection[0]
            self.folders_listbox.delete(index)
            self.additional_folders.pop(index)
    
    def add_hidden_import(self):
        import_name = self.import_entry.get().strip()
        if import_name and import_name not in self.hidden_imports:
            self.hidden_imports.append(import_name)
            self.imports_listbox.insert(tk.END, import_name)
            self.import_entry.delete(0, tk.END)
    
    def remove_hidden_import(self):
        selection = self.imports_listbox.curselection()
        if selection:
            index = selection[0]
            self.imports_listbox.delete(index)
            self.hidden_imports.pop(index)
    
    def toggle_proxy(self):
        if self.use_proxy.get():
            self.proxy_entry.config(state=tk.NORMAL)
        else:
            self.proxy_entry.config(state=tk.DISABLED)
    
    def save_settings(self):
        settings = {
            'proxy_url': self.proxy_url.get(),
            'use_proxy': self.use_proxy.get(),
            'output_dir': self.output_dir.get(),
            'exe_name': self.exe_name.get(),
            'icon_path': self.icon_path.get(),
            'one_file': self.one_file.get(),
            'console_mode': self.console_mode.get(),
            'upx_compress': self.upx_compress.get(),
            'clean_build': self.clean_build.get(),
            'additional_files': self.additional_files,
            'additional_folders': self.additional_folders,
            'hidden_imports': self.hidden_imports
        }
        
        file_path = filedialog.asksaveasfilename(
            title="Save Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(settings, f, indent=2)
                self.log_message(f"Settings saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
    
    def load_settings(self):
        file_path = filedialog.askopenfilename(
            title="Load Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    settings = json.load(f)
                
                # Load settings
                self.proxy_url.set(settings.get('proxy_url', 'http://proxy'))
                self.use_proxy.set(settings.get('use_proxy', False))
                self.output_dir.set(settings.get('output_dir', ''))
                self.exe_name.set(settings.get('exe_name', ''))
                self.icon_path.set(settings.get('icon_path', ''))
                self.one_file.set(settings.get('one_file', True))
                self.console_mode.set(settings.get('console_mode', False))
                self.upx_compress.set(settings.get('upx_compress', False))
                self.clean_build.set(settings.get('clean_build', True))
                
                # Load lists
                self.additional_files = settings.get('additional_files', [])
                self.additional_folders = settings.get('additional_folders', [])
                self.hidden_imports = settings.get('hidden_imports', [])
                
                # Update UI
                self.update_listboxes()
                self.toggle_proxy()
                
                self.log_message(f"Settings loaded from: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load settings: {str(e)}")
    
    def update_listboxes(self):
        # Clear and populate files listbox
        self.files_listbox.delete(0, tk.END)
        for file_path, dest_path in self.additional_files:
            self.files_listbox.insert(tk.END, f"{file_path} -> {dest_path}")
        
        # Clear and populate folders listbox
        self.folders_listbox.delete(0, tk.END)
        for folder_path, dest_path in self.additional_folders:
            self.folders_listbox.insert(tk.END, f"{folder_path} -> {dest_path}")
        
        # Clear and populate imports listbox
        self.imports_listbox.delete(0, tk.END)
        for import_name in self.hidden_imports:
            self.imports_listbox.insert(tk.END, import_name)
    
    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
    
    def update_progress(self, value, message):
        self.progress_bar['value'] = value
        self.progress_var.set(message)
        self.status_var.set(message)
        self.root.update()
    
    def start_compilation(self):
        if not self.file_path.get():
            messagebox.showerror("Error", "Please select a Python script first!")
            return
        
        if not os.path.exists(self.file_path.get()):
            messagebox.showerror("Error", "Selected file does not exist!")
            return
        
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.browse_button.config(state=tk.DISABLED)
        
        # Start compilation in a separate thread
        self.compilation_thread = threading.Thread(target=self.compile_script)
        self.compilation_thread.daemon = True
        self.compilation_thread.start()
    
    def stop_compilation(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.NORMAL)
        self.update_progress(0, "Stopped by user")
        self.log_message("Compilation stopped by user")
    
    def compile_script(self):
        try:
            file_name = self.file_path.get()
            output_dir = self.output_dir.get() or os.path.dirname(file_name)
            exe_name = self.exe_name.get() or os.path.splitext(os.path.basename(file_name))[0]
            
            # Step 1: Check PyInstaller installation
            if not self.is_running:
                return
            
            self.update_progress(10, "Checking PyInstaller installation...")
            self.log_message("Checking PyInstaller installation...")
            
            try:
                result = subprocess.run([sys.executable, "-m", "pip", "show", "pyinstaller"], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.update_progress(20, "Installing PyInstaller...")
                    self.log_message("Installing PyInstaller...")
                    
                    install_cmd = [sys.executable, "-m", "pip", "install", "pyinstaller"]
                    if self.use_proxy.get() and self.proxy_url.get():
                        install_cmd.extend(["--proxy", self.proxy_url.get()])
                    
                    result = subprocess.run(install_cmd, capture_output=True, text=True)
                    if result.returncode != 0:
                        raise Exception(f"Failed to install PyInstaller: {result.stderr}")
                    
                    self.log_message("PyInstaller installed successfully")
                else:
                    self.log_message("PyInstaller already installed")
            except Exception as e:
                raise Exception(f"Error checking/installing PyInstaller: {str(e)}")
            
            # Step 2: Build PyInstaller command
            if not self.is_running:
                return
            
            self.update_progress(40, "Building PyInstaller command...")
            self.log_message("Building PyInstaller command...")
            
            cmd = [sys.executable, "-m", "PyInstaller"]
            
            # Basic options
            if self.one_file.get():
                cmd.append("--onefile")
            else:
                cmd.append("--onedir")
            
            if not self.console_mode.get():
                cmd.append("--windowed")
            
            if self.clean_build.get():
                cmd.append("--clean")
            
            # Output directory
            cmd.extend(["--distpath", output_dir])
            
            # Executable name
            if exe_name:
                cmd.extend(["--name", exe_name])
            
            # Icon
            if self.icon_path.get() and os.path.exists(self.icon_path.get()):
                cmd.extend(["--icon", self.icon_path.get()])
            
            # UPX compression
            if self.upx_compress.get():
                cmd.append("--upx-dir")
            
            # Additional files
            for file_path, dest_path in self.additional_files:
                cmd.extend(["--add-data", f"{file_path}{os.pathsep}{dest_path}"])
            
            # Additional folders
            for folder_path, dest_path in self.additional_folders:
                cmd.extend(["--add-data", f"{folder_path}{os.pathsep}{dest_path}"])
            
            # Hidden imports
            for import_name in self.hidden_imports:
                cmd.extend(["--hidden-import", import_name])
            
            # Add common hidden imports
            common_imports = [
                "IPython.lib.inputhook",
                "pkg_resources.py2_warn",
                "charset_normalizer.constant"
            ]
            for import_name in common_imports:
                cmd.extend(["--hidden-import", import_name])
            
            # Script file
            cmd.append(file_name)
            
            # Step 3: Run PyInstaller
            if not self.is_running:
                return
            
            self.update_progress(60, "Running PyInstaller...")
            self.log_message("Starting PyInstaller compilation...")
            self.log_message(f"Command: {' '.join(cmd)}")
            
            # Change to script directory
            script_dir = os.path.dirname(os.path.abspath(file_name))
            original_cwd = os.getcwd()
            os.chdir(script_dir)
            
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT, text=True, 
                                         universal_newlines=True)
                
                # Read output in real-time
                for line in iter(process.stdout.readline, ''):
                    if not self.is_running:
                        process.terminate()
                        return
                    
                    self.log_message(line.strip())
                
                process.wait()
                
                if process.returncode != 0:
                    raise Exception(f"PyInstaller failed with return code {process.returncode}")
                
            finally:
                os.chdir(original_cwd)
            
            # Step 4: Post-compilation cleanup
            if not self.is_running:
                return
            
            self.update_progress(80, "Post-compilation cleanup...")
            self.log_message("Post-compilation cleanup...")
            
            if self.clean_build.get():
                # Clean up build directory
                build_dir = os.path.join(script_dir, 'build')
                if os.path.exists(build_dir):
                    try:
                        import shutil
                        shutil.rmtree(build_dir)
                        self.log_message(f"Removed build directory: {build_dir}")
                    except Exception as e:
                        self.log_message(f"Warning: Could not remove build directory: {str(e)}")
                
                # Clean up spec file
                spec_file = os.path.join(script_dir, f"{exe_name}.spec")
                if os.path.exists(spec_file):
                    try:
                        os.remove(spec_file)
                        self.log_message(f"Removed spec file: {spec_file}")
                    except Exception as e:
                        self.log_message(f"Warning: Could not remove spec file: {str(e)}")
            
            # Step 5: Verify output
            if not self.is_running:
                return
            
            self.update_progress(90, "Verifying output...")
            self.log_message("Verifying output...")
            
            if self.one_file.get():
                expected_exe = os.path.join(output_dir, f"{exe_name}.exe")
            else:
                expected_exe = os.path.join(output_dir, exe_name, f"{exe_name}.exe")
            
            if os.path.exists(expected_exe):
                file_size = os.path.getsize(expected_exe)
                size_mb = file_size / (1024 * 1024)
                self.log_message(f"Executable created: {expected_exe}")
                self.log_message(f"File size: {size_mb:.2f} MB")
            else:
                self.log_message("Warning: Expected executable not found at expected location")
            
            # Step 6: Complete
            if not self.is_running:
                return
            
            self.update_progress(100, "Compilation completed successfully!")
            self.log_message("="*60)
            self.log_message("COMPILATION COMPLETED SUCCESSFULLY!")
            self.log_message(f"Output directory: {output_dir}")
            if os.path.exists(expected_exe):
                self.log_message(f"Executable: {expected_exe}")
            self.log_message("="*60)
            
            messagebox.showinfo("Success", f"Compilation completed successfully!\nOutput directory: {output_dir}")
            
        except Exception as e:
            self.log_message(f"ERROR: {str(e)}")
            self.update_progress(0, "Error occurred during compilation")
            messagebox.showerror("Error", f"Compilation failed: {str(e)}")
        
        finally:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.browse_button.config(state=tk.NORMAL)

def main():
    root = tk.Tk()
    PyInstallerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
