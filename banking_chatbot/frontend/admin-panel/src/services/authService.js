// frontend/admin-panel/src/services/authService.js
import api from './api';

// Mock credentials para desarrollo
const MOCK_USERS = [
    {
        email: 'admin@joxai.com',
        password: 'admin123',
        user: {
            id: 1,
            name: 'Admin User',
            email: 'admin@joxai.com',
            role: 'admin'
        }
    },
    {
        email: 'agent@joxai.com',
        password: 'agent123',
        user: {
            id: 2,
            name: 'Agent User',
            email: 'agent@joxai.com',
            role: 'agent'
        }
    }
];

class AuthService {
    constructor() {
        this.useMockAuth = import.meta.env.VITE_USE_MOCK_AUTH === 'true' || true; // Default true para desarrollo
    }

    // Login
    async login(email, password) {
        // Si usamos mock auth (modo desarrollo)
        if (this.useMockAuth) {
            return this.mockLogin(email, password);
        }

        // Login real con API
        try {
            const response = await api.post('/auth/login', {
                email,
                password
            });

            if (response.token) {
                localStorage.setItem('token', response.token);
                localStorage.setItem('user', JSON.stringify(response.user));
            }

            return {
                success: true,
                token: response.token,
                user: response.user
            };
        } catch (error) {
            return {
                success: false,
                message: error.message || 'Error al iniciar sesión'
            };
        }
    }

    // Mock login para desarrollo
    mockLogin(email, password) {
        return new Promise((resolve) => {
            // Simular delay de red
            setTimeout(() => {
                const user = MOCK_USERS.find(
                    u => u.email === email && u.password === password
                );

                if (user) {
                    const mockToken = 'mock-jwt-token-' + Date.now();
                    localStorage.setItem('token', mockToken);
                    localStorage.setItem('user', JSON.stringify(user.user));

                    resolve({
                        success: true,
                        token: mockToken,
                        user: user.user
                    });
                } else {
                    resolve({
                        success: false,
                        message: 'Email o contraseña incorrectos'
                    });
                }
            }, 500);
        });
    }

    // Logout
    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    }

    // Get current user
    getCurrentUser() {
        const userStr = localStorage.getItem('user');
        if (userStr) {
            try {
                return JSON.parse(userStr);
            } catch (error) {
                console.error('Error parsing user data:', error);
                return null;
            }
        }
        return null;
    }

    // Check if user is authenticated
    isAuthenticated() {
        const token = localStorage.getItem('token');
        return !!token;
    }

    // Verify token
    async verifyToken() {
        if (this.useMockAuth) {
            return !!localStorage.getItem('token');
        }

        try {
            const response = await api.get('/auth/verify');
            return response.valid;
        } catch (error) {
            return false;
        }
    }

    // Refresh token
    async refreshToken() {
        if (this.useMockAuth) {
            const token = localStorage.getItem('token');
            return token;
        }

        try {
            const response = await api.post('/auth/refresh');
            if (response.token) {
                localStorage.setItem('token', response.token);
            }
            return response.token;
        } catch (error) {
            console.error('Error refreshing token:', error);
            return null;
        }
    }

    // Change password
    async changePassword(currentPassword, newPassword) {
        if (this.useMockAuth) {
            return {
                success: true,
                message: 'Contraseña actualizada (mock)'
            };
        }

        try {
            const response = await api.post('/auth/change-password', {
                currentPassword,
                newPassword
            });
            return {
                success: true,
                message: response.message
            };
        } catch (error) {
            return {
                success: false,
                message: error.message
            };
        }
    }

    // Request password reset
    async requestPasswordReset(email) {
        if (this.useMockAuth) {
            return {
                success: true,
                message: 'Email de recuperación enviado (mock)'
            };
        }

        try {
            const response = await api.post('/auth/forgot-password', { email });
            return {
                success: true,
                message: response.message
            };
        } catch (error) {
            return {
                success: false,
                message: error.message
            };
        }
    }

    // Reset password with token
    async resetPassword(token, newPassword) {
        if (this.useMockAuth) {
            return {
                success: true,
                message: 'Contraseña restablecida (mock)'
            };
        }

        try {
            const response = await api.post('/auth/reset-password', {
                token,
                newPassword
            });
            return {
                success: true,
                message: response.message
            };
        } catch (error) {
            return {
                success: false,
                message: error.message
            };
        }
    }

    // Update user profile
    async updateProfile(userData) {
        if (this.useMockAuth) {
            const currentUser = this.getCurrentUser();
            const updatedUser = { ...currentUser, ...userData };
            localStorage.setItem('user', JSON.stringify(updatedUser));

            return {
                success: true,
                user: updatedUser
            };
        }

        try {
            const response = await api.put('/auth/profile', userData);

            // Update local models
            const currentUser = this.getCurrentUser();
            const updatedUser = { ...currentUser, ...response.user };
            localStorage.setItem('user', JSON.stringify(updatedUser));

            return {
                success: true,
                user: updatedUser
            };
        } catch (error) {
            return {
                success: false,
                message: error.message
            };
        }
    }
}

export default new AuthService();