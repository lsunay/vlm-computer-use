# 🌐 REST API Documentation

The VLM Demo application includes a full-featured REST API built with FastAPI.

## Getting Started

### Start the API Server

```bash
# Method 1: Standalone
python api.py

# Method 2: With Uvicorn
uvicorn api:app --host 0.0.0.0 --port 8000

# Method 3: Development mode (auto-reload)
uvicorn api:app --reload
```

### Base URL

```
http://localhost:8000
```

### Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Currently, the API is open. For production, add authentication:

```python
from fastapi import Header, HTTPException

async def verify_token(x_api_key: str = Header(...)):
    if x_api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return x_api_key
```

## Endpoints

### 1. Root / Health Check

```http
GET /
GET /health
```

**Response:**
```json
{
  "name": "VLM Demo API",
  "version": "1.0.0",
  "status": "healthy"
}
```

### 2. Chat with Images

```http
POST /api/chat
```

**Parameters:**
- `message` (form): Your text message
- `images` (files): One or more image files
- `provider` (form, optional): Provider name (default: "openai")
- `model` (form, optional): Model name
- `api_key` (form, optional): API key
- `base_url` (form, optional): Base URL
- `system_prompt` (form, optional): System prompt
- `save_history` (form, optional): Save to database (default: false)

**Example (Python):**
```python
import requests

files = [
    ('images', open('image1.jpg', 'rb')),
    ('images', open('image2.jpg', 'rb'))
]

data = {
    'message': 'What do you see in these images?',
    'provider': 'openai',
    'model': 'gpt-4o',
    'save_history': True
}

response = requests.post(
    'http://localhost:8000/api/chat',
    files=files,
    data=data
)

print(response.json())
```

**Example (cURL):**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -F "message=Describe this image" \
  -F "images=@image.jpg" \
  -F "provider=openai" \
  -F "model=gpt-4o"
```

**Response:**
```json
{
  "response": "I see a beautiful landscape...",
  "tokens_used": 1234,
  "cost": 0.0123,
  "session_id": 42
}
```

### 3. Analyze Single Image

```http
POST /api/analyze
```

**Parameters:**
- `image` (file): Image file
- `prompt` (form): Analysis prompt (default: "Analyze this image in detail")
- `provider` (form, optional): Provider name
- `model` (form, optional): Model name
- `api_key` (form, optional): API key
- `base_url` (form, optional): Base URL

**Example:**
```python
import requests

files = {'image': open('screenshot.png', 'rb')}
data = {'prompt': 'Extract all text from this image'}

response = requests.post(
    'http://localhost:8000/api/analyze',
    files=files,
    data=data
)

print(response.json()['analysis'])
```

**Response:**
```json
{
  "analysis": "This image contains the following text..."
}
```

### 4. Batch Process Images

```http
POST /api/batch
```

**Parameters:**
- `images` (files): Multiple image files
- `prompt` (form): Prompt to apply to all images
- `provider` (form, optional): Provider name
- `model` (form, optional): Model name
- `api_key` (form, optional): API key
- `base_url` (form, optional): Base URL

**Example:**
```python
import requests

files = [
    ('images', open('img1.jpg', 'rb')),
    ('images', open('img2.jpg', 'rb')),
    ('images', open('img3.jpg', 'rb'))
]

data = {'prompt': 'Generate a caption for this image'}

response = requests.post(
    'http://localhost:8000/api/batch',
    files=files,
    data=data
)

results = response.json()['results']
for result in results:
    print(f"{result['image']}: {result['result']}")
```

**Response:**
```json
{
  "results": [
    {
      "image": "img1.jpg",
      "result": "A serene mountain landscape...",
      "success": true,
      "error": null
    },
    {
      "image": "img2.jpg",
      "result": "A busy city street...",
      "success": true,
      "error": null
    }
  ]
}
```

### 5. Generate Code from Screenshots

```http
POST /api/code
```

**Parameters:**
- `images` (files): Screenshot image files
- `framework` (form): Target framework (default: "html")
- `instructions` (form, optional): Additional instructions
- `provider` (form, optional): Provider name
- `model` (form, optional): Model name
- `api_key` (form, optional): API key
- `base_url` (form, optional): Base URL

**Example:**
```python
import requests

files = {'images': open('design.png', 'rb')}
data = {
    'framework': 'react',
    'instructions': 'Use Tailwind CSS and make it responsive'
}

response = requests.post(
    'http://localhost:8000/api/code',
    files=files,
    data=data
)

print(response.json()['code'])
```

**Response:**
```json
{
  "code": "import React from 'react';\n\nconst Component = () => {...}",
  "framework": "react"
}
```

### 6. OCR Text Extraction

```http
POST /api/ocr
```

**Parameters:**
- `image` (file): Image file
- `lang` (form, optional): Language code (default: "eng")

**Example:**
```python
import requests

files = {'image': open('document.jpg', 'rb')}
data = {'lang': 'eng'}

response = requests.post(
    'http://localhost:8000/api/ocr',
    files=files,
    data=data
)

print(response.json()['text'])
```

**Response:**
```json
{
  "text": "Extracted text content here..."
}
```

### 7. Get Chat History

```http
GET /api/history?limit=50
```

**Parameters:**
- `limit` (query, optional): Number of sessions to return (default: 50)

**Example:**
```python
import requests

response = requests.get('http://localhost:8000/api/history?limit=10')
sessions = response.json()['sessions']

for session in sessions:
    print(f"Session {session['id']}: {session['title']}")
```

**Response:**
```json
{
  "sessions": [
    {
      "id": 1,
      "title": "Image Analysis",
      "created_at": "2025-11-06T10:00:00",
      "updated_at": "2025-11-06T10:30:00",
      "provider": "openai",
      "model": "gpt-4o",
      "mode": "chat",
      "message_count": 5
    }
  ]
}
```

### 8. Get Specific Session

```http
GET /api/history/{session_id}
```

**Example:**
```python
import requests

response = requests.get('http://localhost:8000/api/history/1')
messages = response.json()['messages']

for msg in messages:
    print(f"{msg['role']}: {msg['content']}")
```

**Response:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "What's in this image?",
      "image_paths": ["path/to/image.jpg"],
      "timestamp": "2025-11-06T10:00:00",
      "tokens": 1024,
      "cost": 0.001
    },
    {
      "role": "assistant",
      "content": "I see a beautiful landscape...",
      "image_paths": [],
      "timestamp": "2025-11-06T10:00:05",
      "tokens": 512,
      "cost": 0.005
    }
  ]
}
```

### 9. Usage Statistics

```http
GET /api/stats?days=30
```

**Parameters:**
- `days` (query, optional): Number of days to analyze (default: 30)

**Example:**
```python
import requests

response = requests.get('http://localhost:8000/api/stats?days=7')
stats = response.json()

print(f"Total cost: ${stats['total_cost']:.2f}")
print(f"Total requests: {stats['total_requests']}")
```

**Response:**
```json
{
  "total_requests": 150,
  "total_cost": 12.34,
  "total_tokens": 123456,
  "by_provider": {},
  "by_operation": {},
  "success_rate": 98.5
}
```

### 10. Prompt Templates

```http
GET /api/templates?category=General%20Analysis
```

**Parameters:**
- `category` (query, optional): Filter by category

**Example:**
```python
import requests

response = requests.get('http://localhost:8000/api/templates')
templates = response.json()['templates']

for template in templates:
    print(f"{template['name']}: {template['template']}")
```

**Response:**
```json
{
  "templates": [
    {
      "id": 1,
      "name": "Describe Image",
      "category": "General Analysis",
      "template": "Describe this image in detail...",
      "description": "General image description"
    }
  ]
}
```

## Error Handling

All endpoints return standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid parameters)
- **403**: Forbidden (authentication failed)
- **404**: Not Found
- **500**: Internal Server Error

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

## Rate Limiting

To add rate limiting:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat_with_image(...):
    ...
```

## CORS Configuration

The API has CORS enabled for all origins. For production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # Restrict methods
    allow_headers=["*"],
)
```

## Webhooks

To add webhook support:

```python
@app.post("/api/webhook")
async def webhook_handler(data: dict):
    # Process webhook
    # Trigger analysis
    # Send results to callback URL
    pass
```

## SDKs

### Python SDK Example

```python
class VLMClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def chat(self, message, images, **kwargs):
        files = [('images', open(img, 'rb')) for img in images]
        data = {'message': message, **kwargs}
        response = requests.post(
            f"{self.base_url}/api/chat",
            files=files,
            data=data
        )
        return response.json()

# Usage
client = VLMClient()
result = client.chat(
    message="What's this?",
    images=["image.jpg"],
    provider="openai"
)
print(result['response'])
```

### JavaScript/Node.js Example

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function chatWithImage(message, imagePath) {
    const form = new FormData();
    form.append('message', message);
    form.append('images', fs.createReadStream(imagePath));
    form.append('provider', 'openai');

    const response = await axios.post(
        'http://localhost:8000/api/chat',
        form,
        { headers: form.getHeaders() }
    );

    return response.data;
}

// Usage
chatWithImage('Describe this', 'image.jpg')
    .then(result => console.log(result.response));
```

## Deployment

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Best Practices

1. **Use API Keys**: Add authentication in production
2. **Rate Limit**: Prevent abuse
3. **Validate Input**: Check file sizes and types
4. **Log Requests**: Monitor usage
5. **Handle Errors**: Graceful error handling
6. **Version API**: Use `/v1/`, `/v2/` prefixes
7. **Document Everything**: Keep docs up-to-date
8. **Monitor Performance**: Track response times
9. **Secure HTTPS**: Use SSL in production
10. **Backup Database**: Regular backups

---

**Questions?** Check the main [README.md](README.md) or open an issue!
