# 🎨 Vision Language Model Demo - Complete Edition

### 30+ Features | Multi-Provider | Privacy-First | Production-Ready

A comprehensive vision-language model application with chat, code generation, batch processing, OCR, analytics, and much more. Built with flexibility and privacy in mind.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Gradio](https://img.shields.io/badge/Gradio-4.0+-orange.svg)](https://gradio.app/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 What's New in V2?

**V2 introduces 25+ new features** while keeping everything from V1:

- 💬 **Chat History & Export** - Persistent conversations, export to MD/JSON/PDF
- 🖼️ **Live Code Preview** - See generated HTML instantly
- 📦 **Batch Processing** - Process 100s of images at once
- ⚖️ **Image Comparison** - Compare multiple images side-by-side
- 📄 **Advanced OCR** - Extract text and tables from images
- ⚡ **70+ Presets** - Quick-action templates for common tasks
- 💰 **Cost Tracking** - Real-time API usage monitoring
- 🗄️ **Database** - SQLite for persistence
- 🌐 **REST API** - FastAPI endpoints
- 🔧 **Code Refinement** - Iteratively improve generated code

 [See all features →](FEATURES.md)

---

## 🆕 Latest Improvements (2025)

**Recent enhancements for better compatibility and performance:**

- 🐳 **AMD GPU Support** - Removed NVIDIA dependencies, CPU-only PyTorch for AMD compatibility
- 🔧 **Docker Optimization** - Updated to Python 3.11-slim-bookworm, port 7861 for external access
- 🎨 **Gradio 6.x Compatibility** - Fixed chat message formats and constructor parameters
- 🗄️ **Database Fixes** - Resolved SQLAlchemy metadata naming conflicts
- 🚀 **Container Ready** - Simplified docker-compose without Ollama dependency
- 🎵 **Whisper Integration** - Audio/video transcription with Whisper-WebUI API
- 📺 **YouTube Transcription** - Direct YouTube video transcription support
- 🎤 **Audio Recording** - Built-in microphone recording and transcription
- ⚙️ **Enhanced Configuration** - Expanded .env with Whisper model/language/format options

---

## 🚀 Quick Start

### One-Command Start

```bash
# Clone and run
git clone https://github.com/yourusername/vlm-computer-use
cd vlm-computer-use
./start.sh  # or: python run_app.py
```

### Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure provider (choose one)
cp .env.example .env
# Edit .env with your settings

# 3. Run the app
python app.py

# 4. Open browser
# http://localhost:7860
```

### Docker

```bash
# Quick start with Docker Compose (includes Ollama)
docker-compose up -d

# Or build and run manually
docker build -t vlm-demo .
docker run -p 7861:7860 --env-file .env vlm-demo
```

---

## ✨ Features Overview

### 🎯 Core Features

| Feature | Description |
|---------|-------------|
| **Multi-Image Chat** | Interactive conversations with images, 3 modes (Chat/Analysis/Thinking) |
| **Screenshot-to-Code** | Generate HTML/React/Vue/Tailwind from designs + Live Preview |
| **Batch Processing** | Process multiple images, export to CSV/JSON |
| **Image Comparison** | Compare 2-10 images with similarity scores |
| **OCR & Tables** | Extract text (multi-language) and tables from images |
| **Video Analysis** | Analyze videos via frame extraction (4-16 frames) |
| **🎵 Whisper Transcription** | Transcribe audio/video files with multiple Whisper models |
| **📺 YouTube Transcription** | Direct transcription of YouTube videos |
| **🎤 Audio Recording** | Record and transcribe audio with built-in microphone |
| **Preset Prompts** | 70+ templates for quick actions |
| **Cost Tracking** | Real-time token counting and cost calculation |
| **Chat History** | Persistent conversations with search and export |
| **REST API** | Full FastAPI backend for integration |

### 🔌 Provider Support

- **OpenAI** (GPT-4o, GPT-4o-mini, GPT-4 Turbo)
- **Anthropic** (Claude 3.5 Sonnet, Opus, Haiku)
- **Ollama** (LLaVA, BakLLaVA - 100% Local & Free)
- **Custom APIs** (LM Studio, vLLM, LocalAI, any OpenAI-compatible)

### 🎨 Code Generation

Generate code in multiple frameworks:
- HTML/CSS (vanilla)
- React (functional components)
- Vue 3 (Composition API)
- Tailwind CSS
- Bootstrap 5

With features:
- Live preview
- Iterative refinement
- Download as files
- Syntax highlighting

---

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Complete Feature List](FEATURES.md)** - All 30+ features explained
- **[API Documentation](API_DOCS.md)** - REST API reference
- **[Upgrade Guide](UPGRADE_GUIDE.md)** - Migrating from V1 to V2

---

## 🎯 Use Cases

### For Developers
- Convert Figma/designs to code
- Debug with screenshots
- Code review assistance
- Documentation generation

### For Designers
- UI/UX critiques
- Accessibility audits
- Design system extraction
- A/B test analysis

### For Business
- Receipt/invoice processing
- Document digitization
- Quality control
- Competitor analysis

### For Content Creators
- Image captions & alt text
- Social media content
- Batch image descriptions
- Brand consistency checks

### For Researchers
- Image classification
- Data extraction from charts
- Experiment documentation
- Visual data analysis

---

## 🏗️ Architecture

```
vlm-computer-use/
├── app.py                 # Main Gradio UI application
├── app_v2.py             # Core VLM logic and features
├── providers.py          # Multi-provider abstraction
├── utils.py              # Basic utilities
├── advanced_utils.py     # OCR, batch, cost tracking
├── database.py           # SQLite persistence
├── presets.py            # Preset prompts library
├── api.py                # FastAPI REST endpoints
├── requirements.txt      # Python dependencies
├── .env.example          # Configuration template
├── Dockerfile            # Container config
├── docker-compose.yml    # Multi-container setup
└── docs/                 # Documentation
```

### Tech Stack

- **UI**: Gradio 4.0+
- **LLM Providers**: OpenAI SDK, Anthropic SDK
- **Database**: SQLAlchemy + SQLite
- **API**: FastAPI + Uvicorn
- **OCR**: Tesseract, EasyOCR
- **Processing**: PIL, OpenCV, pandas
- **Cost Tracking**: tiktoken

---

## ⚙️ Configuration

### Quick Setup (Ollama - Free & Local)

```bash
# 1. Install Ollama
# Download from https://ollama.ai

# 2. Pull a vision model
ollama pull llava

# 3. Configure
DEFAULT_PROVIDER=ollama
OLLAMA_MODEL=llava:latest

# 4. Run
python app.py
```

### OpenAI Setup

```bash
# .env
DEFAULT_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o
```

### Anthropic Setup

```bash
# .env
DEFAULT_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### All Options

See [.env.example](.env.example) for complete configuration options.

---

## 🚢 Deployment

### Local Development

```bash
python app.py
# or
python run_app.py
```

### Production (Docker)

```bash
docker-compose up -d
```

### Heroku

```bash
heroku create your-app-name
git push heroku main
```

### Railway

```bash
# Connect your repo to Railway
# Set environment variables
# Deploy automatically
```

### VPS/Cloud

```bash
# Install dependencies
pip install -r requirements.txt

# Run with supervisor/systemd
# nginx reverse proxy
# SSL with Let's Encrypt
```

---

## 📊 API Usage

### Start API Server

```bash
# Standalone
python api.py

# Or with Uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000

# Docs at http://localhost:8000/docs
```

### Quick Example

```python
import requests

# Chat with image
files = {'images': open('image.jpg', 'rb')}
data = {'message': 'What is this?', 'provider': 'openai'}

response = requests.post(
    'http://localhost:8000/api/chat',
    files=files,
    data=data
)

print(response.json()['response'])
```

[Full API Documentation →](API_DOCS.md)

---

## 🎨 Screenshots

### Chat Interface
```
┌─────────────────────────────────────────┐
│  💬 Chat with Images                    │
├─────────────────────────────────────────┤
│  [Image]                                │
│  User: What's in this image?            │
│  Assistant: I see a beautiful...        │
│  ┌───────────────────────────────┐     │
│  │ 💰 Cost: $0.0012 | 1,234 tokens│     │
│  └───────────────────────────────┘     │
└─────────────────────────────────────────┘
```

### Code Generation
```
┌─────────────────────────────────────────┐
│  🖼️ Screenshot to Code                  │
├─────────────────────────────────────────┤
│  [Screenshot] → [Generated Code]        │
│  ┌────────────┐   ┌──────────────────┐ │
│  │   Design   │   │  Live Preview    │ │
│  └────────────┘   └──────────────────┘ │
│  Framework: React | Tailwind           │
└─────────────────────────────────────────┘
```

---

## 🔒 Privacy & Security

### Local-First Option

Run 100% locally with Ollama:
- No data leaves your machine
- No API costs
- Complete privacy
- Full control

### Security Best Practices

1. ✅ Store API keys in `.env` (gitignored)
2. ✅ Use environment variables for secrets
3. ✅ Enable API authentication in production
4. ✅ Restrict CORS origins
5. ✅ Regular dependency updates
6. ✅ Database backups

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by GLM-4.5V Demo App
- Built with [Gradio](https://gradio.app/)
- Powered by [OpenAI](https://openai.com/), [Anthropic](https://anthropic.com/), and [Ollama](https://ollama.ai/)

---

## 📞 Support

- 📖 **Documentation**: [/docs](/docs)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/vlm-computer-use/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/vlm-computer-use/discussions)
- 📧 **Email**: support@example.com

---

## 🗺️ Roadmap

### V2.1 (Current)
- [x] All 30+ features
- [x] Full documentation
- [x] REST API
- [ ] Unit tests
- [ ] Performance benchmarks

### V3.0 (Planned)
- [ ] Voice input/output
- [ ] Multi-user support
- [ ] Browser extension
- [ ] Mobile apps (iOS/Android)
- [ ] Advanced automation
- [ ] Fine-tuning support
- [ ] Real-time collaboration

[See detailed roadmap →](ROADMAP.md)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Made with ❤️ by the open source community**

**Version:** 2.0 Complete | **Features:** 30+ | **Providers:** 4+
