#!/usr/bin/env python3
"""
Entry point for P2E Web Interface.
Run this script to start the Streamlit web interface.

Usage:
    python run_web.py
    
Or use streamlit directly:
    streamlit run p2e/web/app.py
"""

import sys
import subprocess

if __name__ == '__main__':
    # Run streamlit with the web app
    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        "p2e/web/app.py"
    ])
