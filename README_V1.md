# 🎨 Vision Language Model Demo Application

A powerful, privacy-focused demo application for vision-language models with **Bring Your Own Provider** support. Chat with images, analyze videos, and generate code from screenshots using OpenAI, Anthropic, Ollama, or any custom OpenAI-compatible API.

## ✨ Features

- **🔌 Multiple Provider Support**: OpenAI, Anthropic Claude, Ollama (local), or custom APIs
- **💬 Multi-Image Chat**: Interactive conversations with multiple images
- **🖼️ Screenshot-to-Code**: Generate HTML/CSS code from design screenshots
- **🎥 Video Analysis**: Analyze videos by extracting and processing key frames
- **🧠 Multiple Modes**: Chat, Analysis, and Deep Thinking modes
- **🔒 Privacy-First**: Use local models via Ollama or your own API endpoints
- **🎛️ Flexible Configuration**: UI-based setup or environment variables

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your provider:**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your preferred settings:
   ```bash
   # Choose your provider
   DEFAULT_PROVIDER=openai  # or anthropic, ollama, custom

   # Add your API keys
   OPENAI_API_KEY=your-key-here
   ANTHROPIC_API_KEY=your-key-here
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   ```
   http://localhost:7860
   ```

## 🔧 Configuration

### Provider Options

#### 1. OpenAI (GPT-4 Vision)
```env
DEFAULT_PROVIDER=openai
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
```

#### 2. Anthropic Claude
```env
DEFAULT_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

#### 3. Ollama (Local Models)
```env
DEFAULT_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llava:latest
```

First, install and run Ollama:
```bash
# Install Ollama from https://ollama.ai

# Pull a vision model
ollama pull llava

# Or use a larger model
ollama pull llava:13b
```

#### 4. Custom Provider (OpenAI-compatible)
```env
DEFAULT_PROVIDER=custom
CUSTOM_API_KEY=your-key
CUSTOM_BASE_URL=http://your-endpoint/v1
CUSTOM_MODEL=your-model-name
```

Works with:
- LM Studio
- LocalAI
- vLLM
- Any OpenAI-compatible API

### Dynamic Configuration

You can also configure providers directly in the UI:
1. Go to the "Configuration" tab
2. Select your provider type
3. Enter API key, base URL, and model (optional)
4. Click "Initialize Provider"

## 📖 Usage Guide

### 💬 Chat with Images

1. Navigate to the "Chat with Images" tab
2. Select a mode:
   - **Chat**: General conversation
   - **Analysis**: Detailed image analysis
   - **Thinking**: Deep reasoning with step-by-step explanation
3. Upload one or more images
4. Type your question and click "Send"

**Example prompts:**
- "What's in this image?"
- "Compare these two screenshots"
- "Describe the color scheme and design patterns"
- "Find any text in this image and transcribe it"

### 🖼️ Screenshot to Code

1. Go to the "Screenshot to Code" tab
2. Upload one or more screenshots of a design
3. (Optional) Add specific instructions
4. Click "Generate Code"
5. Copy the generated HTML/CSS code

**Tips:**
- Works best with clean, complete designs
- Upload multiple screenshots for complex layouts
- Specify frameworks in instructions (e.g., "Use Tailwind CSS")

### 🎥 Video Analysis

1. Open the "Video Analysis" tab
2. Upload a video file
3. Enter your question about the video
4. Adjust the number of frames to extract (4-16)
5. Click "Analyze Video"

**Use cases:**
- Summarize video content
- Identify specific moments or objects
- Analyze changes over time
- Extract information from tutorials

## 🏗️ Architecture

```
vlm-computer-use/
├── app.py              # Main Gradio application
├── providers.py        # Provider abstraction layer
├── utils.py           # Utility functions
├── requirements.txt   # Python dependencies
├── .env.example       # Environment template
└── README.md          # Documentation
```

### Key Components

- **`providers.py`**: Abstraction layer supporting multiple LLM providers
- **`app.py`**: Gradio UI with tabs for different features
- **`utils.py`**: Helper functions for image/video processing

## 🔐 Privacy & Security

- **Local-first**: Use Ollama to run everything locally
- **No data sharing**: Your images never leave your infrastructure
- **API key security**: Store keys in `.env` (never commit!)
- **Flexible hosting**: Run on your own servers

## 🛠️ Advanced Usage

### Using with LM Studio

1. Download and run [LM Studio](https://lmstudio.ai/)
2. Load a vision model
3. Start the local server
4. Configure the app:
   ```env
   DEFAULT_PROVIDER=custom
   CUSTOM_BASE_URL=http://localhost:1234/v1
   CUSTOM_MODEL=your-model-name
   ```

### Using with vLLM

```bash
# Start vLLM server
vllm serve llava-hf/llava-1.5-7b-hf --port 8000

# Configure app
DEFAULT_PROVIDER=custom
CUSTOM_BASE_URL=http://localhost:8000/v1
CUSTOM_MODEL=llava-hf/llava-1.5-7b-hf
```

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t vlm-demo .
docker run -p 7860:7860 --env-file .env vlm-demo
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Inspired by the GLM-4.5V Demo App, rebuilt from scratch to support multiple providers and prioritize privacy and flexibility.

## 📚 Resources

- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Anthropic Claude](https://www.anthropic.com/claude)
- [Ollama](https://ollama.ai/)
- [Gradio](https://gradio.app/)

## 🐛 Troubleshooting

### "Provider not initialized" error
- Go to Configuration tab and initialize your provider first

### Ollama connection failed
- Make sure Ollama is running: `ollama serve`
- Check the base URL is correct: `http://localhost:11434/v1`

### Images not uploading
- Ensure images are in supported formats (JPEG, PNG, WebP)
- Check file size (very large images are automatically resized)

### Video analysis not working
- Install OpenCV: `pip install opencv-python`
- Ensure video file is in a common format (MP4, AVI, MOV)

## 💡 Tips & Best Practices

1. **Cost Optimization**: Use Ollama for development and testing
2. **Quality**: Use GPT-4o or Claude 3.5 Sonnet for production
3. **Performance**: Reduce video frames for faster processing
4. **Security**: Never commit `.env` file to version control
5. **Scaling**: Deploy behind a reverse proxy (nginx) for production

---

Made with ❤️ for the open source community
