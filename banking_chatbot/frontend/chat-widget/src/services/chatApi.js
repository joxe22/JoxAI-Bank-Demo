// Service para comunicación con la API del chat
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ChatApiService {
    constructor() {
        this.baseUrl = `${API_BASE_URL}/api/v1`;
    }

    // Helper para hacer requests
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;

        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
            ...options,
        };

        try {
            const response = await fetch(url, config);

            if (!response.ok) {
                const error = await response.json().catch(() => ({}));
                throw new Error(error.message || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request error:', error);
            throw error;
        }
    }

    // Iniciar nueva conversación
    async startConversation(userData = {}) {
        return this.request('/chat/start', {
            method: 'POST',
            body: JSON.stringify({
                user_id: userData.userId || `user_${Date.now()}`,
                metadata: {
                    source: 'web-widget',
                    ...userData
                }
            })
        });
    }

    // Enviar mensaje
    async sendMessage(conversationId, message, context = {}) {
        return this.request('/chat/message', {
            method: 'POST',
            body: JSON.stringify({
                conversation_id: conversationId,
                message,
                context
            })
        });
    }

    // Obtener historial de conversación
    async getConversationHistory(conversationId) {
        return this.request(`/chat/history/${conversationId}`);
    }

    // Escalar a agente humano
    async escalateToAgent(conversationId, reason = {}) {
        return this.request('/chat/escalate', {
            method: 'POST',
            body: JSON.stringify({
                conversation_id: conversationId,
                category: reason.category || 'general',
                priority: reason.priority || 'medium',
                description: reason.description || '',
                metadata: reason.metadata || {}
            })
        });
    }

    // Finalizar conversación
    async endConversation(conversationId, feedback = null) {
        return this.request('/chat/end', {
            method: 'POST',
            body: JSON.stringify({
                conversation_id: conversationId,
                feedback
            })
        });
    }

    // Enviar feedback
    async sendFeedback(conversationId, rating, comment = '') {
        return this.request('/chat/feedback', {
            method: 'POST',
            body: JSON.stringify({
                conversation_id: conversationId,
                rating,
                comment
            })
        });
    }

    // Subir archivo
    async uploadFile(conversationId, file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('conversation_id', conversationId);

        return this.request('/chat/upload', {
            method: 'POST',
            headers: {}, // Remover Content-Type para que el browser lo setee automáticamente
            body: formData
        });
    }

    // Verificar estado del servicio
    async healthCheck() {
        return this.request('/health');
    }

    // Obtener configuración del widget
    async getWidgetConfig() {
        return this.request('/chat/config');
    }
}

export default new ChatApiService();