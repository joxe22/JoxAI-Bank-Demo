// frontend/admin-panel/src/utils/validators.js

/**
 * Validate email address
 */
export const isValidEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
};

/**
 * Validate password strength
 */
export const validatePassword = (password) => {
    const errors = [];

    if (password.length < 8) {
        errors.push('La contraseña debe tener al menos 8 caracteres');
    }

    if (!/[A-Z]/.test(password)) {
        errors.push('Debe contener al menos una letra mayúscula');
    }

    if (!/[a-z]/.test(password)) {
        errors.push('Debe contener al menos una letra minúscula');
    }

    if (!/[0-9]/.test(password)) {
        errors.push('Debe contener al menos un número');
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        errors.push('Debe contener al menos un carácter especial');
    }

    return {
        isValid: errors.length === 0,
        errors
    };
};

/**
 * Validate phone number
 */
export const isValidPhone = (phone) => {
    const cleaned = phone.replace(/\D/g, '');
    return cleaned.length >= 10 && cleaned.length <= 15;
};

/**
 * Validate URL
 */
export const isValidURL = (url) => {
    try {
        new URL(url);
        return true;
    } catch {
        return false;
    }
};

/**
 * Validate IP address
 */
export const isValidIP = (ip) => {
    const ipRegex = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipRegex.test(ip)) return false;

    return ip.split('.').every(part => {
        const num = parseInt(part, 10);
        return num >= 0 && num <= 255;
    });
};

/**
 * Validate file type
 */
export const isValidFileType = (file, allowedTypes) => {
    if (!file || !allowedTypes) return false;

    return allowedTypes.some(type => {
        if (type.includes('*')) {
            const baseType = type.split('/')[0];
            return file.type.startsWith(baseType);
        }
        return file.type === type;
    });
};

/**
 * Validate file size
 */
export const isValidFileSize = (file, maxSizeInBytes) => {
    if (!file) return false;
    return file.size <= maxSizeInBytes;
};

/**
 * Validate required field
 */
export const isRequired = (value) => {
    if (value === null || value === undefined) return false;
    if (typeof value === 'string') return value.trim().length > 0;
    if (Array.isArray(value)) return value.length > 0;
    return true;
};

/**
 * Validate min length
 */
export const hasMinLength = (value, minLength) => {
    if (!value) return false;
    return String(value).length >= minLength;
};

/**
 * Validate max length
 */
export const hasMaxLength = (value, maxLength) => {
    if (!value) return true;
    return String(value).length <= maxLength;
};

/**
 * Validate number range
 */
export const isInRange = (value, min, max) => {
    const num = Number(value);
    if (isNaN(num)) return false;
    return num >= min && num <= max;
};

/**
 * Validate date is in the past
 */
export const isPastDate = (date) => {
    const inputDate = new Date(date);
    const now = new Date();
    return inputDate < now;
};

/**
 * Validate date is in the future
 */
export const isFutureDate = (date) => {
    const inputDate = new Date(date);
    const now = new Date();
    return inputDate > now;
};

/**
 * Validate credit card number (Luhn algorithm)
 */
export const isValidCreditCard = (cardNumber) => {
    const cleaned = cardNumber.replace(/\D/g, '');

    if (cleaned.length < 13 || cleaned.length > 19) return false;

    let sum = 0;
    let isEven = false;

    for (let i = cleaned.length - 1; i >= 0; i--) {
        let digit = parseInt(cleaned[i], 10);

        if (isEven) {
            digit *= 2;
            if (digit > 9) digit -= 9;
        }

        sum += digit;
        isEven = !isEven;
    }

    return sum % 10 === 0;
};

/**
 * Validate form data
 */
export const validateForm = (data, rules) => {
    const errors = {};

    Object.keys(rules).forEach(field => {
        const value = data[field];
        const fieldRules = rules[field];

        if (fieldRules.required && !isRequired(value)) {
            errors[field] = fieldRules.requiredMessage || 'Este campo es requerido';
            return;
        }

        if (fieldRules.email && value && !isValidEmail(value)) {
            errors[field] = fieldRules.emailMessage || 'Email inválido';
            return;
        }

        if (fieldRules.minLength && value && !hasMinLength(value, fieldRules.minLength)) {
            errors[field] = fieldRules.minLengthMessage || `Mínimo ${fieldRules.minLength} caracteres`;
            return;
        }

        if (fieldRules.maxLength && value && !hasMaxLength(value, fieldRules.maxLength)) {
            errors[field] = fieldRules.maxLengthMessage || `Máximo ${fieldRules.maxLength} caracteres`;
            return;
        }

        if (fieldRules.pattern && value && !fieldRules.pattern.test(value)) {
            errors[field] = fieldRules.patternMessage || 'Formato inválido';
            return;
        }

        if (fieldRules.custom && value) {
            const customError = fieldRules.custom(value, data);
            if (customError) {
                errors[field] = customError;
                return;
            }
        }
    });

    return {
        isValid: Object.keys(errors).length === 0,
        errors
    };
};

/**
 * Sanitize string input
 */
export const sanitizeInput = (input) => {
    if (!input) return '';

    return String(input)
        .replace(/[<>]/g, '') // Remove < and >
        .trim();
};

/**
 * Validate hex color
 */
export const isValidHexColor = (color) => {
    return /^#[0-9A-Fa-f]{6}$/.test(color);
};

/**
 * Validate time format (HH:MM)
 */
export const isValidTime = (time) => {
    const regex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    return regex.test(time);
};

/**
 * Validate JSON string
 */
export const isValidJSON = (str) => {
    try {
        JSON.parse(str);
        return true;
    } catch {
        return false;
    }
};