"""
Simplified models.py for Railway deployment
This version uses direct API calls instead of langchain to avoid dependency issues
"""

from enum import Enum
import os
import json
import requests
from typing import Any, Optional
from python.helpers import dotenv

# Load environment variables
dotenv.load_dotenv()


class ModelType(Enum):
    CHAT = "Chat"
    EMBEDDING = "Embedding"


class ModelProvider(Enum):
    ANTHROPIC = "Anthropic"
    OPENAI = "OpenAI"
    OTHER = "Other"


class SimpleChat:
    """Simple chat wrapper for direct API calls"""
    
    def __init__(self, provider: str, model: str, api_key: str):
        self.provider = provider
        self.model = model
        self.api_key = api_key
    
    def invoke(self, messages):
        """Simple invoke method for compatibility"""
        if self.provider == "openai":
            return self._call_openai(messages)
        elif self.provider == "anthropic":
            return self._call_anthropic(messages)
        else:
            return SimpleResponse("Model not available in simplified mode")
    
    def _call_openai(self, messages):
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            # Convert to OpenAI format
            if isinstance(messages, str):
                messages = [{"role": "user", "content": messages}]
            elif hasattr(messages, 'content'):
                messages = [{"role": "user", "content": messages.content}]
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000
            )
            
            return SimpleResponse(response.choices[0].message.content)
        except Exception as e:
            return SimpleResponse(f"OpenAI error: {str(e)}")
    
    def _call_anthropic(self, messages):
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # Convert to Anthropic format
            if isinstance(messages, str):
                content = messages
            elif hasattr(messages, 'content'):
                content = messages.content
            else:
                content = str(messages)
            
            response = client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": content}]
            )
            
            return SimpleResponse(response.content[0].text)
        except Exception as e:
            return SimpleResponse(f"Anthropic error: {str(e)}")


class SimpleResponse:
    """Simple response wrapper"""
    
    def __init__(self, content: str):
        self.content = content
    
    def __str__(self):
        return self.content


def get_api_key(service):
    """Get API key from environment"""
    return (
        dotenv.get_dotenv_value(f"API_KEY_{service.upper()}")
        or dotenv.get_dotenv_value(f"{service.upper()}_API_KEY")
        or os.getenv(f"API_KEY_{service.upper()}")
        or os.getenv(f"{service.upper()}_API_KEY")
        or "None"
    )


def get_model(type: ModelType, provider: ModelProvider, name: str, **kwargs):
    """Get a simple model instance"""
    
    if provider == ModelProvider.OPENAI:
        api_key = get_api_key("openai")
        return SimpleChat("openai", name, api_key)
    
    elif provider == ModelProvider.ANTHROPIC:
        api_key = get_api_key("anthropic")
        return SimpleChat("anthropic", name, api_key)
    
    else:
        # Return a fallback that explains the limitation
        class UnavailableModel:
            def invoke(self, messages):
                return SimpleResponse(f"Model {provider.value} not available in simplified mode. Please use OpenAI or Anthropic models.")
        
        return UnavailableModel()


def parse_chunk(chunk: Any):
    """Parse response chunks"""
    if isinstance(chunk, str):
        return chunk
    elif hasattr(chunk, "content"):
        return str(chunk.content)
    else:
        return str(chunk)


# Simple implementations for specific providers
def get_openai_chat(model_name: str, api_key=None, **kwargs):
    """Get OpenAI chat model"""
    if not api_key:
        api_key = get_api_key("openai")
    return SimpleChat("openai", model_name, api_key)


def get_anthropic_chat(model_name: str, api_key=None, **kwargs):
    """Get Anthropic chat model"""
    if not api_key:
        api_key = get_api_key("anthropic")
    return SimpleChat("anthropic", model_name, api_key)


# Fallback functions for unsupported providers
def get_ollama_chat(*args, **kwargs):
    raise ImportError("Ollama not available in simplified mode")

def get_groq_chat(*args, **kwargs):
    raise ImportError("Groq not available in simplified mode")

def get_huggingface_chat(*args, **kwargs):
    raise ImportError("HuggingFace not available in simplified mode")

def get_google_chat(*args, **kwargs):
    raise ImportError("Google models not available in simplified mode")

def get_mistralai_chat(*args, **kwargs):
    raise ImportError("Mistral AI not available in simplified mode")

# Embedding functions (simplified)
def get_openai_embedding(*args, **kwargs):
    raise ImportError("Embeddings not available in simplified mode")

def get_anthropic_embedding(*args, **kwargs):
    raise ImportError("Embeddings not available in simplified mode")


# Rate limiter placeholder
class SimpleRateLimiter:
    def __init__(self, seconds=60):
        self.limits = {"requests": 0, "input": 0, "output": 0}
    
    def wait_if_needed(self, *args, **kwargs):
        pass  # No rate limiting in simple mode


def get_rate_limiter(provider: ModelProvider, name: str, requests: int, input: int, output: int):
    """Get a simple rate limiter"""
    return SimpleRateLimiter() 