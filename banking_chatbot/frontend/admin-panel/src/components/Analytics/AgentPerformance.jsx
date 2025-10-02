// frontend/admin-panel/src/components/Analytics/AgentPerformance.jsx
import React, { useState } from 'react';
import '../../styles/components/AgentPerformance.css';

const AgentPerformance = () => {
    const [selectedAgent, setSelectedAgent] = useState(null);
    const [sortBy, setSortBy] = useState('conversations');

    const agents = [
        {
            id: 1,
            name: 'Juan Pérez',
            avatar: null,
            status: 'online',
            conversations: 342,
            avgResponseTime: '2.1 min',
            satisfaction: 4.8,
            resolutionRate: 92,
            activeTickets: 8,
            totalTickets: 156,
            firstResponseTime: '45 seg',
            onlineTime: '7.5 hrs'
        },
        {
            id: 2,
            name: 'María García',
            avatar: null,
            status: 'online',
            conversations: 318,
            avgResponseTime: '2.3 min',
            satisfaction: 4.7,
            resolutionRate: 90,
            activeTickets: 6,
            totalTickets: 142,
            firstResponseTime: '52 seg',
            onlineTime: '8.2 hrs'
        },
        {
            id: 3,
            name: 'Carlos López',
            avatar: null,
            status: 'away',
            conversations: 289,
            avgResponseTime: '2.5 min',
            satisfaction: 4.6,
            resolutionRate: 88,
            activeTickets: 5,
            totalTickets: 128,
            firstResponseTime: '1.1 min',
            onlineTime: '6.8 hrs'
        },
        {
            id: 4,
            name: 'Ana Martínez',
            avatar: null,
            status: 'online',
            conversations: 256,
            avgResponseTime: '2.2 min',
            satisfaction: 4.9,
            resolutionRate: 94,
            activeTickets: 7,
            totalTickets: 118,
            firstResponseTime: '38 seg',
            onlineTime: '7.9 hrs'
        }
    ];

    const sortAgents = (agents, sortBy) => {
        return [...agents].sort((a, b) => {
            switch(sortBy) {
                case 'conversations':
                    return b.conversations - a.conversations;
                case 'satisfaction':
                    return b.satisfaction - a.satisfaction;
                case 'resolution':
                    return b.resolutionRate - a.resolutionRate;
                case 'responseTime':
                    return parseFloat(a.avgResponseTime) - parseFloat(b.avgResponseTime);
                default:
                    return 0;
            }
        });
    };

    const sortedAgents = sortAgents(agents, sortBy);

    const getStatusColor = (status) => {
        switch(status) {
            case 'online': return '#43e97b';
            case 'away': return '#feca57';
            case 'offline': return '#95a5a6';
            default: return '#95a5a6';
        }
    };

    const getStatusLabel = (status) => {
        switch(status) {
            case 'online': return 'En línea';
            case 'away': return 'Ausente';
            case 'offline': return 'Desconectado';
            default: return 'Desconocido';
        }
    };

    return (
        <div className="agent-performance">
            <div className="performance-header">
                <div className="header-left">
                    <h2>Performance de Agentes</h2>
                    <p className="subtitle">Rendimiento individual y métricas de equipo</p>
                </div>
                <div className="header-right">
                    <select
                        value={sortBy}
                        onChange={(e) => setSortBy(e.target.value)}
                        className="sort-select"
                    >
                        <option value="conversations">Más conversaciones</option>
                        <option value="satisfaction">Mayor satisfacción</option>
                        <option value="resolution">Mayor resolución</option>
                        <option value="responseTime">Menor tiempo respuesta</option>
                    </select>
                </div>
            </div>

            {/* Estadísticas del Equipo */}
            <div className="team-stats">
                <div className="stat-card">
                    <span className="stat-icon">👥</span>
                    <div className="stat-content">
                        <span className="stat-label">Agentes Activos</span>
                        <span className="stat-value">{agents.filter(a => a.status === 'online').length}/{agents.length}</span>
                    </div>
                </div>

                <div className="stat-card">
                    <span className="stat-icon">💬</span>
                    <div className="stat-content">
                        <span className="stat-label">Conversaciones Totales</span>
                        <span className="stat-value">{agents.reduce((acc, a) => acc + a.conversations, 0)}</span>
                    </div>
                </div>

                <div className="stat-card">
                    <span className="stat-icon">⭐</span>
                    <div className="stat-content">
                        <span className="stat-label">Satisfacción Promedio</span>
                        <span className="stat-value">
              {(agents.reduce((acc, a) => acc + a.satisfaction, 0) / agents.length).toFixed(1)}
            </span>
                    </div>
                </div>

                <div className="stat-card">
                    <span className="stat-icon">✅</span>
                    <div className="stat-content">
                        <span className="stat-label">Tasa Resolución</span>
                        <span className="stat-value">
              {(agents.reduce((acc, a) => acc + a.resolutionRate, 0) / agents.length).toFixed(0)}%
            </span>
                    </div>
                </div>
            </div>

            {/* Lista de Agentes */}
            <div className="agents-grid">
                {sortedAgents.map((agent) => (
                    <div
                        key={agent.id}
                        className={`agent-card ${selectedAgent === agent.id ? 'selected' : ''}`}
                        onClick={() => setSelectedAgent(agent.id)}
                    >
                        <div className="agent-card-header">
                            <div className="agent-info">
                                <div className="agent-avatar">
                                    {agent.avatar ? (
                                        <img src={agent.avatar} alt={agent.name} />
                                    ) : (
                                        <span>{agent.name.charAt(0)}</span>
                                    )}
                                    <span
                                        className="status-indicator"
                                        style={{ background: getStatusColor(agent.status) }}
                                    ></span>
                                </div>
                                <div className="agent-details">
                                    <h4 className="agent-name">{agent.name}</h4>
                                    <span className="agent-status">{getStatusLabel(agent.status)}</span>
                                </div>
                            </div>
                            <button className="more-btn">⋮</button>
                        </div>

                        <div className="agent-card-body">
                            <div className="metric-row">
                                <div className="metric-item">
                                    <span className="metric-label">Conversaciones</span>
                                    <span className="metric-value">{agent.conversations}</span>
                                </div>
                                <div className="metric-item">
                                    <span className="metric-label">Tickets Activos</span>
                                    <span className="metric-value">{agent.activeTickets}</span>
                                </div>
                            </div>

                            <div className="metric-row">
                                <div className="metric-item">
                                    <span className="metric-label">Tiempo Respuesta</span>
                                    <span className="metric-value">{agent.avgResponseTime}</span>
                                </div>
                                <div className="metric-item">
                                    <span className="metric-label">Primer Respuesta</span>
                                    <span className="metric-value">{agent.firstResponseTime}</span>
                                </div>
                            </div>

                            <div className="satisfaction-row">
                                <span className="satisfaction-label">Satisfacción</span>
                                <div className="satisfaction-bar">
                                    <div
                                        className="satisfaction-fill"
                                        style={{ width: `${(agent.satisfaction / 5) * 100}%` }}
                                    ></div>
                                </div>
                                <span className="satisfaction-value">⭐ {agent.satisfaction}</span>
                            </div>

                            <div className="resolution-row">
                                <span className="resolution-label">Tasa de Resolución</span>
                                <div className="resolution-bar">
                                    <div
                                        className="resolution-fill"
                                        style={{ width: `${agent.resolutionRate}%` }}
                                    ></div>
                                </div>
                                <span className="resolution-value">{agent.resolutionRate}%</span>
                            </div>

                            <div className="time-online">
                                <span className="time-icon">⏱️</span>
                                <span>Tiempo en línea hoy: <strong>{agent.onlineTime}</strong></span>
                            </div>
                        </div>

                        <div className="agent-card-footer">
                            <button className="view-details-btn">
                                Ver Detalles →
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Comparación de Agentes */}
            <div className="comparison-section">
                <h3>Comparación de Performance</h3>
                <div className="comparison-table">
                    <table>
                        <thead>
                        <tr>
                            <th>Agente</th>
                            <th>Conversaciones</th>
                            <th>Tiempo Respuesta</th>
                            <th>Satisfacción</th>
                            <th>Resolución</th>
                            <th>Tiempo Online</th>
                        </tr>
                        </thead>
                        <tbody>
                        {sortedAgents.map((agent) => (
                            <tr key={agent.id}>
                                <td>
                                    <div className="table-agent">
                                        <div className="table-avatar">
                                            {agent.name.charAt(0)}
                                        </div>
                                        <span>{agent.name}</span>
                                    </div>
                                </td>
                                <td>{agent.conversations}</td>
                                <td>{agent.avgResponseTime}</td>
                                <td>
                                    <span className="table-rating">⭐ {agent.satisfaction}</span>
                                </td>
                                <td>
                                    <div className="table-resolution">
                                        <span>{agent.resolutionRate}%</span>
                                        <div className="mini-bar">
                                            <div
                                                className="mini-bar-fill"
                                                style={{ width: `${agent.resolutionRate}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                </td>
                                <td>{agent.onlineTime}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default AgentPerformance;