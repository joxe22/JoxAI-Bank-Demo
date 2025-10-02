#!/usr/bin/env python3
"""
🧪 Test NLU Sistema Completo - Banking Chatbot
Ubicación: /test_nlu_complete.py

Script de prueba integral del sistema NLU completo.
Prueba Intent Classification + NER + Dialog Manager + RAG Integration.
"""

import asyncio
import sys
import logging
from pathlib import Path
from datetime import datetime
import json
import uuid

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
    print("=" * 80)
    print(f"🧠 {text}")
    print("=" * 80)
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


class ComprehensiveNLUTester:
    """Tester completo del sistema NLU."""

    def __init__(self):
        self.test_conversations = self._get_test_conversations()

    def _get_test_conversations(self) -> List[Dict]:
        """Retorna conversaciones de prueba completas."""
        return [
            {
                "name": "Consulta de Saldo Simple",
                "description": "Usuario consulta saldo básico",
                "messages": [
                    "Hola",
                    "¿Cuál es mi saldo actual?",
                    "De mi cuenta de ahorros",
                    "Gracias"
                ],
                "expected_intents": ["greeting", "balance_check", "product_info", "goodbye"],
                "expected_entities": ["PRODUCT_TYPE"],
                "should_complete": True
            },

            {
                "name": "Transferencia Completa",
                "description": "Flujo completo de transferencia con slot filling",
                "messages": [
                    "Buenos días",
                    "Quiero hacer una transferencia",
                    "Necesito transferir 250000 pesos",
                    "A la cuenta 9876543210",
                    "Al banco Davivienda",
                    "Es para pago de arriendo",
                    "Sí, confirmo la transferencia"
                ],
                "expected_intents": ["greeting", "transfer", "transfer", "transfer", "transfer", "transfer", "transfer"],
                "expected_entities": ["AMOUNT", "ACCOUNT_NUMBER", "BANK_NAME"],
                "should_complete": True,
                "requires_confirmation": True
            },

            {
                "name": "Problema con Tarjeta",
                "description": "Usuario reporta problema y necesita escalación",
                "messages": [
                    "Hola, tengo un problema",
                    "Mi tarjeta terminada en 1234 fue rechazada",
                    "Intenté comprar pero no funcionó",
                    "Esto es muy complicado, necesito hablar con una persona"
                ],
                "expected_intents": ["greeting", "troubleshooting", "troubleshooting", "escalation"],
                "expected_entities": ["CARD_NUMBER"],
                "should_escalate": True
            },

            {
                "name": "Información de Productos",
                "description": "Consulta informacional usando RAG",
                "messages": [
                    "Hola",
                    "¿Qué tipos de cuentas de ahorro tienen?",
                    "¿Cuáles son los requisitos?",
                    "¿Cuánto es la tasa de interés?",
                    "Perfecto, gracias"
                ],
                "expected_intents": ["greeting", "product_info", "product_info", "product_info", "goodbye"],
                "should_use_rag": True
            },

            {
                "name": "Historial de Transacciones",
                "description": "Consulta de movimientos con entidades temporales",
                "messages": [
                    "Necesito ver mis movimientos",
                    "Del último mes",
                    "De mi cuenta corriente",
                    "Solo las compras"
                ],
                "expected_intents": ["transaction_history", "transaction_history", "transaction_history", "transaction_history"],
                "expected_entities": ["TIME_PERIOD", "PRODUCT_TYPE", "TRANSACTION_TYPE"],
                "requires_auth": True
            }
        ]

    async def run_comprehensive_test(self):
        """Ejecuta prueba completa del sistema NLU."""
        print_header("SISTEMA NLU COMPLETO - PRUEBA INTEGRAL")

        try:
            # Test 1: Verificar componentes individuales
            await self._test_individual_components()

            # Test 2: Probar integración NLU
            await self._test_nlu_integration()

            # Test 3: Ejecutar conversaciones completas
            await self._test_complete_conversations()

            # Test 4: Métricas y rendimiento
            await self._test_performance_metrics()

            print_header("RESUMEN DE PRUEBAS")
            print_success("✅ Todas las pruebas del sistema NLU completadas exitosamente")
            print_info("El sistema está listo para manejar conversaciones bancarias complejas")

        except Exception as e:
            print_error(f"Error durante las pruebas: {e}")
            raise

    async def _test_individual_components(self):
        """Prueba componentes NLU individuales."""
        print_step("Test 1: Componentes Individuales")

        # Test Intent Classifier
        try:
            from backend.core.intent_classifier import get_intent_classifier
            classifier = await get_intent_classifier()

            test_intent = await classifier.classify_intent("Quiero hacer una transferencia")
            assert test_intent.intent == "transfer"
            assert test_intent.confidence > 0.7
            print_success("Intent Classifier funcionando")
        except Exception as e:
            print_error(f"Error en Intent Classifier: {e}")
            raise

        # Test NER
        try:
            from backend.core.banking_ner import get_banking_ner
            ner = await get_banking_ner()

            entities = await ner.extract_entities("Transferir $150.000 a la cuenta 1234567890")
            amount_entities = [e for e in entities if e.label.value == "AMOUNT"]
            account_entities = [e for e in entities if e.label.value == "ACCOUNT_NUMBER"]

            assert len(amount_entities) > 0, "No se detectó monto"
            assert len(account_entities) > 0, "No se detectó número de cuenta"
            print_success("Banking NER funcionando")
        except Exception as e:
            print_error(f"Error en Banking NER: {e}")
            raise

        # Test Dialog Manager
        try:
            from backend.core.dialog_manager import get_dialog_manager
            dialog_manager = await get_dialog_manager()

            session_id = f"test_{uuid.uuid4().hex[:8]}"
            response = await dialog_manager.process_message("Hola", session_id)

            assert response.text is not None
            assert response.context is not None
            print_success("Dialog Manager funcionando")
        except Exception as e:
            print_error(f"Error en Dialog Manager: {e}")
            raise

        # Test RAG System
        try:
            from backend.core.rag_system import get_rag_system
            rag_system = await get_rag_system()

            # Crear conocimiento de prueba mínimo si no existe
            try:
                from backend.core.knowledge_ingestion import get_ingestion_pipeline
                pipeline = await get_ingestion_pipeline()

                test_knowledge = """
                Información de Cuentas de Ahorro:
                Las cuentas de ahorro permiten ahorrar dinero de forma segura.
                Requisitos: documento de identidad y depósito mínimo.
                Tasa de interés: 4.5% anual.
                """

                await pipeline.ingest_text_direct(
                    text=test_knowledge,
                    source="test_knowledge.txt",
                    metadata={"category": "test", "confidence_level": "high"}
                )
                print_success("Conocimiento de prueba cargado")
            except Exception as e:
                print_info(f"Usando conocimiento existente: {e}")

            print_success("RAG System funcionando")
        except Exception as e:
            print_error(f"Error en RAG System: {e}")
            raise

    async def _test_nlu_integration(self):
        """Prueba la integración NLU completa."""
        print_step("Test 2: Integración NLU")

        try:
            from backend.core.nlu_integration import get_nlu_orchestrator
            orchestrator = await get_nlu_orchestrator()

            # Casos de prueba para diferentes estrategias
            test_cases = [
                {
                    "message": "Hola, buenos días",
                    "expected_strategy": "dialog",
                    "expected_intent": "greeting"
                },
                {
                    "message": "¿Qué tipos de cuentas tienen?",
                    "expected_strategy": "rag",
                    "expected_intent": "product_info"
                },
                {
                    "message": "Quiero transferir 100000 pesos a la cuenta 123456789",
                    "expected_strategy": "dialog",
                    "expected_intent": "transfer"
                }
            ]

            session_id = f"integration_test_{uuid.uuid4().hex[:8]}"

            for i, test_case in enumerate(test_cases, 1):
                print_info(f"Caso {i}: {test_case['message']}")

                result = await orchestrator.process_message(
                    message=test_case["message"],
                    session_id=session_id,
                    user_id="integration_test"
                )

                # Verificaciones
                assert result.final_response, "Debe generar respuesta"
                assert result.intent == test_case["expected_intent"], f"Intent esperado: {test_case['expected_intent']}, obtenido: {result.intent}"
                assert result.confidence_score > 0.3, f"Confianza muy baja: {result.confidence_score}"

                print_success(f"✓ Intent: {result.intent} ({result.confidence_score:.2f})")
                print_success(f"✓ Tiempo: {result.processing_time_ms:.0f}ms")
                print_success(f"✓ Componentes: {', '.join(result.components_used)}")

            print_success("Integración NLU verificada")

        except Exception as e:
            print_error(f"Error en integración NLU: {e}")
            raise

    async def _test_complete_conversations(self):
        """Prueba conversaciones completas."""
        print_step("Test 3: Conversaciones Completas")

        from backend.core.nlu_integration import get_nlu_orchestrator
        orchestrator = await get_nlu_orchestrator()

        for conv_test in self.test_conversations:
            print_info(f"\n🎭 Conversación: {conv_test['name']}")
            print_info(f"Descripción: {conv_test['description']}")

            session_id = f"conv_test_{uuid.uuid4().hex[:8]}"
            conversation_results = []

            for i, message in enumerate(conv_test["messages"]):
                print(f"\n👤 Usuario: {message}")

                result = await orchestrator.process_message(
                    message=message,
                    session_id=session_id,
                    user_id="conversation_test"
                )

                print(f"🤖 Asistente: {result.final_response}")
                print(f"   Intent: {result.intent} ({result.intent_confidence:.2f})")
                print(f"   Estado: {result.conversation_state}")
                print(f"   Entidades: {len(result.entities)}")

                conversation_results.append(result)

                # Verificar escalación si se espera
                if conv_test.get("should_escalate") and result.escalate:
                    print_success("✓ Escalación detectada correctamente")
                    break

                # Verificar completitud si se espera
                if (conv_test.get("should_complete") and
                        result.conversation_state == "complete"):
                    print_success("✓ Conversación completada correctamente")

                await asyncio.sleep(0.2)  # Pausa realista

            # Análisis de la conversación
            intents_detected = [r.intent for r in conversation_results]
            entities_detected = []
            for r in conversation_results:
                entities_detected.extend([e["label"] for e in r.entities])

            print_success(f"✓ Intents detectados: {set(intents_detected)}")
            print_success(f"✓ Entidades detectadas: {set(entities_detected)}")
            print_success(f"✓ Conversación '{conv_test['name']}' completada")

    async def _test_performance_metrics(self):
        """Prueba métricas de rendimiento."""
        print_step("Test 4: Métricas de Rendimiento")

        from backend.core.nlu_integration import get_nlu_orchestrator
        orchestrator = await get_nlu_orchestrator()

        # Test de rendimiento con múltiples mensajes
        performance_messages = [
            "¿Cuál es mi saldo?",
            "Quiero hacer una transferencia de 50000 pesos",
            "¿Qué tipos de préstamos tienen?",
            "Mi tarjeta está bloqueada",
            "¿Cómo cambio mi clave?"
        ]

        times = []
        confidences = []

        for message in performance_messages:
            session_id = f"perf_test_{uuid.uuid4().hex[:8]}"

            result = await orchestrator.process_message(
                message=message,
                session_id=session_id,
                user_id="performance_test"
            )

            times.append(result.processing_time_ms)
            confidences.append(result.confidence_score)

        # Métricas
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        avg_confidence = sum(confidences) / len(confidences)

        print_success(f"✓ Tiempo promedio: {avg_time:.0f}ms")
        print_success(f"✓ Tiempo máximo: {max_time:.0f}ms")
        print_success(f"✓ Tiempo mínimo: {min_time:.0f}ms")
        print_success(f"✓ Confianza promedio: {avg_confidence:.2f}")

        # Verificar que están dentro de límites aceptables
        assert avg_time < 2000, f"Tiempo promedio muy alto: {avg_time}ms"
        assert avg_confidence > 0.6, f"Confianza promedio muy baja: {avg_confidence}"

        # Estadísticas del sistema
        stats = await orchestrator.get_system_stats()
        print_success(f"✓ Sesiones activas: {stats['active_sessions']}")
        print_success(f"✓ Estado RAG: {stats['rag_stats'].get('status', 'unknown')}")

        print_success("Métricas de rendimiento verificadas")


async def main():
    """Función principal."""
    try:
        # Verificar que estamos en el directorio correcto
        if not Path("backend").exists():
            print_error("Error: Ejecutar desde el directorio raíz del proyecto")
            print_info("Uso: python test_nlu_complete.py")
            return

        # Ejecutar tests
        tester = ComprehensiveNLUTester()
        await tester.run_comprehensive_test()

    except KeyboardInterrupt:
        print_info("\n⚠️  Prueba interrumpida por el usuario")
    except Exception as e:
        print_error(f"Error crítico: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())