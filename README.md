# PDFtoMD Converter

A robust Python utility to convert PDF documents into clean, structured Markdown using the [Docling](https://github.com/DS4SD/docling) library. This tool is designed for high-fidelity conversion, handling complex layouts and tables better than standard PDF parsers.

## 🚀 Features
- **High-Fidelity Layout Analysis**: Recognizes headers, tables, and complex lists using AI.
- **Offline Mode**: Run without checking for model updates (improves startup speed and privacy).
- **CLI-First**: Designed for quick terminal usage and automation scripts.
- **Environment Configuration**: Support for `.env` files to store API tokens and default settings.
- **Secure Encoding**: Full UTF-8 support for output files.


## 🛠️ Installation

**Prerequisites**: Python 3.10+ (Works on Windows, macOS, and Linux)

1. Clone the repository or download the script.
2. Install the required dependencies:
   ```bash
   pip install docling python-dotenv
   ```

## 💻 Usage

Run the script from your terminal using the following syntax:

```bash
python PDFtoMD.py <input_pdf_path> [options]
```

### Options:
- `-o <path>`: Specify a custom output path.
- `--offline`: Skip checking for model updates (faster startup).
- `--debug`: Enable verbose logging for troubleshooting.

### Examples:
- **Basic conversion**: `python PDFtoMD.py resume.pdf` (Creates `resume.md` in the same folder).
- **Custom output**: `python PDFtoMD.py resume.pdf -o custom_folder/my_resume.md`
- **Offline Mode**: `python PDFtoMD.py resume.pdf --offline`

---

## ⚙️ Configuration

You can create a `.env` file in the project root to manage settings:

```env
# Optional: Hugging Face token for higher rate limits
HF_TOKEN=your_hugging_face_token_here

# Set to 1 to default to offline mode, 0 to check for updates
OFFLINE_DEFAULT=0
```

> [!IMPORTANT]
> **Security Note**: Never commit your `.env` file to version control. Add `.env` to your `.gitignore` to protect your `HF_TOKEN`.

## 📂 Project Structure
```text
.
├── PDFtoMD.py      # Main conversion script 
├── .env            # Configuration file (Manual setup)
├── .gitignore      # Prevents sensitive files from being committed 
└── README.md       # Documentation
```

## 🔍 Technical Notes & Troubleshooting
- **First Run**: This tool uses models hosted on Hugging Face. On the first run, it will download 100-300MB of weights to your local cache.
- **Memory Usage**: Complex PDFs with many images or tables may require significant RAM (4GB+).
- **Logs**: For detailed error logs, use the `--debug` flag.

## 📄 License
This project is licensed under the MIT License.