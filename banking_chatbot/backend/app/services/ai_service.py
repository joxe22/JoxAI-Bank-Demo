# AI Service for chatbot responses
import os
from typing import Dict, List, Optional
import httpx


class AIService:
    """
    AI Service that supports both Anthropic and OpenAI
    Configurable via environment variables
    """
    
    def __init__(self):
        # Auto-detect provider based on available API keys
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")
        
        # Priority: explicit AI_PROVIDER > anthropic > openai > mock
        explicit_provider = os.getenv("AI_PROVIDER", "").lower()
        
        if explicit_provider in ["anthropic", "openai", "mock"]:
            self.provider = explicit_provider
        elif anthropic_key:
            self.provider = "anthropic"
        elif openai_key:
            self.provider = "openai"
        else:
            self.provider = "mock"
        
        self.api_key = None
        self.client = None
        
        if self.provider == "anthropic":
            self.api_key = anthropic_key
            # The newest Anthropic model is "claude-sonnet-4-20250514"
            self.model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
        elif self.provider == "openai":
            self.api_key = openai_key
            self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    async def generate_response(
        self,
        message: str,
        conversation_history: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict:
        """Generate AI response based on provider"""
        
        if self.provider == "anthropic":
            return await self._generate_anthropic(message, conversation_history, system_prompt)
        elif self.provider == "openai":
            return await self._generate_openai(message, conversation_history, system_prompt)
        else:
            return self._generate_mock(message)
    
    async def _generate_anthropic(
        self,
        message: str,
        conversation_history: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict:
        """Generate response using Anthropic Claude"""
        
        if not self.api_key:
            return {
                "content": "Error: ANTHROPIC_API_KEY no configurada. Por favor configura tu API key en Settings.",
                "metadata": {"error": "missing_api_key"}
            }
        
        try:
            # Build messages array
            messages = []
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages for context
                    if msg["role"] in ["user", "assistant"]:
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
            
            # Add current message
            messages.append({
                "role": "user",
                "content": message
            })
            
            # Default banking system prompt
            if not system_prompt:
                system_prompt = """Eres un asistente virtual de JoxAI Bank, un banco moderno y confiable. 

Tus responsabilidades:
- Ayudar a clientes con consultas sobre productos bancarios, saldos, transferencias y servicios
- Proporcionar información clara y precisa sobre procedimientos bancarios
- Ser amable, profesional y eficiente
- Escalar a un agente humano cuando la consulta requiera autorización o información sensible

Productos que ofreces:
- Tarjetas de crédito (Clásica, Gold, Platinum)
- Cuentas de ahorro e inversión
- Transferencias (SPEI y tradicionales)
- Préstamos personales e hipotecarios

Si el cliente necesita:
- Acceder a información de cuenta: solicita autenticación
- Realizar transacciones: deriva a un agente humano
- Resolver problemas complejos: escala el caso

Responde siempre en español, de forma concisa y útil."""
            
            # Call Anthropic API with full error handling
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://api.anthropic.com/v1/messages",
                        headers={
                            "x-api-key": self.api_key,
                            "anthropic-version": "2023-06-01",
                            "content-type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "max_tokens": 1024,
                            "system": system_prompt,
                            "messages": messages
                        },
                        timeout=30.0
                    )
                    
                    # Parse response safely
                    try:
                        result = response.json()
                    except Exception as e:
                        return {
                            "content": f"Error: Respuesta inválida de Anthropic API (status {response.status_code})",
                            "metadata": {"error": "invalid_json", "status": response.status_code, "details": str(e)}
                        }
                    
                    if response.status_code != 200:
                        error_detail = result.get("error", {}).get("message", "Unknown error")
                        return {
                            "content": f"Error de IA: {error_detail}",
                            "metadata": {"error": "api_error", "status": response.status_code}
                        }
                    
                    # Extract content safely with validation
                    try:
                        if not isinstance(result, dict):
                            raise ValueError("Response is not a dictionary")
                        if "content" not in result or not isinstance(result["content"], list):
                            raise ValueError("Missing or invalid content field")
                        if len(result["content"]) == 0:
                            raise ValueError("Empty content array")
                        if "text" not in result["content"][0]:
                            raise ValueError("Missing text field in content")
                        content = result["content"][0]["text"]
                    except (KeyError, IndexError, TypeError, ValueError) as e:
                        return {
                            "content": f"Error: Formato de respuesta inesperado de Anthropic - {str(e)}",
                            "metadata": {"error": "invalid_response_format", "details": str(e)}
                        }
                    
                    # Detect if escalation is needed
                    suggest_escalation = any(keyword in message.lower() for keyword in [
                        "agente", "humano", "persona", "hablar con alguien", "representante"
                    ])
                    
                    return {
                        "content": content,
                        "metadata": {
                            "model": self.model,
                            "provider": "anthropic",
                            "suggest_escalation": suggest_escalation
                        }
                    }
                    
            except httpx.TimeoutException:
                return {
                    "content": "Error: Timeout al contactar a Anthropic API (30s)",
                    "metadata": {"error": "timeout"}
                }
            except Exception as e:
                return {
                    "content": f"Error al comunicarse con Anthropic: {str(e)}",
                    "metadata": {"error": "connection_error", "details": str(e)}
                }
                
        except Exception as e:
            return {
                "content": f"Error al generar respuesta: {str(e)}",
                "metadata": {"error": "exception", "details": str(e)}
            }
    
    async def _generate_openai(
        self,
        message: str,
        conversation_history: Optional[List[Dict]] = None,
        system_prompt: Optional[str] = None
    ) -> Dict:
        """Generate response using OpenAI GPT"""
        
        if not self.api_key:
            return {
                "content": "Error: OPENAI_API_KEY no configurada. Por favor configura tu API key en Settings.",
                "metadata": {"error": "missing_api_key"}
            }
        
        try:
            # Build messages array
            messages = []
            
            # System prompt
            if not system_prompt:
                system_prompt = """Eres un asistente virtual de JoxAI Bank, un banco moderno y confiable. 

Tus responsabilidades:
- Ayudar a clientes con consultas sobre productos bancarios, saldos, transferencias y servicios
- Proporcionar información clara y precisa sobre procedimientos bancarios
- Ser amable, profesional y eficiente
- Escalar a un agente humano cuando la consulta requiera autorización o información sensible

Productos que ofreces:
- Tarjetas de crédito (Clásica, Gold, Platinum)
- Cuentas de ahorro e inversión
- Transferencias (SPEI y tradicionales)
- Préstamos personales e hipotecarios

Si el cliente necesita:
- Acceder a información de cuenta: solicita autenticación
- Realizar transacciones: deriva a un agente humano
- Resolver problemas complejos: escala el caso

Responde siempre en español, de forma concisa y útil."""
            
            messages.append({"role": "system", "content": system_prompt})
            
            # Conversation history
            if conversation_history:
                for msg in conversation_history[-10:]:  # Last 10 messages
                    if msg["role"] in ["user", "assistant"]:
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
            
            # Current message
            messages.append({"role": "user", "content": message})
            
            # Call OpenAI API with full error handling
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": messages,
                            "max_tokens": 1024,
                            "temperature": 0.7
                        },
                        timeout=30.0
                    )
                    
                    # Parse response safely
                    try:
                        result = response.json()
                    except Exception as e:
                        return {
                            "content": f"Error: Respuesta inválida de OpenAI API (status {response.status_code})",
                            "metadata": {"error": "invalid_json", "status": response.status_code, "details": str(e)}
                        }
                    
                    if response.status_code != 200:
                        error_detail = result.get("error", {}).get("message", "Unknown error")
                        return {
                            "content": f"Error de IA: {error_detail}",
                            "metadata": {"error": "api_error", "status": response.status_code}
                        }
                    
                    # Extract content safely with validation
                    try:
                        if not isinstance(result, dict):
                            raise ValueError("Response is not a dictionary")
                        if "choices" not in result or not isinstance(result["choices"], list):
                            raise ValueError("Missing or invalid choices field")
                        if len(result["choices"]) == 0:
                            raise ValueError("Empty choices array")
                        if "message" not in result["choices"][0]:
                            raise ValueError("Missing message field in choice")
                        if "content" not in result["choices"][0]["message"]:
                            raise ValueError("Missing content field in message")
                        content = result["choices"][0]["message"]["content"]
                    except (KeyError, IndexError, TypeError, ValueError) as e:
                        return {
                            "content": f"Error: Formato de respuesta inesperado de OpenAI - {str(e)}",
                            "metadata": {"error": "invalid_response_format", "details": str(e)}
                        }
                    
                    # Detect if escalation is needed
                    suggest_escalation = any(keyword in message.lower() for keyword in [
                        "agente", "humano", "persona", "hablar con alguien", "representante"
                    ])
                    
                    return {
                        "content": content,
                        "metadata": {
                            "model": self.model,
                            "provider": "openai",
                            "suggest_escalation": suggest_escalation
                        }
                    }
                    
            except httpx.TimeoutException:
                return {
                    "content": "Error: Timeout al contactar a OpenAI API (30s)",
                    "metadata": {"error": "timeout"}
                }
            except Exception as e:
                return {
                    "content": f"Error al comunicarse con OpenAI: {str(e)}",
                    "metadata": {"error": "connection_error", "details": str(e)}
                }
                
        except Exception as e:
            return {
                "content": f"Error al generar respuesta: {str(e)}",
                "metadata": {"error": "exception", "details": str(e)}
            }
    
    def _generate_mock(self, message: str) -> Dict:
        """Generate mock response (for development/testing)"""
        message_lower = message.lower()
        
        # Banking knowledge responses
        if "saldo" in message_lower or "balance" in message_lower:
            return {
                "content": "Para consultar tu saldo, necesito verificar tu identidad. ¿Podrías proporcionarme tu número de cliente o iniciar sesión en la aplicación móvil?",
                "metadata": {"intent": "balance_inquiry", "requires_auth": True}
            }
        
        elif "tarjeta" in message_lower or "crédito" in message_lower or "credit" in message_lower:
            return {
                "content": "Ofrecemos varias opciones de tarjetas de crédito:\n\n🔷 **Tarjeta Clásica**: Sin anualidad el primer año, 3% cashback en supermercados\n🔷 **Tarjeta Gold**: Acceso a salas VIP, 5% cashback en viajes\n🔷 **Tarjeta Platinum**: Servicio de conserjería 24/7, 10% cashback en restaurantes\n\n¿Sobre cuál te gustaría saber más?",
                "metadata": {"intent": "credit_card_info", "category": "products"}
            }
        
        elif "transferencia" in message_lower or "transfer" in message_lower or "enviar dinero" in message_lower:
            return {
                "content": "Para hacer una transferencia:\n\n1. Ingresa a tu banca en línea o app móvil\n2. Selecciona 'Transferencias'\n3. Elige el tipo: SPEI (inmediata) o tradicional\n4. Ingresa los datos del beneficiario (CLABE o número de tarjeta)\n5. Confirma el monto y autoriza con tu token\n\n¿Necesitas ayuda con algún paso específico?",
                "metadata": {"intent": "transfer_help", "category": "transactions"}
            }
        
        elif "plan" in message_lower or "ahorro" in message_lower or "inversión" in message_lower:
            return {
                "content": "Tenemos excelentes planes de ahorro e inversión:\n\n💰 **Plan Ahorro Básico**: 4% anual, sin comisiones\n💰 **Inversión Plus**: 6-8% anual, liquidez a 30 días\n💰 **Portafolio Premium**: Gestión profesional, rendimientos variables\n\n¿Te gustaría que un asesor te contacte para personalizar un plan?",
                "metadata": {"intent": "savings_plans", "category": "financial_planning"}
            }
        
        elif "agente" in message_lower or "humano" in message_lower or "persona" in message_lower:
            return {
                "content": "Entiendo que prefieres hablar con un agente humano. Puedo escalar tu consulta a nuestro equipo de soporte.\n\n¿Podrías describirme brevemente tu consulta para asignarla al departamento correcto?",
                "metadata": {"intent": "agent_request", "suggest_escalation": True}
            }
        
        # Default response
        return {
            "content": f"Entiendo tu consulta. Te puedo ayudar con:\n\n• Información sobre productos bancarios\n• Procedimientos y trámites\n• Consultas generales\n\nSi necesitas algo más específico o ayuda personalizada, puedo conectarte con un agente humano. ¿En qué más puedo ayudarte?",
            "metadata": {"intent": "general_inquiry"}
        }


# Global instance
ai_service = AIService()
