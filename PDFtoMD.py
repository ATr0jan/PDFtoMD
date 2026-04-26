import os
import sys
import argparse
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file located in the script's directory
load_dotenv(Path(__file__).parent / ".env")

# Set up logger
logger = logging.getLogger(__name__)

def convert_pdf_to_markdown(input_path: str, output_path: str = None, offline: bool = False):
    """
    Converts a PDF document to Markdown using Docling.
    
    Args:
        input_path: Path to the source PDF file.
        output_path: Path where the Markdown file will be saved. 
                     If None, it uses the input filename with a .md extension.
        offline: If True, skips checking Hugging Face Hub for model updates.
    """
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        os.environ["HF_DATASETS_OFFLINE"] = "1" # Extra safety for Docling

    # Import here so environment variables are respected during initialization
    from docling.document_converter import DocumentConverter

    try:
        # 1. Path validation and resolution
        input_p = Path(input_path).resolve()
        if not input_p.is_file():
            logger.error(f"File not found: {input_p}")
            return # Exit early instead of raising a naked exception

        if input_p.stat().st_size > 50_000_000: # 50MB limit
            logger.warning("Large file detected. Conversion may take significant time/RAM.")

        # Resolve output path relative to input if not provided
        if output_path:
            output_p = Path(output_path).resolve()
        else:
            output_p = input_p.with_suffix(".md")

        # 2. Initialize the DocumentConverter (moved inside try to catch init errors)
        converter = DocumentConverter()
        logger.info(f"Processing: {input_p.name}")

        # 3. Perform the conversion
        # Using the resolved string path
        result = converter.convert(str(input_p))

        # 4. Export the document to Markdown format
        markdown_content = result.document.export_to_markdown()
        
        # Ensure parent directory exists
        output_p.parent.mkdir(parents=True, exist_ok=True)

        # 5. Save the result securely
        with open(output_p, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            
        logger.info(f"Successfully converted! Saved to: {output_p}")

    except PermissionError:
        logger.error("Permission denied. Check if the output file is open elsewhere.")
    except Exception as e:
        logger.error(f"Conversion failed. Use --debug for full trace.")
        logger.debug(f"Error: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a PDF file to Markdown.")
    parser.add_argument("input", help="Path to the input PDF file")
    parser.add_argument("-o", "--output", help="Path to the output Markdown file (optional)", default=None)
    parser.add_argument("--offline", action="store_true", help="Run in offline mode (uses cached models only)")
    parser.add_argument("--debug", action="store_true", help="Show detailed debug information")

    args = parser.parse_args()

    # Configure logging based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    # Determine offline status: CLI flag takes precedence, then .env default
    # .env uses "OFFLINE_DEFAULT=1" to enable by default
    env_offline = os.getenv("OFFLINE_DEFAULT") == "1"
    final_offline = args.offline or env_offline

    convert_pdf_to_markdown(args.input, args.output, final_offline)