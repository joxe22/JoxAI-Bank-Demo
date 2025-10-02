// frontend/admin-panel/src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Common/Header';
import Sidebar from './components/Common/Sidebar';
import ErrorBoundary from './components/Common/ErrorBoundary';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import TicketsPage from './pages/TicketsPage';
import ConversationsPage from './pages/ConversationPage';
import AnalyticsPage from './pages/AnalyticsPage';
import CustomersPage from './pages/CustomerPage';
import KnowledgeBasePage from './pages/KnowledgeBasePage';
import SettingsPage from './pages/SettingsPage';
import authService from './services/authService';
import websocketService from './services/websocketService';
import './styles/globals.css';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
    const isAuthenticated = authService.isAuthenticated();

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return children;
};

// Main Layout Component
const MainLayout = ({ children }) => {
    const [sidebarCollapsed, setSidebarCollapsed] = useState(
        localStorage.getItem('sidebarCollapsed') === 'true'
    );
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Load user data
        const currentUser = authService.getCurrentUser();
        setUser(currentUser);

        // Connect to WebSocket
        if (authService.isAuthenticated()) {
            websocketService.connect();
        }

        // Cleanup on unmount
        return () => {
            websocketService.disconnect();
        };
    }, []);

    const handleToggleSidebar = () => {
        const newState = !sidebarCollapsed;
        setSidebarCollapsed(newState);
        localStorage.setItem('sidebarCollapsed', newState);
    };

    const handleLogout = () => {
        authService.logout();
    };

    return (
        <div className={`app-container ${sidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
            <Sidebar
                collapsed={sidebarCollapsed}
                onToggle={handleToggleSidebar}
            />

            <div className="main-content">
                <Header
                    user={user}
                    onLogout={handleLogout}
                />

                <main className="page-container">
                    {children}
                </main>
            </div>
        </div>
    );
};

function App() {
    return (
        <ErrorBoundary>
            <Router>
                <Routes>
                    {/* Public Routes */}
                    <Route path="/login" element={<LoginPage />} />

                    {/* Protected Routes */}
                    <Route
                        path="/"
                        element={
                            <ProtectedRoute>
                                <Navigate to="/dashboard" replace />
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/dashboard"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <DashboardPage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/tickets"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <TicketsPage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/conversations"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <ConversationsPage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/analytics"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <AnalyticsPage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/customers"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <CustomersPage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/knowledge"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <KnowledgeBasePage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    <Route
                        path="/settings"
                        element={
                            <ProtectedRoute>
                                <MainLayout>
                                    <SettingsPage />
                                </MainLayout>
                            </ProtectedRoute>
                        }
                    />

                    {/* Catch all - 404 */}
                    <Route
                        path="*"
                        element={
                            <div style={{ padding: '40px', textAlign: 'center' }}>
                                <h1>404 - Página no encontrada</h1>
                                <p>La página que buscas no existe.</p>
                                <a href="/dashboard">Volver al Dashboard</a>
                            </div>
                        }
                    />
                </Routes>
            </Router>
        </ErrorBoundary>
    );
}

export default App;