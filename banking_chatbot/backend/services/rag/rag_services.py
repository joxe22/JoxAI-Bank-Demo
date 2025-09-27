"""
🔍 RAG Service - Retrieval-Augmented Generation
Ubicación: backend/services/rag/rag_service.py

Implementa el sistema RAG para buscar información relevante en la knowledge base
y proporcionar contexto enriquecido para el LLM.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

from .vector_store import VectorStore
from .document_processor import DocumentProcessor

logger = logging.getLogger(__name__)

class RAGService:
    """
    🔍 Servicio de Retrieval-Augmented Generation

    Responsabilidades:
    - Buscar documentos relevantes en vector store
    - Rankear resultados por relevancia
    - Filtrar por metadatos (productos, fechas, etc.)
    - Proporcionar contexto enriquecido al LLM
    """

    def __init__(self):
        """Inicializar servicio RAG"""

        self.vector_store = VectorStore()
        self.document_processor = DocumentProcessor()

        # Configuración de búsqueda
        self.default_top_k = 5
        self.similarity_threshold = 0.7
        self.max_context_length = 2000  # caracteres

        # Knowledge base simulada (en producción vendría de Qdrant)
        self.mock_knowledge_base = self._load_mock_knowledge()

        logger.info("🔍 RAG Service inicializado")

    def _load_mock_knowledge(self) -> List[Dict[str, Any]]:
        """
        📚 Cargar knowledge base simulada para desarrollo
        En producción esto vendría de Qdrant/vector DB
        """

        return [
            {
                "id": "kb_001",
                "content": "Las transferencias bancarias se pueden realizar las 24 horas del día, los 7 días de la semana a través de nuestra plataforma digital. El límite diario para transferencias es de $100,000 pesos para cuentas verificadas.",
                "title": "Transferencias Bancarias - Horarios y Límites",
                "category": "transferencias",
                "source": "Manual de Productos Bancarios",
                "confidence": 0.95,
                "last_updated": "2024-01-15"
            },
            {
                "id": "kb_002",
                "content": "Para consultar tu saldo puedes usar: 1) App móvil, 2) Cajeros automáticos, 3) Banca por internet, 4) Llamada telefónica al *224. La consulta es gratuita en todos los canales.",
                "title": "Consulta de Saldo - Canales Disponibles",
                "category": "saldos",
                "source": "Guía de Servicios Digitales",
                "confidence": 0.98,
                "last_updated": "2024-01-10"
            },
            {
                "id": "kb_003",
                "content": "Las tarjetas de crédito tienen diferentes tipos: Clásica (sin anualidad primer año), Gold (beneficios premium), Platinum (servicios exclusivos). Todas incluyen seguro de fraude 24/7.",
                "title": "Tipos de Tarjetas de Crédito",
                "category": "tarjetas",
                "source": "Catálogo de Productos 2024",
                "confidence": 0.92,
                "last_updated": "2024-01-20"
            },
            {
                "id": "kb_004",
                "content": "Los préstamos personales tienen tasas desde 15.9% anual, montos hasta $500,000, plazo hasta 48 meses. Requisitos: ingresos comprobables, no estar en buró negativo.",
                "title": "Préstamos Personales - Condiciones",
                "category": "prestamos",
                "source": "Manual de Crédito",
                "confidence": 0.90,
                "last_updated": "2024-01-18"
            },
            {
                "id": "kb_005",
                "content": "Para reportar fraude llama inmediatamente al 01-800-FRAUDE (24/7). Bloquea tu tarjeta desde la app. Nunca compartas tu NIP o claves por teléfono.",
                "title": "Reporte de Fraude - Procedimiento Emergencia",
                "category": "seguridad",
                "source": "Protocolo de Seguridad",
                "confidence": 0.99,
                "last_updated": "2024-01-12"
            },
            {
                "id": "kb_006",
                "content": "Las cuentas de ahorro ofrecen rendimientos desde 2.5% hasta 4.2% anual. Sin comisiones por manejo de cuenta. Retiros ilimitados sin penalización.",
                "title": "Cuentas de Ahorro - Beneficios y Rendimientos",
                "category": "ahorro",
                "source": "Folleto de Inversiones",
                "confidence": 0.93,
                "last_updated": "2024-01-14"
            }
        ]

    async def retrieve_relevant_documents(
            self,
            query: str,
            top_k: int = None,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        🔍 Buscar documentos relevantes para una consulta

        Args:
            query: Consulta del usuario
            top_k: Número máximo de documentos a retornar
            filters: Filtros por metadata (categoría, fecha, etc.)
        """

        top_k = top_k or self.default_top_k

        logger.info(f"🔍 Buscando documentos relevantes para: '{query[:50]}...'")

        try:
            # 1. Procesar consulta
            processed_query = await self._preprocess_query(query)

            # 2. Búsqueda semántica (simulada por ahora)
            candidates = await self._semantic_search(processed_query, self.mock_knowledge_base)

            # 3. Aplicar filtros si existen
            if filters:
                candidates = self._apply_filters(candidates, filters)

            # 4. Rankear por relevancia
            ranked_results = self._rank_results(candidates, processed_query)

            # 5. Tomar top_k resultados
            top_results = ranked_results[:top_k]

            # 6. Filtrar por threshold de similaridad
            filtered_results = [
                doc for doc in top_results
                if doc.get('similarity_score', 0) >= self.similarity_threshold
            ]

            logger.info(f"✅ Encontrados {len(filtered_results)} documentos relevantes")

            return filtered_results

        except Exception as e:
            logger.error(f"❌ Error en búsqueda RAG: {str(e)}")
            return []

    async def _preprocess_query(self, query: str) -> str:
        """
        📝 Preprocesar consulta para mejor búsqueda
        """

        # Normalizar texto
        processed = query.lower().strip()

        # Expandir sinónimos bancarios
        synonyms = {
            "plata": "dinero",
            "lana": "dinero",
            "varo": "dinero",
            "cuenta": "saldo",
            "tarjeta": "tarjeta de crédito",
            "préstamo": "crédito",
            "robo": "fraude",
            "estafa": "fraude"
        }

        for original, replacement in synonyms.items():
            processed = processed.replace(original, replacement)

        return processed

    async def _semantic_search(
            self,
            query: str,
            documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        🎯 Búsqueda semántica simulada
        En producción usaría embeddings y vector similarity
        """

        results = []
        query_words = set(query.split())

        for doc in documents:
            # Calcular similaridad básica por palabras comunes
            doc_words = set(doc['content'].lower().split())
            doc_title_words = set(doc['title'].lower().split())

            # Similaridad por contenido
            content_similarity = len(query_words.intersection(doc_words)) / len(query_words.union(doc_words))

            # Similaridad por título (más peso)
            title_similarity = len(query_words.intersection(doc_title_words)) / max(len(query_words.union(doc_title_words)), 1)

            # Boost por categoría exacta
            category_boost = 0.2 if any(word in doc['category'] for word in query_words) else 0

            # Score final
            final_score = (content_similarity * 0.6) + (title_similarity * 0.3) + category_boost

            if final_score > 0:
                doc_copy = doc.copy()
                doc_copy['similarity_score'] = final_score
                results.append(doc_copy)

        return results

    def _apply_filters(
            self,
            documents: List[Dict[str, Any]],
            filters: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        🔽 Aplicar filtros por metadata
        """

        filtered = documents.copy()

        # Filtro por categoría
        if 'category' in filters:
            filtered = [doc for doc in filtered if doc.get('category') == filters['category']]

        # Filtro por fecha (documentos recientes)
        if 'max_age_days' in filters:
            # Implementar filtrado por fecha
            pass

        # Filtro por confianza mínima
        if 'min_confidence' in filters:
            filtered = [doc for doc in filtered if doc.get('confidence', 0) >= filters['min_confidence']]

        return filtered

    def _rank_results(
            self,
            documents: List[Dict[str, Any]],
            query: str
    ) -> List[Dict[str, Any]]:
        """
        📊 Rankear resultados por relevancia
        """

        # Ordenar por similarity_score descendente
        ranked = sorted(
            documents,
            key=lambda x: x.get('similarity_score', 0),
            reverse=True
        )

        return ranked

    async def get_context_for_llm(
            self,
            query: str,
            max_length: int = None
    ) -> str:
        """
        📄 Obtener contexto formateado para el LLM
        """

        max_length = max_length or self.max_context_length

        # Buscar documentos relevantes
        relevant_docs = await self.retrieve_relevant_documents(query)

        if not relevant_docs:
            return "No se encontró información específica en la base de conocimientos."

        # Formatear contexto
        context_parts = []
        current_length = 0

        for i, doc in enumerate(relevant_docs, 1):
            doc_text = f"[Fuente {i}: {doc['title']}]\n{doc['content']}"

            if current_length + len(doc_text) > max_length:
                break

            context_parts.append(doc_text)
            current_length += len(doc_text)

        return "\n\n".join(context_parts)

    async def update_knowledge_base(
            self,
            documents: List[Dict[str, Any]]
    ) -> bool:
        """
        🔄 Actualizar base de conocimientos
        """

        try:
            # En producción: procesar y vectorizar documentos
            processed_docs = []

            for doc in documents:
                processed = await self.document_processor.process_document(doc)
                processed_docs.append(processed)

            # Guardar en vector store
            success = await self.vector_store.add_documents(processed_docs)

            if success:
                logger.info(f"✅ {len(processed_docs)} documentos actualizados en KB")

            return success

        except Exception as e:
            logger.error(f"❌ Error actualizando KB: {str(e)}")
            return False

    async def get_knowledge_stats(self) -> Dict[str, Any]:
        """
        📊 Obtener estadísticas de la knowledge base
        """

        return {
            "total_documents": len(self.mock_knowledge_base),
            "categories": list(set(doc['category'] for doc in self.mock_knowledge_base)),
            "last_update": "2024-01-20",
            "search_queries_today": 156,  # Mock
            "avg_relevance_score": 0.89,  # Mock
            "cache_hit_rate": 0.73  # Mock
        }