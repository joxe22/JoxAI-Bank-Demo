"""
🤖 LLM Service - Orquestador de Modelos de Lenguaje
Ubicación: backend/services/llm/llm_service.py

Servicio principal que orquesta la interacción con diferentes proveedores de LLM.
Implementa RAG (Retrieval Augmented Generation) y manejo de prompts.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from .providers import OpenAIProvider, AnthropicProvider
from .prompt_templates import PromptTemplates
from ..rag.rag_service import RAGService

logger = logging.getLogger(__name__)

class LLMService:
    """
    🤖 Servicio principal de LLM

    Responsabilidades:
    - Orquestar diferentes proveedores de LLM
    - Implementar RAG (Retrieval Augmented Generation)
    - Aplicar templates de prompts bancarios
    - Manejar contexto conversacional
    - Aplicar guardrails de seguridad
    """

    def __init__(self):
        """Inicializar servicio LLM"""

        # Inicializar proveedores
        self.openai_provider = OpenAIProvider()
        self.anthropic_provider = AnthropicProvider()

        # Servicios relacionados
        self.rag_service = RAGService()
        self.prompt_templates = PromptTemplates()

        # Configuración
        self.default_provider = "openai"
        self.max_tokens = 1000
        self.temperature = 0.7

        # Guardrails
        self.forbidden_topics = [
            "política", "religión", "inversiones no bancarias",
            "asesoría legal", "consejos médicos"
        ]

        logger.info("🤖 LLM Service inicializado")

    async def generate_response(
            self,
            user_message: str,
            session_id: str,
            context: Optional[Dict[str, Any]] = None,
            provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        🎯 Generar respuesta usando RAG + LLM

        Flujo:
        1. Retrieve: Buscar información relevante en KB
        2. Augment: Enriquecer prompt con contexto
        3. Generate: Generar respuesta con LLM
        4. Validate: Aplicar guardrails y validaciones
        """

        start_time = datetime.now()
        logger.info(f"🎯 Generando respuesta para: {user_message[:50]}...")

        try:
            # 1. RETRIEVE: Buscar información relevante
            relevant_docs = await self.rag_service.retrieve_relevant_documents(
                query=user_message,
                top_k=3
            )

            # 2. AUGMENT: Construir prompt enriquecido
            enhanced_prompt = await self._build_enhanced_prompt(
                user_message=user_message,
                relevant_docs=relevant_docs,
                context=context
            )

            # 3. GENERATE: Generar respuesta con LLM
            llm_response = await self._call_llm(
                prompt=enhanced_prompt,
                provider=provider or self.default_provider
            )

            # 4. VALIDATE: Aplicar guardrails
            validated_response = await self._apply_guardrails(llm_response, user_message)

            # 5. Calcular métricas
            processing_time = (datetime.now() - start_time).total_seconds()

            return {
                "message": validated_response["message"],
                "confidence": validated_response["confidence"],
                "sources": relevant_docs,
                "requires_auth": validated_response.get("requires_auth", False),
                "escalate_to_human": validated_response.get("escalate_to_human", False),
                "suggested_actions": validated_response.get("suggested_actions", []),
                "processing_time_seconds": processing_time,
                "provider_used": provider or self.default_provider,
                "tokens_used": llm_response.get("tokens_used", 0)
            }

        except Exception as e:
            logger.error(f"❌ Error generando respuesta: {str(e)}")
            return await self._fallback_response(user_message)

    async def _build_enhanced_prompt(
            self,
            user_message: str,
            relevant_docs: List[Dict[str, Any]],
            context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        📝 Construir prompt enriquecido con RAG
        """

        # Obtener template base
        base_prompt = self.prompt_templates.get_banking_assistant_prompt()

        # Agregar documentos relevantes
        knowledge_context = ""
        if relevant_docs:
            knowledge_context = "### Información Relevante:\n"
            for i, doc in enumerate(relevant_docs, 1):
                knowledge_context += f"{i}. {doc['content'][:200]}...\n"
                knowledge_context += f"   Fuente: {doc.get('source', 'KB')}\n\n"

        # Agregar contexto de sesión si existe
        session_context = ""
        if context and context.get("conversation_history"):
            session_context = "### Contexto de Conversación:\n"
            for msg in context["conversation_history"][-3:]:  # Últimos 3 mensajes
                role = "Usuario" if msg["role"] == "user" else "Asistente"
                session_context += f"{role}: {msg['content']}\n"

        # Construir prompt final
        enhanced_prompt = f"""
{base_prompt}

{knowledge_context}

{session_context}

### Pregunta del Usuario:
{user_message}

### Instrucciones:
- Responde ÚNICAMENTE basado en la información proporcionada
- Si no tienes información suficiente, di que necesitas más datos
- Para operaciones sensibles, solicita autenticación
- Mantén un tono profesional pero amigable
- Si detectas una consulta compleja, sugiere escalación a un agente humano
- SIEMPRE cita las fuentes de información cuando sea posible

### Respuesta:
"""

        return enhanced_prompt

    async def _call_llm(self, prompt: str, provider: str) -> Dict[str, Any]:
        """
        🔄 Llamar al proveedor de LLM especificado
        """

        try:
            if provider == "openai":
                response = await self.openai_provider.generate(
                    prompt=prompt,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            elif provider == "anthropic":
                response = await self.anthropic_provider.generate(
                    prompt=prompt,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            else:
                raise ValueError(f"Proveedor no soportado: {provider}")

            logger.info(f"✅ LLM response generado con {provider}")
            return response

        except Exception as e:
            logger.error(f"❌ Error llamando LLM {provider}: {str(e)}")
            raise

    async def _apply_guardrails(
            self,
            llm_response: Dict[str, Any],
            original_message: str
    ) -> Dict[str, Any]:
        """
        🛡️ Aplicar guardrails de seguridad y bancarios
        """

        response_text = llm_response.get("message", "")

        # 1. Verificar temas prohibidos
        for forbidden_topic in self.forbidden_topics:
            if forbidden_topic.lower() in original_message.lower():
                return {
                    "message": f"No puedo ayudarte con temas relacionados a {forbidden_topic}. Mi especialidad son los servicios bancarios. ¿Hay algo relacionado con tu cuenta que pueda ayudarte?",
                    "confidence": "low",
                    "escalate_to_human": True
                }

        # 2. Detectar si requiere autenticación
        auth_keywords = ["saldo", "transferir", "movimientos", "estado de cuenta", "bloquear"]
        requires_auth = any(keyword in original_message.lower() for keyword in auth_keywords)

        # 3. Detectar si debe escalar
        escalate_keywords = ["hablar con agente", "persona real", "no entiendo", "no funciona"]
        escalate_to_human = any(keyword in original_message.lower() for keyword in escalate_keywords)

        # 4. Sugerir acciones
        suggested_actions = []
        if "saldo" in original_message.lower():
            suggested_actions.append("check_balance")
        if "transferir" in original_message.lower():
            suggested_actions.append("transfer_money")
        if any(keyword in original_message.lower() for keyword in escalate_keywords):
            suggested_actions.append("create_ticket")

        # 5. Evaluar confianza
        confidence = "high"
        if len(response_text) < 20:
            confidence = "low"
        elif "no tengo información" in response_text.lower():
            confidence = "medium"

        return {
            "message": response_text,
            "confidence": confidence,
            "requires_auth": requires_auth,
            "escalate_to_human": escalate_to_human,
            "suggested_actions": suggested_actions
        }

    async def _fallback_response(self, user_message: str) -> Dict[str, Any]:
        """
        🆘 Respuesta de fallback cuando falla el LLM
        """

        return {
            "message": "Disculpa, estoy experimentando dificultades técnicas en este momento. ¿Te gustaría que te conecte con un agente humano para ayudarte mejor?",
            "confidence": "low",
            "sources": [],
            "requires_auth": False,
            "escalate_to_human": True,
            "suggested_actions": ["create_ticket", "transfer_agent"],
            "processing_time_seconds": 0.1,
            "provider_used": "fallback",
            "tokens_used": 0
        }

    async def get_available_providers(self) -> List[str]:
        """📋 Obtener proveedores disponibles"""

        available = []

        # Verificar OpenAI
        if await self.openai_provider.is_available():
            available.append("openai")

        # Verificar Anthropic
        if await self.anthropic_provider.is_available():
            available.append("anthropic")

        return available

    async def get_usage_stats(self) -> Dict[str, Any]:
        """📊 Obtener estadísticas de uso"""

        return {
            "openai_calls": self.openai_provider.call_count,
            "anthropic_calls": self.anthropic_provider.call_count,
            "total_tokens_used": (
                    self.openai_provider.total_tokens +
                    self.anthropic_provider.total_tokens
            ),
            "average_response_time": 1.2,  # Mock por ahora
            "success_rate": 0.95
        }