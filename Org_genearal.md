# 🗂️ Estructura Completa de Archivos - Chatbot Bancario

## 📁 Organización General del Proyecto

```
banking_chatbot/
│
├── 🎨 frontend/                          # Todo lo visual
├── ⚙️ backend/                           # APIs y lógica de negocio  
├── 🗄️ infrastructure/                    # Infraestructura
├── 📊 data/                             # Datos del proyecto
├── 🧪 tests/                            # Testing
├── 📚 docs/                             # Documentación
├── 🔧 scripts/                          # Scripts de automatización
├── ⚙️ config/                           # Configuraciones
└── 📄 Archivos raíz del proyecto
```

---

## 🎨 FRONTEND - Estructura Detallada

### `/frontend/chat-widget/` - Widget del Chat
```
frontend/chat-widget/
├── src/
│   ├── components/
│   │   ├── ChatWidget.js           # ✅ Ya creado - Componente principal
│   │   ├── MessageBubble.js        # Burbujas de mensajes
│   │   ├── InputArea.js            # Área de entrada de texto
│   │   ├── TypingIndicator.js      # Indicador "escribiendo..."
│   │   └── EscalationModal.js      # Modal para escalación
│   ├── services/
│   │   ├── chatApi.js              # Cliente API para chat
│   │   └── websocket.js            # Cliente WebSocket
│   ├── utils/
│   │   ├── constants.js            # Constantes del widget
│   │   └── helpers.js              # Funciones auxiliares
│   ├── styles/
│   │   └── widget.css              # Estilos del widget
│   └── index.js                    # Punto de entrada
├── public/
│   └── embed.js                    # Script de embebido
└── package.json                    # Dependencias del widget
```

### `/frontend/admin-panel/` - Panel Administrativo
```
frontend/admin-panel/
├── src/
│   ├── components/
│   │   ├── Dashboard/
│   │   │   ├── DashboardOverview.js    # ✅ Ya creado - Vista general
│   │   │   ├── MetricsCards.js         # Tarjetas de métricas
│   │   │   └── ChartsSection.js        # Sección de gráficos
│   │   ├── Tickets/
│   │   │   ├── TicketList.js           # ✅ Ya creado - Lista de tickets
│   │   │   ├── TicketDetail.js         # Detalle del ticket
│   │   │   ├── TicketChat.js           # Chat del ticket
│   │   │   └── TicketFilters.js        # Filtros de tickets
│   │   ├── Analytics/
│   │   │   ├── AnalyticsDashboard.js   # Dashboard de analíticas
│   │   │   ├── ConversationAnalytics.js # Análisis de conversaciones
│   │   │   └── AgentPerformance.js     # Performance de agentes
│   │   ├── Settings/
│   │   │   ├── BotConfiguration.js     # Configuración del bot
│   │   │   ├── UserManagement.js       # Gestión de usuarios
│   │   │   └── SystemSettings.js       # Configuración del sistema
│   │   └── Common/
│   │       ├── Header.js               # Header de la aplicación
│   │       ├── Sidebar.js              # Barra lateral
│   │       ├── LoadingSpinner.js       # Indicador de carga
│   │       └── ErrorBoundary.js        # Manejo de errores
│   ├── pages/
│   │   ├── LoginPage.js                # Página de login
│   │   ├── DashboardPage.js            # Página principal
│   │   ├── TicketsPage.js              # Página de tickets
│   │   ├── AnalyticsPage.js            # Página de analíticas
│   │   └── SettingsPage.js             # Página de configuración
│   ├── services/
│   │   ├── api.js                      # Cliente API general
│   │   ├── authService.js              # Servicio de autenticación
│   │   ├── ticketService.js            # Servicio de tickets
│   │   ├── analyticsService.js         # Servicio de analíticas
│   │   └── websocketService.js         # Cliente WebSocket
│   ├── utils/
│   │   ├── constants.js                # Constantes de la aplicación
│   │   ├── formatters.js               # Formateadores de datos
│   │   ├── validators.js               # Validadores
│   │   └── dateUtils.js                # Utilidades de fechas
│   ├── styles/
│   │   ├── globals.css                 # Estilos globales
│   │   └── components/                 # Estilos por componente
│   └── App.js                          # Componente raíz
├── public/
│   ├── index.html                      # HTML base
│   └── manifest.json                   # Manifiesto PWA
└── package.json                        # Dependencias React
```

---

## ⚙️ BACKEND - Estructura Detallada

### `/backend/api/` - FastAPI Gateway
```
backend/api/
├── main.py                         # ✅ Ya creado - Punto de entrada FastAPI
├── routers/
│   ├── __init__.py
│   ├── chat.py                     # ✅ Ya creado - Endpoints de chat
│   ├── auth.py                     # ✅ Ya creado - Autenticación
│   ├── tickets.py                  # ✅ Ya creado - Sistema de tickets
│   ├── analytics.py                # Endpoints de analíticas
│   └── websocket.py                # ✅ Ya creado - WebSocket endpoints
├── middleware/
│   ├── __init__.py
│   ├── auth.py                     # ✅ Ya creado - Middleware de auth
│   ├── rate_limiting.py            # Rate limiting
│   ├── security.py                 # Headers de seguridad
│   └── cors.py                     # Configuración CORS
├── models/
│   ├── __init__.py
│   ├── chat_models.py              # ✅ Ya creado - Modelos de chat
│   ├── ticket_models.py            # Modelos de tickets
│   └── user_models.py              # Modelos de usuario
└── config/
    ├── __init__.py
    ├── settings.py                 # ✅ Ya creado - Configuración general
    └── database.py                 # Configuración base de datos
```

### `/backend/services/` - Servicios Core
```
backend/services/
├── chat/
│   ├── __init__.py
│   ├── chat_service.py             # ✅ Ya creado - Servicio principal de chat
│   ├── session_manager.py          # ✅ Ya creado - Gestión de sesiones
│   └── response_generator.py       # Generación de respuestas
├── rag/
│   ├── __init__.py
│   ├── retriever.py                # ✅ Ya creado - Búsqueda semántica
│   ├── generator.py                # ✅ Ya creado - Generación con LLM
│   ├── embeddings.py               # ✅ Ya creado - Gestión de embeddings
│   └── vector_store.py             # ✅ Ya creado - Vector database
├── nlu/
│   ├── __init__.py
│   ├── intent_classifier.py        # ✅ Ya creado - Clasificación de intents
│   ├── ner.py                      # ✅ Ya creado - Named Entity Recognition
│   └── dialog_manager.py           # ✅ Ya creado - Gestión de diálogos
├── banking/
│   ├── __init__.py
│   ├── core_banking.py             # ✅ Ya creado - APIs del core bancario
│   ├── auth_service.py             # ✅ Ya creado - Autenticación bancaria
│   └── transaction_service.py      # ✅ Ya creado - Servicios de transacciones
├── security/
│   ├── __init__.py
│   ├── dlp.py                      # ✅ Ya creado - Data Loss Prevention
│   ├── encryption.py               # ✅ Ya creado - Encriptación
│   └── audit.py                    # ✅ Ya creado - Auditoría
├── ticketing/
│   ├── __init__.py
│   ├── ticket_service.py           # ✅ Ya creado - Servicio de tickets
│   └── escalation_service.py       # Lógica de escalación
├── websocket/
│   ├── __init__.py
│   ├── ticket_websocket.py         # ✅ Ya creado - WebSocket para tickets
│   └── chat_websocket.py           # WebSocket para chat en tiempo real
├── integration/
│   ├── __init__.py
│   └── chat_ticket_integration.py  # ✅ Ya creado - Integración chat-tickets
└── analytics/
    ├── __init__.py
    ├── metrics_service.py          # Servicio de métricas
    └── reporting_service.py        # Generación de reportes
```

### `/backend/data/` - Gestión de Datos
```
backend/data/
├── ingestion/
│   ├── __init__.py
│   ├── pdf_processor.py            # ✅ Ya creado - Procesamiento de PDFs
│   ├── kb_loader.py                # ✅ Ya creado - Carga de knowledge base
│   └── embeddings_generator.py     # ✅ Ya creado - Generación de embeddings
├── models/
│   ├── __init__.py
│   ├── database.py                 # ✅ Ya creado - Modelos SQLAlchemy
│   ├── vector_store.py             # Modelos para vector DB
│   └── cache.py                    # Modelos para Redis
└── migrations/
    ├── __init__.py
    └── 001_initial_schema.py       # Migración inicial
```

### `/backend/utils/` - Utilidades
```
backend/utils/
├── __init__.py
├── logger.py                       # ✅ Ya creado - Sistema de logging
├── metrics.py                      # ✅ Ya creado - Métricas y monitoreo
├── validators.py                   # Validaciones comunes
├── formatters.py                   # Formateadores de datos
├── notifications.py                # ✅ Ya creado - Sistema de notificaciones
└── helpers.py                      # Funciones auxiliares
```

---

## 🗄️ INFRASTRUCTURE - Infraestructura

### `/infrastructure/docker/` - Containerización
```
infrastructure/docker/
├── Dockerfile.api                  # Dockerfile para FastAPI
├── Dockerfile.frontend             # Dockerfile para React
├── Dockerfile.worker              # Dockerfile para workers
├── docker-compose.yml              # Composición completa
├── docker-compose.dev.yml          # Desarrollo
└── docker-compose.prod.yml         # Producción
```

### `/infrastructure/kubernetes/` - Orchestración
```
infrastructure/kubernetes/
├── deployments/
│   ├── api-deployment.yaml         # Deployment de API
│   ├── frontend-deployment.yaml    # Deployment de frontend
│   └── worker-deployment.yaml      # Deployment de workers
├── services/
│   ├── api-service.yaml            # Servicio de API
│   └── frontend-service.yaml       # Servicio de frontend
├── configmaps/
│   ├── app-config.yaml             # ConfigMap de aplicación
│   └── nginx-config.yaml           # ConfigMap de Nginx
└── secrets/
    └── app-secrets.yaml.template   # Template de secretos
```

### `/infrastructure/terraform/` - Infrastructure as Code
```
infrastructure/terraform/
├── main.tf                         # Configuración principal
├── variables.tf                    # Variables
├── outputs.tf                      # Outputs
├── modules/
│   ├── database/                   # Módulo de base de datos
│   ├── cache/                      # Módulo de cache (Redis)
│   └── monitoring/                 # Módulo de monitoreo
└── environments/
    ├── dev.tfvars                  # Variables de desarrollo
    ├── staging.tfvars              # Variables de staging
    └── prod.tfvars                 # Variables de producción
```

---

## 📊 DATA - Datos del Proyecto

### `/data/documents/` - Documentos del Banco
```
data/documents/
├── products/
│   ├── cuentas_ahorro.pdf          # Información de cuentas
│   ├── tarjetas_credito.pdf        # Info de tarjetas
│   └── prestamos.pdf               # Info de préstamos
├── procedures/
│   ├── apertura_cuenta.pdf         # Procedimientos
│   └── solicitud_credito.pdf       # Solicitudes
└── faqs/
    ├── general.json                # FAQ general
    └── por_producto.json           # FAQ por producto
```

### `/data/training/` - Datos de Entrenamiento
```
data/training/
├── intents.json                    # Intenciones etiquetadas
├── entities.json                   # Entidades nombradas
├── conversations.json              # Conversaciones ejemplo
└── knowledge_base/
    ├── productos.txt               # Base de conocimiento productos
    ├── procedimientos.txt          # Base de conocimiento procedimientos
    └── regulaciones.txt            # Información regulatoria
```

---

## 🧪 TESTS - Testing

### `/tests/` - Estructura de Pruebas
```
tests/
├── unit/
│   ├── test_chat_service.py        # Tests del servicio de chat
│   ├── test_rag_service.py         # Tests del sistema RAG
│   ├── test_ticket_service.py      # Tests del sistema de tickets
│   └── test_security.py            # Tests de seguridad
├── integration/
│   ├── test_chat_flow.py           # Tests de flujo completo
│   ├── test_banking_integration.py # Tests de integración bancaria
│   └── test_websocket.py           # Tests de WebSocket
├── e2e/
│   ├── test_complete_conversation.py # Tests end-to-end
│   └── test_ticket_escalation.py   # Tests de escalación
├── security/
│   ├── test_authentication.py      # Tests de autenticación
│   ├── test_dlp.py                 # Tests de DLP
│   └── test_audit.py               # Tests de auditoría
├── fixtures/
│   ├── chat_data.json              # Datos de prueba
│   └── mock_responses.json         # Respuestas simuladas
└── conftest.py                     # Configuración de pytest
```

---

## 🔧 SCRIPTS - Automatización

### `/scripts/` - Scripts de Automatización
```
scripts/
├── setup/
│   ├── install_dependencies.sh     # Instalación de dependencias
│   ├── setup_database.py           # Configuración de BD
│   └── generate_sample_data.py     # Datos de prueba
├── deployment/
│   ├── deploy.sh                   # Script de despliegue
│   ├── rollback.sh                 # Script de rollback
│   └── health_check.py             # Verificación de salud
├── maintenance/
│   ├── backup_data.py              # Backup de datos
│   ├── clean_logs.py               # Limpieza de logs
│   └── update_embeddings.py        # Actualización de embeddings
└── monitoring/
    ├── check_services.py           # Verificación de servicios
    └── generate_reports.py         # Generación de reportes
```

---

## ⚙️ CONFIG - Configuraciones

### `/config/` - Archivos de Configuración
```
config/
├── development.yaml                # Configuración de desarrollo
├── staging.yaml                    # Configuración de staging
├── production.yaml                 # Configuración de producción
├── secrets.yaml.template           # Template de secretos
├── logging.yaml                    # Configuración de logging
└── monitoring.yaml                 # Configuración de monitoreo
```

---

## 📄 Archivos Raíz del Proyecto

```
banking_chatbot/
├── requirements.txt                # Dependencias Python
├── package.json                   # Dependencias Node.js
├── docker-compose.yml             # Docker compose principal
├── Makefile                       # Comandos automatizados
├── .env.template                  # Template de variables de entorno
├── .gitignore                     # Archivos a ignorar en Git
├── .dockerignore                  # Archivos a ignorar en Docker
├── README.md                      # Documentación principal
├── CHANGELOG.md                   # Historial de cambios
├── LICENSE                        # Licencia del proyecto
└── pyproject.toml                 # Configuración de Python
```

---

## 🚀 Comandos de Desarrollo Recomendados

### Makefile con comandos útiles:
```makefile
.PHONY: install dev test build deploy clean

# Instalación
install:
    pip install -r requirements.txt
    npm install --prefix frontend

# Desarrollo
dev:
    docker-compose -f docker-compose.dev.yml up

# Tests
test:
    pytest tests/ -v --cov=backend

# Build
build:
    docker-compose build

# Deploy
deploy:
    ./scripts/deployment/deploy.sh

# Limpieza
clean:
    docker-compose down -v
    docker system prune -f
```

---

## 📋 Resumen de Archivos Creados vs Pendientes

### ✅ **YA CREADOS** (Artefactos entregados):
- Frontend: ChatWidget, Admin Panel, Sistema de Tickets
- Backend: Servicios de Chat, RAG, NLU, Seguridad, Banking, Tickets
- WebSocket: Sistema completo de tiempo real
- Configuración: Settings, Database, Auth
- Integraciones: Chat-Ticket integration

### 📝 **PENDIENTES** (Para implementar):
- Scripts de deployment y mantenimiento
- Archivos de configuración por ambiente
- Tests unit