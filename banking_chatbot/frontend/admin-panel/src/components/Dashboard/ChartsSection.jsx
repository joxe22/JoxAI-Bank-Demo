// frontend/admin-panel/src/components/Dashboard/ChartsSection.jsx - MEJORADO
import React, { useState, useEffect } from 'react';
import '../../styles/components/ChartsSection.css';

const ChartsSection = ({ data, timeRange, loading }) => {
    const [conversationsPeriod, setConversationsPeriod] = useState('week');
    const [ticketsPeriod, setTicketsPeriod] = useState('week');
    const [isAnimating, setIsAnimating] = useState(false);

    // Datos de ejemplo mejorados para las gráficas
    const conversationsData = {
        week: [120, 150, 180, 165, 200, 190, 210],
        month: [1200, 1400, 1600, 1500, 1800, 2000, 2200, 2100, 2300, 2400, 2500, 2600],
        year: [12000, 14000, 16000, 15000, 18000, 20000, 22000, 24000, 26000, 28000, 30000, 32000]
    };

    const ticketsData = {
        week: { open: 45, inProgress: 30, resolved: 80, closed: 120 },
        month: { open: 180, inProgress: 120, resolved: 320, closed: 480 },
        year: { open: 2160, inProgress: 1440, resolved: 3840, closed: 5760 }
    };

    const days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];

    const getMaxValue = (data) => Math.max(...data);
    const getLabels = (period) => period === 'week' ? days : months;

    const handlePeriodChange = (setter, period) => {
        setIsAnimating(true);
        setter(period);
        setTimeout(() => setIsAnimating(false), 600);
    };

    const handleActivityClick = (activity) => {
        console.log('Activity clicked:', activity);
        // Navegar a la actividad o mostrar detalles
    };

    if (loading) {
        return (
            <div className="charts-section">
                {[1, 2, 3].map((index) => (
                    <div key={index} className={`chart-card ${index === 3 ? 'full-width' : ''} skeleton`}>
                        <div className="chart-header">
                            <div className="skeleton-line" style={{width: '40%', height: '24px'}}></div>
                            <div className="chart-controls">
                                {[1, 2, 3].map(btn => (
                                    <div key={btn} className="skeleton-line" style={{width: '60px', height: '32px'}}></div>
                                ))}
                            </div>
                        </div>
                        <div className="chart-body">
                            <div className="skeleton-line" style={{height: '200px'}}></div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    return (
        <div className="charts-section">
            {/* Conversaciones en el tiempo */}
            <div className="chart-card">
                <div className="chart-header">
                    <h3 className="chart-title">Conversaciones</h3>
                    <div className="chart-controls">
                        <button
                            className={`period-btn ${conversationsPeriod === 'week' ? 'active' : ''}`}
                            onClick={() => handlePeriodChange(setConversationsPeriod, 'week')}
                            aria-label="Ver datos de la semana"
                        >
                            Semana
                        </button>
                        <button
                            className={`period-btn ${conversationsPeriod === 'month' ? 'active' : ''}`}
                            onClick={() => handlePeriodChange(setConversationsPeriod, 'month')}
                            aria-label="Ver datos del mes"
                        >
                            Mes
                        </button>
                        <button
                            className={`period-btn ${conversationsPeriod === 'year' ? 'active' : ''}`}
                            onClick={() => handlePeriodChange(setConversationsPeriod, 'year')}
                            aria-label="Ver datos del año"
                        >
                            Año
                        </button>
                    </div>
                </div>

                <div className="chart-body">
                    <div className={`line-chart ${isAnimating ? 'animating' : ''}`}>
                        {conversationsData[conversationsPeriod].map((value, index) => {
                            const maxValue = getMaxValue(conversationsData[conversationsPeriod]);
                            const height = (value / maxValue) * 100;
                            const labels = getLabels(conversationsPeriod);

                            return (
                                <div key={index} className="chart-bar-wrapper">
                                    <div className="chart-tooltip">
                                        {value.toLocaleString()} conversaciones
                                    </div>
                                    <div
                                        className="chart-bar"
                                        style={{
                                            height: `${height}%`,
                                            animationDelay: `${index * 0.1}s`
                                        }}
                                    ></div>
                                    <span className="chart-label">{labels[index]}</span>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Estado de Tickets */}
            <div className="chart-card">
                <div className="chart-header">
                    <h3 className="chart-title">Estado de Tickets</h3>
                    <div className="chart-controls">
                        <button
                            className={`period-btn ${ticketsPeriod === 'week' ? 'active' : ''}`}
                            onClick={() => handlePeriodChange(setTicketsPeriod, 'week')}
                            aria-label="Ver tickets de la semana"
                        >
                            Semana
                        </button>
                        <button
                            className={`period-btn ${ticketsPeriod === 'month' ? 'active' : ''}`}
                            onClick={() => handlePeriodChange(setTicketsPeriod, 'month')}
                            aria-label="Ver tickets del mes"
                        >
                            Mes
                        </button>
                        <button
                            className={`period-btn ${ticketsPeriod === 'year' ? 'active' : ''}`}
                            onClick={() => handlePeriodChange(setTicketsPeriod, 'year')}
                            aria-label="Ver tickets del año"
                        >
                            Año
                        </button>
                    </div>
                </div>

                <div className="chart-body">
                    <div className="stats-grid">
                        {Object.entries(ticketsData[ticketsPeriod]).map(([key, value], index) => {
                            const total = Object.values(ticketsData[ticketsPeriod]).reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);

                            const colors = {
                                open: '#f093fb',
                                inProgress: '#4facfe',
                                resolved: '#43e97b',
                                closed: '#c2e9fb'
                            };

                            const labels = {
                                open: 'Abiertos',
                                inProgress: 'En Progreso',
                                resolved: 'Resueltos',
                                closed: 'Cerrados'
                            };

                            const icons = {
                                open: '📋',
                                inProgress: '🔄',
                                resolved: '✅',
                                closed: '🔒'
                            };

                            return (
                                <div
                                    key={key}
                                    className="ticket-stat"
                                    style={{ animationDelay: `${index * 0.1}s` }}
                                >
                                    <div className="stat-header">
                                        <span className="stat-icon">{icons[key]}</span>
                                        <div className="stat-indicator" style={{ background: colors[key] }}></div>
                                    </div>
                                    <div className="stat-info">
                                        <span className="stat-label">{labels[key]}</span>
                                        <div className="stat-values">
                                            <span className="stat-count">{value.toLocaleString()}</span>
                                            <span className="stat-percentage">{percentage}%</span>
                                        </div>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Actividad Reciente */}
            <div className="chart-card full-width">
                <div className="chart-header">
                    <h3 className="chart-title">Actividad Reciente</h3>
                    <button
                        className="link-button"
                        aria-label="Ver toda la actividad"
                    >
                        Ver todo →
                    </button>
                </div>

                <div className="chart-body">
                    <div className="activity-list">
                        {[
                            { type: 'ticket', user: 'Juan Pérez', action: 'creó el ticket', item: '#1234', time: 'hace 5 min', icon: '🎫', priority: 'high' },
                            { type: 'message', user: 'María García', action: 'respondió en', item: '#1233', time: 'hace 12 min', icon: '💬', priority: 'medium' },
                            { type: 'resolved', user: 'Carlos López', action: 'resolvió', item: '#1232', time: 'hace 25 min', icon: '✅', priority: 'low' },
                            { type: 'escalated', user: 'Ana Martínez', action: 'escaló', item: '#1231', time: 'hace 1 hora', icon: '⬆️', priority: 'high' },
                            { type: 'closed', user: 'Sistema', action: 'cerró automáticamente', item: '#1230', time: 'hace 2 horas', icon: '🔒', priority: 'low' }
                        ].map((activity, index) => (
                            <div
                                key={index}
                                className={`activity-item priority-${activity.priority}`}
                                onClick={() => handleActivityClick(activity)}
                                role="button"
                                tabIndex={0}
                                aria-label={`Actividad: ${activity.user} ${activity.action} ${activity.item}`}
                                onKeyPress={(e) => {
                                    if (e.key === 'Enter' || e.key === ' ') {
                                        handleActivityClick(activity);
                                    }
                                }}
                            >
                                <span className="activity-icon">{activity.icon}</span>
                                <div className="activity-content">
                                    <p className="activity-text">
                                        <strong>{activity.user}</strong> {activity.action} <span className="activity-highlight">{activity.item}</span>
                                    </p>
                                    <span className="activity-time">{activity.time}</span>
                                </div>
                                <div className="activity-priority-indicator"></div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChartsSection;