// frontend/admin-panel/src/pages/AnalyticsPage.jsx
import React, { useState } from 'react';
import AnalyticsDashboard from '../components/Analytics/AnalyticsDashboard';
import ConversationAnalytics from '../components/Analytics/ConversationAnalytics';
import AgentPerformance from '../components/Analytics/AgentPerformance';
import '../styles/pages/AnalyticsPage.css';

const AnalyticsPage = () => {
    const [activeView, setActiveView] = useState('overview');

    const views = [
        { id: 'overview', label: 'Vista General', icon: '📊', description: 'Métricas globales y tendencias' },
        { id: 'conversations', label: 'Conversaciones', icon: '💬', description: 'Análisis detallado de chats' },
        { id: 'agents', label: 'Agentes', icon: '👥', description: 'Rendimiento del equipo' }
    ];

    const getActiveView = () => {
        switch(activeView) {
            case 'overview': return <AnalyticsDashboard />;
            case 'conversations': return <ConversationAnalytics />;
            case 'agents': return <AgentPerformance />;
            default: return <AnalyticsDashboard />;
        }
    };

    return (
        <div className="analytics-page">
            {/* Header Modernizado */}
            <div className="analytics-page-header">
                <h1>Analytics Dashboard</h1>
                <p>Monitoriza el rendimiento y optimiza tu servicio al cliente con datos en tiempo real</p>
            </div>

            {/* Tabs de Navegación Rápida Modernizadas */}
            <div className="analytics-tabs">
                {views.map(view => (
                    <button
                        key={view.id}
                        className={`analytics-tab ${activeView === view.id ? 'active' : ''}`}
                        onClick={() => setActiveView(view.id)}
                    >
                        <span className="tab-icon">{view.icon}</span>
                        <div className="tab-content">
                            <span className="tab-label">{view.label}</span>
                            <span className="tab-description">{view.description}</span>
                        </div>
                        <div className="tab-indicator"></div>
                    </button>
                ))}
            </div>

            {/* Controles de Fecha y Exportación */}
            <div className="analytics-controls">
                <div className="control-group">
                    <button className="control-btn date-picker">
                        <span className="control-icon">📅</span>
                        <span className="control-text">Últimos 7 días</span>
                        <span className="control-arrow">⌄</span>
                    </button>

                    <button className="control-btn export-btn">
                        <span className="control-icon">📥</span>
                        <span className="control-text">Exportar Reporte</span>
                    </button>
                </div>

                <div className="view-stats">
                    <span className="stat-badge">📈 Datos en tiempo real</span>
                    <span className="stat-badge">🔄 Actualizado hace 5 min</span>
                </div>
            </div>

            {/* Contenido de Analytics */}
            <div className="analytics-content">
                {getActiveView()}
            </div>
        </div>
    );
};

export default AnalyticsPage;
