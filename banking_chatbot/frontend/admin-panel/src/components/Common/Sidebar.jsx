// frontend/admin-panel/src/components/Common/Sidebar.jsx
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../../styles/components/Sidebar.css';

const Sidebar = ({ collapsed, onToggle }) => {
    const navigate = useNavigate();
    const location = useLocation();

    const menuItems = [
        {
            id: 'dashboard',
            icon: '📊',
            label: 'Dashboard',
            path: '/dashboard',
            badge: null
        },
        {
            id: 'tickets',
            icon: '🎫',
            label: 'Tickets',
            path: '/tickets',
            badge: 12
        },
        {
            id: 'conversations',
            icon: '💬',
            label: 'Conversaciones',
            path: '/conversations',
            badge: 5
        },
        {
            id: 'analytics',
            icon: '📈',
            label: 'Analytics',
            path: '/analytics',
            badge: null
        },
        {
            id: 'customers',
            icon: '👥',
            label: 'Clientes',
            path: '/customers',
            badge: null
        },
        {
            id: 'knowledge',
            icon: '📚',
            label: 'Base de Conocimiento',
            path: '/knowledge',
            badge: null
        },
        {
            id: 'settings',
            icon: '⚙️',
            label: 'Configuración',
            path: '/settings',
            badge: null
        }
    ];

    const isActive = (path) => {
        return location.pathname === path || location.pathname.startsWith(path + '/');
    };

    const handleNavigate = (path) => {
        navigate(path);
    };

    return (
        <aside className={`admin-sidebar ${collapsed ? 'collapsed' : ''}`}>
            <button
                className="sidebar-toggle"
                onClick={onToggle}
                title={collapsed ? 'Expandir' : 'Contraer'}
            >
                {collapsed ? '▶' : '◀'}
            </button>

            <nav className="sidebar-nav">
                <ul className="nav-list">
                    {menuItems.map(item => (
                        <li key={item.id} className="nav-item">
                            <button
                                className={`nav-link ${isActive(item.path) ? 'active' : ''}`}
                                onClick={() => handleNavigate(item.path)}
                                title={collapsed ? item.label : ''}
                            >
                                <span className="nav-icon">{item.icon}</span>
                                {!collapsed && (
                                    <>
                                        <span className="nav-label">{item.label}</span>
                                        {item.badge && (
                                            <span className="nav-badge">{item.badge}</span>
                                        )}
                                    </>
                                )}
                            </button>
                        </li>
                    ))}
                </ul>
            </nav>

            {!collapsed && (
                <div className="sidebar-footer">
                    <div className="status-card">
                        <div className="status-header">
                            <span className="status-dot online"></span>
                            <span className="status-text">Sistema Operativo</span>
                        </div>
                        <div className="status-stats">
                            <div className="stat">
                                <span className="stat-label">Agentes activos</span>
                                <span className="stat-value">8/12</span>
                            </div>
                            <div className="stat">
                                <span className="stat-label">Tiempo de respuesta</span>
                                <span className="stat-value">2.3 min</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </aside>
    );
};

export default Sidebar;