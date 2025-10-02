// frontend/admin-panel/src/utils/formatters.js

/**
 * Format date to string
 */
export const formatDate = (date, format = 'full') => {
    if (!date) return '';

    const d = new Date(date);
    if (isNaN(d.getTime())) return '';

    const pad = (num) => String(num).padStart(2, '0');

    const day = pad(d.getDate());
    const month = pad(d.getMonth() + 1);
    const year = d.getFullYear();
    const hours = pad(d.getHours());
    const minutes = pad(d.getMinutes());
    const seconds = pad(d.getSeconds());

    switch (format) {
        case 'date':
            return `${day}/${month}/${year}`;
        case 'time':
            return `${hours}:${minutes}`;
        case 'datetime':
            return `${day}/${month}/${year} ${hours}:${minutes}`;
        case 'full':
        default:
            return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
    }
};

/**
 * Format relative time (e.g., "hace 5 minutos")
 */
export const formatRelativeTime = (date) => {
    if (!date) return '';

    const now = new Date();
    const past = new Date(date);
    const diffMs = now - past;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHour / 24);

    if (diffSec < 60) return 'ahora mismo';
    if (diffMin < 60) return `hace ${diffMin} min`;
    if (diffHour < 24) return `hace ${diffHour} hora${diffHour !== 1 ? 's' : ''}`;
    if (diffDay < 7) return `hace ${diffDay} día${diffDay !== 1 ? 's' : ''}`;
    if (diffDay < 30) return `hace ${Math.floor(diffDay / 7)} semana${Math.floor(diffDay / 7) !== 1 ? 's' : ''}`;
    if (diffDay < 365) return `hace ${Math.floor(diffDay / 30)} mes${Math.floor(diffDay / 30) !== 1 ? 'es' : ''}`;
    return `hace ${Math.floor(diffDay / 365)} año${Math.floor(diffDay / 365) !== 1 ? 's' : ''}`;
};

/**
 * Format number with thousands separator
 */
export const formatNumber = (num) => {
    if (num === null || num === undefined) return '0';
    return new Intl.NumberFormat('es-ES').format(num);
};

/**
 * Format currency
 */
export const formatCurrency = (amount, currency = 'USD') => {
    if (amount === null || amount === undefined) return '$0.00';

    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: currency
    }).format(amount);
};

/**
 * Format percentage
 */
export const formatPercentage = (value, decimals = 1) => {
    if (value === null || value === undefined) return '0%';
    return `${Number(value).toFixed(decimals)}%`;
};

/**
 * Format file size
 */
export const formatFileSize = (bytes) => {
    if (!bytes || bytes === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));

    return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
};

/**
 * Format duration (seconds to human readable)
 */
export const formatDuration = (seconds) => {
    if (!seconds || seconds === 0) return '0 seg';

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    const parts = [];
    if (hours > 0) parts.push(`${hours}h`);
    if (minutes > 0) parts.push(`${minutes}m`);
    if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);

    return parts.join(' ');
};

/**
 * Format phone number
 */
export const formatPhoneNumber = (phone) => {
    if (!phone) return '';

    const cleaned = phone.replace(/\D/g, '');

    if (cleaned.length === 10) {
        return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }

    return phone;
};

/**
 * Truncate text
 */
export const truncateText = (text, maxLength = 100) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return `${text.slice(0, maxLength)}...`;
};

/**
 * Capitalize first letter
 */
export const capitalize = (str) => {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
};

/**
 * Convert camelCase to Title Case
 */
export const camelToTitle = (str) => {
    if (!str) return '';
    return str
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, (str) => str.toUpperCase())
        .trim();
};

/**
 * Format ticket ID
 */
export const formatTicketId = (id) => {
    if (!id) return '';
    return `#${String(id).padStart(6, '0')}`;
};

/**
 * Get initials from name
 */
export const getInitials = (name) => {
    if (!name) return '?';

    const parts = name.trim().split(' ');
    if (parts.length === 1) {
        return parts[0].charAt(0).toUpperCase();
    }

    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
};

/**
 * Format array to comma-separated string
 */
export const formatList = (arr, separator = ', ', lastSeparator = ' y ') => {
    if (!arr || arr.length === 0) return '';
    if (arr.length === 1) return arr[0];

    const allButLast = arr.slice(0, -1).join(separator);
    const last = arr[arr.length - 1];

    return `${allButLast}${lastSeparator}${last}`;
};

/**
 * Format boolean to Yes/No
 */
export const formatBoolean = (value) => {
    return value ? 'Sí' : 'No';
};

/**
 * Format status label
 */
export const formatStatusLabel = (status) => {
    const statusLabels = {
        open: 'Abierto',
        in_progress: 'En Progreso',
        waiting: 'Esperando',
        resolved: 'Resuelto',
        closed: 'Cerrado',
        active: 'Activo',
        inactive: 'Inactivo'
    };

    return statusLabels[status] || capitalize(status);
};

/**
 * Format priority label
 */
export const formatPriorityLabel = (priority) => {
    const priorityLabels = {
        low: 'Baja',
        medium: 'Media',
        high: 'Alta',
        urgent: 'Urgente'
    };

    return priorityLabels[priority] || capitalize(priority);
};

/**
 * Format satisfaction score
 */
export const formatSatisfactionScore = (score) => {
    if (score === null || score === undefined) return 'N/A';
    const stars = '⭐'.repeat(Math.round(score));
    return `${stars} ${score.toFixed(1)}`;
};

/**
 * Format IP address (mask partially)
 */
export const formatIPAddress = (ip, mask = true) => {
    if (!ip) return '';
    if (!mask) return ip;

    const parts = ip.split('.');
    if (parts.length !== 4) return ip;

    return `${parts[0]}.${parts[1]}.xxx.xxx`;
};

/**
 * Format error message for display
 */
export const formatErrorMessage = (error) => {
    if (typeof error === 'string') return error;
    if (error.message) return error.message;
    if (error.error) return error.error;
    return 'Ha ocurrido un error inesperado';
};