"""
Provider abstraction layer for multiple LLM providers
Supports OpenAI, Anthropic, Ollama, and custom OpenAI-compatible APIs
"""

import os
import base64
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
import anthropic
from openai import OpenAI


def encode_image(image_path: str) -> str:
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class VLMProvider(ABC):
    """Abstract base class for VLM providers"""

    @abstractmethod
    def chat(self, messages: List[Dict[str, Any]], system_prompt: Optional[str] = None) -> str:
        """Send chat request to the provider"""
        pass

    @abstractmethod
    def format_message_with_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Format a message with text and images"""
        pass


class OpenAIProvider(VLMProvider):
    """OpenAI provider (works with OpenAI-compatible APIs too)"""

    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def format_message_with_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Format message with images for OpenAI API"""
        content = []

        # Add images first
        for image_path in image_paths:
            # Determine image format from file extension
            ext = image_path.lower().split('.')[-1]
            mime_type = f"image/{ext}" if ext in ['jpeg', 'jpg', 'png', 'gif', 'webp'] else "image/jpeg"

            base64_image = encode_image(image_path)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}"
                }
            })

        # Add text
        if text:
            content.append({
                "type": "text",
                "text": text
            })

        return {"role": "user", "content": content}

    def chat(self, messages: List[Dict[str, Any]], system_prompt: Optional[str] = None) -> str:
        """Send chat request to OpenAI API"""
        api_messages = []

        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})

        api_messages.extend(messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=api_messages,
            max_tokens=4096,
            temperature=0.7,
        )

        return response.choices[0].message.content


class AnthropicProvider(VLMProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: str, model: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def format_message_with_images(self, text: str, image_paths: List[str]) -> Dict[str, Any]:
        """Format message with images for Anthropic API"""
        content = []

        # Add images first
        for image_path in image_paths:
            ext = image_path.lower().split('.')[-1]
            media_type = f"image/{ext}" if ext in ['jpeg', 'jpg', 'png', 'gif', 'webp'] else "image/jpeg"
            if media_type == "image/jpg":
                media_type = "image/jpeg"

            base64_image = encode_image(image_path)
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": media_type,
                    "data": base64_image,
                }
            })

        # Add text
        if text:
            content.append({
                "type": "text",
                "text": text
            })

        return {"role": "user", "content": content}

    def chat(self, messages: List[Dict[str, Any]], system_prompt: Optional[str] = None) -> str:
        """Send chat request to Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            system=system_prompt or "You are a helpful AI assistant with vision capabilities.",
            messages=messages,
        )

        return response.content[0].text


class ProviderFactory:
    """Factory class to create provider instances"""

    @staticmethod
    def create_provider(
        provider_type: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ) -> VLMProvider:
        """Create a provider instance based on type"""

        provider_type = provider_type.lower()

        if provider_type == "openai":
            api_key = api_key or os.getenv("OPENAI_API_KEY")
            base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
            return OpenAIProvider(api_key, base_url, model)

        elif provider_type == "anthropic":
            api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
            model = model or os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
            return AnthropicProvider(api_key, model)

        elif provider_type == "custom":
            api_key = api_key or os.getenv("CUSTOM_API_KEY", "dummy")
            base_url = base_url or os.getenv("CUSTOM_BASE_URL", "http://localhost:11434/v1")
            model = model or os.getenv("CUSTOM_MODEL", "llava:latest")
            return OpenAIProvider(api_key, base_url, model)

        elif provider_type == "ollama":
            api_key = "ollama"  # Ollama doesn't require an API key
            base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            model = model or os.getenv("OLLAMA_MODEL", "llava:latest")
            return OpenAIProvider(api_key, base_url, model)

        else:
            raise ValueError(f"Unknown provider type: {provider_type}")
