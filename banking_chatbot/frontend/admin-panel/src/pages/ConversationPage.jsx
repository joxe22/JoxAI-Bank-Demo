// frontend/admin-panel/src/pages/ConversationsPage.jsx
import React, { useState, useEffect } from 'react';
import conversationsService from '../services/conversationsService';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import '../styles/pages/ConversationPage.css';

const ConversationsPage = () => {
    const [conversations, setConversations] = useState([]);
    const [selectedConversation, setSelectedConversation] = useState(null);
    const [selectedMessages, setSelectedMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        loadConversations();
    }, [filter]);

    const loadConversations = async () => {
        setIsLoading(true);
        setError(null);
        try {
            let data;
            const params = { limit: 100 };
            
            if (filter === 'active') {
                data = await conversationsService.getActiveConversations(100);
            } else if (filter === 'escalated') {
                data = await conversationsService.getEscalatedConversations(100);
            } else {
                data = await conversationsService.getAllConversations(params);
            }

            const conversationsList = data.conversations || [];
            setConversations(conversationsList);
        } catch (error) {
            console.error('Error cargando conversaciones:', error);
            setError('Error al cargar las conversaciones. Por favor, intente nuevamente.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleSelectConversation = async (conversation) => {
        setSelectedConversation(conversation);
        try {
            const data = await conversationsService.getConversation(conversation.id);
            setSelectedMessages(data.messages || []);
        } catch (error) {
            console.error('Error loading conversation messages:', error);
            setSelectedMessages([]);
        }
    };

    const activeCount = conversations.filter(c => c.status === 'active').length;
    const escalatedCount = conversations.filter(c => c.escalated).length;
    const endedCount = conversations.filter(c => c.status === 'ended').length;

    const filterOptions = [
        { value: 'all', label: 'Todas', count: conversations.length, icon: '💬', color: '#667eea' },
        { value: 'active', label: 'Activas', count: activeCount, icon: '🟢', color: '#43e97b' },
        { value: 'escalated', label: 'Escaladas', count: escalatedCount, icon: '🔴', color: '#ff6b6b' },
        { value: 'ended', label: 'Finalizadas', count: endedCount, icon: '⚫', color: '#95a5a6' }
    ];

    const getStatusColor = (status) => {
        switch(status) {
            case 'active': return '#43e97b';
            case 'ended': return '#95a5a6';
            default: return '#667eea';
        }
    };

    const filteredConversations = conversations.filter(conv => {
        if (searchTerm) {
            const searchLower = searchTerm.toLowerCase();
            const matchesSearch = 
                String(conv.user_id ?? '').toLowerCase().includes(searchLower) ||
                String(conv.id).toLowerCase().includes(searchLower);
            if (!matchesSearch) return false;
        }
        
        if (filter === 'all') return true;
        if (filter === 'escalated') return conv.escalated;
        return conv.status === filter;
    });

    if (isLoading) {
        return (
            <div className="conversations-page">
                <LoadingSpinner size="large" message="Cargando conversaciones..." />
            </div>
        );
    }

    return (
        <div className="conversations-page">
            {/* Header Modernizado */}
            <div className="conversations-header">
                <div className="header-content">
                    <h1>💬 Conversaciones</h1>
                    <p className="page-subtitle">Gestiona todas las conversaciones en tiempo real con tu equipo</p>
                </div>
                <div className="header-actions">
                    <div className="search-container">
                        <input
                            type="text"
                            placeholder="🔍 Buscar conversaciones..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="search-input"
                        />
                    </div>
                    <button className="btn-secondary refresh-btn" onClick={loadConversations}>
                        <span className="btn-icon">🔄</span>
                        Actualizar
                    </button>
                </div>
            </div>

            {/* Error Display */}
            {error && (
                <div className="error-message" style={{
                    padding: '12px',
                    margin: '16px 0',
                    backgroundColor: '#fee',
                    color: '#c33',
                    borderRadius: '8px'
                }}>
                    {error}
                </div>
            )}

            {/* Filtros Modernizados */}
            <div className="conversations-filters">
                {filterOptions.map(option => (
                    <button
                        key={option.value}
                        className={`filter-card ${filter === option.value ? 'active' : ''}`}
                        onClick={() => setFilter(option.value)}
                        style={{ '--filter-color': option.color }}
                    >
                        <div className="filter-icon">{option.icon}</div>
                        <div className="filter-content">
                            <span className="filter-label">{option.label}</span>
                            <span className="filter-count">{option.count}</span>
                        </div>
                        <div className="filter-indicator"></div>
                    </button>
                ))}
            </div>

            <div className="conversations-content">
                {/* Lista de Conversaciones Modernizada */}
                <div className="conversations-list-container">
                    <div className="list-header">
                        <h3>Conversaciones Recientes</h3>
                        <span className="total-count">{filteredConversations.length} conversaciones</span>
                    </div>
                    <div className="conversations-list">
                        {filteredConversations.map(conversation => (
                            <div
                                key={conversation.id}
                                className={`conversation-card ${selectedConversation?.id === conversation.id ? 'selected' : ''}`}
                                onClick={() => handleSelectConversation(conversation)}
                            >
                                <div className="card-header">
                                    <div className="customer-info">
                                        <div className="avatar-container">
                                            <div
                                                className="conversation-avatar"
                                                style={{
                                                    background: `linear-gradient(135deg, ${getStatusColor(conversation.status)}, #667eea)`
                                                }}
                                            >
                                                {conversation.user_id ? String(conversation.user_id).charAt(0).toUpperCase() : '?'}
                                            </div>
                                            <div
                                                className="status-indicator"
                                                style={{ backgroundColor: getStatusColor(conversation.status) }}
                                            ></div>
                                        </div>
                                        <div className="customer-details">
                                            <h4 className="customer-name">Usuario: {conversation.user_id || 'Anónimo'}</h4>
                                            <div className="conversation-meta">
                                                <span className="conversation-id">ID: {conversation.id}</span>
                                                {conversation.escalated && (
                                                    <span className="escalated-badge" style={{ backgroundColor: '#ff6b6b', color: 'white', padding: '2px 8px', borderRadius: '12px', fontSize: '11px' }}>
                                                        Escalada
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="conversation-time">
                                        {new Date(conversation.updated_at).toLocaleTimeString('es-ES', {
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                    </div>
                                </div>

                                <div className="card-body">
                                    <p className="last-message">
                                        {conversation.status === 'active' ? 'Conversación activa' : 'Conversación finalizada'}
                                        {conversation.escalated && ' - Requiere atención'}
                                    </p>
                                </div>

                                <div className="card-footer">
                                    <span className="status-text" style={{ color: getStatusColor(conversation.status) }}>
                                        {conversation.status === 'active' ? 'Activa' : 'Finalizada'}
                                    </span>
                                    <div className="action-buttons">
                                        <button className="action-btn">💬</button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Panel de Detalles Modernizado */}
                <div className="conversation-detail-panel">
                    {selectedConversation ? (
                        <div className="chat-container">
                            <div className="chat-header">
                                <div className="chat-customer-info">
                                    <div
                                        className="customer-avatar-large"
                                        style={{
                                            background: `linear-gradient(135deg, ${getStatusColor(selectedConversation.status)}, #667eea)`
                                        }}
                                    >
                                        {selectedConversation.user_id ? String(selectedConversation.user_id).charAt(0).toUpperCase() : '?'}
                                    </div>
                                    <div className="customer-details">
                                        <h3>Usuario: {selectedConversation.user_id || 'Anónimo'}</h3>
                                        <div className="customer-status">
                                            <span
                                                className="status-badge"
                                                style={{ backgroundColor: getStatusColor(selectedConversation.status) }}
                                            >
                                                {selectedConversation.status}
                                            </span>
                                            {selectedConversation.escalated && (
                                                <span className="channel-info" style={{ color: '#ff6b6b' }}>
                                                    🔴 Escalada
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                                <div className="chat-actions">
                                    <button className="chat-action-btn">🔄</button>
                                    <button className="chat-action-btn">⋮</button>
                                </div>
                            </div>

                            <div className="chat-messages">
                                {selectedMessages.length > 0 ? (
                                    selectedMessages.map((msg, index) => (
                                        <div key={index} className={`message ${msg.role}`}>
                                            <div className="message-content">
                                                <p>{msg.content}</p>
                                                <span className="message-time">
                                                    {new Date(msg.timestamp).toLocaleTimeString('es-ES', {
                                                        hour: '2-digit',
                                                        minute: '2-digit'
                                                    })}
                                                </span>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="empty-chat-state">
                                        <div className="empty-icon">💬</div>
                                        <h3>No hay mensajes</h3>
                                        <p>Esta conversación aún no tiene mensajes</p>
                                    </div>
                                )}
                            </div>

                            <div className="chat-input-container">
                                <div className="input-actions">
                                    <button className="input-action-btn">😊</button>
                                    <button className="input-action-btn">📎</button>
                                    <button className="input-action-btn">🖼️</button>
                                </div>
                                <input
                                    type="text"
                                    placeholder="Escribe tu mensaje..."
                                    className="chat-input"
                                />
                                <button className="send-btn">
                                    ➤
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="no-conversation-selected">
                            <div className="empty-state">
                                <div className="empty-icon">💬</div>
                                <h3>Selecciona una conversación</h3>
                                <p>Elige una conversación de la lista para ver los detalles y chatear</p>
                                <div className="empty-actions">
                                    <button className="btn-primary">
                                        ➕ Crear Nueva Conversación
                                    </button>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ConversationsPage;
