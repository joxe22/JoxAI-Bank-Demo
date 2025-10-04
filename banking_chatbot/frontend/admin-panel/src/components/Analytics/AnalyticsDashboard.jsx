// frontend/admin-panel/src/components/Analytics/AnalyticsDashboard.jsx
import React, { useState, useEffect } from 'react';
import analyticsService from '../../services/analyticsService';
import '../../styles/components/AnalyticsDashboard.css';

const AnalyticsDashboard = () => {
    const [period, setPeriod] = useState('week');
    const [selectedMetric, setSelectedMetric] = useState('conversations');
    const [loading, setLoading] = useState(true);
    const [dashboardData, setDashboardData] = useState(null);
    const [ticketStats, setTicketStats] = useState(null);

    useEffect(() => {
        loadDashboardData();
    }, [period]);

    const loadDashboardData = async () => {
        try {
            setLoading(true);
            const [dashboard, tickets] = await Promise.all([
                analyticsService.getDashboardMetrics(period),
                analyticsService.getTicketStatistics(period)
            ]);
            setDashboardData(dashboard);
            setTicketStats(tickets);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="analytics-dashboard"><div className="loading">Cargando analytics...</div></div>;
    }

    if (!dashboardData) {
        return <div className="analytics-dashboard"><div className="error">Error al cargar datos</div></div>;
    }

    const metrics = {
        overview: [
            { 
                label: 'Total Conversaciones', 
                value: dashboardData.total_conversations?.toString() || '0', 
                change: '+12.5%', 
                trend: 'up', 
                icon: '💬' 
            },
            { 
                label: 'Tiempo Prom. Respuesta', 
                value: ticketStats?.avg_resolution_hours ? `${ticketStats.avg_resolution_hours.toFixed(1)}h` : 'N/A',
                change: '-8.2%', 
                trend: 'down', 
                icon: '⏱️' 
            },
            { 
                label: 'Total Tickets', 
                value: dashboardData.total_tickets?.toString() || '0',
                change: '+5.1%', 
                trend: 'up', 
                icon: '✅' 
            },
            { 
                label: 'Tasa Escalación', 
                value: `${dashboardData.escalation_rate || 0}%`,
                change: '+0.3', 
                trend: 'up', 
                icon: '⭐' 
            }
        ],
        channels: [
            { name: 'Web Widget', value: 1245, percentage: 50.6, color: '#667eea' },
            { name: 'WhatsApp', value: 734, percentage: 29.9, color: '#25D366' },
            { name: 'Email', value: 321, percentage: 13.1, color: '#EA4335' },
            { name: 'Teléfono', value: 158, percentage: 6.4, color: '#4285F4' }
        ],
        topIssues: [
            { issue: 'Consulta de saldo', count: 456, percentage: 18.5, trend: 'up' },
            { issue: 'Problemas de acceso', count: 342, percentage: 13.9, trend: 'down' },
            { issue: 'Transferencias', count: 298, percentage: 12.1, trend: 'up' },
            { issue: 'Tarjetas bloqueadas', count: 234, percentage: 9.5, trend: 'stable' },
            { issue: 'Solicitud de préstamo', count: 187, percentage: 7.6, trend: 'up' }
        ],
        responseTime: {
            labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            data: [3.2, 2.8, 1.9, 2.5, 3.1, 2.7]
        }
    };

    const getTrendIcon = (trend) => {
        if (trend === 'up') return '↗';
        if (trend === 'down') return '↘';
        return '→';
    };

    const getTrendClass = (trend) => {
        if (trend === 'up') return 'trend-up';
        if (trend === 'down') return 'trend-down';
        return 'trend-stable';
    };

    return (
        <div className="analytics-dashboard">
            {/* Header con selector de período */}
            <div className="analytics-header">
                <div className="header-left">
                    <h2>Analytics</h2>
                    <p className="subtitle">Análisis detallado del rendimiento</p>
                </div>
                <div className="period-selector">
                    <button
                        className={`period-btn ${period === 'day' ? 'active' : ''}`}
                        onClick={() => setPeriod('day')}
                    >
                        Hoy
                    </button>
                    <button
                        className={`period-btn ${period === 'week' ? 'active' : ''}`}
                        onClick={() => setPeriod('week')}
                    >
                        Semana
                    </button>
                    <button
                        className={`period-btn ${period === 'month' ? 'active' : ''}`}
                        onClick={() => setPeriod('month')}
                    >
                        Mes
                    </button>
                    <button
                        className={`period-btn ${period === 'year' ? 'active' : ''}`}
                        onClick={() => setPeriod('year')}
                    >
                        Año
                    </button>
                    <button className="period-btn custom">
                        📅 Personalizado
                    </button>
                </div>
            </div>

            {/* Métricas Overview */}
            <div className="metrics-overview">
                {metrics.overview.map((metric, index) => (
                    <div key={index} className="overview-card">
                        <div className="card-icon">{metric.icon}</div>
                        <div className="card-content">
                            <span className="card-label">{metric.label}</span>
                            <h3 className="card-value">{metric.value}</h3>
                            <span className={`card-change ${getTrendClass(metric.trend)}`}>
                {getTrendIcon(metric.trend)} {metric.change}
              </span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Sección de Gráficas */}
            <div className="analytics-grid">

                {/* Tiempo de Respuesta */}
                <div className="analytics-card full-width">
                    <div className="card-header">
                        <h3>Tiempo de Respuesta Promedio</h3>
                        <div className="card-actions">
                            <button className="icon-btn">📊</button>
                            <button className="icon-btn">⋮</button>
                        </div>
                    </div>
                    <div className="card-body">
                        <div className="line-chart">
                            {metrics.responseTime.data.map((value, index) => {
                                const maxValue = Math.max(...metrics.responseTime.data);
                                const height = (value / maxValue) * 100;

                                return (
                                    <div key={index} className="chart-column">
                                        <div className="chart-tooltip">{value} min</div>
                                        <div
                                            className="chart-bar"
                                            style={{ height: `${height}%` }}
                                        ></div>
                                        <span className="chart-label">{metrics.responseTime.labels[index]}</span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* Canales de Comunicación */}
                <div className="analytics-card">
                    <div className="card-header">
                        <h3>Canales de Comunicación</h3>
                    </div>
                    <div className="card-body">
                        <div className="channels-chart">
                            {metrics.channels.map((channel, index) => (
                                <div key={index} className="channel-item">
                                    <div className="channel-info">
                                        <div
                                            className="channel-indicator"
                                            style={{ background: channel.color }}
                                        ></div>
                                        <span className="channel-name">{channel.name}</span>
                                    </div>
                                    <div className="channel-stats">
                                        <span className="channel-value">{channel.value}</span>
                                        <span className="channel-percentage">{channel.percentage}%</span>
                                    </div>
                                    <div className="channel-bar-container">
                                        <div
                                            className="channel-bar"
                                            style={{
                                                width: `${channel.percentage}%`,
                                                background: channel.color
                                            }}
                                        ></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Top Issues */}
                <div className="analytics-card">
                    <div className="card-header">
                        <h3>Principales Problemas</h3>
                        <button className="link-btn">Ver todo →</button>
                    </div>
                    <div className="card-body">
                        <div className="issues-list">
                            {metrics.topIssues.map((issue, index) => (
                                <div key={index} className="issue-item">
                                    <div className="issue-rank">{index + 1}</div>
                                    <div className="issue-content">
                                        <div className="issue-header">
                                            <span className="issue-name">{issue.issue}</span>
                                            <span className={`issue-trend ${getTrendClass(issue.trend)}`}>
                        {getTrendIcon(issue.trend)}
                      </span>
                                        </div>
                                        <div className="issue-stats">
                                            <span className="issue-count">{issue.count} casos</span>
                                            <span className="issue-percentage">{issue.percentage}%</span>
                                        </div>
                                        <div className="issue-progress">
                                            <div
                                                className="progress-bar"
                                                style={{ width: `${issue.percentage * 5}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Tasa de Resolución por Hora */}
                <div className="analytics-card">
                    <div className="card-header">
                        <h3>Tasa de Resolución</h3>
                    </div>
                    <div className="card-body">
                        <div className="resolution-stats">
                            <div className="stat-circle">
                                <svg viewBox="0 0 36 36" className="circular-chart">
                                    <path
                                        className="circle-bg"
                                        d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                                    />
                                    <path
                                        className="circle"
                                        strokeDasharray="89.4, 100"
                                        d="M18 2.0845
                      a 15.9155 15.9155 0 0 1 0 31.831
                      a 15.9155 15.9155 0 0 1 0 -31.831"
                                    />
                                    <text x="18" y="20.35" className="percentage">89.4%</text>
                                </svg>
                            </div>
                            <div className="stat-details">
                                <div className="stat-row">
                                    <span className="stat-label">✅ Resueltos</span>
                                    <span className="stat-value">2,197</span>
                                </div>
                                <div className="stat-row">
                                    <span className="stat-label">⏳ Pendientes</span>
                                    <span className="stat-value">261</span>
                                </div>
                                <div className="stat-row">
                                    <span className="stat-label">📊 Total</span>
                                    <span className="stat-value">2,458</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Performance por Agente */}
                <div className="analytics-card full-width">
                    <div className="card-header">
                        <h3>Performance por Agente</h3>
                        <button className="link-btn">Ver detalles →</button>
                    </div>
                    <div className="card-body">
                        <div className="agents-table">
                            <table>
                                <thead>
                                <tr>
                                    <th>Agente</th>
                                    <th>Conversaciones</th>
                                    <th>Tiempo Prom.</th>
                                    <th>Satisfacción</th>
                                    <th>Tasa Resolución</th>
                                </tr>
                                </thead>
                                <tbody>
                                {[
                                    { name: 'Juan Pérez', conversations: 342, avgTime: '2.1 min', satisfaction: 4.8, resolution: 92 },
                                    { name: 'María García', conversations: 318, avgTime: '2.3 min', satisfaction: 4.7, resolution: 90 },
                                    { name: 'Carlos López', conversations: 289, avgTime: '2.5 min', satisfaction: 4.6, resolution: 88 },
                                    { name: 'Ana Martínez', conversations: 256, avgTime: '2.2 min', satisfaction: 4.9, resolution: 94 }
                                ].map((agent, index) => (
                                    <tr key={index}>
                                        <td>
                                            <div className="agent-cell">
                                                <div className="agent-avatar">{agent.name.charAt(0)}</div>
                                                <span>{agent.name}</span>
                                            </div>
                                        </td>
                                        <td>{agent.conversations}</td>
                                        <td>{agent.avgTime}</td>
                                        <td>
                                            <span className="rating">⭐ {agent.satisfaction}</span>
                                        </td>
                                        <td>
                                            <div className="resolution-cell">
                                                <span>{agent.resolution}%</span>
                                                <div className="mini-progress">
                                                    <div
                                                        className="mini-progress-bar"
                                                        style={{ width: `${agent.resolution}%` }}
                                                    ></div>
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default AnalyticsDashboard;