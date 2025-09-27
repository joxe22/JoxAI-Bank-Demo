"""
📄 Document Processor - Procesamiento de Documentos Bancarios
Ubicación: backend/services/rag/document_processor.py

Procesa y prepara documentos para indexación en el vector store.
Incluye chunking semántico, cleaning, y extracción de metadatos.
"""

import logging
from typing import List, Dict, Any, Optional
import re
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    📄 Procesador de documentos para RAG

    Responsabilidades:
    - Limpiar y normalizar texto
    - Chunking semántico inteligente
    - Extraer metadatos relevantes
    - Identificar entidades bancarias
    - Preparar para vectorización
    """

    def __init__(self):
        """Inicializar procesador"""

        # Configuración de chunking
        self.chunk_size = 500  # caracteres por chunk
        self.chunk_overlap = 50  # overlap entre chunks
        self.max_chunk_size = 1000

        # Patrones de limpieza
        self.cleanup_patterns = [
            (r'\s+', ' '),  # Espacios múltiples
            (r'\n+', '\n'),  # Saltos de línea múltiples
            (r'[^\w\s\.,;:!?()%-]', ''),  # Caracteres especiales
        ]

        # Entidades bancarias comunes
        self.banking_entities = {
            'productos': ['tarjeta', 'cuenta', 'préstamo', 'crédito', 'inversión'],
            'operaciones': ['transferencia', 'pago', 'retiro', 'depósito', 'consulta'],
            'canales': ['app', 'cajero', 'sucursal', 'internet', 'teléfono'],
            'documentos': ['estado', 'contrato', 'solicitud', 'comprobante']
        }

        logger.info("📄 Document Processor inicializado")

    async def process_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔄 Procesar documento completo

        Flujo:
        1. Limpiar texto
        2. Extraer metadatos
        3. Chunking semántico
        4. Identificar entidades
        5. Preparar para vectorización
        """

        try:
            logger.info(f"🔄 Procesando documento: {document.get('title', 'Sin título')}")

            # 1. Limpiar texto
            cleaned_content = await self._clean_text(document.get('content', ''))

            # 2. Extraer metadatos
            metadata = await self._extract_metadata(document)

            # 3. Chunking semántico
            chunks = await self._semantic_chunking(cleaned_content)

            # 4. Identificar entidades por chunk
            enriched_chunks = []
            for i, chunk in enumerate(chunks):
                entities = await self._extract_entities(chunk)

                enriched_chunk = {
                    'content': chunk,
                    'chunk_id': f"{document.get('id', 'unknown')}_{i}",
                    'entities': entities,
                    'metadata': metadata.copy(),
                    'processed_at': datetime.now().isoformat()
                }

                enriched_chunks.append(enriched_chunk)

            result = {
                'original_id': document.get('id'),
                'title': document.get('title', ''),
                'total_chunks': len(enriched_chunks),
                'chunks': enriched_chunks,
                'metadata': metadata,
                'processing_stats': {
                    'original_length': len(document.get('content', '')),
                    'cleaned_length': len(cleaned_content),
                    'chunks_created': len(enriched_chunks)
                }
            }

            logger.info(f"✅ Documento procesado: {len(enriched_chunks)} chunks creados")
            return result

        except Exception as e:
            logger.error(f"❌ Error procesando documento: {str(e)}")
            raise

    async def _clean_text(self, text: str) -> str:
        """
        🧹 Limpiar y normalizar texto
        """

        if not text:
            return ""

        # Aplicar patrones de limpieza
        cleaned = text
        for pattern, replacement in self.cleanup_patterns:
            cleaned = re.sub(pattern, replacement, cleaned)

        # Normalizar espacios
        cleaned = cleaned.strip()

        # Remover líneas vacías múltiples
        lines = [line.strip() for line in cleaned.split('\n')]
        cleaned = '\n'.join(line for line in lines if line)

        return cleaned

    async def _extract_metadata(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        📊 Extraer metadatos del documento
        """

        metadata = {
            'source': document.get('source', 'unknown'),
            'category': document.get('category', 'general'),
            'confidence': document.get('confidence', 1.0),
            'last_updated': document.get('last_updated', datetime.now().isoformat()),
            'language': 'es',  # Asumir español por defecto
            'document_type': self._infer_document_type(document),
            'priority': self._calculate_priority(document)
        }

        # Agregar metadatos adicionales si existen
        if 'metadata' in document:
            metadata.update(document['metadata'])

        return metadata

    def _infer_document_type(self, document: Dict[str, Any]) -> str:
        """
        🔍 Inferir tipo de documento basado en contenido y título
        """

        title = document.get('title', '').lower()
        content = document.get('content', '').lower()

        # Reglas de inferencia
        if any(word in title for word in ['manual', 'procedimiento', 'proceso']):
            return 'manual'
        elif any(word in title for word in ['tarjeta', 'crédito', 'débito']):
            return 'producto_tarjeta'
        elif any(word in title for word in ['cuenta', 'ahorro', 'corriente']):
            return 'producto_cuenta'
        elif any(word in title for word in ['préstamo', 'crédito', 'hipoteca']):
            return 'producto_credito'
        elif any(word in title for word in ['seguridad', 'fraude', 'robo']):
            return 'seguridad'
        elif 'faq' in title or 'pregunta' in title:
            return 'faq'
        else:
            return 'general'

    def _calculate_priority(self, document: Dict[str, Any]) -> float:
        """
        ⭐ Calcular prioridad del documento
        """

        base_priority = 0.5

        # Boost por confianza
        confidence = document.get('confidence', 1.0)
        confidence_boost = confidence * 0.3

        # Boost por tipo crítico
        critical_keywords = ['seguridad', 'fraude', 'emergencia', 'bloqueo']
        title_content = f"{document.get('title', '')} {document.get('content', '')}"
        critical_boost = 0.3 if any(kw in title_content.lower() for kw in critical_keywords) else 0

        # Penalty por antigüedad (documentos muy viejos)
        date_penalty = 0  # Implementar si se tiene fecha del documento

        final_priority = min(base_priority + confidence_boost + critical_boost - date_penalty, 1.0)
        return round(final_priority, 2)

    async def _semantic_chunking(self, text: str) -> List[str]:
        """
        ✂️ Chunking semántico del texto

        Intenta mantener coherencia semántica en cada chunk
        """

        if not text:
            return []

        # Dividir por párrafos primero
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = ""

        for paragraph in paragraphs:
            # Si el párrafo cabe en el chunk actual
            if len(current_chunk + paragraph) <= self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                # Guardar chunk actual si no está vacío
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Si el párrafo es muy largo, dividirlo por oraciones
                if len(paragraph) > self.max_chunk_size:
                    sentence_chunks = await self._split_by_sentences(paragraph)
                    chunks.extend(sentence_chunks)
                    current_chunk = ""
                else:
                    current_chunk = paragraph + "\n\n"

        # Agregar último chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Aplicar overlap si es necesario
        if self.chunk_overlap > 0:
            chunks = await self._apply_overlap(chunks)

        return chunks

    async def _split_by_sentences(self, text: str) -> List[str]:
        """
        📝 Dividir texto por oraciones manteniendo contexto
        """

        # Patrones para detectar fin de oración
        sentence_endings = r'[.!?]\s+'
        sentences = re.split(sentence_endings, text)

        chunks = []
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Agregar punto si no termina con puntuación
            if not sentence[-1] in '.!?':
                sentence += '.'

            if len(current_chunk + sentence) <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return chunks

    async def _apply_overlap(self, chunks: List[str]) -> List[str]:
        """
        🔗 Aplicar overlap entre chunks para mantener contexto
        """

        if len(chunks) <= 1:
            return chunks

        overlapped_chunks = [chunks[0]]  # Primer chunk sin cambios

        for i in range(1, len(chunks)):
            previous_chunk = chunks[i-1]
            current_chunk = chunks[i]

            # Tomar últimas palabras del chunk anterior
            prev_words = previous_chunk.split()
            overlap_words = prev_words[-self.chunk_overlap:] if len(prev_words) > self.chunk_overlap else prev_words
            overlap_text = " ".join(overlap_words)

            # Combinar con chunk actual
            overlapped_chunk = f"{overlap_text} [...] {current_chunk}"
            overlapped_chunks.append(overlapped_chunk)

        return overlapped_chunks

    async def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        🏷️ Extraer entidades bancarias del texto
        """

        entities = {}
        text_lower = text.lower()

        # Buscar entidades por categoría
        for category, entity_list in self.banking_entities.items():
            found_entities = []

            for entity in entity_list:
                if entity in text_lower:
                    found_entities.append(entity)

            if found_entities:
                entities[category] = found_entities

        # Extraer números (montos, cuentas, etc.) - básico
        numbers = re.findall(r'\$?[\d,]+\.?\d*', text)
        if numbers:
            entities['numeros'] = numbers

        # Extraer porcentajes
        percentages = re.findall(r'\d+\.?\d*%', text)
        if percentages:
            entities['porcentajes'] = percentages

        return entities

    async def process_pdf_document(self, file_path: str) -> Dict[str, Any]:
        """
        📑 Procesar documento PDF específicamente
        """

        try:
            # En producción: usar PyPDF2 o similar
            """
            import PyPDF2
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            """

            # Mock para desarrollo
            mock_text = f"Contenido simulado del PDF: {file_path}"

            document = {
                'id': f"pdf_{hash(file_path)}",
                'title': file_path.split('/')[-1],
                'content': mock_text,
                'source': 'pdf_upload',
                'category': 'documento'
            }

            return await self.process_document(document)

        except Exception as e:
            logger.error(f"❌ Error procesando PDF {file_path}: {str(e)}")
            raise

    async def batch_process_documents(
            self,
            documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        📦 Procesar múltiples documentos en lote
        """

        processed_documents = []
        failed_count = 0

        for i, document in enumerate(documents):
            try:
                processed = await self.process_document(document)
                processed_documents.append(processed)

                if (i + 1) % 10 == 0:
                    logger.info(f"📦 Procesados {i + 1}/{len(documents)} documentos")

            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Error procesando documento {i}: {str(e)}")
                continue

        logger.info(
            f"✅ Procesamiento en lote completado: "
            f"{len(processed_documents)} exitosos, {failed_count} fallidos"
        )

        return processed_documents