// frontend/admin-panel/src/utils/dateUtils.js

/**
 * Get start of day
 */
export const getStartOfDay = (date = new Date()) => {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    return d;
};

/**
 * Get end of day
 */
export const getEndOfDay = (date = new Date()) => {
    const d = new Date(date);
    d.setHours(23, 59, 59, 999);
    return d;
};

/**
 * Get start of week
 */
export const getStartOfWeek = (date = new Date()) => {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1); // Monday as first day
    return new Date(d.setDate(diff));
};

/**
 * Get end of week
 */
export const getEndOfWeek = (date = new Date()) => {
    const start = getStartOfWeek(date);
    const end = new Date(start);
    end.setDate(end.getDate() + 6);
    return getEndOfDay(end);
};

/**
 * Get start of month
 */
export const getStartOfMonth = (date = new Date()) => {
    return new Date(date.getFullYear(), date.getMonth(), 1);
};

/**
 * Get end of month
 */
export const getEndOfMonth = (date = new Date()) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0, 23, 59, 59, 999);
};

/**
 * Get start of year
 */
export const getStartOfYear = (date = new Date()) => {
    return new Date(date.getFullYear(), 0, 1);
};

/**
 * Get end of year
 */
export const getEndOfYear = (date = new Date()) => {
    return new Date(date.getFullYear(), 11, 31, 23, 59, 59, 999);
};

/**
 * Add days to date
 */
export const addDays = (date, days) => {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
};

/**
 * Add months to date
 */
export const addMonths = (date, months) => {
    const result = new Date(date);
    result.setMonth(result.getMonth() + months);
    return result;
};

/**
 * Add years to date
 */
export const addYears = (date, years) => {
    const result = new Date(date);
    result.setFullYear(result.getFullYear() + years);
    return result;
};

/**
 * Get difference in days
 */
export const getDaysDifference = (date1, date2) => {
    const diffTime = Math.abs(date2 - date1);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

/**
 * Get difference in hours
 */
export const getHoursDifference = (date1, date2) => {
    const diffTime = Math.abs(date2 - date1);
    return Math.floor(diffTime / (1000 * 60 * 60));
};

/**
 * Get difference in minutes
 */
export const getMinutesDifference = (date1, date2) => {
    const diffTime = Math.abs(date2 - date1);
    return Math.floor(diffTime / (1000 * 60));
};

/**
 * Check if date is today
 */
export const isToday = (date) => {
    const today = new Date();
    const d = new Date(date);
    return d.toDateString() === today.toDateString();
};

/**
 * Check if date is yesterday
 */
export const isYesterday = (date) => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const d = new Date(date);
    return d.toDateString() === yesterday.toDateString();
};

/**
 * Check if date is this week
 */
export const isThisWeek = (date) => {
    const d = new Date(date);
    const startOfWeek = getStartOfWeek();
    const endOfWeek = getEndOfWeek();
    return d >= startOfWeek && d <= endOfWeek;
};

/**
 * Check if date is this month
 */
export const isThisMonth = (date) => {
    const d = new Date(date);
    const now = new Date();
    return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
};

/**
 * Check if date is this year
 */
export const isThisYear = (date) => {
    const d = new Date(date);
    const now = new Date();
    return d.getFullYear() === now.getFullYear();
};

/**
 * Get date range for period
 */
export const getDateRangeForPeriod = (period) => {
    const now = new Date();

    switch (period) {
        case 'today':
            return {
                start: getStartOfDay(now),
                end: getEndOfDay(now)
            };

        case 'yesterday':
            const yesterday = addDays(now, -1);
            return {
                start: getStartOfDay(yesterday),
                end: getEndOfDay(yesterday)
            };

        case 'week':
            return {
                start: getStartOfWeek(now),
                end: getEndOfWeek(now)
            };

        case 'month':
            return {
                start: getStartOfMonth(now),
                end: getEndOfMonth(now)
            };

        case 'quarter':
            const currentQuarter = Math.floor(now.getMonth() / 3);
            return {
                start: new Date(now.getFullYear(), currentQuarter * 3, 1),
                end: new Date(now.getFullYear(), (currentQuarter + 1) * 3, 0, 23, 59, 59, 999)
            };

        case 'year':
            return {
                start: getStartOfYear(now),
                end: getEndOfYear(now)
            };

        case 'last7days':
            return {
                start: getStartOfDay(addDays(now, -7)),
                end: getEndOfDay(now)
            };

        case 'last30days':
            return {
                start: getStartOfDay(addDays(now, -30)),
                end: getEndOfDay(now)
            };

        default:
            return {
                start: getStartOfDay(now),
                end: getEndOfDay(now)
            };
    }
};

/**
 * Format date to ISO string for API
 */
export const toISOString = (date) => {
    return new Date(date).toISOString();
};

/**
 * Parse date from various formats
 */
export const parseDate = (dateString) => {
    if (!dateString) return null;

    // Try ISO format
    let date = new Date(dateString);
    if (!isNaN(date.getTime())) return date;

    // Try DD/MM/YYYY
    const parts = dateString.split('/');
    if (parts.length === 3) {
        date = new Date(parts[2], parts[1] - 1, parts[0]);
        if (!isNaN(date.getTime())) return date;
    }

    return null;
};

/**
 * Get week number
 */
export const getWeekNumber = (date = new Date()) => {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    d.setDate(d.getDate() + 4 - (d.getDay() || 7));
    const yearStart = new Date(d.getFullYear(), 0, 1);
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
};

/**
 * Get days in month
 */
export const getDaysInMonth = (year, month) => {
    return new Date(year, month + 1, 0).getDate();
};

/**
 * Check if leap year
 */
export const isLeapYear = (year) => {
    return (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
};

/**
 * Get age from birthdate
 */
export const getAge = (birthDate) => {
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();

    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
        age--;
    }

    return age;
};