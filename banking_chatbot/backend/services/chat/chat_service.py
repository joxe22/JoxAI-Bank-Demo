"""
🤖 Chat Service
Ubicación: backend/services/chat/chat_service.py

Servicio principal que orquesta la lógica del chatbot.
ACTUALIZADO: Ahora integra RAG + LLM real en lugar de respuestas hardcodeadas.
"""

import asyncio
import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

# Importar servicios LLM y RAG
try:
    from ..llm.llm_service import LLMService
    from ..rag.rag_service import RAGService
except ImportError:
    # Fallback si no se pueden importar (para evitar errores de desarrollo)
    LLMService = None
    RAGService = None

logger = logging.getLogger(__name__)

class ChatService:
    """
    🤖 Servicio principal del chatbot con IA real

    ACTUALIZADO para usar:
    - LLM real (OpenAI/Anthropic) en lugar de respuestas hardcodeadas
    - RAG para búsqueda semántica en knowledge base
    - Prompt templates especializados en banking
    - Guardrails de seguridad avanzados
    """

    def __init__(self):
        """Inicializar el servicio con IA real"""

        # Servicios de IA (con fallback si no disponibles)
        try:
            self.llm_service = LLMService() if LLMService else None
            self.rag_service = RAGService() if RAGService else None
            logger.info("✅ Servicios LLM y RAG inicializados")
        except Exception as e:
            logger.warning(f"⚠️ No se pudieron inicializar servicios IA: {e}")
            self.llm_service = None
            self.rag_service = None

        # Configuración
        self.use_ai = True if self.llm_service else False
        self.fallback_to_mock = True

        # Knowledge base básica (para fallback)
        self.banking_knowledge = self._load_banking_knowledge()
        self.common_responses = self._load_common_responses()

        # Métricas
        self.ai_calls = 0
        self.fallback_calls = 0
        self.total_processing_time = 0.0

        logger.info(f"🤖 Chat Service inicializado - IA: {self.use_ai}, Fallback: {self.fallback_to_mock}")

    async def process_message(
            self,
            message: str,
            session_id: str,
            user_id: Optional[str] = None,
            context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🔄 Procesar mensaje con IA real

        Flujo actualizado:
        1. Intentar respuesta con LLM + RAG
        2. Si falla, usar fallback inteligente
        3. Aplicar post-procesamiento
        4. Retornar respuesta enriquecida
        """

        start_time = datetime.now()
        logger.info(f"🔄 Procesando mensaje: {message[:50]}...")

        try:
            # Intentar respuesta con IA real
            if self.use_ai and self.llm_service:
                ai_response = await self._process_with_ai(
                    message=message,
                    session_id=session_id,
                    user_id=user_id,
                    context=context
                )

                if ai_response:
                    self.ai_calls += 1
                    processing_time = (datetime.now() - start_time).total_seconds()
                    self.total_processing_time += processing_time

                    return self._enrich_response(ai_response, processing_time)

            # Fallback si IA no disponible o falla
            logger.info("🔄 Usando fallback - IA no disponible o falló")
            fallback_response = await self._process_with_fallback(
                message, session_id, user_id, context
            )

            self.fallback_calls += 1
            processing_time = (datetime.now() - start_time).total_seconds()

            return self._enrich_response(fallback_response, processing_time, is_fallback=True)

        except Exception as e:
            logger.error(f"❌ Error procesando mensaje: {str(e)}")
            return await self._emergency_fallback(message, session_id)

    async def _process_with_ai(
            self,
            message: str,
            session_id: str,
            user_id: Optional[str] = None,
            context: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        🧠 Procesar mensaje con LLM + RAG
        """

        try:
            logger.info("🧠 Procesando con LLM + RAG...")

            # Preparar contexto enriquecido
            enhanced_context = await self._build_enhanced_context(
                message, session_id, user_id, context
            )

            # Llamar al LLM Service
            llm_response = await self.llm_service.generate_response(
                user_message=message,
                session_id=session_id,
                context=enhanced_context
            )

            if llm_response and llm_response.get('message'):
                logger.info("✅ Respuesta generada con IA")
                return llm_response

            return None

        except Exception as e:
            logger.error(f"❌ Error en procesamiento IA: {str(e)}")
            return None

    async def _build_enhanced_context(
            self,
            message: str,
            session_id: str,
            user_id: Optional[str] = None,
            context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🔍 Construir contexto enriquecido para el LLM
        """

        enhanced_context = context.copy() if context else {}

        # Agregar información de usuario
        enhanced_context.update({
            'user_id': user_id,
            'session_id': session_id,
            'timestamp': datetime.now().isoformat(),
            'user_type': 'authenticated' if user_id else 'anonymous'
        })

        # Agregar contexto conversacional básico
        enhanced_context['conversation_history'] = context.get('conversation_history', []) if context else []

        # Detectar contexto especial
        message_lower = message.lower()

        # Contexto de urgencia
        urgent_keywords = ['urgente', 'emergencia', 'robo', 'fraude', 'bloquear']
        if any(keyword in message_lower for keyword in urgent_keywords):
            enhanced_context['urgency_level'] = 'high'
            enhanced_context['priority'] = 'critical'

        # Contexto de autenticación necesaria
        auth_keywords = ['saldo', 'transferir', 'movimientos', 'cuenta']
        if any(keyword in message_lower for keyword in auth_keywords):
            enhanced_context['requires_auth'] = True

        # Contexto temporal
        current_hour = datetime.now().hour
        if current_hour < 6 or current_hour > 22:
            enhanced_context['after_hours'] = True

        return enhanced_context

    async def _process_with_fallback(
            self,
            message: str,
            session_id: str,
            user_id: Optional[str] = None,
            context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        🆘 Procesar con sistema de fallback mejorado
        """

        logger.info("🆘 Procesando con fallback inteligente...")

        # 1. Detectar intención básica
        intent, confidence = await self._detect_intent_enhanced(message)
        logger.info(f"🎯 Intención detectada: {intent} (confianza: {confidence:.2f})")

        # 2. Buscar en knowledge base local
        local_knowledge = await self._search_local_knowledge(message, intent)

        # 3. Generar respuesta inteligente
        response_text = await self._generate_fallback_response(
            intent, local_knowledge, message, confidence, context
        )

        # 4. Determinar acciones y metadata
        suggested_actions = self._get_suggested_actions_enhanced(intent, message)
        requires_auth = self._requires_authentication_enhanced(intent, message)
        escalate = self._should_escalate_enhanced(intent, confidence, context)

        return {
            "message": response_text,
            "confidence": self._determine_confidence_level(confidence),
            "confidence_score": confidence,
            "sources": local_knowledge.get("sources", []),
            "suggested_actions": suggested_actions,
            "requires_auth": requires_auth,
            "escalate_to_human": escalate,
            "metadata": {
                "intent": intent,
                "processing_method": "fallback",
                "local_knowledge_used": len(local_knowledge.get("sources", [])) > 0
            }
        }

    async def _detect_intent_enhanced(self, message: str) -> tuple[str, float]:
        """
        🎯 Detección de intención mejorada
        """

        message_lower = message.lower()

        # Patrones más sofisticados
        intent_patterns = {
            "greeting": {
                "patterns": ["hola", "buenos días", "buenas tardes", "hi", "hello", "saludos"],
                "boost": 0.1
            },
            "saldo": {
                "patterns": ["saldo", "balance", "cuanto tengo", "dinero disponible", "cuenta"],
                "context_words": ["consultar", "ver", "revisar", "mostrar"],
                "boost": 0.2
            },
            "transferir": {
                "patterns": ["transferir", "enviar dinero", "transferencia", "mandar plata", "enviar"],
                "context_words": ["hacer", "realizar", "quiero", "necesito"],
                "boost": 0.2
            },
            "tarjeta": {
                "patterns": ["tarjeta", "card", "crédito", "débito", "visa", "mastercard"],
                "context_words": ["información", "solicitar", "bloquear", "activar", "límite"],
                "boost": 0.1
            },
            "fraude_emergencia": {
                "patterns": ["robo", "fraude", "estafa", "bloquear", "urgente", "emergencia", "robaron"],
                "boost": 0.3  # Mayor boost por importancia
            },
            "prestamo": {
                "patterns": ["préstamo", "prestamo", "loan", "financiamiento", "crédito", "hipoteca"],
                "context_words": ["solicitar", "información", "requisitos", "tasa"],
                "boost": 0.1
            },
            "horarios": {
                "patterns": ["horarios", "horas", "atención", "abierto", "cerrado", "horario"],
                "context_words": ["cuando", "que", "funcionan"],
                "boost": 0.1
            },
            "ayuda": {
                "patterns": ["ayuda", "help", "no entiendo", "que puedes hacer", "opciones", "menú"],
                "boost": 0.1
            },
            "despedida": {
                "patterns": ["adiós", "chao", "gracias", "bye", "hasta luego", "nos vemos"],
                "boost": 0.1
            }
        }

        best_intent = "unknown"
        best_confidence = 0.0

        for intent, config in intent_patterns.items():
            confidence = 0.0
            patterns = config["patterns"]

            # Buscar patrones principales
            pattern_matches = sum(1 for pattern in patterns if pattern in message_lower)
            if pattern_matches > 0:
                confidence = 0.6 + (pattern_matches * 0.1)

                # Boost por palabras de contexto
                if "context_words" in config:
                    context_matches = sum(1 for word in config["context_words"] if word in message_lower)
                    confidence += context_matches * 0.05

                # Boost específico del intent
                confidence += config.get("boost", 0)

                # Penalty por longitud (mensajes muy largos son menos específicos)
                if len(message.split()) > 10:
                    confidence *= 0.9

                if confidence > best_confidence:
                    best_confidence = confidence
                    best_intent = intent

        # Cap confidence at 1.0
        best_confidence = min(best_confidence, 1.0)

        return best_intent, best_confidence

    async def _search_local_knowledge(self, message: str, intent: str) -> Dict[str, Any]:
        """
        🔍 Buscar en knowledge base local (fallback de RAG)
        """

        sources = []

        # Buscar por intent específico
        if intent in self.banking_knowledge:
            knowledge = self.banking_knowledge[intent]
            sources.append({
                "title": f"Información sobre {intent}",
                "content": knowledge.get("info", ""),
                "confidence": 0.8,
                "source": "knowledge_base_local"
            })

        # Búsqueda por palabras clave si no hay match directo
        if not sources:
            message_words = message.lower().split()
            for kb_intent, kb_data in self.banking_knowledge.items():
                kb_content = kb_data.get("info", "").lower()
                matches = sum(1 for word in message_words if word in kb_content)

                if matches >= 2:  # Al menos 2 palabras coincidentes
                    sources.append({
                        "title": f"Información relacionada: {kb_intent}",
                        "content": kb_data.get("info", ""),
                        "confidence": 0.6 + (matches * 0.05),
                        "source": "knowledge_base_local"
                    })

        return {"sources": sources}

    async def _generate_fallback_response(
            self,
            intent: str,
            local_knowledge: Dict[str, Any],
            original_message: str,
            confidence: float,
            context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        🗣️ Generar respuesta de fallback más inteligente
        """

        # Si hay knowledge local disponible, usarlo
        sources = local_knowledge.get("sources", [])
        if sources and confidence > 0.6:
            primary_source = sources[0]
            base_response = primary_source["content"]

            # Personalizar respuesta según contexto
            if context and context.get("urgency_level") == "high":
                base_response = f"🚨 Entiendo que es urgente. {base_response}"

            return base_response

        # Respuestas por intent (mejoradas)
        enhanced_responses = {
            "greeting": [
                "¡Hola! 👋 Soy tu asistente bancario JovAI. Estoy aquí para ayudarte con todas tus consultas bancarias. ¿En qué puedo asistirte hoy?",
                "¡Buen día! 😊 Soy JovAI, tu asistente virtual bancario. ¿Cómo puedo ayudarte con tus servicios bancarios?",
                "¡Hola! Me da mucho gusto atenderte. Soy JovAI y estoy aquí para resolver tus dudas bancarias. ¿Qué necesitas?"
            ],

            "saldo": [
                "Para consultar tu saldo de forma segura, necesito verificar tu identidad. Una vez autenticado, podrás ver tu saldo actual, movimientos recientes y más detalles de tu cuenta. ¿Procedo con la verificación?",
                "Claro, te ayudo a consultar tu saldo. Por seguridad bancaria, necesito que te autentiques primero. ¿Tienes a la mano tu documento y teléfono registrado?"
            ],

            "transferir": [
                "Te guío para realizar tu transferencia de forma segura. Primero necesito verificar tu identidad, luego te explico el proceso paso a paso. Las transferencias están disponibles 24/7 con diferentes límites según el canal.",
                "¡Por supuesto! Te ayudo con tu transferencia. Para tu seguridad, primero verificaré tu identidad y luego te guío en todo el proceso. ¿Es una transferencia a otra cuenta del mismo banco o externa?"
            ],

            "fraude_emergencia": [
                "🚨 ALERTA DE SEGURIDAD: Si sospechas fraude, actúa inmediatamente:\n\n1️⃣ Bloquea tu tarjeta desde la app\n2️⃣ Llama al 01-800-FRAUDE (24/7)\n3️⃣ No compartas claves por teléfono\n4️⃣ Reporta movimientos sospechosos\n\n¿Necesitas ayuda inmediata?",
                "🚨 Situación de emergencia detectada. Tu seguridad es nuestra prioridad. Te conectaré inmediatamente con nuestro equipo especializado en fraude. Mientras tanto, bloquea cualquier tarjeta comprometida desde la app."
            ],

            "tarjeta": [
                "Te explico sobre nuestras tarjetas de crédito y débito. Tenemos diferentes opciones con beneficios únicos: desde tarjetas sin anualidad hasta productos premium con cashback y seguros incluidos. ¿Buscas una tarjeta específica o quieres conocer todas las opciones?",
                "¡Excelente! Nuestras tarjetas ofrecen grandes beneficios. ¿Te interesa una tarjeta de crédito para compras y cashback, o una de débito para uso diario? También tengo información sobre bloqueos, activaciones y más."
            ],

            "prestamo": [
                "Te ayudo con información sobre préstamos. Ofrecemos: préstamos personales (desde 15.9% anual), créditos hipotecarios, y financiamiento automotriz. Cada uno tiene requisitos y beneficios específicos. ¿Qué tipo de préstamo te interesa?",
                "Claro, hablemos de préstamos. Tenemos opciones flexibles con tasas competitivas y procesos ágiles. ¿Es para un proyecto personal, compra de casa, auto, o algo específico? Así te doy información más precisa."
            ],

            "horarios": [
                "Nuestros horarios de atención son:\n🏦 **Sucursales**: Lunes a Viernes 8:00 AM - 6:00 PM, Sábados 9:00 AM - 2:00 PM\n📱 **Banca Digital**: 24/7 disponible\n📞 **Atención Telefónica**: 24/7 al *224\n🏧 **Cajeros**: Disponibles las 24 horas\n\n¿Necesitas algo específico?",
                "Te comparto los horarios:\n• Sucursales: L-V 8:00-18:00, Sábados 9:00-14:00\n• App y Banca Online: 24/7\n• Centro de Atención: 24 horas\n• Cajeros automáticos: Siempre disponibles\n\n¿En qué más puedo ayudarte?"
            ],

            "ayuda": [
                "¡Por supuesto! Te ayudo con:\n\n🏦 **Consultas bancarias**: saldos, movimientos, estados de cuenta\n💳 **Tarjetas**: información, bloqueos, activaciones\n💰 **Préstamos**: tipos, requisitos, tasas\n🔄 **Transferencias**: nacionales e internacionales\n🔐 **Seguridad**: fraude, claves, protección\n\n¿Con cuál de estos temas te ayudo?",
                "Estoy aquí para ayudarte con todos tus servicios bancarios. Puedo resolver dudas sobre productos, procesos, seguridad, y mucho más. Si algo es muy específico, te conectaré con un especialista humano. ¿Qué necesitas saber?"
            ],

            "despedida": [
                "¡Gracias por contactarnos! Ha sido un placer ayudarte. Si necesitas más información, no dudes en escribirme cuando quieras. ¡Que tengas un excelente día! 😊",
                "¡Excelente! Me alegra haber podido ayudarte. Recuerda que estoy disponible 24/7 para cualquier consulta bancaria. ¡Cuídate mucho! 👋",
                "¡Perfecto! Espero haber resuelto tu consulta. Siempre estoy aquí para ayudarte con tus servicios bancarios. ¡Hasta pronto! ✨"
            ]
        }

        if intent in enhanced_responses:
            responses = enhanced_responses[intent]
            selected = random.choice(responses)

            # Personalizar según hora del día
            current_hour = datetime.now().hour
            if intent == "greeting":
                if current_hour < 12:
                    selected = selected.replace("¡Hola!", "¡Buenos días!").replace("¡Buen día!", "¡Buenos días!")
                elif current_hour < 18:
                    selected = selected.replace("¡Hola!", "¡Buenas tardes!").replace("¡Buen día!", "¡Buenas tardes!")
                else:
                    selected = selected.replace("¡Hola!", "¡Buenas noches!").replace("¡Buen día!", "¡Buenas noches!")

            return selected

        # Fallback genérico mejorado
        return f"Entiendo que preguntas sobre {intent if intent != 'unknown' else 'servicios bancarios'}. Aunque no tengo información específica en este momento, puedo conectarte con un especialista que te dará una respuesta completa. ¿Te parece bien que programe esa conexión?"

    def _get_suggested_actions_enhanced(self, intent: str, message: str) -> List[str]:
        """💡 Obtener acciones sugeridas mejoradas"""

        message_lower = message.lower()

        # Mapeo mejorado de acciones
        action_mapping = {
            "saldo": ["check_balance", "view_transactions", "download_statement"],
            "transferir": ["transfer_money", "check_balance"],
            "tarjeta": ["card_info", "block_card", "activate_card"],
            "prestamo": ["loan_info", "apply_loan", "calculate_payment"],
            "fraude_emergencia": ["block_card", "report_fraud", "transfer_agent"],
            "horarios": ["show_locations", "contact_info"],
            "ayuda": ["show_menu", "transfer_agent"],
            "unknown": ["create_ticket", "transfer_agent", "show_menu"]
        }

        base_actions = action_mapping.get(intent, ["send_message"])

        # Acciones adicionales basadas en palabras clave
        additional_actions = []

        if any(word in message_lower for word in ["urgente", "rápido", "ya"]):
            additional_actions.append("escalate_priority")

        if any(word in message_lower for word in ["agente", "persona", "humano"]):
            additional_actions.append("transfer_agent")

        if any(word in message_lower for word in ["email", "correo", "enviar"]):
            additional_actions.append("send_email")

        return list(set(base_actions + additional_actions))

    def _requires_authentication_enhanced(self, intent: str, message: str) -> bool:
        """🔐 Verificar autenticación con lógica mejorada"""

        # Intents que siempre requieren auth
        auth_required_intents = {
            "saldo", "transferir", "movimientos", "bloquear_tarjeta",
            "estado_cuenta", "cambiar_limite", "solicitar_credito"
        }

        if intent in auth_required_intents:
            return True

        # Palabras que indican necesidad de auth
        auth_keywords = [
            "mi saldo", "mi cuenta", "mis movimientos", "transferir",
            "bloquear", "límite", "estado de cuenta", "mi dinero"
        ]

        message_lower = message.lower()
        return any(keyword in message_lower for keyword in auth_keywords)

    def _should_escalate_enhanced(
            self,
            intent: str,
            confidence: float,
            context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """👥 Determinar si debe escalarse a humano"""

        # Escalación por confianza baja
        if confidence < 0.3:
            return True

        # Intents que siempre escalan
        escalation_intents = {"fraude_emergencia", "complex_complaint", "legal_issue"}
        if intent in escalation_intents:
            return True

        # Escalación por contexto
        if context:
            if context.get("urgency_level") == "high":
                return True

            if context.get("conversation_count", 0) > 5:  # Conversación muy larga
                return True

            if context.get("user_frustrated", False):
                return True

        return False

    def _enrich_response(
            self,
            response: Dict[str, Any],
            processing_time: float,
            is_fallback: bool = False
    ) -> Dict[str, Any]:
        """
        ✨ Enriquecer respuesta con metadata adicional
        """

        enriched = response.copy()

        # Agregar métricas de procesamiento
        enriched["processing_time_ms"] = int(processing_time * 1000)
        enriched["timestamp"] = datetime.now().isoformat()

        # Inicializar metadata si no existe
        if "metadata" not in enriched:
            enriched["metadata"] = {}

        # Agregar información sobre el método usado
        if is_fallback:
            enriched["metadata"]["ai_available"] = False
            enriched["metadata"]["response_quality"] = "fallback"
        else:
            enriched["metadata"]["ai_available"] = True
            enriched["metadata"]["response_quality"] = "ai_generated"

        # Agregar sugerencias de seguimiento si corresponde
        if enriched.get("confidence") == "low":
            enriched["follow_up_suggestions"] = [
                "¿Podrías ser más específico?",
                "¿Te gustaría hablar con un especialista?",
                "¿Hay algo más en lo que pueda ayudarte?"
            ]

        return enriched

    async def _emergency_fallback(self, message: str, session_id: str) -> Dict[str, Any]:
        """
        🆘 Fallback de emergencia cuando todo falla
        """

        return {
            "message": "Disculpa, estoy experimentando dificultades técnicas. Te conectaré inmediatamente con un agente humano para asistirte mejor. Tu consulta es importante para nosotros.",
            "confidence": "low",
            "confidence_score": 0.1,
            "sources": [],
            "suggested_actions": ["transfer_agent", "create_ticket"],
            "requires_auth": False,
            "escalate_to_human": True,
            "processing_time_ms": 100,
            "metadata": {
                "intent": "emergency_fallback",
                "processing_method": "emergency",
                "ai_available": False,
                "system_error": True
            }
        }

    # Métodos heredados del sistema original (para compatibilidad)
    def _load_banking_knowledge(self) -> Dict[str, Any]:
        """📚 Knowledge base local para fallback"""
        return {
            "saldo": {
                "info": "Para consultar tu saldo, necesito verificar tu identidad. Una vez autenticado, podrás ver tu saldo actual, movimientos y más detalles de tu cuenta.",
                "requires_auth": True
            },
            "transferir": {
                "info": "Las transferencias se pueden realizar 24/7 a través de nuestra app móvil o banca en línea. Te guío paso a paso una vez que verifiques tu identidad.",
                "requires_auth": True
            },
            "tarjeta": {
                "info": "Ofrecemos tarjetas de crédito y débito con diferentes beneficios: Clásica, Gold y Platinum. Cada una con ventajas específicas y seguros incluidos."
            },
            "prestamo": {
                "info": "Préstamos disponibles: Personales (desde 15.9%), Hipotecarios (desde 8.9%), y Automotriz (desde 12.5%). Requisitos y condiciones varían por producto."
            },
            "fraude_emergencia": {
                "info": "🚨 EMERGENCIA: Bloquea inmediatamente tu tarjeta desde la app o llama al 01-800-FRAUDE. Nunca compartas claves por teléfono.",
                "requires_auth": False,
                "priority": "critical"
            },
            "horarios": {
                "info": "Horarios: Sucursales L-V 8:00-18:00, Sáb 9:00-14:00. Banca digital y cajeros 24/7. Centro de atención telefónica 24 horas."
            }
        }

    def _load_common_responses(self) -> Dict[str, List[str]]:
        """💬 Respuestas comunes de fallback"""
        return {
            "greeting": [
                "¡Hola! Soy JovAI, tu asistente bancario inteligente. ¿En qué puedo ayudarte hoy?",
                "¡Buen día! Estoy aquí para resolver tus consultas bancarias. ¿Qué necesitas?",
                "¡Hola! ¿Cómo puedo asistirte con tus servicios bancarios?"
            ],
            "fallback": [
                "No tengo información específica sobre eso, pero puedo conectarte con un especialista que sí puede ayudarte.",
                "Esa consulta requiere atención personalizada. ¿Te conecto con un agente especializado?",
                "Para darte la mejor respuesta, necesito derivarte con nuestro equipo experto. ¿Procedo?"
            ],
            "auth_required": [
                "Por tu seguridad, necesito verificar tu identidad antes de mostrar información personal.",
                "Para proteger tus datos, debo autenticarte primero. ¿Tienes tu documento a la mano?",
                "Por regulaciones bancarias, requiero verificación de identidad para continuar."
            ]
        }

    def _determine_confidence_level(self, confidence_score: float) -> str:
        """📊 Determinar nivel de confianza categórico"""
        if confidence_score >= 0.8:
            return "high"
        elif confidence_score >= 0.5:
            return "medium"
        else:
            return "low"

    # Métodos de compatibilidad (simplificados)
    def _get_suggested_actions(self, intent: str) -> List[str]:
        """💡 Versión simple de acciones sugeridas"""
        return self._get_suggested_actions_enhanced(intent, "")

    def _requires_authentication(self, intent: str) -> bool:
        """🔐 Versión simple de verificación de auth"""
        return intent in ["saldo", "transferir", "movimientos", "bloquear_tarjeta"]

    async def get_analytics(self) -> Dict[str, Any]:
        """
        📊 Analytics del chatbot con métricas de IA
        """

        total_calls = self.ai_calls + self.fallback_calls
        ai_success_rate = (self.ai_calls / total_calls) if total_calls > 0 else 0
        avg_processing_time = (self.total_processing_time / total_calls) if total_calls > 0 else 0

        return {
            "active_sessions": random.randint(15, 50),
            "total_messages_today": random.randint(500, 2000),
            "avg_response_time": avg_processing_time,
            "satisfaction_score": random.uniform(4.2, 4.8),
            "resolution_rate": random.uniform(0.85, 0.95),
            "ai_metrics": {
                "ai_calls": self.ai_calls,
                "fallback_calls": self.fallback_calls,
                "ai_success_rate": ai_success_rate,
                "llm_providers_available": [],  # Se llena dinámicamente
                "avg_confidence": 0.82,  # Mock
                "rag_hits": random.randint(200, 800)
            },
            "top_intents": [
                {"intent": "saldo", "count": random.randint(100, 300)},
                {"intent": "transferir", "count": random.randint(80, 200)},
                {"intent": "tarjeta", "count": random.randint(50, 150)},
                {"intent": "prestamo", "count": random.randint(30, 100)},
                {"intent": "fraude_emergencia", "count": random.randint(5, 25)}
            ]
        }

    async def toggle_ai_mode(self, enable_ai: bool = True) -> Dict[str, str]:
        """
        🔄 Alternar entre modo IA y fallback
        """

        self.use_ai = enable_ai

        if enable_ai:
            if self.llm_service:
                # Verificar disponibilidad de proveedores LLM
                try:
                    available_providers = await self.llm_service.get_available_providers()

                    if available_providers:
                        logger.info(f"✅ Modo IA activado. Proveedores: {available_providers}")
                        return {
                            "status": "ai_enabled",
                            "message": f"Modo IA activado con {len(available_providers)} proveedores disponibles",
                            "providers": str(available_providers)
                        }
                    else:
                        logger.warning("⚠️ No hay proveedores LLM disponibles, usando fallback")
                        self.use_ai = False
                        return {
                            "status": "fallback_forced",
                            "message": "No hay proveedores LLM disponibles, usando modo fallback",
                            "providers": "none"
                        }
                except Exception as e:
                    logger.error(f"❌ Error verificando proveedores: {e}")
                    self.use_ai = False
                    return {
                        "status": "error",
                        "message": f"Error verificando proveedores IA: {str(e)}",
                        "providers": "error"
                    }
            else:
                logger.warning("⚠️ LLM Service no disponible, usando fallback")
                self.use_ai = False
                return {
                    "status": "service_unavailable",
                    "message": "Servicio LLM no disponible, usando modo fallback",
                    "providers": "unavailable"
                }
        else:
            logger.info("🔄 Modo fallback activado manualmente")
            return {
                "status": "fallback_enabled",
                "message": "Modo fallback activado. Usando respuestas predeterminadas",
                "providers": "disabled"
            }

    async def get_service_health(self) -> Dict[str, Any]:
        """
        🏥 Health check del servicio completo
        """

        health_status = {
            "chat_service": "healthy",
            "ai_mode_enabled": self.use_ai,
            "total_processed": self.ai_calls + self.fallback_calls,
            "uptime": "operational",  # Mock
            "ai_calls": self.ai_calls,
            "fallback_calls": self.fallback_calls
        }

        # Verificar salud de servicios IA
        if self.use_ai and self.llm_service:
            try:
                # Health check LLM Service
                llm_providers = await self.llm_service.get_available_providers()
                health_status["llm_service"] = {
                    "status": "healthy" if llm_providers else "degraded",
                    "available_providers": llm_providers
                }

                # Health check RAG Service
                if self.rag_service:
                    rag_stats = await self.rag_service.get_knowledge_stats()
                    health_status["rag_service"] = {
                        "status": "healthy",
                        "documents_indexed": rag_stats.get("total_documents", 0)
                    }
                else:
                    health_status["rag_service"] = {
                        "status": "unavailable",
                        "error": "RAG Service not initialized"
                    }

            except Exception as e:
                health_status["ai_services"] = {
                    "status": "error",
                    "error": str(e)
                }
        else:
            health_status["ai_services"] = {
                "status": "disabled",
                "message": "AI mode disabled or services unavailable"
            }

        return health_status

    # Métodos adicionales para compatibilidad y testing
    async def _detect_intent(self, message: str) -> tuple[str, float]:
        """🎯 Método de compatibilidad para detección de intención"""
        return await self._detect_intent_enhanced(message)

    async def _retrieve_information(self, intent: str, message: str) -> Dict[str, Any]:
        """🔍 Método de compatibilidad para búsqueda de información"""
        return await self._search_local_knowledge(message, intent)

    async def _generate_response(
            self,
            intent: str,
            relevant_info: Dict[str, Any],
            message: str,
            confidence: float
    ) -> str:
        """🗣️ Método de compatibilidad para generación de respuesta"""
        return await self._generate_fallback_response(intent, relevant_info, message, confidence, None)