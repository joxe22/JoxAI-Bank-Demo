#!/usr/bin/env python3
"""
🧪 Test AI Integration - Banking Chatbot
Ubicación: /test_ai_integration.py

Script para probar la integración completa de LLM + RAG
sin necesidad de ejecutar el servidor completo.
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Agregar backend al path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Configurar variables de entorno básicas
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("LLM_PROVIDER", "openai")
os.environ.setdefault("AI_ENABLED", "False")  # Empezar en modo fallback

async def test_chat_service():
    """
    🧪 Test básico del ChatService integrado
    """

    print("🧪 Testing ChatService con IA integrada...")

    try:
        # Importar servicios
        from services.chat.chat_service import ChatService

        # Inicializar servicio
        chat_service = ChatService()

        print("✅ ChatService inicializado correctamente")

        # Test messages
        test_messages = [
            "Hola, ¿cómo estás?",
            "Quiero consultar mi saldo",
            "¿Cómo puedo transferir dinero?",
            "Me robaron mi tarjeta, es urgente",
            "¿Qué tipos de préstamos tienen?",
        ]

        print("\n🔄 Ejecutando tests de mensajes...")

        for i, message in enumerate(test_messages, 1):
            print(f"\n--- Test {i}/5 ---")
            print(f"📝 Usuario: {message}")

            # Procesar mensaje
            response = await chat_service.process_message(
                message=message,
                session_id=f"test_session_{i}",
                user_id="test_user"
            )

            print(f"🤖 Bot ({response['confidence']}): {response['message'][:100]}...")
            print(f"⚡ Tiempo: {response.get('processing_time_ms', 0)}ms")
            print(f"🎯 Método: {response.get('metadata', {}).get('processing_method', 'unknown')}")

            if response.get('suggested_actions'):
                print(f"💡 Acciones: {response['suggested_actions']}")

            if response.get('escalate_to_human'):
                print("👤 Requiere escalación humana")

        # Test analytics
        print(f"\n📊 Testing analytics...")
        analytics = await chat_service.get_analytics()
        print(f"   - Llamadas IA: {analytics.get('ai_metrics', {}).get('ai_calls', 0)}")
        print(f"   - Llamadas fallback: {analytics.get('ai_metrics', {}).get('fallback_calls', 0)}")

        # Test health check
        print(f"\n🏥 Testing health check...")
        health = await chat_service.get_service_health()
        print(f"   - Estado: {health.get('chat_service')}")
        print(f"   - IA habilitada: {health.get('ai_mode_enabled')}")

        print("\n✅ Todos los tests de ChatService pasaron!")
        return True

    except Exception as e:
        print(f"❌ Error en test de ChatService: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

async def test_llm_service():
    """
    🧪 Test del LLM Service
    """

    print("\n🤖 Testing LLM Service...")

    try:
        from services.llm.llm_service import LLMService

        llm_service = LLMService()
        print("✅ LLM Service inicializado")

        # Test disponibilidad de proveedores
        providers = await llm_service.get_available_providers()
        print(f"🔌 Proveedores disponibles: {providers}")

        if not providers:
            print("⚠️  Sin proveedores LLM disponibles (modo fallback)")
            return True

        # Test generación de respuesta
        print("\n🧠 Testing generación de respuesta...")
        response = await llm_service.generate_response(
            user_message="¿Cuál es el límite de transferencia?",
            session_id="test_llm_session"
        )

        print(f"📝 Respuesta generada: {response.get('message', 'No message')[:100]}...")
        print(f"🎯 Confianza: {response.get('confidence', 'unknown')}")
        print(f"⚡ Tiempo: {response.get('processing_time_seconds', 0):.2f}s")

        # Test estadísticas
        stats = await llm_service.get_usage_stats()
        print(f"📊 Stats - Total tokens: {stats.get('total_tokens_used', 0)}")

        print("✅ LLM Service test completado!")
        return True

    except Exception as e:
        print(f"❌ Error en test de LLM Service: {str(e)}")
        return False

async def test_rag_service():
    """
    🧪 Test del RAG Service
    """

    print("\n🔍 Testing RAG Service...")

    try:
        from services.rag.rag_service import RAGService

        rag_service = RAGService()
        print("✅ RAG Service inicializado")

        # Test búsqueda de documentos
        print("\n📚 Testing búsqueda de documentos...")
        docs = await rag_service.retrieve_relevant_documents(
            query="transferencias bancarias límites",
            top_k=3
        )

        print(f"📄 Documentos encontrados: {len(docs)}")
        for i, doc in enumerate(docs, 1):
            print(f"   {i}. {doc.get('title', 'Sin título')[:50]}... (Score: {doc.get('similarity_score', 0):.2f})")

        # Test contexto para LLM
        print("\n🧠 Testing contexto para LLM...")
        context = await rag_service.get_context_for_llm("¿Cómo transferir dinero?")
        print(f"📝 Contexto generado: {len(context)} caracteres")

        # Test estadísticas de KB
        stats = await rag_service.get_knowledge_stats()
        print(f"📊 KB Stats - Docs: {stats.get('total_documents', 0)}, Categorías: {len(stats.get('categories', []))}")

        print("✅ RAG Service test completado!")
        return True

    except Exception as e:
        print(f"❌ Error en test de RAG Service: {str(e)}")
        return False

async def main():
    """
    🚀 Ejecutar todos los tests
    """

    print("🏦 Banking Chatbot - Test de Integración IA")
    print("=" * 50)

    results = []

    # Test ChatService (principal)
    results.append(await test_chat_service())

    # Test LLM Service
    results.append(await test_llm_service())

    # Test RAG Service
    results.append(await test_rag_service())

    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE TESTS")
    print("=" * 50)

    test_names = ["ChatService", "LLM Service", "RAG Service"]
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")

    passed = sum(results)
    total = len(results)

    print(f"\n🏆 Resultado: {passed}/{total} tests pasaron")

    if passed == total:
        print("🎉 ¡Integración IA completamente funcional!")
        return 0
    else:
        print("⚠️  Algunos tests fallaron - revisar logs arriba")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)