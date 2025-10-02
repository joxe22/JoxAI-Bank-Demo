// frontend/admin-panel/src/components/Analytics/ConversationAnalytics.jsx
import React, { useState } from 'react';
import '../../styles/components/ConversationAnalytics.css';

const ConversationAnalytics = () => {
    const [viewMode, setViewMode] = useState('overview');

    const conversationMetrics = {
        totalConversations: 2458,
        activeConversations: 45,
        avgDuration: '8.5 min',
        avgMessagesPerConversation: 12.3,
        escalationRate: '15.2%',
        abandonmentRate: '5.8%'
    };

    const conversationFlow = [
        { stage: 'Iniciadas', count: 2458, percentage: 100, color: '#667eea' },
        { stage: 'Bot Respondió', count: 2401, percentage: 97.7, color: '#764ba2' },
        { stage: 'Escaladas', count: 374, percentage: 15.2, color: '#f093fb' },
        { stage: 'Resueltas', count: 2197, percentage: 89.4, color: '#43e97b' },
        { stage: 'Abandonadas', count: 143, percentage: 5.8, color: '#ea4335' }
    ];

    const intentDistribution = [
        { intent: 'Consulta de saldo', count: 456, percentage: 18.5, confidence: 95 },
        { intent: 'Transferencias', count: 398, percentage: 16.2, confidence: 92 },
        { intent: 'Problemas de acceso', count: 342, percentage: 13.9, confidence: 88 },
        { intent: 'Tarjetas', count: 298, percentage: 12.1, confidence: 90 },
        { intent: 'Préstamos', count: 234, percentage: 9.5, confidence: 87 },
        { intent: 'Otros', count: 730, percentage: 29.7, confidence: 75 }
    ];

    const hourlyDistribution = [
        { hour: '00-04', conversations: 45, percentage: 1.8 },
        { hour: '04-08', conversations: 89, percentage: 3.6 },
        { hour: '08-12', conversations: 678, percentage: 27.6 },
        { hour: '12-16', conversations: 892, percentage: 36.3 },
        { hour: '16-20', conversations: 534, percentage: 21.7 },
        { hour: '20-00', conversations: 220, percentage: 9.0 }
    ];

    return (
        <div className="conversation-analytics">
            <div className="analytics-header">
                <h2>Análisis de Conversaciones</h2>
                <div className="view-mode-toggle">
                    <button
                        className={viewMode === 'overview' ? 'active' : ''}
                        onClick={() => setViewMode('overview')}
                    >
                        Vista General
                    </button>
                    <button
                        className={viewMode === 'detailed' ? 'active' : ''}
                        onClick={() => setViewMode('detailed')}
                    >
                        Detallado
                    </button>
                </div>
            </div>

            {/* Métricas Clave */}
            <div className="metrics-grid">
                <div className="metric-box">
                    <span className="metric-icon">💬</span>
                    <div className="metric-content">
                        <span className="metric-label">Total Conversaciones</span>
                        <span className="metric-value">{conversationMetrics.totalConversations}</span>
                    </div>
                </div>

                <div className="metric-box">
                    <span className="metric-icon">🟢</span>
                    <div className="metric-content">
                        <span className="metric-label">Conversaciones Activas</span>
                        <span className="metric-value">{conversationMetrics.activeConversations}</span>
                    </div>
                </div>

                <div className="metric-box">
                    <span className="metric-icon">⏱️</span>
                    <div className="metric-content">
                        <span className="metric-label">Duración Promedio</span>
                        <span className="metric-value">{conversationMetrics.avgDuration}</span>
                    </div>
                </div>

                <div className="metric-box">
                    <span className="metric-icon">✉️</span>
                    <div className="metric-content">
                        <span className="metric-label">Mensajes Promedio</span>
                        <span className="metric-value">{conversationMetrics.avgMessagesPerConversation}</span>
                    </div>
                </div>

                <div className="metric-box">
                    <span className="metric-icon">⬆️</span>
                    <div className="metric-content">
                        <span className="metric-label">Tasa de Escalación</span>
                        <span className="metric-value">{conversationMetrics.escalationRate}</span>
                    </div>
                </div>

                <div className="metric-box">
                    <span className="metric-icon">🚪</span>
                    <div className="metric-content">
                        <span className="metric-label">Tasa de Abandono</span>
                        <span className="metric-value">{conversationMetrics.abandonmentRate}</span>
                    </div>
                </div>
            </div>

            {/* Flujo de Conversaciones */}
            <div className="analytics-card">
                <h3>Flujo de Conversaciones</h3>
                <div className="conversation-flow">
                    {conversationFlow.map((stage, index) => (
                        <div key={index} className="flow-stage">
                            <div className="stage-header">
                                <span className="stage-name">{stage.stage}</span>
                                <span className="stage-count">{stage.count}</span>
                            </div>
                            <div className="stage-bar-container">
                                <div
                                    className="stage-bar"
                                    style={{
                                        width: `${stage.percentage}%`,
                                        background: stage.color
                                    }}
                                >
                                    <span className="stage-percentage">{stage.percentage}%</span>
                                </div>
                            </div>
                            {index < conversationFlow.length - 1 && (
                                <div className="flow-arrow">↓</div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            <div className="analytics-row">
                {/* Distribución de Intenciones */}
                <div className="analytics-card half-width">
                    <h3>Distribución de Intenciones</h3>
                    <div className="intent-list">
                        {intentDistribution.map((intent, index) => (
                            <div key={index} className="intent-item">
                                <div className="intent-header">
                                    <span className="intent-name">{intent.intent}</span>
                                    <span className="intent-count">{intent.count}</span>
                                </div>
                                <div className="intent-bars">
                                    <div className="intent-bar-container">
                                        <div
                                            className="intent-bar"
                                            style={{ width: `${intent.percentage * 5}%` }}
                                        >
                                            <span className="bar-label">{intent.percentage}%</span>
                                        </div>
                                    </div>
                                    <div className="confidence-bar-container">
                                        <div
                                            className="confidence-bar"
                                            style={{ width: `${intent.confidence}%` }}
                                            title={`Confianza: ${intent.confidence}%`}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Distribución Horaria */}
                <div className="analytics-card half-width">
                    <h3>Distribución Horaria</h3>
                    <div className="hourly-chart">
                        {hourlyDistribution.map((period, index) => {
                            const maxConversations = Math.max(...hourlyDistribution.map(p => p.conversations));
                            const height = (period.conversations / maxConversations) * 100;

                            return (
                                <div key={index} className="hour-column">
                                    <div className="hour-bar-container">
                                        <div
                                            className="hour-bar"
                                            style={{ height: `${height}%` }}
                                        >
                                            <span className="bar-tooltip">{period.conversations}</span>
                                        </div>
                                    </div>
                                    <div className="hour-info">
                                        <span className="hour-label">{period.hour}</span>
                                        <span className="hour-percentage">{period.percentage}%</span>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>

            {/* Sentimiento de Conversaciones */}
            <div className="analytics-card">
                <h3>Análisis de Sentimiento</h3>
                <div className="sentiment-analysis">
                    <div className="sentiment-overview">
                        <div className="sentiment-card positive">
                            <span className="sentiment-icon">😊</span>
                            <span className="sentiment-label">Positivo</span>
                            <span className="sentiment-value">64.3%</span>
                            <span className="sentiment-count">1,580 conversaciones</span>
                        </div>
                        <div className="sentiment-card neutral">
                            <span className="sentiment-icon">😐</span>
                            <span className="sentiment-label">Neutral</span>
                            <span className="sentiment-value">28.5%</span>
                            <span className="sentiment-count">701 conversaciones</span>
                        </div>
                        <div className="sentiment-card negative">
                            <span className="sentiment-icon">😞</span>
                            <span className="sentiment-label">Negativo</span>
                            <span className="sentiment-value">7.2%</span>
                            <span className="sentiment-count">177 conversaciones</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ConversationAnalytics;