import React, { useState } from 'react';
import { Copy, Download, Plus, Trash2, Settings, FileCode, FolderPlus, Package } from 'lucide-react';

export default function PyInstallerGenerator() {
  const [scriptName, setScriptName] = useState('');
  const [exeName, setExeName] = useState('');
  const [outputDir, setOutputDir] = useState('./dist');
  const [iconPath, setIconPath] = useState('');
  
  const [oneFile, setOneFile] = useState(true);
  const [consoleMode, setConsoleMode] = useState(false);
  const [cleanBuild, setCleanBuild] = useState(true);
  const [upxCompress, setUpxCompress] = useState(false);
  
  const [useProxy, setUseProxy] = useState(false);
  const [proxyUrl, setProxyUrl] = useState('http://proxy');
  
  const [hiddenImports, setHiddenImports] = useState([]);
  const [newImport, setNewImport] = useState('');
  
  const [additionalFiles, setAdditionalFiles] = useState([]);
  const [newFile, setNewFile] = useState({ source: '', dest: '' });
  
  const [additionalFolders, setAdditionalFolders] = useState([]);
  const [newFolder, setNewFolder] = useState({ source: '', dest: '' });
  
  const [copied, setCopied] = useState(false);

  const addHiddenImport = () => {
    if (newImport.trim() && !hiddenImports.includes(newImport.trim())) {
      setHiddenImports([...hiddenImports, newImport.trim()]);
      setNewImport('');
    }
  };

  const removeHiddenImport = (index) => {
    setHiddenImports(hiddenImports.filter((_, i) => i !== index));
  };

  const addFile = () => {
    if (newFile.source.trim() && newFile.dest.trim()) {
      setAdditionalFiles([...additionalFiles, { ...newFile }]);
      setNewFile({ source: '', dest: '' });
    }
  };

  const removeFile = (index) => {
    setAdditionalFiles(additionalFiles.filter((_, i) => i !== index));
  };

  const addFolder = () => {
    if (newFolder.source.trim() && newFolder.dest.trim()) {
      setAdditionalFolders([...additionalFolders, { ...newFolder }]);
      setNewFolder({ source: '', dest: '' });
    }
  };

  const removeFolder = (index) => {
    setAdditionalFolders(additionalFolders.filter((_, i) => i !== index));
  };

  const generateCommand = () => {
    if (!scriptName.trim()) return '';

    let cmd = 'pyinstaller';
    
    if (oneFile) cmd += ' --onefile';
    else cmd += ' --onedir';
    
    if (!consoleMode) cmd += ' --windowed';
    if (cleanBuild) cmd += ' --clean';
    
    if (outputDir.trim()) cmd += ` --distpath "${outputDir}"`;
    if (exeName.trim()) cmd += ` --name "${exeName}"`;
    if (iconPath.trim()) cmd += ` --icon "${iconPath}"`;
    if (upxCompress) cmd += ' --upx-dir';
    
    additionalFiles.forEach(file => {
      const separator = process.platform === 'win32' ? ';' : ':';
      cmd += ` --add-data "${file.source}${separator}${file.dest}"`;
    });
    
    additionalFolders.forEach(folder => {
      const separator = process.platform === 'win32' ? ';' : ':';
      cmd += ` --add-data "${folder.source}${separator}${folder.dest}"`;
    });
    
    hiddenImports.forEach(imp => {
      cmd += ` --hidden-import ${imp}`;
    });
    
    cmd += ` "${scriptName}"`;
    
    return cmd;
  };

  const generatePythonScript = () => {
    const command = generateCommand();
    if (!command) return '';

    return `import subprocess
import sys

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"${useProxy && proxyUrl ? `, "--proxy", "${proxyUrl}"` : ''}])
        print("PyInstaller installed successfully")

def compile_script():
    """Compile the Python script to executable"""
    install_pyinstaller()
    
    cmd = ${JSON.stringify(command.split(' '))}
    
    print("Running PyInstaller with command:")
    print(" ".join(cmd))
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False, text=True)
        print("-" * 60)
        print("Compilation completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during compilation: {e}")
        return False

if __name__ == "__main__":
    compile_script()
`;
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const downloadPythonScript = () => {
    const script = generatePythonScript();
    const blob = new Blob([script], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compile_script.py';
    a.click();
    URL.revokeObjectURL(url);
  };

  const command = generateCommand();
  const pythonScript = generatePythonScript();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 text-white">
            <div className="flex items-center gap-3">
              <Package className="w-10 h-10" />
              <div>
                <h1 className="text-3xl font-bold">PyInstaller Command Generator</h1>
                <p className="text-blue-100 mt-1">Create PyInstaller commands for your Python projects</p>
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Left Column - Main Settings */}
              <div className="space-y-6">
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-lg border border-blue-200">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    <FileCode className="w-5 h-5 text-blue-600" />
                    Basic Configuration
                  </h2>
                  
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Python Script Path *
                      </label>
                      <input
                        type="text"
                        value={scriptName}
                        onChange={(e) => setScriptName(e.target.value)}
                        placeholder="script.py or /path/to/script.py"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Executable Name
                      </label>
                      <input
                        type="text"
                        value={exeName}
                        onChange={(e) => setExeName(e.target.value)}
                        placeholder="MyApp (optional)"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Output Directory
                      </label>
                      <input
                        type="text"
                        value={outputDir}
                        onChange={(e) => setOutputDir(e.target.value)}
                        placeholder="./dist"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Icon File (.ico)
                      </label>
                      <input
                        type="text"
                        value={iconPath}
                        onChange={(e) => setIconPath(e.target.value)}
                        placeholder="icon.ico (optional)"
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-purple-50 to-pink-50 p-4 rounded-lg border border-purple-200">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    <Settings className="w-5 h-5 text-purple-600" />
                    Build Options
                  </h2>
                  
                  <div className="space-y-3">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={oneFile}
                        onChange={(e) => setOneFile(e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                      />
                      <span className="text-sm font-medium text-gray-700">
                        Single File (--onefile)
                      </span>
                    </label>

                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={consoleMode}
                        onChange={(e) => setConsoleMode(e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                      />
                      <span className="text-sm font-medium text-gray-700">
                        Console Mode (show terminal)
                      </span>
                    </label>

                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={cleanBuild}
                        onChange={(e) => setCleanBuild(e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                      />
                      <span className="text-sm font-medium text-gray-700">
                        Clean Build (--clean)
                      </span>
                    </label>

                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={upxCompress}
                        onChange={(e) => setUpxCompress(e.target.checked)}
                        className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                      />
                      <span className="text-sm font-medium text-gray-700">
                        UPX Compression
                      </span>
                    </label>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-teal-50 p-4 rounded-lg border border-green-200">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Proxy Settings</h2>
                  
                  <label className="flex items-center gap-2 cursor-pointer mb-3">
                    <input
                      type="checkbox"
                      checked={useProxy}
                      onChange={(e) => setUseProxy(e.target.checked)}
                      className="w-4 h-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500"
                    />
                    <span className="text-sm font-medium text-gray-700">Use Proxy</span>
                  </label>

                  {useProxy && (
                    <input
                      type="text"
                      value={proxyUrl}
                      onChange={(e) => setProxyUrl(e.target.value)}
                      placeholder="http://proxy:port"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                  )}
                </div>
              </div>

              {/* Right Column - Advanced Settings */}
              <div className="space-y-6">
                <div className="bg-gradient-to-br from-orange-50 to-red-50 p-4 rounded-lg border border-orange-200">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Hidden Imports</h2>
                  
                  <div className="flex gap-2 mb-3">
                    <input
                      type="text"
                      value={newImport}
                      onChange={(e) => setNewImport(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && addHiddenImport()}
                      placeholder="module.name"
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <button
                      onClick={addHiddenImport}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      <Plus className="w-5 h-5" />
                    </button>
                  </div>

                  <div className="space-y-2 max-h-40 overflow-y-auto">
                    {hiddenImports.map((imp, index) => (
                      <div key={index} className="flex items-center justify-between bg-white p-2 rounded border">
                        <span className="text-sm font-mono">{imp}</span>
                        <button
                          onClick={() => removeHiddenImport(index)}
                          className="text-red-600 hover:text-red-800"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-gradient-to-br from-yellow-50 to-amber-50 p-4 rounded-lg border border-yellow-200">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4">Additional Files</h2>
                  
                  <div className="space-y-2 mb-3">
                    <input
                      type="text"
                      value={newFile.source}
                      onChange={(e) => setNewFile({ ...newFile, source: e.target.value })}
                      placeholder="Source path"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={newFile.dest}
                        onChange={(e) => setNewFile({ ...newFile, dest: e.target.value })}
                        placeholder="Destination"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <button
                        onClick={addFile}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <Plus className="w-5 h-5" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2 max-h-32 overflow-y-auto">
                    {additionalFiles.map((file, index) => (
                      <div key={index} className="flex items-center justify-between bg-white p-2 rounded border">
                        <span className="text-xs font-mono truncate">{file.source} → {file.dest}</span>
                        <button
                          onClick={() => removeFile(index)}
                          className="text-red-600 hover:text-red-800 ml-2"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="bg-gradient-to-br from-cyan-50 to-blue-50 p-4 rounded-lg border border-cyan-200">
                  <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    <FolderPlus className="w-5 h-5 text-cyan-600" />
                    Additional Folders
                  </h2>
                  
                  <div className="space-y-2 mb-3">
                    <input
                      type="text"
                      value={newFolder.source}
                      onChange={(e) => setNewFolder({ ...newFolder, source: e.target.value })}
                      placeholder="Source folder"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={newFolder.dest}
                        onChange={(e) => setNewFolder({ ...newFolder, dest: e.target.value })}
                        placeholder="Destination"
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                      <button
                        onClick={addFolder}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        <Plus className="w-5 h-5" />
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2 max-h-32 overflow-y-auto">
                    {additionalFolders.map((folder, index) => (
                      <div key={index} className="flex items-center justify-between bg-white p-2 rounded border">
                        <span className="text-xs font-mono truncate">{folder.source} → {folder.dest}</span>
                        <button
                          onClick={() => removeFolder(index)}
                          className="text-red-600 hover:text-red-800 ml-2"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Generated Output */}
            {command && (
              <div className="mt-6 space-y-4">
                <div className="bg-gray-900 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-white font-semibold">Generated Command</h3>
                    <button
                      onClick={() => copyToClipboard(command)}
                      className="flex items-center gap-2 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm"
                    >
                      <Copy className="w-4 h-4" />
                      {copied ? 'Copied!' : 'Copy'}
                    </button>
                  </div>
                  <pre className="text-green-400 text-sm overflow-x-auto">{command}</pre>
                </div>

                <div className="bg-indigo-900 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-white font-semibold">Python Compilation Script</h3>
                    <div className="flex gap-2">
                      <button
                        onClick={() => copyToClipboard(pythonScript)}
                        className="flex items-center gap-2 px-3 py-1 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors text-sm"
                      >
                        <Copy className="w-4 h-4" />
                        Copy
                      </button>
                      <button
                        onClick={downloadPythonScript}
                        className="flex items-center gap-2 px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors text-sm"
                      >
                        <Download className="w-4 h-4" />
                        Download
                      </button>
                    </div>
                  </div>
                  <pre className="text-purple-300 text-xs overflow-x-auto max-h-64">{pythonScript}</pre>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2">📋 How to Use:</h4>
                  <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
                    <li>Copy the command above and run it in your terminal</li>
                    <li>OR download the Python script and run it: <code className="bg-blue-100 px-2 py-1 rounded">python compile_script.py</code></li>
                    <li>Your executable will be created in the output directory</li>
                  </ol>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
