// Constantes del Chat Widget

export const MESSAGE_STATUS = {
    SENDING: 'sending',
    SENT: 'sent',
    DELIVERED: 'delivered',
    READ: 'read',
    ERROR: 'error'
};

export const MESSAGE_TYPES = {
    TEXT: 'text',
    IMAGE: 'image',
    FILE: 'file',
    QUICK_REPLY: 'quick_reply',
    CARD: 'card',
    SYSTEM: 'system'
};

export const CONVERSATION_STATUS = {
    ACTIVE: 'active',
    WAITING: 'waiting',
    ESCALATED: 'escalated',
    CLOSED: 'closed'
};

export const WIDGET_POSITION = {
    BOTTOM_RIGHT: 'bottom-right',
    BOTTOM_LEFT: 'bottom-left',
    TOP_RIGHT: 'top-right',
    TOP_LEFT: 'top-left'
};

export const THEME = {
    LIGHT: 'light',
    DARK: 'dark',
    AUTO: 'auto'
};

export const PRIORITIES = {
    LOW: 'low',
    MEDIUM: 'medium',
    HIGH: 'high',
    URGENT: 'urgent'
};

export const CATEGORIES = {
    GENERAL: 'general',
    TECHNICAL: 'technical',
    ACCOUNT: 'account',
    TRANSACTION: 'transaction',
    LOAN: 'loan',
    CARD: 'card',
    COMPLAINT: 'complaint',
    OTHER: 'other'
};

export const MAX_MESSAGE_LENGTH = 1000;
export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
export const ALLOWED_FILE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf', 'application/msword'];

export const TYPING_TIMEOUT = 2000; // ms
export const MESSAGE_SEND_DELAY = 500; // ms para simular typing del bot

export const ERROR_MESSAGES = {
    NETWORK_ERROR: 'Error de conexión. Por favor verifica tu internet.',
    SERVER_ERROR: 'Error del servidor. Intenta nuevamente.',
    FILE_TOO_LARGE: 'El archivo es demasiado grande. Máximo 10MB.',
    FILE_TYPE_NOT_ALLOWED: 'Tipo de archivo no permitido.',
    MESSAGE_TOO_LONG: 'El mensaje es demasiado largo. Máximo 1000 caracteres.',
    CONVERSATION_CLOSED: 'La conversación ha finalizado.',
    ESCALATION_FAILED: 'Error al escalar la conversación. Intenta nuevamente.'
};

export const DEFAULT_CONFIG = {
    position: WIDGET_POSITION.BOTTOM_RIGHT,
    theme: THEME.LIGHT,
    primaryColor: '#1976d2',
    headerText: 'Chat Bancario',
    welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
    placeholderText: 'Escribe tu mensaje...',
    enableFileUpload: true,
    enableEscalation: true,
    autoOpen: false,
    soundEnabled: true
};

export const WEBSOCKET_EVENTS = {
    CONNECTED: 'connected',
    DISCONNECTED: 'disconnected',
    MESSAGE: 'message',
    TYPING: 'typing',
    AGENT_JOINED: 'agent_joined',
    AGENT_LEFT: 'agent_left',
    CONVERSATION_ESCALATED: 'conversation_escalated',
    CONVERSATION_CLOSED: 'conversation_closed',
    ERROR: 'error'
};