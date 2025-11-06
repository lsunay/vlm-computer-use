# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Option 1: Quick Start Script (Recommended)

```bash
# Make script executable (if not already)
chmod +x start.sh

# Run the start script
./start.sh
```

The script will:
1. Check Python installation
2. Create virtual environment
3. Install dependencies
4. Start the application

## Option 2: Manual Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Provider
```bash
# Copy example config
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your favorite editor
```

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open Browser
Navigate to: http://localhost:7860

## Option 3: Docker (Easiest for Deployment)

### With Docker Compose (Includes Ollama)
```bash
# Edit .env first
cp .env.example .env

# Start everything
docker-compose up -d

# View logs
docker-compose logs -f
```

### Docker Only
```bash
# Build
docker build -t vlm-demo .

# Run
docker run -p 7860:7860 --env-file .env vlm-demo
```

## First Time Setup

1. **Choose Your Provider:**
   - **Free & Local**: Use Ollama
   - **Best Quality**: Use OpenAI GPT-4o or Claude 3.5 Sonnet
   - **Custom**: Use your own API endpoint

2. **For Ollama (Free, Local):**
   ```bash
   # Install Ollama from https://ollama.ai

   # Pull a vision model
   ollama pull llava

   # Configure in .env
   DEFAULT_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434/v1
   OLLAMA_MODEL=llava:latest
   ```

3. **For OpenAI:**
   ```bash
   # Get API key from https://platform.openai.com

   # Configure in .env
   DEFAULT_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o
   ```

4. **For Anthropic:**
   ```bash
   # Get API key from https://console.anthropic.com

   # Configure in .env
   DEFAULT_PROVIDER=anthropic
   ANTHROPIC_API_KEY=sk-ant-...
   ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
   ```

## Testing the App

1. **Open the app**: http://localhost:7860

2. **Go to Configuration tab**
   - Verify your provider is initialized
   - Or configure dynamically in the UI

3. **Try Chat with Images**
   - Upload a test image
   - Ask: "What's in this image?"

4. **Try Screenshot to Code**
   - Upload a screenshot of a simple website
   - Click "Generate Code"

5. **Try Video Analysis** (if you have a short video)
   - Upload video
   - Ask: "Summarize this video"

## Troubleshooting

### Port 7860 already in use
```bash
# Change port in .env
APP_PORT=8080

# Or set when running
APP_PORT=8080 python app.py
```

### Ollama not connecting
```bash
# Make sure Ollama is running
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Module not found errors
```bash
# Ensure you're in the project directory
cd vlm-computer-use

# Reinstall dependencies
pip install -r requirements.txt
```

### Permission denied on start.sh
```bash
chmod +x start.sh
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore all tabs in the UI
- Try different modes (Chat, Analysis, Thinking)
- Experiment with different providers

## Support

- Check [README.md](README.md) for detailed troubleshooting
- Review provider documentation:
  - [OpenAI](https://platform.openai.com/docs)
  - [Anthropic](https://docs.anthropic.com)
  - [Ollama](https://ollama.ai/docs)

---

**Happy coding! 🎉**
