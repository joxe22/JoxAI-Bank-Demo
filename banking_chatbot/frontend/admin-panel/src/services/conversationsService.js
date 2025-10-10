// frontend/admin-panel/src/services/conversationsService.js
import api from './api';

class ConversationsService {
    async getAllConversations(params = {}) {
        try {
            const queryParams = new URLSearchParams(params);
            return await api.get(`/conversations/?${queryParams.toString()}`);
        } catch (error) {
            console.error('Error fetching conversations:', error);
            throw error;
        }
    }

    async getConversation(conversationId) {
        try {
            return await api.get(`/conversations/${conversationId}`);
        } catch (error) {
            console.error('Error fetching conversation:', error);
            throw error;
        }
    }

    async getActiveConversations(limit = 50) {
        try {
            return await api.get(`/conversations/?status=active&limit=${limit}`);
        } catch (error) {
            console.error('Error fetching active conversations:', error);
            throw error;
        }
    }

    async getEscalatedConversations(limit = 50) {
        try {
            return await api.get(`/conversations/?status=escalated&limit=${limit}`);
        } catch (error) {
            console.error('Error fetching escalated conversations:', error);
            throw error;
        }
    }
}

export default new ConversationsService();
