// frontend/admin-panel/src/utils/constants.js

// Ticket Status
export const TICKET_STATUS = {
    OPEN: 'open',
    IN_PROGRESS: 'in_progress',
    WAITING: 'waiting',
    RESOLVED: 'resolved',
    CLOSED: 'closed'
};

export const TICKET_STATUS_LABELS = {
    [TICKET_STATUS.OPEN]: 'Abierto',
    [TICKET_STATUS.IN_PROGRESS]: 'En Progreso',
    [TICKET_STATUS.WAITING]: 'Esperando',
    [TICKET_STATUS.RESOLVED]: 'Resuelto',
    [TICKET_STATUS.CLOSED]: 'Cerrado'
};

export const TICKET_STATUS_COLORS = {
    [TICKET_STATUS.OPEN]: '#f093fb',
    [TICKET_STATUS.IN_PROGRESS]: '#4facfe',
    [TICKET_STATUS.WAITING]: '#feca57',
    [TICKET_STATUS.RESOLVED]: '#43e97b',
    [TICKET_STATUS.CLOSED]: '#95a5a6'
};

// Ticket Priority
export const TICKET_PRIORITY = {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    URGENT: 'urgent'
};

export const TICKET_PRIORITY_LABELS = {
    [TICKET_PRIORITY.LOW]: 'Baja',
    [TICKET_PRIORITY.MEDIUM]: 'Media',
    [TICKET_PRIORITY.HIGH]: 'Alta',
    [TICKET_PRIORITY.URGENT]: 'Urgente'
};

export const TICKET_PRIORITY_COLORS = {
    [TICKET_PRIORITY.LOW]: '#4CAF50',
    [TICKET_PRIORITY.MEDIUM]: '#FF9800',
    [TICKET_PRIORITY.HIGH]: '#F44336',
    [TICKET_PRIORITY.URGENT]: '#9C27B0'
};

// Ticket Categories
export const TICKET_CATEGORIES = {
    GENERAL: 'general',
    TECHNICAL: 'technical',
    ACCOUNT: 'account',
    TRANSACTION: 'transaction',
    LOAN: 'loan',
    CARD: 'card',
    COMPLAINT: 'complaint',
    OTHER: 'other'
};

export const TICKET_CATEGORY_LABELS = {
    [TICKET_CATEGORIES.GENERAL]: 'Consulta General',
    [TICKET_CATEGORIES.TECHNICAL]: 'Problema Técnico',
    [TICKET_CATEGORIES.ACCOUNT]: 'Gestión de Cuenta',
    [TICKET_CATEGORIES.TRANSACTION]: 'Transacciones',
    [TICKET_CATEGORIES.LOAN]: 'Préstamos/Créditos',
    [TICKET_CATEGORIES.CARD]: 'Tarjetas',
    [TICKET_CATEGORIES.COMPLAINT]: 'Reclamo',
    [TICKET_CATEGORIES.OTHER]: 'Otro'
};

// User Roles
export const USER_ROLES = {
    ADMIN: 'admin',
    SUPERVISOR: 'supervisor',
    AGENT: 'agent',
    VIEWER: 'viewer'
};

export const USER_ROLE_LABELS = {
    [USER_ROLES.ADMIN]: 'Administrador',
    [USER_ROLES.SUPERVISOR]: 'Supervisor',
    [USER_ROLES.AGENT]: 'Agente',
    [USER_ROLES.VIEWER]: 'Observador'
};

// User Status
export const USER_STATUS = {
    ACTIVE: 'active',
    INACTIVE: 'inactive',
    SUSPENDED: 'suspended'
};

// Agent Status
export const AGENT_STATUS = {
    ONLINE: 'online',
    AWAY: 'away',
    BUSY: 'busy',
    OFFLINE: 'offline'
};

export const AGENT_STATUS_LABELS = {
    [AGENT_STATUS.ONLINE]: 'En línea',
    [AGENT_STATUS.AWAY]: 'Ausente',
    [AGENT_STATUS.BUSY]: 'Ocupado',
    [AGENT_STATUS.OFFLINE]: 'Desconectado'
};

export const AGENT_STATUS_COLORS = {
    [AGENT_STATUS.ONLINE]: '#43e97b',
    [AGENT_STATUS.AWAY]: '#feca57',
    [AGENT_STATUS.BUSY]: '#ff6b6b',
    [AGENT_STATUS.OFFLINE]: '#95a5a6'
};

// Conversation Status
export const CONVERSATION_STATUS = {
    ACTIVE: 'active',
    WAITING: 'waiting',
    ESCALATED: 'escalated',
    CLOSED: 'closed'
};

// Message Types
export const MESSAGE_TYPES = {
    TEXT: 'text',
    IMAGE: 'image',
    FILE: 'file',
    SYSTEM: 'system'
};

// Analytics Periods
export const ANALYTICS_PERIODS = {
    TODAY: 'today',
    YESTERDAY: 'yesterday',
    WEEK: 'week',
    MONTH: 'month',
    QUARTER: 'quarter',
    YEAR: 'year',
    CUSTOM: 'custom'
};

export const ANALYTICS_PERIOD_LABELS = {
    [ANALYTICS_PERIODS.TODAY]: 'Hoy',
    [ANALYTICS_PERIODS.YESTERDAY]: 'Ayer',
    [ANALYTICS_PERIODS.WEEK]: 'Esta Semana',
    [ANALYTICS_PERIODS.MONTH]: 'Este Mes',
    [ANALYTICS_PERIODS.QUARTER]: 'Este Trimestre',
    [ANALYTICS_PERIODS.YEAR]: 'Este Año',
    [ANALYTICS_PERIODS.CUSTOM]: 'Personalizado'
};

// Notification Types
export const NOTIFICATION_TYPES = {
    TICKET: 'ticket',
    MESSAGE: 'message',
    ESCALATION: 'escalation',
    SYSTEM: 'system',
    ALERT: 'alert'
};

// WebSocket Events
export const WS_EVENTS = {
    CONNECTED: 'connected',
    DISCONNECTED: 'disconnected',
    MESSAGE: 'message',
    TICKET_CREATED: 'ticket_created',
    TICKET_UPDATED: 'ticket_updated',
    TICKET_ASSIGNED: 'ticket_assigned',
    NEW_MESSAGE: 'new_message',
    TYPING: 'typing',
    AGENT_STATUS_CHANGED: 'agent_status_changed',
    STATS_UPDATE: 'stats_update',
    ERROR: 'error'
};

// Date Formats
export const DATE_FORMATS = {
    FULL: 'DD/MM/YYYY HH:mm:ss',
    DATE: 'DD/MM/YYYY',
    TIME: 'HH:mm',
    DATETIME: 'DD/MM/YYYY HH:mm',
    ISO: 'YYYY-MM-DDTHH:mm:ss'
};

// Pagination
export const PAGINATION = {
    DEFAULT_PAGE_SIZE: 20,
    PAGE_SIZE_OPTIONS: [10, 20, 50, 100]
};

// File Upload
export const FILE_UPLOAD = {
    MAX_SIZE: 10 * 1024 * 1024, // 10MB
    ALLOWED_TYPES: ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword'],
    ALLOWED_EXTENSIONS: ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']
};

// Local Storage Keys
export const STORAGE_KEYS = {
    TOKEN: 'token',
    USER: 'user',
    THEME: 'theme',
    SIDEBAR_COLLAPSED: 'sidebarCollapsed',
    FILTERS: 'filters',
    TABLE_PREFERENCES: 'tablePreferences'
};

// API Endpoints
export const API_ENDPOINTS = {
    AUTH: '/auth',
    TICKETS: '/tickets',
    CONVERSATIONS: '/conversations',
    ANALYTICS: '/analytics',
    USERS: '/users',
    AGENTS: '/agents',
    SETTINGS: '/settings'
};

// Error Messages
export const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Error de red. Por favor verifica tu conexión.',
    SERVER_ERROR: 'Error del servidor. Intenta nuevamente.',
    UNAUTHORIZED: 'No autorizado. Por favor inicia sesión nuevamente.',
    FORBIDDEN: 'No tienes permisos para realizar esta acción.',
    NOT_FOUND: 'Recurso no encontrado.',
    VALIDATION_ERROR: 'Error de validación. Verifica los datos ingresados.',
    UNKNOWN_ERROR: 'Ha ocurrido un error inesperado.'
};

// Success Messages
export const SUCCESS_MESSAGES = {
    SAVED: 'Guardado exitosamente',
    UPDATED: 'Actualizado exitosamente',
    DELETED: 'Eliminado exitosamente',
    CREATED: 'Creado exitosamente',
    SENT: 'Enviado exitosamente'
};