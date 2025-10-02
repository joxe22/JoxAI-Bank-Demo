# backend/app/services/chatbot_service.py

import spacy
from app.services.rag_service import RAGService

class ChatbotService:
    def __init__(self):
        # NLU con spaCy
        self.nlp = spacy.load("es_core_news_md")
        self.rag = RAGService()

        # Intent classifier (simplificado)
        self.intents = {
            "consulta_saldo": ["saldo", "cuánto tengo", "mi cuenta"],
            "transferencia": ["transferir", "enviar dinero", "pagar"],
            "bloquear_tarjeta": ["bloquear", "robo", "tarjeta perdida"],
            "prestamo": ["préstamo", "crédito", "financiamiento"]
        }

    async def process_message(self, message: str, user_id: str, session_id: str):
        """
        Procesa mensaje del usuario y genera respuesta

        Flujo:
        1. Intent classification
        2. NER (detectar PII para enmascarar)
        3. RAG retrieval
        4. Generate response
        5. Determinar si escalar a humano
        """
        # 1. NER para detectar datos sensibles
        doc = self.nlp(message)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        # Redaction de PII
        message_clean = self._redact_pii(message, entities)

        # 2. Detect intent
        intent = self._classify_intent(message_clean)

        # 3. RAG query
        if intent == "general_query":
            rag_result = await self.rag.query_knowledge(message_clean)
            response = rag_result["answer"]
            confidence = rag_result["confidence"]
            sources = rag_result["sources"]
        else:
            # Intent específico (consulta saldo, etc.)
            response, confidence = await self._handle_specific_intent(intent, entities)
            sources = []

        # 4. Determinar si escalar
        needs_escalation = confidence < 0.7 or intent == "complaint"

        return {
            "response": response,
            "intent": intent,
            "confidence": confidence,
            "sources": sources,
            "needs_escalation": needs_escalation,
            "entities": entities
        }

    def _classify_intent(self, message: str):
        """Intent classification simple con keywords"""
        message_lower = message.lower()

        for intent, keywords in self.intents.items():
            if any(kw in message_lower for kw in keywords):
                return intent

        return "general_query"

    def _redact_pii(self, text: str, entities: list):
        """Enmascara PII detectado por spaCy"""
        for ent_text, label in entities:
            if label in ["PER", "ORG", "LOC"]:  # Nombres, organizaciones, lugares
                text = text.replace(ent_text, "[REDACTED]")
        return text