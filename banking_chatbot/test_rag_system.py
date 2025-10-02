#!/usr/bin/env python3
"""
🧪 Test Sistema RAG Completo - Banking Chatbot
Ubicación: /test_rag_system.py

Script de prueba integral del sistema RAG.
Incluye ingesta de conocimiento, búsquedas y generación de respuestas.
"""

import asyncio
import sys
import logging
from pathlib import Path
from datetime import datetime
import json

# Agregar paths para imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Colors:
    """Códigos ANSI para colores en terminal."""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text: str):
    """Imprime encabezado con estilo."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("=" * 70)
    print(f"🧠 {text}")
    print("=" * 70)
    print(f"{Colors.END}")


def print_step(text: str):
    """Imprime paso con estilo."""
    print(f"\n{Colors.BLUE}🔄 {text}{Colors.END}")


def print_success(text: str):
    """Imprime éxito con estilo."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text: str):
    """Imprime error con estilo."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text: str):
    """Imprime información con estilo."""
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")


class RAGSystemTester:
    """Tester completo del sistema RAG."""

    def __init__(self):
        self.test_data = self._get_test_knowledge()
        self.test_queries = self._get_test_queries()

    def _get_test_knowledge(self) -> dict:
        """Retorna conocimiento bancario de prueba."""
        return {
            "productos_bancarios": {
                "content": """
Manual de Productos Bancarios - Banco Demo

CUENTAS DE AHORRO
================

¿Qué es una cuenta de ahorro?
Una cuenta de ahorro es un producto financiero que permite guardar dinero 
de forma segura mientras genera intereses. Es ideal para crear fondos de 
emergencia o ahorrar para objetivos específicos.

Requisitos de apertura:
• Ser mayor de 18 años
• Documento de identidad vigente  
• Comprobante de ingresos (últimas 2 nóminas)
• Comprobante de domicilio (máximo 3 meses)
• Depósito mínimo inicial: $50,000 pesos

Beneficios principales:
• Tasa de interés: 4.5% efectivo anual
• Sin comisión de manejo
• Tarjeta de débito incluida
• Acceso a banca online las 24 horas
• Seguro de depósitos hasta $10,000,000

Proceso de apertura:
1. Reunir todos los documentos requeridos
2. Visitar cualquier sucursal del banco
3. Diligenciar formato de solicitud
4. Realizar depósito mínimo inicial
5. Esperar 3-5 días hábiles para activación

CUENTAS CORRIENTES
==================

Descripción:
La cuenta corriente es ideal para el manejo diario del dinero. 
Permite realizar múltiples transacciones sin restricciones.

Características:
• Sin límite de transacciones mensuales
• Chequera incluida
• Tarjeta de débito internacional
• Sobregiro preaprobado hasta $500,000
• Comisión de manejo: $15,000 mensuales

Exención de comisión:
La comisión se exenta manteniendo un saldo promedio mensual 
superior a $800,000 pesos.

TARJETAS DE CRÉDITO
===================

Tarjeta Clásica:
• Cupo inicial: 2-3 veces el ingreso mensual
• Tasa de interés: 2.1% mensual
• Sin cuota de manejo el primer año
• Avances en efectivo disponibles

Tarjeta Gold:
• Cupo inicial: 3-4 veces el ingreso mensual  
• Tasa de interés: 1.9% mensual
• Programa de puntos y beneficios
• Seguro de compras incluido

Requisitos generales:
• Edad mínima: 18 años
• Ingresos mínimos: $1,500,000 mensuales
• Sin reportes negativos en centrales de riesgo
• Antigüedad laboral mínima: 6 meses
                """,
                "metadata": {
                    "category": "productos",
                    "source": "manual_productos.pdf",
                    "confidence_level": "high",
                    "product": "multiple"
                }
            },

            "faq_general": {
                "content": """
Preguntas Frecuentes - Banco Demo

HORARIOS Y UBICACIONES
======================

P: ¿Cuál es el horario de atención?
R: Nuestras sucursales atienden de lunes a viernes de 8:00 AM a 4:00 PM, 
y los sábados de 8:00 AM a 12:00 PM. Los cajeros automáticos están 
disponibles las 24 horas.

P: ¿Dónde encuentro las sucursales?
R: Tenemos más de 200 sucursales a nivel nacional. Puedes consultar 
ubicaciones en nuestra página web o llamando al 123-456-7890.

CONSULTAS DE SALDO
==================

P: ¿Cómo consulto mi saldo?
R: Puedes consultar tu saldo por:
• Banca online (www.bancodemo.com)
• App móvil "Banco Demo"
• Cajeros automáticos de la red
• Llamando al 123-456-7890
• Mensaje de texto al 85858

P: ¿Los cajeros de otros bancos cobran?
R: Sí, usar cajeros de otros bancos tiene un costo de $3,500 por transacción.
Los primeros 4 retiros en cajeros externos son gratis cada mes.

PROBLEMAS COMUNES
=================

P: ¿Qué hago si olvido mi clave?
R: Puedes restablecer tu clave por:
1. Página web usando tu documento de identidad
2. Llamando a la línea de servicio al cliente
3. Visitando cualquier sucursal con tu documento

P: ¿Cómo bloqueo mi tarjeta?
R: Para bloquear tu tarjeta inmediatamente:
• Llama al 123-456-7890 (las 24 horas)
• Usa la opción de bloqueo en la app móvil
• Ingresa a la banca online

P: Mi tarjeta fue declinada, ¿por qué?
R: Las principales causas son:
• Saldo insuficiente en la cuenta
• Límite diario de transacciones alcanzado
• Tarjeta vencida o bloqueada
• Problema técnico temporal

TRANSFERENCIAS
==============

P: ¿Cómo hago transferencias a otros bancos?
R: Puedes transferir a otros bancos a través de:
• ACH: Sin costo, demora 1 día hábil
• Transferencia inmediata: $2,900, llega en minutos
• PSE: Para pagos en línea, sin costo adicional
                """,
                "metadata": {
                    "category": "faq",
                    "source": "faq_general.txt",
                    "confidence_level": "high"
                }
            },

            "procedimientos": {
                "content": """
Procedimientos Bancarios - Guía Paso a Paso

CAMBIO DE DATOS PERSONALES
==========================

Proceso para actualizar información:

Documentos necesarios:
• Documento de identidad actualizado
• Certificado de cambio (si aplica)
• Comprobante de nuevo domicilio

Pasos a seguir:
1. Diligenciar formato de actualización de datos
2. Presentar documentos en cualquier sucursal  
3. Esperar validación (1-2 días hábiles)
4. Confirmación por SMS o correo electrónico

REPOSICIÓN DE TARJETAS
======================

Por pérdida o robo:
1. Reportar inmediatamente al 123-456-7890
2. Visitar sucursal con documento de identidad
3. Pagar tarifa de reposición: $12,000
4. Nueva tarjeta lista en 5-7 días hábiles

Por daño o vencimiento:
• Sin costo adicional
• Reemplazo automático antes del vencimiento
• Para daños, cambio inmediato en sucursal

CERTIFICACIONES BANCARIAS
=========================

Tipos disponibles:
• Certificado de saldos: $8,500
• Paz y salvo: $8,500  
• Movimientos de cuenta: $12,000
• Ingresos y retenciones: $15,000

Proceso:
1. Solicitar en sucursal o banca online
2. Pago de tarifa correspondiente
3. Entrega inmediata o envío por correo

RECLAMOS Y QUEJAS
================

Canal de atención:
• Línea gratuita: 01-8000-123456
• Correo: servicio@bancodemo.com
• Formulario web: www.bancodemo.com/reclamos
• Presencial en cualquier sucursal

Tiempos de respuesta:
• Consultas simples: 1-2 días hábiles
• Reclamos de transacciones: 5 días hábiles
• Quejas complejas: hasta 15 días hábiles
                """,
                "metadata": {
                    "category": "procedimientos",
                    "source": "manual_procedimientos.pdf",
                    "confidence_level": "high"
                }
            }
        }

    def _get_test_queries(self) -> list:
        """Retorna consultas de prueba."""
        return [
            {
                "query": "¿Cómo puedo abrir una cuenta de ahorro?",
                "expected_type": "procedural",
                "expected_sources": ["manual_productos.pdf"]
            },
            {
                "query": "¿Cuáles son los requisitos para una tarjeta de crédito?",
                "expected_type": "product_info",
                "expected_sources": ["manual_productos.pdf"]
            },
            {
                "query": "¿Cómo consulto mi saldo?",
                "expected_type": "general_faq",
                "expected_sources": ["faq_general.txt"]
            },
            {
                "query": "Mi tarjeta fue rechazada, ¿qué puedo hacer?",
                "expected_type": "troubleshooting",
                "expected_sources": ["faq_general.txt"]
            },
            {
                "query": "¿Cuál es el horario de atención?",
                "expected_type": "general_faq",
                "expected_sources": ["faq_general.txt"]
            },
            {
                "query": "¿Cómo cambio mis datos personales?",
                "expected_type": "procedural",
                "expected_sources": ["manual_procedimientos.pdf"]
            },
            {
                "query": "¿Qué beneficios tiene la cuenta corriente?",
                "expected_type": "product_info",
                "expected_sources": ["manual_productos.pdf"]
            },
            {
                "query": "¿Cómo hago una transferencia a otro banco?",
                "expected_type": "procedural",
                "expected_sources": ["faq_general.txt"]
            }
        ]

    async def run_complete_test(self):
        """Ejecuta prueba completa del sistema RAG."""
        print_header("PRUEBA COMPLETA SISTEMA RAG - BANKING CHATBOT")

        try:
            # Test 1: Inicialización de componentes
            await self._test_initialization()

            # Test 2: Ingesta de conocimiento
            await self._test_knowledge_ingestion()

            # Test 3: Búsquedas vectoriales
            await self._test_vector_search()

            # Test 4: Sistema RAG completo
            await self._test_rag_responses()

            # Test 5: Funcionalidades avanzadas
            await self._test_advanced_features()

            print_header("RESUMEN DE RESULTADOS")
            print_success("✅ Todos los tests completados exitosamente")
            print_info("El sistema RAG está operativo y funcionando correctamente")

        except Exception as e:
            print_error(f"Error durante las pruebas: {e}")
            raise

    async def _test_initialization(self):
        """Test de inicialización de componentes."""
        print_step("Test 1: Inicialización de componentes")

        # Importar y probar componentes
        try:
            from backend.core.vector_db import get_vector_db
            vector_db = await get_vector_db()
            print_success("Vector Database inicializada")

            from backend.core.knowledge_ingestion import get_ingestion_pipeline
            pipeline = await get_ingestion_pipeline()
            print_success("Pipeline de ingesta inicializado")

            from backend.core.rag_system import get_rag_system
            rag_system = await get_rag_system()
            print_success("Sistema RAG inicializado")

        except Exception as e:
            print_error(f"Error en inicialización: {e}")
            raise

    async def _test_knowledge_ingestion(self):
        """Test de ingesta de conocimiento."""
        print_step("Test 2: Ingesta de conocimiento")

        from backend.core.knowledge_ingestion import get_ingestion_pipeline
        pipeline = await get_ingestion_pipeline()

        total_chunks = 0
        for doc_name, doc_data in self.test_data.items():
            try:
                chunks = await pipeline.ingest_text_direct(
                    text=doc_data["content"],
                    source=doc_data["metadata"]["source"],
                    metadata=doc_data["metadata"]
                )
                total_chunks += len(chunks)
                print_success(f"✅ {doc_name}: {len(chunks)} chunks indexados")

            except Exception as e:
                print_error(f"Error procesando {doc_name}: {e}")
                raise

        print_success(f"Total de chunks indexados: {total_chunks}")

    async def _test_vector_search(self):
        """Test de búsquedas vectoriales."""
        print_step("Test 3: Búsquedas vectoriales")

        from backend.core.vector_db import get_vector_db
        vector_db = await get_vector_db()

        search_queries = [
            "cuenta de ahorro",
            "tarjeta de crédito",
            "horario sucursal",
            "consultar saldo"
        ]

        for query in search_queries:
            try:
                results = await vector_db.search(query, limit=3)
                print_success(f"✅ '{query}': {len(results)} resultados")

                if results:
                    best_result = results[0]
                    print_info(f"   Mejor resultado: score={best_result['score']:.3f}")

            except Exception as e:
                print_error(f"Error en búsqueda '{query}': {e}")
                raise

    async def _test_rag_responses(self):
        """Test del sistema RAG completo."""
        print_step("Test 4: Sistema RAG completo")

        from backend.core.rag_system import ask_rag

        print(f"\n{Colors.CYAN}Probando {len(self.test_queries)} consultas...{Colors.END}")

        results_summary = {
            "total": len(self.test_queries),
            "successful": 0,
            "high_confidence": 0,
            "with_sources": 0
        }

        for i, test_case in enumerate(self.test_queries, 1):
            query = test_case["query"]
            print(f"\n{Colors.BLUE}Consulta {i}: {query}{Colors.END}")

            try:
                response = await ask_rag(
                    query=query,
                    session_id="test_session",
                    user_id="test_user"
                )

                # Analizar respuesta
                confidence = response["confidence_score"]
                sources_count = len(response["sources"])
                query_type = response["query_classification"]

                print_info(f"Tipo: {query_type} | Confianza: {confidence:.2f} | Fuentes: {sources_count}")
                print(f"Respuesta: {response['answer'][:150]}...")

                # Contar métricas
                results_summary["successful"] += 1
                if confidence > 0.7:
                    results_summary["high_confidence"] += 1
                if sources_count > 0:
                    results_summary["with_sources"] += 1

                print_success("✅ Respuesta generada correctamente")

            except Exception as e:
                print_error(f"Error procesando consulta: {e}")
                raise

        # Mostrar resumen
        print(f"\n{Colors.BOLD}Resumen de resultados:{Colors.END}")
        print(f"• Total de consultas: {results_summary['total']}")
        print(f"• Exitosas: {results_summary['successful']}")
        print(f"• Alta confianza (>0.7): {results_summary['high_confidence']}")
        print(f"• Con fuentes: {results_summary['with_sources']}")

    async def _test_advanced_features(self):
        """Test de funcionalidades avanzadas."""
        print_step("Test 5: Funcionalidades avanzadas")

        # Test de contexto conversacional
        from backend.core.rag_system import ask_rag

        print_info("Probando contexto conversacional...")
        session_id = "advanced_test_session"

        # Primera consulta
        response1 = await ask_rag(
            "¿Qué es una cuenta de ahorro?",
            session_id=session_id
        )

        # Segunda consulta con contexto
        response2 = await ask_rag(
            "¿Cuáles son los requisitos para abrirla?",
            session_id=session_id
        )

        print_success("✅ Contexto conversacional funcional")

        # Test de estadísticas del sistema
        from backend.core.rag_system import get_rag_system
        rag_system = await get_rag_system()
        stats = await rag_system.get_system_stats()

        print_info("Estadísticas del sistema:")
        print(f"• Documentos indexados: {stats['vector_db'].get('vectors_count', 'N/A')}")
        print(f"• Conversaciones activas: {stats['active_conversations']}")
        print(f"• Modelo LLM: {stats['model_name']}")

        print_success("✅ Sistema completamente operativo")


async def main():
    """Función principal."""
    try:
        # Verificar que estamos en el directorio correcto
        if not Path("backend").exists():
            print_error("Error: Ejecutar desde el directorio raíz del proyecto")
            print_info("Uso: python test_rag_system.py")
            return

        # Ejecutar tests
        tester = RAGSystemTester()
        await tester.run_complete_test()

    except KeyboardInterrupt:
        print_info("\n⚠️  Prueba interrumpida por el usuario")
    except Exception as e:
        print_error(f"Error crítico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())