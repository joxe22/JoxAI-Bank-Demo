// frontend/admin-panel/src/services/analyticsService.js
import api from './api';

class AnalyticsService {
    // Get dashboard metrics
    async getDashboardMetrics(period = 'week') {
        try {
            return await api.get(`/analytics/dashboard?period=${period}`);
        } catch (error) {
            console.error('Error fetching dashboard metrics:', error);
            throw error;
        }
    }

    // Get conversation analytics
    async getConversationAnalytics(filters = {}) {
        try {
            const queryParams = new URLSearchParams(filters);
            return await api.get(`/analytics/conversations?${queryParams.toString()}`);
        } catch (error) {
            console.error('Error fetching conversation analytics:', error);
            throw error;
        }
    }

    // Get agent performance
    async getAgentPerformance(agentId = null, period = 'week') {
        try {
            const endpoint = agentId
                ? `/analytics/agents/${agentId}?period=${period}`
                : `/analytics/agents?period=${period}`;

            return await api.get(endpoint);
        } catch (error) {
            console.error('Error fetching agent performance:', error);
            throw error;
        }
    }

    // Get ticket statistics
    async getTicketStatistics(period = 'week') {
        try {
            return await api.get(`/analytics/tickets?period=${period}`);
        } catch (error) {
            console.error('Error fetching ticket statistics:', error);
            throw error;
        }
    }

    // Get response time analytics
    async getResponseTimeAnalytics(period = 'week') {
        try {
            return await api.get(`/analytics/response-time?period=${period}`);
        } catch (error) {
            console.error('Error fetching response time analytics:', error);
            throw error;
        }
    }

    // Get satisfaction scores
    async getSatisfactionScores(period = 'week') {
        try {
            return await api.get(`/analytics/satisfaction?period=${period}`);
        } catch (error) {
            console.error('Error fetching satisfaction scores:', error);
            throw error;
        }
    }

    // Get intent distribution
    async getIntentDistribution(period = 'week') {
        try {
            return await api.get(`/analytics/intents?period=${period}`);
        } catch (error) {
            console.error('Error fetching intent distribution:', error);
            throw error;
        }
    }

    // Get channel analytics
    async getChannelAnalytics(period = 'week') {
        try {
            return await api.get(`/analytics/channels?period=${period}`);
        } catch (error) {
            console.error('Error fetching channel analytics:', error);
            throw error;
        }
    }

    // Get sentiment analysis
    async getSentimentAnalysis(period = 'week') {
        try {
            return await api.get(`/analytics/sentiment?period=${period}`);
        } catch (error) {
            console.error('Error fetching sentiment analysis:', error);
            throw error;
        }
    }

    // Get peak hours
    async getPeakHours(period = 'week') {
        try {
            return await api.get(`/analytics/peak-hours?period=${period}`);
        } catch (error) {
            console.error('Error fetching peak hours:', error);
            throw error;
        }
    }

    // Get escalation analytics
    async getEscalationAnalytics(period = 'week') {
        try {
            return await api.get(`/analytics/escalations?period=${period}`);
        } catch (error) {
            console.error('Error fetching escalation analytics:', error);
            throw error;
        }
    }

    // Export analytics report
    async exportReport(reportType, filters = {}, format = 'pdf') {
        try {
            const queryParams = new URLSearchParams({
                ...filters,
                format
            });

            return await api.get(`/analytics/export/${reportType}?${queryParams.toString()}`);
        } catch (error) {
            console.error('Error exporting report:', error);
            throw error;
        }
    }

    // Get custom metrics
    async getCustomMetrics(metricIds, period = 'week') {
        try {
            return await api.post('/analytics/custom', {
                metrics: metricIds,
                period
            });
        } catch (error) {
            console.error('Error fetching custom metrics:', error);
            throw error;
        }
    }

    // Get real-time stats
    async getRealTimeStats() {
        try {
            return await api.get('/analytics/realtime');
        } catch (error) {
            console.error('Error fetching real-time stats:', error);
            throw error;
        }
    }
}

export default new AnalyticsService();