# 🚀 Upgrade Guide - V1 to V2

## What's New in V2?

V2 includes **30+ new features** while maintaining backward compatibility with V1.

### Major Additions

1. **Live Code Preview** - See generated HTML/CSS in real-time
2. **Chat History & Export** - Persistent conversations, export to MD/JSON/PDF
3. **Batch Processing** - Process multiple images at once
4. **Image Comparison** - Compare 2+ images side-by-side
5. **Advanced OCR** - Extract text and tables from images
6. **Preset Prompts** - 70+ quick-action templates
7. **Cost Tracking** - Real-time API usage and cost monitoring
8. **Database Integration** - SQLite for persistence
9. **REST API** - FastAPI endpoints for programmatic access
10. **Code Refinement** - Iteratively improve generated code

### Full Feature List

See [FEATURES.md](FEATURES.md) for complete details.

## Migration Steps

### Option 1: Fresh Install (Recommended)

```bash
# Backup old installation
cp -r vlm-computer-use vlm-computer-use-backup

# Pull latest changes
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run new version
python run_app.py
```

### Option 2: In-Place Upgrade

```bash
# Update requirements
pip install --upgrade -r requirements.txt

# Initialize database (automatic on first run)
python -c "from database import db; print('Database initialized')"

# Run application
python app.py
```

## Configuration Changes

### New Environment Variables

Add these to your `.env` file:

```bash
# Optional: Database path
DATABASE_PATH=sqlite:///vlm_demo.db

# Optional: API server port
API_PORT=8000

# Optional: Enable API
ENABLE_API=true
```

### Updated .env Structure

The new `.env.example` includes:
- Additional provider options
- Cost tracking settings
- Database configuration
- API settings

## Database

V2 introduces a SQLite database for:
- Chat history
- Generated code
- Usage analytics
- Prompt templates
- Workspaces

**Location:** `vlm_demo.db` (created automatically)

**Backup:** Copy `vlm_demo.db` file

## Breaking Changes

### None!

V2 is fully backward compatible. All V1 features work exactly as before.

### Deprecations

- None in V2

## New Dependencies

V2 adds these dependencies (automatically installed):

```
sqlalchemy>=2.0.0
chromadb>=0.4.0
pytesseract>=0.3.10
pdf2image>=1.16.3
easyocr>=1.7.0
pandas>=2.0.0
openpyxl>=3.1.0
pygments>=2.16.0
black>=23.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
tiktoken>=0.5.0
reportlab>=4.0.0
```

## Feature Migration

### From V1 to V2

| V1 Feature | V2 Enhancement |
|------------|----------------|
| Chat | + History, Export, Cost tracking |
| Code Gen | + Multi-framework, Live preview, Refinement |
| Video | + Advanced frame extraction, GIF creation |
| Config | + Dynamic switching, Multiple profiles |

## Performance Improvements

- **Faster loading**: Lazy import of heavy dependencies
- **Better caching**: Image processing cache
- **Database indexing**: Fast history queries
- **Async operations**: Non-blocking UI

## Troubleshooting

### Database Issues

```bash
# Reset database
rm vlm_demo.db
python -c "from database import db; print('Database reset')"
```

### Dependency Conflicts

```bash
# Clean install
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

### Port Conflicts

```bash
# Change port
APP_PORT=8080 python app.py
```

### OCR Not Working

```bash
# Install Tesseract
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# macOS:
brew install tesseract

# Windows: Download from GitHub
```

## Rollback to V1

If you need to rollback:

```bash
# Restore backup
rm -rf vlm-computer-use
mv vlm-computer-use-backup vlm-computer-use
cd vlm-computer-use

# Use V1
python app_backup.py
```

Or:

```bash
# Use V1 with current installation
python app_backup.py
```

## Getting Help

- Check [FEATURES.md](FEATURES.md) for feature documentation
- See [README.md](README.md) for general setup
- Review [QUICKSTART.md](QUICKSTART.md) for quick start
- Open an issue on GitHub

## Gradual Adoption

You can use V2 gradually:

1. **Week 1**: Try new chat features (history, export)
2. **Week 2**: Explore batch processing
3. **Week 3**: Use OCR and comparison tools
4. **Week 4**: Set up REST API if needed

All V1 features continue to work!

## API Migration

If you were using V1 programmatically:

### V1 (Direct Python)
```python
from providers import ProviderFactory
provider = ProviderFactory.create_provider("openai")
```

### V2 (Same + REST API)
```python
# Python still works
from providers import ProviderFactory
provider = ProviderFactory.create_provider("openai")

# OR use REST API
import requests
response = requests.post("http://localhost:8000/api/chat", ...)
```

## What Stayed the Same

- Provider configuration
- Core chat functionality
- Code generation basics
- Video analysis
- All original features

## Tips for Power Users

1. **Use Presets**: Save time with 70+ built-in prompts
2. **Batch Process**: Process hundreds of images efficiently
3. **Track Costs**: Monitor spending in Analytics tab
4. **Export Everything**: Save your work in multiple formats
5. **API Access**: Integrate with other tools via REST API

## Roadmap

See V3 features coming soon:
- Voice input/output
- Multi-user support
- Browser extension
- Mobile apps
- Advanced automation

---

**Questions?** Check the documentation or open an issue!
