// frontend/admin-panel/src/pages/ConversationsPage.jsx
import React, { useState, useEffect } from 'react';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import '../styles/pages/ConversationPage.css';

const ConversationsPage = () => {
    const [conversations, setConversations] = useState([]);
    const [selectedConversation, setSelectedConversation] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [filter, setFilter] = useState('all');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        loadConversations();
    }, [filter]);

    const loadConversations = async () => {
        setIsLoading(true);
        try {
            await new Promise(resolve => setTimeout(resolve, 800));

            const mockConversations = [
                {
                    id: 1,
                    customerName: 'Juan Pérez',
                    status: 'active',
                    lastMessage: 'Necesito ayuda con mi cuenta, no puedo acceder',
                    timestamp: new Date().toISOString(),
                    unreadCount: 2,
                    avatar: null,
                    priority: 'high',
                    channel: 'whatsapp'
                },
                {
                    id: 2,
                    customerName: 'María García',
                    status: 'waiting',
                    lastMessage: 'Gracias por la información, fue muy útil',
                    timestamp: new Date(Date.now() - 3600000).toISOString(),
                    unreadCount: 0,
                    avatar: null,
                    priority: 'medium',
                    channel: 'web'
                },
                {
                    id: 3,
                    customerName: 'Carlos López',
                    status: 'active',
                    lastMessage: '¿Pueden ayudarme con una transferencia?',
                    timestamp: new Date(Date.now() - 1800000).toISOString(),
                    unreadCount: 1,
                    avatar: null,
                    priority: 'high',
                    channel: 'phone'
                },
                {
                    id: 4,
                    customerName: 'Ana Martínez',
                    status: 'closed',
                    lastMessage: 'Problema resuelto, muchas gracias',
                    timestamp: new Date(Date.now() - 7200000).toISOString(),
                    unreadCount: 0,
                    avatar: null,
                    priority: 'low',
                    channel: 'email'
                }
            ];

            setConversations(mockConversations);
        } catch (error) {
            console.error('Error cargando conversaciones:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const filterOptions = [
        { value: 'all', label: 'Todas', count: 48, icon: '💬', color: '#667eea' },
        { value: 'active', label: 'Activas', count: 12, icon: '🟢', color: '#43e97b' },
        { value: 'waiting', label: 'En Espera', count: 8, icon: '🟡', color: '#feca57' },
        { value: 'closed', label: 'Cerradas', count: 25, icon: '⚫', color: '#95a5a6' }
    ];

    const getStatusColor = (status) => {
        switch(status) {
            case 'active': return '#43e97b';
            case 'waiting': return '#feca57';
            case 'closed': return '#95a5a6';
            default: return '#667eea';
        }
    };

    const getChannelIcon = (channel) => {
        switch(channel) {
            case 'whatsapp': return '💚';
            case 'web': return '🌐';
            case 'phone': return '📞';
            case 'email': return '📧';
            default: return '💬';
        }
    };

    const getPriorityColor = (priority) => {
        switch(priority) {
            case 'high': return '#ff6b6b';
            case 'medium': return '#feca57';
            case 'low': return '#48dbfb';
            default: return '#95a5a6';
        }
    };

    const filteredConversations = conversations.filter(conv => {
        if (filter === 'all') return true;
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
                    <button className="btn-secondary refresh-btn">
                        <span className="btn-icon">🔄</span>
                        Actualizar
                    </button>
                    <button className="btn-primary new-conversation-btn">
                        <span className="btn-icon">➕</span>
                        Nueva Conversación
                    </button>
                </div>
            </div>

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
                                onClick={() => setSelectedConversation(conversation)}
                            >
                                <div className="card-header">
                                    <div className="customer-info">
                                        <div className="avatar-container">
                                            <div
                                                className="conversation-avatar"
                                                style={{
                                                    background: `linear-gradient(135deg, ${getStatusColor(conversation.status)}, ${getPriorityColor(conversation.priority)})`
                                                }}
                                            >
                                                {conversation.customerName.charAt(0)}
                                            </div>
                                            <div
                                                className="status-indicator"
                                                style={{ backgroundColor: getStatusColor(conversation.status) }}
                                            ></div>
                                        </div>
                                        <div className="customer-details">
                                            <h4 className="customer-name">{conversation.customerName}</h4>
                                            <div className="conversation-meta">
                                                <span className="channel">{getChannelIcon(conversation.channel)}</span>
                                                <span
                                                    className="priority-badge"
                                                    style={{ backgroundColor: getPriorityColor(conversation.priority) }}
                                                >
                                                    {conversation.priority}
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="conversation-time">
                                        {new Date(conversation.timestamp).toLocaleTimeString('es-ES', {
                                            hour: '2-digit',
                                            minute: '2-digit'
                                        })}
                                    </div>
                                </div>

                                <div className="card-body">
                                    <p className="last-message">{conversation.lastMessage}</p>
                                </div>

                                <div className="card-footer">
                                    {conversation.unreadCount > 0 && (
                                        <span className="unread-badge">{conversation.unreadCount} no leídos</span>
                                    )}
                                    <div className="action-buttons">
                                        <button className="action-btn">💬</button>
                                        <button className="action-btn">📋</button>
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
                                            background: `linear-gradient(135deg, ${getStatusColor(selectedConversation.status)}, ${getPriorityColor(selectedConversation.priority)})`
                                        }}
                                    >
                                        {selectedConversation.customerName.charAt(0)}
                                    </div>
                                    <div className="customer-details">
                                        <h3>{selectedConversation.customerName}</h3>
                                        <div className="customer-status">
                                            <span
                                                className="status-badge"
                                                style={{ backgroundColor: getStatusColor(selectedConversation.status) }}
                                            >
                                                {selectedConversation.status}
                                            </span>
                                            <span className="channel-info">
                                                {getChannelIcon(selectedConversation.channel)} {selectedConversation.channel}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <div className="chat-actions">
                                    <button className="chat-action-btn">📞</button>
                                    <button className="chat-action-btn">📧</button>
                                    <button className="chat-action-btn">🔔</button>
                                    <button className="chat-action-btn">⋮</button>
                                </div>
                            </div>

                            <div className="chat-messages">
                                <div className="empty-chat-state">
                                    <div className="empty-icon">💬</div>
                                    <h3>Inicia la conversación</h3>
                                    <p>Envía un mensaje para comenzar a chatear con {selectedConversation.customerName}</p>
                                    <button className="start-chat-btn">
                                        ✨ Comenzar Conversación
                                    </button>
                                </div>
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
