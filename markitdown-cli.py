import os
import sys
import argparse
import re
import logging
import warnings
import shutil
import traceback
from datetime import datetime
import time

# Silenziamo avvisi inutili
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")
logging.getLogger("pdfminer").setLevel(logging.CRITICAL)

from markitdown import MarkItDown

def get_now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def setup_logging(is_debug):
    """Configura il sistema di logging in modo condizionale."""
    logger = logging.getLogger("MarkItDownCLI")
    logger.setLevel(logging.DEBUG)
    
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    if is_debug:
        info_handler = logging.FileHandler("conversion.log", encoding='utf-8')
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)
        logger.addHandler(info_handler)

    class DelayFileHandler(logging.FileHandler):
        """Handler che apre il file solo se viene effettivamente scritto un errore."""
        def emit(self, record):
            if self.stream is None:
                self.stream = self._open()
            super().emit(record)

    error_handler = DelayFileHandler("error.log", encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    return logger

def clean_markdown(text):
    """Pulisce il markdown rimuovendo eccessive linee vuote."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="MarkItDown CLI - Convert files or URLs to Markdown")
    parser.add_argument("input", help="Path to input file or YouTube URL")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("--key", help="OpenAI API Key")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI Model (default: gpt-4o)")
    parser.add_argument("--base-url", help="OpenAI Base URL")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging and FFmpeg check")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress console output")

    args = parser.parse_args()
    
    is_debug = args.debug
    is_quiet = args.quiet
    logger = setup_logging(is_debug)

    input_path = args.input
    output_path = args.output
    
    # Riconoscimento URL
    is_url = input_path.startswith(('http://', 'https://'))
    
    if not is_url and not os.path.exists(input_path):
        msg = f"Input file '{input_path}' not found."
        if not is_quiet:
            print(f"[{get_now()}] ERROR: {msg}")
        logger.error(msg)
        sys.exit(1)

    if not output_path:
        if is_url:
            # Estrazione basilare per URL o nome generico
            base_name = "youtube_conversion" if "youtube" in input_path.lower() else "web_conversion"
        else:
            base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}-markdown.md"

    start_time = time.time()
    if not is_quiet:
        print(f"[{get_now()}] START: {input_path}...")
    logger.info(f"Start: {input_path}")

    try:
        if args.key:
            if is_debug and not is_quiet:
                print(f"[{get_now()}] AI: Engine enabled ({args.model})")
            from openai import OpenAI
            client = OpenAI(api_key=args.key, base_url=args.base_url)
            md = MarkItDown(llm_client=client, llm_model=args.model)
        else:
            md = MarkItDown()

        if is_debug and not is_quiet:
            has_ffmpeg = shutil.which("ffmpeg") is not None
            print(f"[{get_now()}] DEBUG: FFmpeg status: {'Found' if has_ffmpeg else 'Not Found'}")

        result = md.convert(input_path)
        cleaned_text = clean_markdown(result.text_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
            
        duration = round(time.time() - start_time, 2)
        
        if not is_quiet:
            print(f"[{get_now()}] SUCCESS: Converted to {output_path}")
            print(f"[{get_now()}] TIME: {duration} seconds")
        
        logger.info(f"Success: {output_path} ({duration}s)")
            
    except Exception as e:
        error_msg = str(e)
        if not is_quiet:
            print(f"[{get_now()}] CRITICAL ERROR: {error_msg}")
        
        logger.error(f"Failed to convert {input_path}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()