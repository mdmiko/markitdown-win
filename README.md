a suite of portable Windows tools based on the Microsoft MarkItDown library. It allows you to convert local files (PDF, DOCX, XLSX, images, audio) and web content (generic URLs and YouTube transcripts) into clean, optimized Markdown files—without requiring a Python installation on the host system.

Key features
CLI Engine (markitdown-cli.exe): A powerful command-line tool supporting both local file paths and web URLs.

GUI Launcher (launcher.exe): An intuitive graphical interface with Drag & Drop support for quick conversions.

YouTube Transcription: Native integration to extract subtitles and convert them to Markdown (requires available subtitles on the video).

Smart Logging: A custom logging system that creates an error.log only when an exception occurs, and an optional conversion.log for debugging.

AI Support: Optional integration with OpenAI (GPT-4o) via API Key for advanced document analysis and description.

Installation and build
The project includes an automation script to manage the development environment and compilation.

Clone the repository:

Bash
git clone https://github.com/your-username/PyExe-MarkItDown.git
cd PyExe-MarkItDown
Run the Build:
Execute build.bat. If a virtual environment (venv) is not detected, the script will offer to create it and install all dependencies from requirements.txt automatically.

build.bat cli: Compiles only the CLI engine.

build.bat gui: Compiles only the graphical launcher.

build.bat: Compiles both.

CLI usage
To convert a file or URL via terminal:

Bash
# Convert a local file
dist\markitdown-cli.exe document.pdf

# Transcribe a YouTube video
dist\markitdown-cli.exe https://www.youtube.com/watch?v=VIDEO_ID

# Enable debug mode and specify output
dist\markitdown-cli.exe input.docx -o output.md -d
Project structure
markitdown-cli.py: Core logic for conversion and input/output management.

launcher.py: Graphical interface built with customtkinter and tkinterdnd2.

build.bat: Automation script for building with PyInstaller and UPX.

requirements.txt: List of required Python dependencies.
