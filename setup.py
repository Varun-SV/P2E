"""Setup configuration for P2E."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')
else:
    long_description = "P2E - Python to EXE Converter"

setup(
    name="p2e-converter",
    version="2.0.0",
    author="Varun S V",
    description="Modern tool for converting Python scripts to executables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Varun-SV/P2E",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "PyYAML>=5.4.0",
        "pyinstaller>=5.0.0",
    ],
    extras_require={
        "web": ["streamlit>=1.20.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "mypy>=0.990",
            "pylint>=2.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "p2e=p2e.cli.app:cli",
        ],
    },
    include_package_data=True,
)
