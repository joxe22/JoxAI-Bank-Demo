"""
📝 Prompt Templates para Banking Chatbot
Ubicación: backend/services/llm/prompt_templates.py

Templates de prompts especializados para diferentes escenarios bancarios.
Incluye system prompts, guardrails y templates específicos.
"""

from typing import Dict, Any, Optional
from datetime import datetime

class PromptTemplates:
    """
    📝 Gestor de templates de prompts bancarios
    """

    def __init__(self):
        """Inicializar templates"""
        pass

    def get_banking_assistant_prompt(self) -> str:
        """
        🏦 System prompt principal para asistente bancario
        """

        return """
Eres un asistente virtual bancario profesional, confiable y útil llamado "JoxAI Assistant". 
Tu misión es ayudar a los clientes con sus consultas bancarias de manera eficiente y segura.

### TU ROL Y PERSONALIDAD:
- Eres profesional pero amigable y cercano
- Siempre mantienes la confidencialidad y seguridad
- Eres paciente y explicas las cosas de manera clara
- No especulas ni inventas información
- Siempre buscas la mejor experiencia para el cliente

### QUÉ PUEDES HACER:
✅ Explicar productos y servicios bancarios
✅ Guiar en procesos y procedimientos
✅ Proporcionar información sobre tasas y tarifas
✅ Ayudar con consultas sobre estados de cuenta
✅ Orientar sobre seguridad bancaria
✅ Escalate consultas complejas a agentes humanos

### QUÉ NO PUEDES HACER:
❌ Realizar transacciones por el cliente
❌ Acceder a información personal sin autenticación
❌ Proporcionar asesoría de inversión no bancaria
❌ Dar consejos legales o fiscales específicos
❌ Compartir información confidencial de otros clientes

### PROTOCOLOS DE SEGURIDAD:
🔐 Para consultas de saldos, movimientos o información personal:
   - SIEMPRE solicita autenticación
   - Explica por qué es necesaria la verificación
   - Nunca muestres información sin verificar identidad

🚨 Para situaciones sospechosas o fraudes:
   - Recomienda contactar inmediatamente al banco
   - Proporciona números de emergencia
   - Nunca solicites información sensible

### INSTRUCCIONES ESPECÍFICAS:
- Si no tienes información completa, admítelo y ofrece alternativas
- Siempre cita fuentes cuando uses información específica
- Para consultas complejas, ofrece derivar a un especialista
- Usa un lenguaje claro y evita jerga técnica excesiva
- Si detectas frustración, ofrece opciones adicionales de ayuda

### FORMATO DE RESPUESTA:
- Responde de manera directa y estructurada
- Si es un proceso, usa pasos numerados
- Incluye emojis apropiados para mejorar la experiencia
- Finaliza preguntando si necesita más ayuda

Recuerda: Tu objetivo es resolver eficientemente las consultas bancarias manteniendo siempre la seguridad y profesionalismo.
"""

    def get_authentication_prompt(self) -> str:
        """
        🔐 Prompt para solicitar autenticación
        """

        return """
Para tu seguridad y cumplir con las regulaciones bancarias, necesito verificar tu identidad antes de proporcionar información de tu cuenta.

Por favor, proporciona:
🆔 Tu número de documento de identidad
📱 Los últimos 4 dígitos de tu teléfono registrado

Esta verificación es estándar y nos ayuda a proteger tu información financiera.
"""

    def get_fraud_alert_prompt(self) -> str:
        """
        🚨 Prompt para alertas de fraude
        """

        return """
🚨 ALERTA DE SEGURIDAD 🚨

He detectado que tu consulta podría estar relacionada con una posible situación de fraude o estafa.

IMPORTANTE:
- NUNCA compartas tus claves o códigos por teléfono o email
- Los empleados del banco NUNCA te pedirán tu PIN o contraseñas
- Si recibiste llamadas sospechosas, repórtalas inmediatamente

📞 Línea de Emergencia Fraude: 01-800-FRAUDE (24/7)
🏦 Sucursal más cercana para reportes presenciales

¿Necesitas ayuda para reportar una situación sospechosa?
"""

    def get_escalation_prompt(self, reason: str = "consulta compleja") -> str:
        """
        👥 Prompt para escalación a agente humano
        """

        return f"""
Entiendo que necesitas ayuda especializada para tu {reason}.

Te voy a conectar con uno de nuestros agentes especializados que podrá ayudarte mejor.

🕐 Tiempo de espera estimado: 2-3 minutos
📋 He guardado el contexto de nuestra conversación
👤 Un agente especializado se hará cargo de tu caso

Mientras esperas, ¿hay alguna otra consulta básica con la que pueda ayudarte?
"""

    def get_product_explanation_prompt(self, product_type: str) -> str:
        """
        💳 Prompts para explicación de productos
        """

        templates = {
            "tarjeta_credito": """
💳 **TARJETAS DE CRÉDITO**

Te ayudo a encontrar la tarjeta ideal para ti:

🌟 **Tarjeta Clásica**
- Sin anualidad el primer año
- Línea desde $10,000
- 2% cashback en supermercados
- Programa de puntos

💎 **Tarjeta Gold**  
- Línea desde $50,000
- Acceso a salas VIP aeropuertos
- Seguro de viaje incluido
- 3% cashback gasolineras

🏆 **Tarjeta Platinum**
- Línea desde $100,000
- Concierge 24/7
- Seguro médico internacional
- 5% cashback restaurantes

¿Qué tipo de beneficios te interesan más?
""",

            "cuenta_ahorro": """
💰 **CUENTAS DE AHORRO**

Opciones para hacer crecer tu dinero:

🌱 **Cuenta Básica**
- $0 manejo de cuenta
- Rendimiento 2.5% anual
- Retiros ilimitados
- App móvil gratis

📈 **Cuenta Premium** 
- Rendimiento hasta 4.2% anual
- Asesor personal asignado
- Productos preferenciales
- Tarjeta de débito Gold

🎯 **Cuenta Meta**
- Ahorro programado automático  
- Metas personalizables
- Rendimiento bonificado 5%
- Sin penalizaciones

¿Tienes alguna meta específica de ahorro?
""",

            "prestamo": """
🏠 **PRÉSTAMOS Y CRÉDITOS**

Te ayudamos a financiar tus proyectos:

🏡 **Crédito Hipotecario**
- Tasa desde 8.9% anual
- Hasta 30 años plazo
- Financiamiento 90% valor
- Sin comisión por apertura

🚗 **Crédito Automotriz**
- Tasa desde 12.5% anual
- Hasta 7 años plazo
- Autos nuevos y seminuevos
- Trámite express 24hrs

💼 **Préstamo Personal**
- Tasa desde 15.9% anual
- Hasta $500,000
- Sin garantía hipotecaria
- Desembolso mismo día

¿Qué tipo de proyecto quieres financiar?
"""
        }

        return templates.get(product_type, "Producto no encontrado en templates")

    def get_error_handling_prompt(self, error_type: str) -> str:
        """
        ❌ Prompts para manejo de errores
        """

        error_templates = {
            "no_information": """
🤔 No tengo información específica sobre esa consulta en mi base de conocimientos.

Sin embargo, puedo:
✅ Conectarte con un especialista que sí tenga esa información
✅ Programar una cita en sucursal
✅ Enviarte información por email
✅ Ayudarte con otras consultas bancarias

¿Cuál opción prefieres?
""",

            "authentication_failed": """
🔐 No pude verificar tu identidad con la información proporcionada.

Por tu seguridad:
✅ Verifica que los datos sean correctos
✅ Si olvidaste tu información, podemos ayudarte a recuperarla
✅ Visita una sucursal con identificación oficial
✅ Llama a nuestro centro de atención

¿Necesitas ayuda para recuperar tu acceso?
""",

            "system_error": """
⚙️ Estoy experimentando dificultades técnicas temporales.

Mientras se resuelve:
✅ Puedes usar nuestra app móvil
✅ Llamar al 01-800-BANCO
✅ Visitar cajeros automáticos
✅ Conectarte con un agente humano

¿Te gustaría que te conecte con un agente?
""",

            "outside_scope": """
🎯 Esa consulta está fuera de mi especialidad bancaria.

Mi expertise incluye:
✅ Productos y servicios bancarios
✅ Procesos y trámites
✅ Consultas de cuenta
✅ Seguridad financiera

Para tu consulta específica, te recomiendo:
👤 Hablar con un especialista
📞 Llamar a atención personalizada
🏦 Visitar una sucursal

¿Te conecto con alguien que pueda ayudarte mejor?
"""
        }

        return error_templates.get(error_type, "Error no identificado")

    def get_transaction_prompt(self, transaction_type: str) -> str:
        """
        💸 Prompts para transacciones
        """

        transaction_templates = {
            "transfer": """
🔄 **TRANSFERENCIAS BANCARIAS**

Para realizar una transferencia necesito verificar tu identidad primero.

**Tipos disponibles:**
📱 Transferencia móvil (hasta $50,000)
🏦 Transferencia en sucursal (sin límite)  
💻 Banca en línea (hasta $100,000)
⚡ Transferencia express (mismo día)

**Información necesaria:**
- Cuenta destino (18 dígitos)
- Nombre completo del beneficiario
- Concepto de la transferencia
- Tu autenticación biométrica/token

¿Qué tipo de transferencia necesitas hacer?
""",

            "payment": """
💳 **PAGOS DE SERVICIOS**

Puedes pagar cómodamente desde diferentes canales:

🏠 **Servicios básicos:**
- Luz, agua, gas, teléfono
- Internet y cable
- Predial y tenencia

💼 **Créditos y seguros:**
- Tarjetas de crédito
- Préstamos personales
- Seguros de vida/auto

📱 **Métodos de pago:**
- App móvil (24/7)
- Cajeros automáticos  
- Banca en línea
- Sucursales

¿Qué servicio necesitas pagar?
""",

            "balance_inquiry": """
💰 **CONSULTA DE SALDO**

Para mostrarte tu saldo actual, necesito verificar tu identidad.

**Una vez autenticado verás:**
💵 Saldo disponible
📊 Saldo contable
🕐 Últimos movimientos
📈 Resumen mensual

**Canales disponibles:**
📱 App móvil (recomendado)
🏧 Cajeros automáticos
💻 Banca en línea
📞 Atención telefónica

¿Cómo prefieres verificar tu identidad?
"""
        }

        return transaction_templates.get(transaction_type, "Tipo de transacción no disponible")

    def get_context_aware_prompt(
            self,
            base_prompt: str,
            context: Dict[str, Any]
    ) -> str:
        """
        🧠 Enriquecer prompt con contexto específico
        """

        context_additions = []

        # Agregar contexto temporal
        current_time = datetime.now()
        if current_time.hour < 12:
            context_additions.append("Es por la mañana, saluda apropiadamente.")
        elif current_time.hour < 18:
            context_additions.append("Es por la tarde.")
        else:
            context_additions.append("Es por la noche, considera que puede ser urgente.")

        # Agregar contexto de usuario
        if context.get("is_premium_customer"):
            context_additions.append("El cliente es Premium, ofrece servicio VIP.")

        if context.get("has_active_loans"):
            context_additions.append("El cliente tiene préstamos activos, menciona opciones relacionadas.")

        if context.get("recent_transaction_issues"):
            context_additions.append("Ha tenido problemas recientes, sé extra atento.")

        # Agregar contexto de conversación
        if context.get("conversation_count", 0) > 5:
            context_additions.append("Es una conversación larga, considera resumir o escalar.")

        # Construir prompt enriquecido
        if context_additions:
            context_section = "\n### CONTEXTO ESPECÍFICO:\n" + "\n".join(f"- {item}" for item in context_additions)
            return base_prompt + context_section

        return base_prompt

    def get_compliance_disclaimer(self) -> str:
        """
        ⚖️ Disclaimer de cumplimiento regulatorio
        """

        return """
---
*Información sujeta a términos y condiciones. Las tasas y tarifas pueden variar. 
Consulta condiciones específicas en sucursales. Tu patrimonio está protegido por IPAB hasta por $400,000 UDI por persona.*
"""