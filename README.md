# MarkItDown wrapper for Windows

It's a suite of two portable Windows tools based on the Microsoft MarkItDown library. 
It allows you to convert local files (PDF, DOCX, XLSX, images, audio) and web content (generic URLs and YouTube transcripts) into clean, optimized Markdown files—without requiring a Python installation on the host system.

Key features
CLI Engine (markitdown-cli.exe): A powerful command-line tool supporting both local file paths and web URLs.

GUI Launcher (launcher.exe): An intuitive graphical interface with Drag & Drop support for quick conversions.

Smart Logging: A custom logging system that creates an error.log only when an exception occurs, and an optional conversion.log for debugging.

AI Support: Optional integration with OpenAI (GPT-4o) via API Key for advanced document analysis and description.

# Download binary
https://github.com/mdmiko/markitdown-win/releases

⚠️ Windows SmartScreen Notice
Since this is an open-source project and the executables are not digitally signed, Windows may show a "SmartScreen" warning.

To run the app:
Click on "More info".
Click on "Run anyway".

You can verify the source code yourself or run the script directly from Python if you prefer not to use the pre-compiled binaries.


# Installation and build
The project includes an automation script to manage the development environment and compilation.

### To build yourself, clone the repository:

git clone https://github.com/mdmiko/markitdown-win.git

cd markitdown-win

### Run the Build:
Execute build.bat. If a virtual environment (venv) is not detected, the script will offer to create it and install all dependencies from requirements.txt automatically.

build.bat cli: Compiles only the CLI engine.

build.bat gui: Compiles only the graphical launcher.

build.bat: Compiles both.

CLI usage
To convert a file or URL via terminal:

# Convert a local file
dist\markitdown-cli.exe document.pdf

# Enable debug mode and specify output
dist\markitdown-cli.exe input.docx -o output.md -d

Project structure

markitdown-cli.py: Core logic for conversion and input/output management.

launcher.py: Graphical interface built with customtkinter and tkinterdnd2.

build.bat: Automation script for building with PyInstaller and UPX.

requirements.txt: List of required Python dependencies.
