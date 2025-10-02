// Helper functions para el Chat Widget
import { MAX_FILE_SIZE, ALLOWED_FILE_TYPES, ERROR_MESSAGES } from './constants';

/**
 * Genera un ID único
 */
export const generateId = () => {
    return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

/**
 * Formatea fecha a string legible
 */
export const formatDate = (date) => {
    const d = new Date(date);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    if (d.toDateString() === today.toDateString()) {
        return 'Hoy';
    } else if (d.toDateString() === yesterday.toDateString()) {
        return 'Ayer';
    } else {
        return d.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        });
    }
};

/**
 * Formatea hora
 */
export const formatTime = (date) => {
    const d = new Date(date);
    return d.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
};

/**
 * Formatea fecha y hora completa
 */
export const formatDateTime = (date) => {
    return `${formatDate(date)} ${formatTime(date)}`;
};

/**
 * Valida archivo
 */
export const validateFile = (file) => {
    if (!file) {
        return { valid: false, error: 'No se seleccionó ningún archivo' };
    }

    if (file.size > MAX_FILE_SIZE) {
        return { valid: false, error: ERROR_MESSAGES.FILE_TOO_LARGE };
    }

    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
        return { valid: false, error: ERROR_MESSAGES.FILE_TYPE_NOT_ALLOWED };
    }

    return { valid: true };
};

/**
 * Formatea tamaño de archivo
 */
export const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

/**
 * Detecta si el texto contiene URL
 */
export const containsUrl = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return urlRegex.test(text);
};

/**
 * Convierte URLs en texto a links clickeables
 */
export const linkifyText = (text) => {
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, (url) => {
        return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
    });
};

/**
 * Sanitiza HTML para prevenir XSS
 */
export const sanitizeHtml = (html) => {
    const temp = document.createElement('div');
    temp.textContent = html;
    return temp.innerHTML;
};

/**
 * Trunca texto largo
 */
export const truncateText = (text, maxLength = 100) => {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
};

/**
 * Detecta si es dispositivo móvil
 */
export const isMobile = () => {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
};

/**
 * Detecta tema del sistema (dark/light)
 */
export const getSystemTheme = () => {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
};

/**
 * Guarda en localStorage con manejo de errores
 */
export const saveToStorage = (key, value) => {
    try {
        localStorage.setItem(key, JSON.stringify(value));
        return true;
    } catch (error) {
        console.error('Error guardando en localStorage:', error);
        return false;
    }
};

/**
 * Lee de localStorage con manejo de errores
 */
export const loadFromStorage = (key, defaultValue = null) => {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : defaultValue;
    } catch (error) {
        console.error('Error leyendo de localStorage:', error);
        return defaultValue;
    }
};

/**
 * Remueve de localStorage
 */
export const removeFromStorage = (key) => {
    try {
        localStorage.removeItem(key);
        return true;
    } catch (error) {
        console.error('Error removiendo de localStorage:', error);
        return false;
    }
};

/**
 * Debounce function
 */
export const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

/**
 * Throttle function
 */
export const throttle = (func, limit) => {
    let inThrottle;
    return function executedFunction(...args) {
        if (!inThrottle) {
            func(...args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
};

/**
 * Scroll al final del contenedor
 */
export const scrollToBottom = (element, smooth = true) => {
    if (!element) return;

    element.scrollTo({
        top: element.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto'
    });
};

/**
 * Copia texto al clipboard
 */
export const copyToClipboard = async (text) => {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (error) {
        console.error('Error copiando al clipboard:', error);
        return false;
    }
};

/**
 * Genera color avatar basado en string
 */
export const getAvatarColor = (str) => {
    const colors = [
        '#1976d2', '#388e3c', '#d32f2f', '#7b1fa2',
        '#f57c00', '#0097a7', '#c2185b', '#512da8'
    ];

    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }

    return colors[Math.abs(hash) % colors.length];
};

/**
 * Formatea número con separadores de miles
 */
export const formatNumber = (num) => {
    return new Intl.NumberFormat('es-ES').format(num);
};

/**
 * Formatea moneda
 */
export const formatCurrency = (amount, currency = 'USD') => {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: currency
    }).format(amount);
};

/**
 * Valida email
 */
export const isValidEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
};

/**
 * Extrae iniciales de nombre
 */
export const getInitials = (name) => {
    if (!name) return '?';

    const parts = name.trim().split(' ');
    if (parts.length === 1) {
        return parts[0].charAt(0).toUpperCase();
    }

    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
};