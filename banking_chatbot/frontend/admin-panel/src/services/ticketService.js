// frontend/admin-panel/src/services/ticketService.js
import api from './api';

class TicketService {
    // Get all tickets with filters
    async getTickets(filters = {}) {
        try {
            const queryParams = new URLSearchParams();

            Object.keys(filters).forEach(key => {
                if (filters[key] && filters[key] !== 'all') {
                    queryParams.append(key, filters[key]);
                }
            });

            const queryString = queryParams.toString();
            const endpoint = queryString ? `/tickets?${queryString}` : '/tickets';

            return await api.get(endpoint);
        } catch (error) {
            console.error('Error fetching tickets:', error);
            throw error;
        }
    }

    // Get ticket by ID
    async getTicketById(ticketId) {
        try {
            return await api.get(`/tickets/${ticketId}`);
        } catch (error) {
            console.error('Error fetching ticket:', error);
            throw error;
        }
    }

    // Create new ticket
    async createTicket(ticketData) {
        try {
            return await api.post('/tickets', ticketData);
        } catch (error) {
            console.error('Error creating ticket:', error);
            throw error;
        }
    }

    // Update ticket
    async updateTicket(ticketId, ticketData) {
        try {
            return await api.put(`/tickets/${ticketId}`, ticketData);
        } catch (error) {
            console.error('Error updating ticket:', error);
            throw error;
        }
    }

    // Delete ticket
    async deleteTicket(ticketId) {
        try {
            return await api.delete(`/tickets/${ticketId}`);
        } catch (error) {
            console.error('Error deleting ticket:', error);
            throw error;
        }
    }

    // Assign ticket to agent
    async assignTicket(ticketId, agentId) {
        try {
            return await api.post(`/tickets/${ticketId}/assign`, { agentId });
        } catch (error) {
            console.error('Error assigning ticket:', error);
            throw error;
        }
    }

    // Change ticket status
    async changeStatus(ticketId, status) {
        try {
            return await api.patch(`/tickets/${ticketId}/status`, { status });
        } catch (error) {
            console.error('Error changing ticket status:', error);
            throw error;
        }
    }

    // Change ticket priority
    async changePriority(ticketId, priority) {
        try {
            return await api.patch(`/tickets/${ticketId}/priority`, { priority });
        } catch (error) {
            console.error('Error changing ticket priority:', error);
            throw error;
        }
    }

    // Get ticket messages
    async getMessages(ticketId) {
        try {
            return await api.get(`/tickets/${ticketId}/messages`);
        } catch (error) {
            console.error('Error fetching messages:', error);
            throw error;
        }
    }

    // Send message to ticket
    async sendMessage(ticketId, message) {
        try {
            return await api.post(`/tickets/${ticketId}/messages`, { message });
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    // Add note to ticket
    async addNote(ticketId, note) {
        try {
            return await api.post(`/tickets/${ticketId}/notes`, { note });
        } catch (error) {
            console.error('Error adding note:', error);
            throw error;
        }
    }

    // Get ticket history
    async getHistory(ticketId) {
        try {
            return await api.get(`/tickets/${ticketId}/history`);
        } catch (error) {
            console.error('Error fetching ticket history:', error);
            throw error;
        }
    }

    // Upload attachment
    async uploadAttachment(ticketId, file) {
        try {
            return await api.upload(`/tickets/${ticketId}/attachments`, file);
        } catch (error) {
            console.error('Error uploading attachment:', error);
            throw error;
        }
    }

    // Get ticket statistics
    async getStatistics(period = 'week') {
        try {
            return await api.get(`/tickets/statistics?period=${period}`);
        } catch (error) {
            console.error('Error fetching statistics:', error);
            throw error;
        }
    }

    // Export tickets
    async exportTickets(filters = {}, format = 'csv') {
        try {
            const queryParams = new URLSearchParams({
                ...filters,
                format
            });

            return await api.get(`/tickets/export?${queryParams.toString()}`);
        } catch (error) {
            console.error('Error exporting tickets:', error);
            throw error;
        }
    }
}

export default new TicketService();