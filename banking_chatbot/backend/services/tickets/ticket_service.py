"""
🎫 Ticket Service - Gestión de Tickets y Escalación
Ubicación: backend/services/tickets/ticket_service.py

Servicio principal para manejar la creación, asignación y seguimiento
de tickets cuando el chatbot necesita escalación a agentes humanos.
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class TicketPriority(str, Enum):
    """🏷️ Prioridades de tickets"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"

class TicketStatus(str, Enum):
    """📊 Estados de tickets"""
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"
    ESCALATED = "escalated"

class TicketCategory(str, Enum):
    """📋 Categorías de tickets"""
    ACCOUNT_INQUIRY = "account_inquiry"
    TRANSACTION_ISSUE = "transaction_issue"
    CARD_PROBLEM = "card_problem"
    LOAN_REQUEST = "loan_request"
    FRAUD_REPORT = "fraud_report"
    TECHNICAL_SUPPORT = "technical_support"
    COMPLAINT = "complaint"
    GENERAL_INQUIRY = "general_inquiry"

class TicketService:
    """
    🎫 Servicio de gestión de tickets

    Responsabilidades:
    - Crear tickets desde conversaciones del chatbot
    - Asignar tickets a agentes disponibles
    - Manejar prioridades y SLAs
    - Tracking de estado y resolución
    - Escalación automática
    - Métricas y reportes
    """

    def __init__(self):
        """Inicializar servicio de tickets"""

        # Storage en memoria (en producción usaría base de datos)
        self.tickets = {}  # ticket_id -> ticket_data
        self.agent_assignments = {}  # agent_id -> [ticket_ids]
        self.ticket_counter = 1

        # Configuración de SLAs (en minutos)
        self.sla_config = {
            TicketPriority.CRITICAL: 5,    # 5 minutos
            TicketPriority.URGENT: 15,     # 15 minutos
            TicketPriority.HIGH: 60,       # 1 hora
            TicketPriority.MEDIUM: 240,    # 4 horas
            TicketPriority.LOW: 1440       # 24 horas
        }

        # Agentes simulados (en producción vendría de DB)
        self.agents = {
            "agent_001": {
                "id": "agent_001",
                "name": "María González",
                "email": "maria.gonzalez@bank.com",
                "specialties": ["account_inquiry", "transaction_issue"],
                "status": "available",
                "current_tickets": 0,
                "max_tickets": 5,
                "rating": 4.8
            },
            "agent_002": {
                "id": "agent_002",
                "name": "Carlos Rodríguez",
                "email": "carlos.rodriguez@bank.com",
                "specialties": ["fraud_report", "card_problem"],
                "status": "available",
                "current_tickets": 0,
                "max_tickets": 3,
                "rating": 4.9
            },
            "agent_003": {
                "id": "agent_003",
                "name": "Ana Martínez",
                "email": "ana.martinez@bank.com",
                "specialties": ["loan_request", "complaint"],
                "status": "busy",
                "current_tickets": 2,
                "max_tickets": 4,
                "rating": 4.7
            }
        }

        logger.info("🎫 Ticket Service inicializado")

    async def create_ticket(
            self,
            session_id: str,
            user_message: str,
            chat_context: Dict[str, Any],
            priority: TicketPriority = TicketPriority.MEDIUM,
            category: Optional[TicketCategory] = None,
            user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        🎫 Crear nuevo ticket desde conversación del chatbot
        """

        try:
            # Generar ID único
            ticket_id = f"TK{self.ticket_counter:06d}"
            self.ticket_counter += 1

            # Auto-detectar categoría si no se especifica
            if not category:
                category = await self._detect_ticket_category(user_message, chat_context)

            # Auto-ajustar prioridad basada en contexto
            detected_priority = await self._detect_priority(user_message, chat_context)
            if detected_priority.value > priority.value:
                priority = detected_priority

            # Crear ticket
            ticket_data = {
                "id": ticket_id,
                "session_id": session_id,
                "user_id": user_id,
                "status": TicketStatus.OPEN,
                "priority": priority,
                "category": category,
                "title": await self._generate_ticket_title(user_message, category),
                "description": await self._generate_ticket_description(user_message, chat_context),
                "chat_context": {
                    "conversation_history": chat_context.get("conversation_history", []),
                    "user_message": user_message,
                    "bot_confidence": chat_context.get("confidence_score", 0),
                    "escalation_reason": chat_context.get("escalation_reason", "low_confidence")
                },
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "sla_due": datetime.now() + timedelta(minutes=self.sla_config[priority]),
                "assigned_agent": None,
                "resolution": None,
                "customer_satisfaction": None,
                "tags": await self._generate_tags(user_message, category),
                "metadata": {
                    "source": "chatbot",
                    "ai_escalation": True,
                    "language": "es"
                }
            }

            # Guardar ticket
            self.tickets[ticket_id] = ticket_data

            # Intentar asignación automática
            assigned_agent = await self._auto_assign_ticket(ticket_id)

            logger.info(f"🎫 Ticket creado: {ticket_id} - Prioridad: {priority.value} - Agente: {assigned_agent}")

            return {
                "ticket_id": ticket_id,
                "status": ticket_data["status"].value,
                "priority": priority.value,
                "category": category.value,
                "title": ticket_data["title"],
                "assigned_agent": assigned_agent,
                "sla_due": ticket_data["sla_due"].isoformat(),
                "estimated_response_time": self._get_estimated_response_time(priority),
                "created_at": ticket_data["created_at"].isoformat()
            }

        except Exception as e:
            logger.error(f"❌ Error creando ticket: {str(e)}")
            raise

    async def _detect_ticket_category(
            self,
            user_message: str,
            chat_context: Dict[str, Any]
    ) -> TicketCategory:
        """
        🔍 Detectar categoría automáticamente basada en el mensaje
        """

        message_lower = user_message.lower()

        # Mapeo de keywords a categorías
        category_keywords = {
            TicketCategory.FRAUD_REPORT: [
                "robo", "fraude", "estafa", "clonaron", "robaron", "sospechoso", "unauthorized"
            ],
            TicketCategory.CARD_PROBLEM: [
                "tarjeta", "card", "bloqueada", "no funciona", "chip", "magnetic", "atm"
            ],
            TicketCategory.TRANSACTION_ISSUE: [
                "transferencia", "pago", "cobro", "cargo", "descuento", "transaction", "movement"
            ],
            TicketCategory.ACCOUNT_INQUIRY: [
                "saldo", "balance", "cuenta", "account", "estado", "movimientos"
            ],
            TicketCategory.LOAN_REQUEST: [
                "préstamo", "crédito", "financiamiento", "loan", "hipoteca", "mortgage"
            ],
            TicketCategory.TECHNICAL_SUPPORT: [
                "app", "aplicación", "sistema", "error", "no carga", "technical", "bug"
            ],
            TicketCategory.COMPLAINT: [
                "queja", "reclamo", "molesto", "disgusto", "complaint", "unsatisfied"
            ]
        }

        # Buscar coincidencias
        for category, keywords in category_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return category

        # Default
        return TicketCategory.GENERAL_INQUIRY

    async def _detect_priority(
            self,
            user_message: str,
            chat_context: Dict[str, Any]
    ) -> TicketPriority:
        """
        ⚡ Detectar prioridad basada en urgencia y contexto
        """

        message_lower = user_message.lower()

        # Palabras de urgencia crítica
        critical_keywords = ["robo", "fraude", "estafa", "emergencia", "urgent", "crítico"]
        if any(keyword in message_lower for keyword in critical_keywords):
            return TicketPriority.CRITICAL

        # Palabras de alta urgencia
        urgent_keywords = ["urgente", "rápido", "ahora", "inmediato", "ya", "pronto"]
        if any(keyword in message_lower for keyword in urgent_keywords):
            return TicketPriority.URGENT

        # Context-based priority
        if chat_context.get("urgency_level") == "high":
            return TicketPriority.HIGH

        # Confidence-based priority
        confidence = chat_context.get("confidence_score", 1.0)
        if confidence < 0.3:
            return TicketPriority.HIGH
        elif confidence < 0.6:
            return TicketPriority.MEDIUM

        return TicketPriority.MEDIUM

    async def _generate_ticket_title(
            self,
            user_message: str,
            category: TicketCategory
    ) -> str:
        """
        📝 Generar título descriptivo para el ticket
        """

        # Templates por categoría
        title_templates = {
            TicketCategory.FRAUD_REPORT: "Reporte de Fraude/Seguridad",
            TicketCategory.CARD_PROBLEM: "Problema con Tarjeta",
            TicketCategory.TRANSACTION_ISSUE: "Consulta sobre Transacción",
            TicketCategory.ACCOUNT_INQUIRY: "Consulta de Cuenta",
            TicketCategory.LOAN_REQUEST: "Solicitud de Préstamo/Crédito",
            TicketCategory.TECHNICAL_SUPPORT: "Soporte Técnico",
            TicketCategory.COMPLAINT: "Queja/Reclamo",
            TicketCategory.GENERAL_INQUIRY: "Consulta General"
        }

        base_title = title_templates.get(category, "Consulta General")

        # Personalizar si es posible
        if len(user_message) > 10:
            preview = user_message[:40] + "..." if len(user_message) > 40 else user_message
            return f"{base_title}: {preview}"

        return base_title

    async def _generate_ticket_description(
            self,
            user_message: str,
            chat_context: Dict[str, Any]
    ) -> str:
        """
        📄 Generar descripción completa del ticket
        """

        description_parts = [
            "=== ESCALACIÓN DESDE CHATBOT ===",
            "",
            f"**Mensaje del cliente:**",
            user_message,
            "",
            f"**Contexto de la conversación:**"
        ]

        # Agregar historial de conversación
        history = chat_context.get("conversation_history", [])
        if history:
            description_parts.append("```")
            for msg in history[-3:]:  # Últimos 3 mensajes
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("timestamp", "")
                description_parts.append(f"[{role}] {content}")
            description_parts.append("```")

        # Agregar metadata técnica
        description_parts.extend([
            "",
            "**Información técnica:**",
            f"- Confianza del bot: {chat_context.get('confidence_score', 0):.2f}",
            f"- Razón de escalación: {chat_context.get('escalation_reason', 'N/A')}",
            f"- Session ID: {chat_context.get('session_id', 'N/A')}",
            f"- Fecha de escalación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ])

        return "\n".join(description_parts)

    async def _generate_tags(
            self,
            user_message: str,
            category: TicketCategory
    ) -> List[str]:
        """
        🏷️ Generar tags automáticos para el ticket
        """

        tags = [category.value, "chatbot-escalation"]

        message_lower = user_message.lower()

        # Tags por keywords
        tag_keywords = {
            "urgent": ["urgente", "rápido", "ahora", "ya"],
            "fraud": ["robo", "fraude", "estafa", "sospechoso"],
            "mobile": ["app", "móvil", "celular", "teléfono"],
            "online": ["internet", "web", "online", "línea"],
            "atm": ["cajero", "atm", "efectivo"],
            "international": ["internacional", "extranjero", "abroad"]
        }

        for tag, keywords in tag_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                tags.append(tag)

        return list(set(tags))  # Remover duplicados

    def _get_estimated_response_time(self, priority: TicketPriority) -> str:
        """
        ⏰ Obtener tiempo estimado de respuesta
        """

        response_times = {
            TicketPriority.CRITICAL: "Inmediato (< 5 min)",
            TicketPriority.URGENT: "15 minutos",
            TicketPriority.HIGH: "1 hora",
            TicketPriority.MEDIUM: "4 horas",
            TicketPriority.LOW: "24 horas"
        }

        return response_times.get(priority, "4 horas")

    async def _auto_assign_ticket(self, ticket_id: str) -> Optional[str]:
        """
        🤖 Asignar ticket automáticamente al mejor agente disponible
        """

        try:
            ticket = self.tickets.get(ticket_id)
            if not ticket:
                return None

            category = ticket["category"]
            priority = ticket["priority"]

            # Buscar agentes especializados y disponibles
            available_agents = []

            for agent_id, agent in self.agents.items():
                # Skip si el agente está offline
                if agent["status"] == "offline":
                    continue

                # Skip si ya tiene demasiados tickets
                if agent["current_tickets"] >= agent["max_tickets"]:
                    continue

                # Calcular score de match
                score = 0

                # Boost por especialización
                if category.value in agent["specialties"]:
                    score += 50

                # Boost por disponibilidad
                if agent["status"] == "available":
                    score += 30
                elif agent["status"] == "busy":
                    score += 10

                # Boost por carga de trabajo (menos tickets = mejor)
                workload_boost = (agent["max_tickets"] - agent["current_tickets"]) * 5
                score += workload_boost

                # Boost por rating
                score += agent["rating"] * 10

                # Boost por prioridad del ticket
                if priority == TicketPriority.CRITICAL:
                    score += 20
                elif priority == TicketPriority.URGENT:
                    score += 10

                available_agents.append((agent_id, score))

            if not available_agents:
                logger.warning(f"⚠️ No hay agentes disponibles para ticket {ticket_id}")
                return None

            # Seleccionar el agente con mayor score
            best_agent_id, best_score = max(available_agents, key=lambda x: x[1])

            # Asignar ticket
            await self._assign_ticket_to_agent(ticket_id, best_agent_id)

            logger.info(f"🎯 Ticket {ticket_id} asignado a {best_agent_id} (score: {best_score})")

            return best_agent_id

        except Exception as e:
            logger.error(f"❌ Error en auto-asignación: {str(e)}")
            return None

    async def _assign_ticket_to_agent(self, ticket_id: str, agent_id: str):
        """
        👤 Asignar ticket específico a agente
        """

        # Actualizar ticket
        if ticket_id in self.tickets:
            self.tickets[ticket_id]["assigned_agent"] = agent_id
            self.tickets[ticket_id]["status"] = TicketStatus.ASSIGNED
            self.tickets[ticket_id]["updated_at"] = datetime.now()

        # Actualizar agente
        if agent_id in self.agents:
            self.agents[agent_id]["current_tickets"] += 1
            if agent_id not in self.agent_assignments:
                self.agent_assignments[agent_id] = []
            self.agent_assignments[agent_id].append(ticket_id)

        logger.info(f"✅ Ticket {ticket_id} asignado a agente {agent_id}")

    async def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        📋 Obtener información de ticket
        """

        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None

        # Preparar respuesta con información enriquecida
        result = ticket.copy()

        # Agregar información del agente asignado
        if ticket["assigned_agent"]:
            agent = self.agents.get(ticket["assigned_agent"])
            if agent:
                result["agent_info"] = {
                    "name": agent["name"],
                    "email": agent["email"],
                    "status": agent["status"],
                    "rating": agent["rating"]
                }

        # Agregar SLA info
        now = datetime.now()
        sla_due = ticket["sla_due"]
        if now > sla_due:
            result["sla_status"] = "breached"
            result["sla_breach_minutes"] = int((now - sla_due).total_seconds() / 60)
        else:
            result["sla_status"] = "on_time"
            result["sla_remaining_minutes"] = int((sla_due - now).total_seconds() / 60)

        return result

    async def update_ticket_status(
            self,
            ticket_id: str,
            new_status: TicketStatus,
            agent_id: Optional[str] = None,
            resolution: Optional[str] = None
    ) -> bool:
        """
        🔄 Actualizar estado del ticket
        """

        try:
            if ticket_id not in self.tickets:
                logger.error(f"❌ Ticket {ticket_id} no encontrado")
                return False

            ticket = self.tickets[ticket_id]
            old_status = ticket["status"]

            # Actualizar status
            ticket["status"] = new_status
            ticket["updated_at"] = datetime.now()

            # Si se está resolviendo/cerrando
            if new_status in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
                if resolution:
                    ticket["resolution"] = resolution
                    ticket["resolved_at"] = datetime.now()

                # Liberar agente
                if ticket["assigned_agent"]:
                    await self._release_agent(ticket["assigned_agent"], ticket_id)

            logger.info(f"🔄 Ticket {ticket_id}: {old_status.value} → {new_status.value}")
            return True

        except Exception as e:
            logger.error(f"❌ Error actualizando ticket {ticket_id}: {str(e)}")
            return False

    async def _release_agent(self, agent_id: str, ticket_id: str):
        """
        🔓 Liberar agente de ticket resuelto
        """

        if agent_id in self.agents:
            self.agents[agent_id]["current_tickets"] = max(0, self.agents[agent_id]["current_tickets"] - 1)

            if agent_id in self.agent_assignments:
                if ticket_id in self.agent_assignments[agent_id]:
                    self.agent_assignments[agent_id].remove(ticket_id)

        logger.info(f"🔓 Agente {agent_id} liberado del ticket {ticket_id}")

    async def get_tickets_by_status(self, status: TicketStatus) -> List[Dict[str, Any]]:
        """
        📊 Obtener tickets por estado
        """

        filtered_tickets = []

        for ticket_id, ticket in self.tickets.items():
            if ticket["status"] == status:
                ticket_summary = {
                    "id": ticket_id,
                    "title": ticket["title"],
                    "priority": ticket["priority"].value,
                    "category": ticket["category"].value,
                    "created_at": ticket["created_at"].isoformat(),
                    "assigned_agent": ticket.get("assigned_agent"),
                    "sla_due": ticket["sla_due"].isoformat()
                }
                filtered_tickets.append(ticket_summary)

        # Ordenar por prioridad y fecha
        priority_order = {
            TicketPriority.CRITICAL: 5,
            TicketPriority.URGENT: 4,
            TicketPriority.HIGH: 3,
            TicketPriority.MEDIUM: 2,
            TicketPriority.LOW: 1
        }

        filtered_tickets.sort(
            key=lambda x: (
                priority_order.get(TicketPriority(x["priority"]), 0),
                x["created_at"]
            ),
            reverse=True
        )

        return filtered_tickets

    async def get_agent_tickets(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        👤 Obtener tickets asignados a un agente
        """

        agent_tickets = []

        for ticket_id, ticket in self.tickets.items():
            if ticket.get("assigned_agent") == agent_id:
                ticket_info = {
                    "id": ticket_id,
                    "title": ticket["title"],
                    "status": ticket["status"].value,
                    "priority": ticket["priority"].value,
                    "category": ticket["category"].value,
                    "created_at": ticket["created_at"].isoformat(),
                    "sla_due": ticket["sla_due"].isoformat()
                }
                agent_tickets.append(ticket_info)

        return agent_tickets

    async def escalate_ticket(
            self,
            ticket_id: str,
            escalation_reason: str,
            target_agent: Optional[str] = None
    ) -> bool:
        """
        ⬆️ Escalar ticket a nivel superior
        """

        try:
            if ticket_id not in self.tickets:
                return False

            ticket = self.tickets[ticket_id]

            # Actualizar prioridad si no es crítica
            if ticket["priority"] != TicketPriority.CRITICAL:
                old_priority = ticket["priority"]
                if ticket["priority"] == TicketPriority.LOW:
                    ticket["priority"] = TicketPriority.MEDIUM
                elif ticket["priority"] == TicketPriority.MEDIUM:
                    ticket["priority"] = TicketPriority.HIGH
                elif ticket["priority"] == TicketPriority.HIGH:
                    ticket["priority"] = TicketPriority.URGENT
                elif ticket["priority"] == TicketPriority.URGENT:
                    ticket["priority"] = TicketPriority.CRITICAL

                logger.info(f"⬆️ Ticket {ticket_id} escalado: {old_priority.value} → {ticket['priority'].value}")

            # Actualizar SLA
            ticket["sla_due"] = datetime.now() + timedelta(minutes=self.sla_config[ticket["priority"]])

            # Cambiar status
            ticket["status"] = TicketStatus.ESCALATED
            ticket["updated_at"] = datetime.now()

            # Agregar nota de escalación
            if "escalation_history" not in ticket:
                ticket["escalation_history"] = []

            ticket["escalation_history"].append({
                "escalated_at": datetime.now().isoformat(),
                "reason": escalation_reason,
                "escalated_by": ticket.get("assigned_agent", "system"),
                "new_priority": ticket["priority"].value
            })

            # Reasignar si se especifica agente
            if target_agent:
                old_agent = ticket.get("assigned_agent")
                if old_agent:
                    await self._release_agent(old_agent, ticket_id)
                await self._assign_ticket_to_agent(ticket_id, target_agent)

            return True

        except Exception as e:
            logger.error(f"❌ Error escalando ticket {ticket_id}: {str(e)}")
            return False

    async def add_ticket_note(
            self,
            ticket_id: str,
            note: str,
            author: str,
            note_type: str = "agent_note"
    ) -> bool:
        """
        📝 Agregar nota al ticket
        """

        try:
            if ticket_id not in self.tickets:
                return False

            ticket = self.tickets[ticket_id]

            if "notes" not in ticket:
                ticket["notes"] = []

            note_data = {
                "id": str(uuid.uuid4()),
                "content": note,
                "author": author,
                "type": note_type,  # agent_note, customer_note, system_note
                "created_at": datetime.now().isoformat(),
                "visibility": "internal" if note_type == "agent_note" else "public"
            }

            ticket["notes"].append(note_data)
            ticket["updated_at"] = datetime.now()

            logger.info(f"📝 Nota agregada al ticket {ticket_id} por {author}")
            return True

        except Exception as e:
            logger.error(f"❌ Error agregando nota a ticket {ticket_id}: {str(e)}")
            return False

    async def get_ticket_statistics(self) -> Dict[str, Any]:
        """
        📊 Obtener estadísticas de tickets
        """

        total_tickets = len(self.tickets)
        if total_tickets == 0:
            return {"total_tickets": 0, "message": "No hay tickets"}

        # Contar por estado
        status_counts = {}
        for status in TicketStatus:
            status_counts[status.value] = 0

        for ticket in self.tickets.values():
            status_counts[ticket["status"].value] += 1

        # Contar por prioridad
        priority_counts = {}
        for priority in TicketPriority:
            priority_counts[priority.value] = 0

        for ticket in self.tickets.values():
            priority_counts[ticket["priority"].value] += 1

        # Contar por categoría
        category_counts = {}
        for category in TicketCategory:
            category_counts[category.value] = 0

        for ticket in self.tickets.values():
            category_counts[ticket["category"].value] += 1

        # SLA compliance
        sla_breached = 0
        now = datetime.now()

        for ticket in self.tickets.values():
            if ticket["status"] not in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
                if now > ticket["sla_due"]:
                    sla_breached += 1

        sla_compliance = ((total_tickets - sla_breached) / total_tickets * 100) if total_tickets > 0 else 100

        # Tiempo promedio de resolución (simulado)
        avg_resolution_time = "2.5 horas"  # En producción se calcularía realmente

        # Agentes activos
        active_agents = sum(1 for agent in self.agents.values() if agent["current_tickets"] > 0)

        return {
            "total_tickets": total_tickets,
            "status_distribution": status_counts,
            "priority_distribution": priority_counts,
            "category_distribution": category_counts,
            "sla_compliance_percentage": round(sla_compliance, 1),
            "tickets_breached_sla": sla_breached,
            "avg_resolution_time": avg_resolution_time,
            "active_agents": active_agents,
            "total_agents": len(self.agents),
            "generated_at": datetime.now().isoformat()
        }

    async def get_overdue_tickets(self) -> List[Dict[str, Any]]:
        """
        ⚠️ Obtener tickets que han excedido SLA
        """

        now = datetime.now()
        overdue_tickets = []

        for ticket_id, ticket in self.tickets.items():
            # Solo considerar tickets activos
            if ticket["status"] in [TicketStatus.RESOLVED, TicketStatus.CLOSED]:
                continue

            if now > ticket["sla_due"]:
                breach_minutes = int((now - ticket["sla_due"]).total_seconds() / 60)

                overdue_ticket = {
                    "id": ticket_id,
                    "title": ticket["title"],
                    "priority": ticket["priority"].value,
                    "category": ticket["category"].value,
                    "status": ticket["status"].value,
                    "assigned_agent": ticket.get("assigned_agent"),
                    "created_at": ticket["created_at"].isoformat(),
                    "sla_due": ticket["sla_due"].isoformat(),
                    "breach_minutes": breach_minutes,
                    "breach_hours": round(breach_minutes / 60, 1)
                }

                overdue_tickets.append(overdue_ticket)

        # Ordenar por tiempo de breach (más críticos primero)
        overdue_tickets.sort(key=lambda x: x["breach_minutes"], reverse=True)

        return overdue_tickets

    async def reassign_ticket(
            self,
            ticket_id: str,
            new_agent_id: str,
            reason: str = "Manual reassignment"
    ) -> bool:
        """
        🔄 Reasignar ticket a otro agente
        """

        try:
            if ticket_id not in self.tickets:
                logger.error(f"❌ Ticket {ticket_id} no encontrado")
                return False

            if new_agent_id not in self.agents:
                logger.error(f"❌ Agente {new_agent_id} no encontrado")
                return False

            ticket = self.tickets[ticket_id]
            old_agent = ticket.get("assigned_agent")

            # Liberar agente anterior
            if old_agent and old_agent != new_agent_id:
                await self._release_agent(old_agent, ticket_id)

            # Asignar al nuevo agente
            await self._assign_ticket_to_agent(ticket_id, new_agent_id)

            # Agregar nota de reasignación
            await self.add_ticket_note(
                ticket_id,
                f"Ticket reasignado de {old_agent or 'sin asignar'} a {new_agent_id}. Razón: {reason}",
                "system",
                "system_note"
            )

            logger.info(f"🔄 Ticket {ticket_id} reasignado: {old_agent} → {new_agent_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error reasignando ticket {ticket_id}: {str(e)}")
            return False