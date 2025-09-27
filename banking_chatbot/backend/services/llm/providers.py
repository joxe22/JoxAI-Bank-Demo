"""
🔌 LLM Providers - Integraciones con diferentes LLMs
Ubicación: backend/services/llm/providers.py

Implementa proveedores específicos para OpenAI, Anthropic, y otros LLMs.
Abstrae las diferencias entre APIs para uso uniforme.
"""

import os
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """
    🔧 Clase base abstracta para proveedores de LLM
    """

    def __init__(self):
        self.call_count = 0
        self.total_tokens = 0
        self.error_count = 0

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generar respuesta usando el LLM"""
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Verificar si el proveedor está disponible"""
        pass

class OpenAIProvider(LLMProvider):
    """
    🤖 Proveedor OpenAI (GPT-3.5, GPT-4)
    """

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = "https://api.openai.com/v1"
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        if not self.api_key:
            logger.warning("⚠️ OPENAI_API_KEY no configurada")

    async def generate(
            self,
            prompt: str,
            max_tokens: int = 1000,
            temperature: float = 0.7,
            **kwargs
    ) -> Dict[str, Any]:
        """
        🎯 Generar respuesta con OpenAI
        """

        if not self.api_key:
            raise ValueError("OpenAI API key no configurada")

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Eres un asistente bancario profesional y útil."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 1,
                "frequency_penalty": 0,
                "presence_penalty": 0
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=30
                ) as response:

                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"OpenAI API error {response.status}: {error_text}")

                    data = await response.json()

            # Extraer respuesta
            message_content = data["choices"][0]["message"]["content"]
            tokens_used = data["usage"]["total_tokens"]

            # Actualizar estadísticas
            self.call_count += 1
            self.total_tokens += tokens_used

            logger.info(f"✅ OpenAI response: {tokens_used} tokens")

            return {
                "message": message_content,
                "tokens_used": tokens_used,
                "model": self.model,
                "finish_reason": data["choices"][0]["finish_reason"]
            }

        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ OpenAI error: {str(e)}")
            raise

    async def is_available(self) -> bool:
        """✅ Verificar disponibilidad de OpenAI"""

        if not self.api_key:
            return False

        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}

            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"{self.base_url}/models",
                        headers=headers,
                        timeout=5
                ) as response:
                    return response.status == 200

        except Exception:
            return False

class AnthropicProvider(LLMProvider):
    """
    🧠 Proveedor Anthropic (Claude)
    """

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1"
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-sonnet-20240229")

        if not self.api_key:
            logger.warning("⚠️ ANTHROPIC_API_KEY no configurada")

    async def generate(
            self,
            prompt: str,
            max_tokens: int = 1000,
            temperature: float = 0.7,
            **kwargs
    ) -> Dict[str, Any]:
        """
        🎯 Generar respuesta con Anthropic Claude
        """

        if not self.api_key:
            raise ValueError("Anthropic API key no configurada")

        try:
            headers = {
                "x-api-key": self.api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/messages",
                        headers=headers,
                        json=payload,
                        timeout=30
                ) as response:

                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Anthropic API error {response.status}: {error_text}")

                    data = await response.json()

            # Extraer respuesta
            message_content = data["content"][0]["text"]
            tokens_used = data["usage"]["input_tokens"] + data["usage"]["output_tokens"]

            # Actualizar estadísticas
            self.call_count += 1
            self.total_tokens += tokens_used

            logger.info(f"✅ Anthropic response: {tokens_used} tokens")

            return {
                "message": message_content,
                "tokens_used": tokens_used,
                "model": self.model,
                "stop_reason": data["stop_reason"]
            }

        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ Anthropic error: {str(e)}")
            raise

    async def is_available(self) -> bool:
        """✅ Verificar disponibilidad de Anthropic"""

        if not self.api_key:
            return False

        try:
            # Hacer una llamada de test simple
            headers = {
                "x-api-key": self.api_key,
                "content-type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": self.model,
                "max_tokens": 10,
                "messages": [{"role": "user", "content": "test"}]
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/messages",
                        headers=headers,
                        json=payload,
                        timeout=5
                ) as response:
                    return response.status == 200

        except Exception:
            return False

class LocalLLMProvider(LLMProvider):
    """
    🏠 Proveedor para LLM local (Ollama, vLLM, etc.)
    """

    def __init__(self, base_url: str = "http://localhost:11434"):
        super().__init__()
        self.base_url = base_url
        self.model = os.getenv("LOCAL_LLM_MODEL", "llama2")

    async def generate(
            self,
            prompt: str,
            max_tokens: int = 1000,
            temperature: float = 0.7,
            **kwargs
    ) -> Dict[str, Any]:
        """
        🎯 Generar respuesta con LLM local
        """

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/api/generate",
                        json=payload,
                        timeout=60  # LLMs locales pueden ser más lentos
                ) as response:

                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Local LLM error {response.status}: {error_text}")

                    data = await response.json()

            # Extraer respuesta
            message_content = data.get("response", "")
            tokens_used = len(message_content.split())  # Aproximación

            # Actualizar estadísticas
            self.call_count += 1
            self.total_tokens += tokens_used

            logger.info(f"✅ Local LLM response: ~{tokens_used} tokens")

            return {
                "message": message_content,
                "tokens_used": tokens_used,
                "model": self.model,
                "done": data.get("done", True)
            }

        except Exception as e:
            self.error_count += 1
            logger.error(f"❌ Local LLM error: {str(e)}")
            raise

    async def is_available(self) -> bool:
        """✅ Verificar disponibilidad del LLM local"""

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        f"{self.base_url}/api/tags",
                        timeout=5
                ) as response:
                    return response.status == 200

        except Exception:
            return False