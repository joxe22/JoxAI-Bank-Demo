// frontend/admin-panel/src/components/Common/Header.jsx
// frontend/admin-panel/src/components/Common/Header.jsx
import React, { useState, useRef, useEffect } from 'react';
import '../../styles/components/Header.css';

const Header = ({ user, onLogout }) => {
    const [showUserMenu, setShowUserMenu] = useState(false);
    const [showNotifications, setShowNotifications] = useState(false);
    const [darkMode, setDarkMode] = useState(false);
    const [notifications, setNotifications] = useState([
        { id: 1, type: 'ticket', message: 'Nuevo ticket #1234 asignado', time: '5 min', unread: true },
        { id: 2, type: 'message', message: 'Cliente esperando respuesta', time: '10 min', unread: true },
        { id: 3, type: 'system', message: 'Sistema actualizado', time: '1 hora', unread: false }
    ]);

    const userMenuRef = useRef(null);
    const notificationRef = useRef(null);

    const unreadCount = notifications.filter(n => n.unread).length;

    // Cargar preferencia del modo oscuro al iniciar
    useEffect(() => {
        const savedTheme = localStorage.getItem('theme');
        const isDark = savedTheme === 'dark';
        setDarkMode(isDark);
        applyTheme(isDark);
    }, []);

    const applyTheme = (isDark) => {
        if (isDark) {
            document.documentElement.setAttribute('data-theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
        }
    };

    // Cerrar menús al hacer click fuera
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
                setShowUserMenu(false);
            }
            if (notificationRef.current && !notificationRef.current.contains(event.target)) {
                setShowNotifications(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const toggleDarkMode = () => {
        const newDarkMode = !darkMode;
        setDarkMode(newDarkMode);
        applyTheme(newDarkMode);
        localStorage.setItem('theme', newDarkMode ? 'dark' : 'light');

        // Cerrar el menú después de cambiar el tema
        setShowUserMenu(false);
    };

    const handleMarkAsRead = (notificationId) => {
        setNotifications(notifications.map(n =>
            n.id === notificationId ? { ...n, unread: false } : n
        ));
    };

    const handleMarkAllAsRead = () => {
        setNotifications(notifications.map(n => ({ ...n, unread: false })));
    };

    const getNotificationIcon = (type) => {
        switch(type) {
            case 'ticket': return '🎫';
            case 'message': return '💬';
            case 'system': return '⚙️';
            default: return '🔔';
        }
    };

    return (
        <header className="admin-header">
            <div className="header-left">
                <div className="brand">
                    <span className="brand-icon">🏦</span>
                    <span className="brand-text">Banking ChatBot</span>
                </div>
            </div>

            <div className="header-center">
                <div className="search-bar">
                    <span className="search-icon">🔍</span>
                    <input
                        type="text"
                        placeholder="Buscar tickets, clientes, conversaciones..."
                        className="search-input"
                    />
                </div>
            </div>

            <div className="header-right">
                {/* Notifications */}
                <div className="header-item" ref={notificationRef}>
                    <button
                        className="icon-button"
                        onClick={() => setShowNotifications(!showNotifications)}
                    >
                        🔔
                        {unreadCount > 0 && (
                            <span className="notification-badge">{unreadCount}</span>
                        )}
                    </button>

                    {showNotifications && (
                        <div className="dropdown-menu notifications-menu">
                            <div className="dropdown-header">
                                <h4>Notificaciones</h4>
                                {unreadCount > 0 && (
                                    <button
                                        className="link-button"
                                        onClick={handleMarkAllAsRead}
                                    >
                                        Marcar todas como leídas
                                    </button>
                                )}
                            </div>

                            <div className="notifications-list">
                                {notifications.length === 0 ? (
                                    <div className="empty-state">
                                        <p>No hay notificaciones</p>
                                    </div>
                                ) : (
                                    notifications.map(notification => (
                                        <div
                                            key={notification.id}
                                            className={`notification-item ${notification.unread ? 'unread' : ''}`}
                                            onClick={() => handleMarkAsRead(notification.id)}
                                        >
                                            <span className="notification-icon">
                                                {getNotificationIcon(notification.type)}
                                            </span>
                                            <div className="notification-content">
                                                <p className="notification-message">{notification.message}</p>
                                                <span className="notification-time">{notification.time}</span>
                                            </div>
                                            {notification.unread && <span className="unread-dot"></span>}
                                        </div>
                                    ))
                                )}
                            </div>

                            <div className="dropdown-footer">
                                <button className="link-button">Ver todas</button>
                            </div>
                        </div>
                    )}
                </div>

                {/* User Menu */}
                <div className="header-item" ref={userMenuRef}>
                    <button
                        className="user-button"
                        onClick={() => setShowUserMenu(!showUserMenu)}
                    >
                        <div className="user-avatar">
                            {user?.avatar ? (
                                <img src={user.avatar} alt={user.name} />
                            ) : (
                                <span>{user?.name?.charAt(0).toUpperCase() || 'U'}</span>
                            )}
                        </div>
                        <div className="user-info">
                            <span className="user-name">{user?.name || 'Usuario'}</span>
                            <span className="user-role">{user?.role || 'Agente'}</span>
                        </div>
                        <span className="dropdown-arrow">▼</span>
                    </button>

                    {showUserMenu && (
                        <div className="dropdown-menu user-menu">
                            <div className="user-menu-header">
                                <div className="user-avatar large">
                                    {user?.avatar ? (
                                        <img src={user.avatar} alt={user.name} />
                                    ) : (
                                        <span>{user?.name?.charAt(0).toUpperCase() || 'U'}</span>
                                    )}
                                </div>
                                <div>
                                    <p className="user-menu-name">{user?.name || 'Usuario'}</p>
                                    <p className="user-menu-email">{user?.email || 'email@example.com'}</p>
                                </div>
                            </div>

                            <div className="menu-divider"></div>

                            {/* Modo Oscuro - CORREGIDO Y FUNCIONAL */}
                            <button className="menu-item dark-mode-toggle" onClick={toggleDarkMode}>
                                <span>{darkMode ? '☀️' : '🌙'}</span>
                                {darkMode ? 'Modo Claro' : 'Modo Oscuro'}
                                <div className={`toggle-switch-small ${darkMode ? 'active' : ''}`}>
                                    <span className="toggle-slider"></span>
                                </div>
                            </button>

                            <button className="menu-item">
                                <span>👤</span> Mi Perfil
                            </button>
                            <button className="menu-item">
                                <span>⚙️</span> Configuración
                            </button>
                            <button className="menu-item">
                                <span>❓</span> Ayuda
                            </button>

                            <div className="menu-divider"></div>

                            <button className="menu-item danger" onClick={onLogout}>
                                <span>🚪</span> Cerrar Sesión
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
};

export default Header;