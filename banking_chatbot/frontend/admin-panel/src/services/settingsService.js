// frontend/admin-panel/src/services/settingsService.js
import api from './api';

class SettingsService {
    async getSystemSettings(category = null) {
        try {
            const params = category ? `?category=${category}` : '';
            return await api.get(`/settings/system${params}`);
        } catch (error) {
            console.error('Error fetching system settings:', error);
            throw error;
        }
    }

    async getSystemSetting(key) {
        try {
            return await api.get(`/settings/system/${key}`);
        } catch (error) {
            console.error('Error fetching system setting:', error);
            throw error;
        }
    }

    async createSystemSetting(settingData) {
        try {
            return await api.post('/settings/system', settingData);
        } catch (error) {
            console.error('Error creating system setting:', error);
            throw error;
        }
    }

    async updateSystemSetting(key, settingData) {
        try {
            return await api.put(`/settings/system/${key}`, settingData);
        } catch (error) {
            console.error('Error updating system setting:', error);
            throw error;
        }
    }

    async deleteSystemSetting(key) {
        try {
            return await api.delete(`/settings/system/${key}`);
        } catch (error) {
            console.error('Error deleting system setting:', error);
            throw error;
        }
    }

    async getUserSettings(category = null) {
        try {
            const params = category ? `?category=${category}` : '';
            return await api.get(`/settings/user/me${params}`);
        } catch (error) {
            console.error('Error fetching user settings:', error);
            throw error;
        }
    }

    async getUserSetting(key) {
        try {
            return await api.get(`/settings/user/me/${key}`);
        } catch (error) {
            console.error('Error fetching user setting:', error);
            throw error;
        }
    }

    async setUserSetting(key, settingData) {
        try {
            return await api.post(`/settings/user/me/${key}`, settingData);
        } catch (error) {
            console.error('Error setting user setting:', error);
            throw error;
        }
    }

    async deleteUserSetting(key) {
        try {
            return await api.delete(`/settings/user/me/${key}`);
        } catch (error) {
            console.error('Error deleting user setting:', error);
            throw error;
        }
    }

    async getPublicSettings() {
        try {
            return await api.get('/settings/public');
        } catch (error) {
            console.error('Error fetching public settings:', error);
            throw error;
        }
    }

    async setBotConfiguration(config) {
        try {
            const settings = Object.entries(config).map(([key, value]) => ({
                key: `bot.${key}`,
                value: value,
                category: 'bot',
                description: `Bot configuration: ${key}`
            }));

            const promises = settings.map(setting =>
                this.updateSystemSetting(setting.key, {
                    value: setting.value,
                    category: setting.category,
                    description: setting.description
                }).catch(() => 
                    this.createSystemSetting({
                        key: setting.key,
                        value: setting.value,
                        category: setting.category,
                        description: setting.description
                    })
                )
            );

            return await Promise.all(promises);
        } catch (error) {
            console.error('Error saving bot configuration:', error);
            throw error;
        }
    }

    async getBotConfiguration() {
        try {
            const settings = await this.getSystemSettings('bot');
            const config = {};
            
            settings.forEach(setting => {
                const key = setting.key.replace('bot.', '');
                config[key] = setting.value;
            });

            return config;
        } catch (error) {
            console.error('Error fetching bot configuration:', error);
            throw error;
        }
    }
}

export default new SettingsService();
