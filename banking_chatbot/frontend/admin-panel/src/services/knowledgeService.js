// frontend/admin-panel/src/services/knowledgeService.js
import api from './api';

class KnowledgeService {
    async getAllArticles(params = {}) {
        try {
            const queryParams = new URLSearchParams(params);
            return await api.get(`/knowledge/?${queryParams.toString()}`);
        } catch (error) {
            console.error('Error fetching articles:', error);
            throw error;
        }
    }

    async getArticleById(id) {
        try {
            return await api.get(`/knowledge/${id}`);
        } catch (error) {
            console.error('Error fetching article:', error);
            throw error;
        }
    }

    async createArticle(articleData) {
        try {
            return await api.post('/knowledge/', articleData);
        } catch (error) {
            console.error('Error creating article:', error);
            throw error;
        }
    }

    async updateArticle(id, articleData) {
        try {
            return await api.put(`/knowledge/${id}`, articleData);
        } catch (error) {
            console.error('Error updating article:', error);
            throw error;
        }
    }

    async deleteArticle(id) {
        try {
            return await api.delete(`/knowledge/${id}`);
        } catch (error) {
            console.error('Error deleting article:', error);
            throw error;
        }
    }

    async searchArticles(query) {
        try {
            return await api.get(`/knowledge/search?q=${encodeURIComponent(query)}`);
        } catch (error) {
            console.error('Error searching articles:', error);
            throw error;
        }
    }

    async getCategories() {
        try {
            return await api.get('/knowledge/categories');
        } catch (error) {
            console.error('Error fetching categories:', error);
            throw error;
        }
    }
}

export default new KnowledgeService();
