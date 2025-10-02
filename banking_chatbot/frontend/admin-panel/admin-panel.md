# 🏦 Banking ChatBot - Admin Panel

Panel de administración completo para gestionar el chatbot bancario, tickets, conversaciones, analytics y configuración del sistema.

## 📋 Características

- ✅ **Dashboard** - Vista general con métricas en tiempo real
- 🎫 **Gestión de Tickets** - Sistema completo de tickets con filtros y estados
- 💬 **Conversaciones** - Monitor de conversaciones activas en tiempo real
- 📊 **Analytics** - Análisis detallado de rendimiento y métricas
- 👥 **Clientes** - Gestión de base de datos de clientes
- 📚 **Base de Conocimiento** - Artículos y documentación para el bot
- ⚙️ **Configuración** - Configuración del bot, usuarios y sistema

## 🚀 Instalación

### Prerrequisitos

- Node.js 18+ y npm/yarn
- Backend API corriendo en `http://localhost:8000`

### Pasos de Instalación

```bash
# 1. Navegar al directorio
cd frontend/admin-panel

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp .env.template .env
# Editar .env con tus configuraciones

# 4. Iniciar en desarrollo
npm run dev

# 5. Build para producción
npm run build
```

## 📁 Estructura del Proyecto

```
admin-panel/
├── src/
│   ├── components/
│   │   ├── Common/          # Componentes compartidos
│   │   ├── Dashboard/       # Componentes del dashboard
│   │   ├── Tickets/         # Componentes de tickets
│   │   ├── Analytics/       # Componentes de analytics
│   │   └── Settings/        # Componentes de configuración
│   ├── pages/              # Páginas principales
│   ├── services/           # Servicios API y WebSocket
│   ├── utils/              # Utilidades y helpers
│   ├── styles/             # Estilos CSS
│   └── App.jsx             # Componente raíz
├── package.json
├── vite.config.js
└── index.html
```

## 🔧 Configuración

### Variables de Entorno (.env)

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME="Banking ChatBot Admin"
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_WEBSOCKET=true
```

## 📖 Uso

### Login

```
Email: admin@banco.com
Password: admin123
```

### Navegación Principal

- **Dashboard** (`/dashboard`) - Vista general del sistema
- **Tickets** (`/tickets`) - Gestión de tickets de soporte
- **Conversaciones** (`/conversations`) - Monitor de conversaciones
- **Analytics** (`/analytics`) - Métricas y reportes
- **Clientes** (`/customers`) - Base de datos de clientes
- **Base de Conocimiento** (`/knowledge`) - Artículos y documentación
- **Configuración** (`/settings`) - Configuración del sistema

## 🎨 Componentes Principales

### Dashboard
- MetricsCards - Tarjetas de métricas
- ChartsSection - Gráficos y estadísticas

### Tickets
- TicketList - Lista de tickets
- TicketDetail - Detalle de ticket
- TicketChat - Chat de ticket
- TicketFilters - Filtros avanzados

### Analytics
- AnalyticsDashboard - Dashboard de analytics
- ConversationAnalytics - Análisis de conversaciones
- AgentPerformance - Performance de agentes

### Settings
- BotConfiguration - Configuración del bot
- UserManagement - Gestión de usuarios
- SystemSettings - Configuración del sistema

## 🔌 API Integration

### Endpoints Principales

```javascript
// Auth
POST /api/v1/auth/login
POST /api/v1/auth/logout
GET  /api/v1/auth/verify

// Tickets
GET    /api/v1/tickets
POST   /api/v1/tickets
GET    /api/v1/tickets/:id
PUT    /api/v1/tickets/:id
DELETE /api/v1/tickets/:id

// Analytics
GET /api/v1/analytics/dashboard
GET /api/v1/analytics/conversations
GET /api/v1/analytics/agents

// Customers
GET    /api/v1/customers
POST   /api/v1/customers
GET    /api/v1/customers/:id
PUT    /api/v1/customers/:id
```

### WebSocket Events

```javascript
// Conectar
websocketService.connect()

// Escuchar eventos
websocketService.on('ticket_created', (data) => {})
websocketService.on('new_message', (data) => {})
websocketService.on('agent_status_changed', (data) => {})
```

## 🧪 Testing

```bash
# Ejecutar tests
npm run test

# Tests con coverage
npm run test:coverage

# Tests en modo watch
npm run test:watch
```

## 📦 Build y Deploy

```bash
# Build para producción
npm run build

# Preview del build
npm run preview

# Lint del código
npm run lint

# Format código
npm run format
```

## 🐳 Docker

```bash
# Build imagen
docker build -t banking-chatbot-admin .

# Ejecutar contenedor
docker run -p 3000:80 banking-chatbot-admin
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

MIT License - ver archivo LICENSE para más detalles

## 👥 Soporte

Para soporte y preguntas:
- Email: support@banco.com
- Documentación: https://docs.chatbot.banco.com

---

Desarrollado con ❤️ por Tu Empresa