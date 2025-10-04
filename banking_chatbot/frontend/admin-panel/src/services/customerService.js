// frontend/admin-panel/src/services/customerService.js
import api from './api';

class CustomerService {
    async getAllCustomers(params = {}) {
        try {
            const queryParams = new URLSearchParams(params);
            return await api.get(`/customers/?${queryParams.toString()}`);
        } catch (error) {
            console.error('Error fetching customers:', error);
            throw error;
        }
    }

    async getCustomerById(id) {
        try {
            return await api.get(`/customers/${id}`);
        } catch (error) {
            console.error('Error fetching customer:', error);
            throw error;
        }
    }

    async createCustomer(customerData) {
        try {
            return await api.post('/customers/', customerData);
        } catch (error) {
            console.error('Error creating customer:', error);
            throw error;
        }
    }

    async updateCustomer(id, customerData) {
        try {
            return await api.put(`/customers/${id}`, customerData);
        } catch (error) {
            console.error('Error updating customer:', error);
            throw error;
        }
    }

    async deleteCustomer(id) {
        try {
            return await api.delete(`/customers/${id}`);
        } catch (error) {
            console.error('Error deleting customer:', error);
            throw error;
        }
    }

    async getCustomerStats() {
        try {
            return await api.get('/customers/stats/summary');
        } catch (error) {
            console.error('Error fetching customer stats:', error);
            throw error;
        }
    }

    async searchCustomers(query) {
        try {
            return await api.get(`/customers/search?q=${encodeURIComponent(query)}`);
        } catch (error) {
            console.error('Error searching customers:', error);
            throw error;
        }
    }
}

export default new CustomerService();
