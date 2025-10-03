# AI News Scraping Pipeline

A comprehensive Scrapy-based pipeline for harvesting news articles from Vietnamese (VI), Khmer (KM), and Burmese/Myanmar (MY) sources. The pipeline extracts, processes, and outputs structured data in JSONL format with advanced content processing capabilities.

## 🚀 Features

- **Multi-language Support**: Vietnamese, Khmer, and Burmese news sources
- **Advanced Content Extraction**: Using Trafilatura and Readability algorithms
- **Content Deduplication**: Simhash and MinHash-based duplicate detection
- **Image Processing**: OCR capabilities with Tesseract integration
- **Content Normalization**: Text cleaning and standardization
- **Flexible Output**: Sharded JSONL files with configurable size limits
- **RSS Feed Support**: Automated RSS feed crawling and parsing
- **Playwright Integration**: Dynamic content rendering for JavaScript-heavy sites

## 📋 Requirements

- **Python 3.11** (required)
- Windows/Linux/macOS support
- At least 4GB RAM recommended
- Internet connection for crawling

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI-scraping
```

### 2. Set Up Python Environment

**Windows (PowerShell):**
```powershell
# Create virtual environment
py -3.11 -m venv .venv

# Activate environment
.venv\Scripts\activate
```

**Linux/macOS:**
```bash
# Create virtual environment
python3.11 -m venv .venv

# Activate environment
source .venv/bin/activate
```

### 3. Install Dependencies

**Windows Installation:**

FastText can be tricky to install on Windows. Try these methods in order:

```powershell
# Method 1: Try direct pip install first
py -3.11 -m pip install --upgrade pip setuptools wheel
py -3.11 -m pip install fasttext==0.9.2

# If Method 1 fails, try Method 2: Use pre-compiled wheel
# Download the wheel file for your system from:
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#fasttext
# Then install it directly:
py -3.11 -m pip install fasttext-0.9.2-cp311-cp311-win_amd64.whl

# Method 3: Install other dependencies first, then FastText
py -3.11 -m pip install pybind11 numpy
py -3.11 -m pip install fasttext==0.9.2

# Install remaining requirements
py -3.11 -m pip install -r requirements.txt
```

**Linux/macOS Installation:**

```bash
# Standard installation
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

**Alternative for Windows (if all above methods fail):**

```powershell
# Install pipwin (if not already installed)
py -3.11 -m pip install pipwin

# Clear pipwin cache and try again
py -3.11 -m pipwin refresh
py -3.11 -m pipwin install fasttext

# Or use conda if available
conda install -c conda-forge fasttext
```

### 4. Install Additional Windows Dependencies

**For OCR functionality (Tesseract):**

1. Download and install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Add Tesseract to your PATH or set the path in your code:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

**For Playwright (Optional):**

```powershell
py -3.11 -m playwright install chromium
```

### 5. Verify Installation

Test that FastText is working correctly:

```powershell
python -c "import fasttext; print('FastText installed successfully!')"
```

## ⚙️ Configuration

### Source Configuration Files

Configure your news sources in the YAML files located in the `configs/` directory:

- `configs/sources_vi.yml` - Vietnamese sources
- `configs/sources_km.yml` - Khmer sources  
- `configs/sources_my.yml` - Burmese/Myanmar sources

Example configuration structure:
```yaml
sources:
  - name: "example_news"
    rss_url: "https://example.com/rss"
    base_url: "https://example.com"
    enabled: true
```

### Scrapy Settings

Modify `harvester/settings.py` to adjust:
- Crawl delays and politeness settings
- Pipeline configurations
- Output file settings
- User agents and headers

## 🏃‍♂️ Usage

### Basic Usage

Run a spider for a specific language:

```bash
# Vietnamese sources
scrapy crawl rss_vi

# Khmer sources
scrapy crawl rss_km

# Burmese/Myanmar sources
scrapy crawl rss_my
```

### Advanced Options

```bash
# Custom output directory
scrapy crawl rss_vi -s FEEDS_PATH=custom/output/path

# Limit number of articles
scrapy crawl rss_vi -s CLOSESPIDER_ITEMCOUNT=1000

# Custom log level
scrapy crawl rss_vi -L INFO
```

## 📁 Project Structure

```
AI-scraping/
├── configs/                 # Source configuration files
│   ├── sources_vi.yml      # Vietnamese sources
│   ├── sources_km.yml      # Khmer sources
│   └── sources_my.yml      # Burmese sources
├── harvester/              # Main Scrapy project
│   ├── spiders/           # Spider implementations
│   │   └── rss_spider.py  # RSS spider
│   ├── utils/             # Utility modules
│   │   ├── anonymize.py   # Data anonymization
│   │   ├── de_duplicator.py # Deduplication logic
│   │   ├── extract_main.py # Content extraction
│   │   ├── image_inject.py # Image processing
│   │   ├── latexify.py    # LaTeX formatting
│   │   ├── normalize.py   # Text normalization
│   │   └── validators.py  # Data validation
│   ├── items.py           # Scrapy items definition
│   ├── pipelines.py       # Processing pipelines
│   └── settings.py        # Scrapy settings
├── tools/                 # Utility tools
│   ├── estimate_ocr_acc.py # OCR accuracy estimation
│   ├── shard_jsonl.py     # JSONL file sharding
│   └── validate_jsonl.py  # JSONL validation
├── requirements.txt       # Python dependencies
├── scrapy.cfg            # Scrapy configuration
└── README.md             # This file
```

## 📊 Output Format

### JSONL Structure

Each article is saved as a JSON object with the following structure:

```json
{
  "url": "https://example.com/article",
  "title": "Article Title",
  "content": "Full article content",
  "published_date": "2024-01-01T00:00:00Z",
  "author": "Author Name",
  "language": "vi",
  "source": "example_news",
  "extracted_at": "2024-01-01T12:00:00Z",
  "content_hash": "abc123...",
  "images": ["image_url1", "image_url2"]
}
```

### Output Files

- **JSONL Files**: `data/jsonl/{language}_news_000.jsonl`
  - Automatically sharded at ~1GB or 10k+ lines per file
  - Sequential numbering (000, 001, 002, etc.)
- **Raw HTML**: `data/raw_html/` (for auditing purposes)
- **Logs**: `logs/scrapy.log`

## 🔧 Tools

### Validate JSONL Output

```bash
py -3.11 tools/validate_jsonl.py data/jsonl/news_1004.jsonl
```

### Shard Large JSONL Files

```bash
py -3.11 tools/shard_jsonl.py input.jsonl --max-size 1GB --max-lines 10000
```

### Estimate OCR Accuracy

```bash
py -3.11 tools/estimate_ocr_acc.py data/images/
```

## 🔍 Monitoring and Debugging

### View Crawl Statistics

```bash
# Enable stats collection in settings.py
STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'
```

### Debug Mode

```bash
# Run with debug logging
scrapy crawl rss_vi -L DEBUG

# Use Scrapy shell for testing
scrapy shell "https://example.com/article"
```

## 🚨 Troubleshooting

### FastText Installation Issues (Windows)

**Problem**: `pipwin` fails with `AttributeError: 'NoneType' object has no attribute 'group'`

**Solutions** (try in order):

1. **Method 1 - Direct pip install:**
   ```powershell
   py -3.11 -m pip install --upgrade pip setuptools wheel
   py -3.11 -m pip install fasttext==0.9.2
   ```

2. **Method 2 - Use pre-compiled wheel:**
   ```powershell
   # Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#fasttext
   py -3.11 -m pip install fasttext-0.9.2-cp311-cp311-win_amd64.whl
   ```

3. **Method 3 - Install build dependencies first:**
   ```powershell
   py -3.11 -m pip install pybind11 numpy cython
   py -3.11 -m pip install fasttext==0.9.2
   ```

4. **Method 4 - Alternative package:**
   ```powershell
   # Use fasttext-wheel (unofficial but works)
   py -3.11 -m pip install fasttext-wheel
   ```

### Common Issues

1. **Import Errors**: Ensure Python 3.11 is used consistently
2. **Memory Issues**: Reduce batch sizes in pipelines
3. **Rate Limiting**: Adjust `DOWNLOAD_DELAY` in settings
4. **Encoding Issues**: Check source encoding in spider configuration
5. **FastText Import Error**: Try the methods above in the FastText section
6. **Playwright Installation**: Run `playwright install` after pip install
7. **Tesseract Not Found**: Install Tesseract and add to PATH or set `tesseract_cmd` path

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🤝 Support

For issues and questions:
- Check the [Issues](link-to-issues) section
- Review the troubleshooting guide above
- Contact the development team

---

**Last Updated**: October 2024
