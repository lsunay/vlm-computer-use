"""
FastAPI REST API for programmatic access
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, Header
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import os
import shutil

from providers import ProviderFactory, VLMProvider
from database import db
from advanced_utils import BatchProcessor, OCRProcessor, count_tokens, calculate_cost

# API Models
class ChatRequest(BaseModel):
    message: str
    provider: str = "openai"
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    system_prompt: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    tokens_used: int
    cost: float
    session_id: Optional[int] = None


class AnalysisRequest(BaseModel):
    provider: str = "openai"
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    prompt: str = "Analyze this image in detail"


class BatchRequest(BaseModel):
    prompt: str
    provider: str = "openai"
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class CodeGenRequest(BaseModel):
    framework: str = "html"
    instructions: Optional[str] = None
    provider: str = "openai"
    model: Optional[str] = None
    api_key: Optional[str] = None
    base_url: Optional[str] = None


# Create FastAPI app
app = FastAPI(
    title="VLM Demo API",
    description="REST API for Vision Language Model operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helper function to create provider
def create_provider_from_request(provider: str, model: Optional[str], api_key: Optional[str], base_url: Optional[str]):
    """Create provider from request parameters"""
    try:
        return ProviderFactory.create_provider(
            provider_type=provider,
            api_key=api_key,
            base_url=base_url,
            model=model
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to initialize provider: {str(e)}")


# Endpoints
@app.get("/")
async def root():
    """API root"""
    return {
        "name": "VLM Demo API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "analyze": "/api/analyze",
            "batch": "/api/batch",
            "code": "/api/code",
            "ocr": "/api/ocr",
            "history": "/api/history",
            "stats": "/api/stats"
        }
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_image(
    message: str = Form(...),
    images: List[UploadFile] = File(...),
    provider: str = Form("openai"),
    model: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    base_url: Optional[str] = Form(None),
    system_prompt: Optional[str] = Form(None),
    save_history: bool = Form(False)
):
    """Chat with images endpoint"""
    try:
        # Save uploaded images temporarily
        temp_dir = tempfile.mkdtemp()
        image_paths = []

        for img in images:
            temp_path = os.path.join(temp_dir, img.filename)
            with open(temp_path, "wb") as f:
                shutil.copyfileobj(img.file, f)
            image_paths.append(temp_path)

        # Create provider
        vlm_provider = create_provider_from_request(provider, model, api_key, base_url)

        # Create message
        msg = vlm_provider.format_message_with_images(text=message, image_paths=image_paths)

        # Get response
        response = vlm_provider.chat(messages=[msg], system_prompt=system_prompt)

        # Calculate tokens and cost
        input_tokens = count_tokens(message, model or "gpt-4")
        output_tokens = count_tokens(response, model or "gpt-4")
        cost = calculate_cost(input_tokens, output_tokens, model or "gpt-4o")

        # Save to database if requested
        session_id = None
        if save_history:
            session_id = db.create_chat_session(provider=provider, model=model)
            db.add_message(session_id, "user", message, image_paths, input_tokens, 0)
            db.add_message(session_id, "assistant", response, None, output_tokens, cost)

        # Cleanup
        shutil.rmtree(temp_dir)

        return ChatResponse(
            response=response,
            tokens_used=input_tokens + output_tokens,
            cost=cost,
            session_id=session_id
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    prompt: str = Form("Analyze this image in detail"),
    provider: str = Form("openai"),
    model: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    base_url: Optional[str] = Form(None)
):
    """Analyze single image endpoint"""
    try:
        # Save image temporarily
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, image.filename)

        with open(temp_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        # Create provider
        vlm_provider = create_provider_from_request(provider, model, api_key, base_url)

        # Analyze
        msg = vlm_provider.format_message_with_images(text=prompt, image_paths=[temp_path])
        response = vlm_provider.chat(messages=[msg])

        # Cleanup
        shutil.rmtree(temp_dir)

        return {"analysis": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/batch")
async def batch_process(
    images: List[UploadFile] = File(...),
    prompt: str = Form(...),
    provider: str = Form("openai"),
    model: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    base_url: Optional[str] = Form(None)
):
    """Batch process multiple images"""
    try:
        # Save images
        temp_dir = tempfile.mkdtemp()
        image_paths = []

        for img in images:
            temp_path = os.path.join(temp_dir, img.filename)
            with open(temp_path, "wb") as f:
                shutil.copyfileobj(img.file, f)
            image_paths.append(temp_path)

        # Create provider
        vlm_provider = create_provider_from_request(provider, model, api_key, base_url)

        # Batch process
        processor = BatchProcessor(vlm_provider)
        results = processor.process_images(image_paths, prompt)

        # Cleanup
        shutil.rmtree(temp_dir)

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/code")
async def generate_code(
    images: List[UploadFile] = File(...),
    framework: str = Form("html"),
    instructions: Optional[str] = Form(None),
    provider: str = Form("openai"),
    model: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    base_url: Optional[str] = Form(None)
):
    """Generate code from screenshots"""
    try:
        # Save images
        temp_dir = tempfile.mkdtemp()
        image_paths = []

        for img in images:
            temp_path = os.path.join(temp_dir, img.filename)
            with open(temp_path, "wb") as f:
                shutil.copyfileobj(img.file, f)
            image_paths.append(temp_path)

        # Create provider
        vlm_provider = create_provider_from_request(provider, model, api_key, base_url)

        # Generate prompt
        prompt = f"Generate {framework} code for this design."
        if instructions:
            prompt += f" {instructions}"

        # Generate
        msg = vlm_provider.format_message_with_images(text=prompt, image_paths=image_paths)
        code = vlm_provider.chat(messages=[msg])

        # Cleanup
        shutil.rmtree(temp_dir)

        return {"code": code, "framework": framework}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ocr")
async def extract_text(
    image: UploadFile = File(...),
    lang: str = Form("eng")
):
    """Extract text from image using OCR"""
    try:
        # Save image
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, image.filename)

        with open(temp_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

        # OCR
        ocr = OCRProcessor()
        text = ocr.extract_text(temp_path, lang)

        # Cleanup
        shutil.rmtree(temp_dir)

        return {"text": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_chat_history(limit: int = 50):
    """Get chat history"""
    try:
        sessions = db.list_chat_sessions(limit=limit)
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history/{session_id}")
async def get_session(session_id: int):
    """Get specific chat session"""
    try:
        messages = db.get_session_history(session_id)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_usage_stats(days: int = 30):
    """Get usage statistics"""
    try:
        stats = db.get_usage_stats(days=days)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/templates")
async def get_templates(category: Optional[str] = None):
    """Get prompt templates"""
    try:
        templates = db.get_prompt_templates(category=category)
        return {"templates": templates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2025-11-06"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
