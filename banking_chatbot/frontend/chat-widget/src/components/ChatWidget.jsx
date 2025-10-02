import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import InputArea from './InputArea';
import TypingIndicator from './TypingIndicator';
import EscalationModal from './EscalationModal';
import chatApi from '../services/chatApi';
import websocketService from '../services/websocket';
import { generateId, scrollToBottom, saveToStorage, loadFromStorage } from '../utils/helpers';
import { MESSAGE_STATUS, WEBSOCKET_EVENTS } from '../utils/constants';
import '../styles/widget.css';

const ChatWidget = ({ config = {} }) => {
    const [isOpen, setIsOpen] = useState(config.autoOpen || false);
    const [isMinimized, setIsMinimized] = useState(false);
    const [messages, setMessages] = useState([]);
    const [conversationId, setConversationId] = useState(null);
    const [isConnected, setIsConnected] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const [agentTyping, setAgentTyping] = useState(false);
    const [showEscalationModal, setShowEscalationModal] = useState(false);
    const [isEscalated, setIsEscalated] = useState(false);
    const [agentName, setAgentName] = useState(null);
    const [unreadCount, setUnreadCount] = useState(0);

    const messagesEndRef = useRef(null);
    const chatContainerRef = useRef(null);

    // Inicializar conversación
    useEffect(() => {
        if (isOpen && !conversationId) {
            initializeConversation();
        }
    }, [isOpen]);

    // Conectar WebSocket cuando hay conversationId
    useEffect(() => {
        if (conversationId) {
            connectWebSocket();
        }

        return () => {
            if (websocketService.isConnected()) {
                websocketService.disconnect();
            }
        };
    }, [conversationId]);

    // Auto-scroll al recibir nuevos mensajes
    useEffect(() => {
        if (isOpen && !isMinimized) {
            scrollToBottom(chatContainerRef.current);
        } else if (!isOpen && messages.length > 0) {
            // Incrementar contador de no leídos si el widget está cerrado
            const lastMessage = messages[messages.length - 1];
            if (!lastMessage.isUser) {
                setUnreadCount(prev => prev + 1);
            }
        }
    }, [messages, isOpen, isMinimized]);

    // Cargar historial del localStorage
    useEffect(() => {
        const savedConversationId = loadFromStorage('conversationId');
        const savedMessages = loadFromStorage('messages', []);

        if (savedConversationId && savedMessages.length > 0) {
            setConversationId(savedConversationId);
            setMessages(savedMessages);
        }
    }, []);

    // Guardar en localStorage cuando cambian mensajes
    useEffect(() => {
        if (conversationId) {
            saveToStorage('conversationId', conversationId);
            saveToStorage('messages', messages);
        }
    }, [conversationId, messages]);

    const initializeConversation = async () => {
        try {
            const response = await chatApi.startConversation({
                userId: loadFromStorage('userId') || `user_${Date.now()}`
            });

            setConversationId(response.conversation_id);

            // Mensaje de bienvenida
            if (response.welcome_message || config.welcomeMessage) {
                addBotMessage(response.welcome_message || config.welcomeMessage);
            }
        } catch (error) {
            console.error('Error iniciando conversación:', error);
            addSystemMessage('Error al conectar. Por favor intenta nuevamente.');
        }
    };

    const connectWebSocket = () => {
        websocketService.connect(conversationId);

        websocketService.on(WEBSOCKET_EVENTS.CONNECTED, () => {
            setIsConnected(true);
            console.log('WebSocket conectado');
        });

        websocketService.on(WEBSOCKET_EVENTS.DISCONNECTED, () => {
            setIsConnected(false);
            console.log('WebSocket desconectado');
        });

        websocketService.on(WEBSOCKET_EVENTS.MESSAGE, (data) => {
            if (data.message) {
                addBotMessage(data.message, data.metadata);
            }
        });

        websocketService.on(WEBSOCKET_EVENTS.TYPING, (data) => {
            setAgentTyping(data.is_typing);
            if (data.agent_name) {
                setAgentName(data.agent_name);
            }
        });

        websocketService.on(WEBSOCKET_EVENTS.AGENT_JOINED, (data) => {
            setIsEscalated(true);
            setAgentName(data.agent_name);
            addSystemMessage(`${data.agent_name} se ha unido a la conversación`);
        });

        websocketService.on(WEBSOCKET_EVENTS.AGENT_LEFT, (data) => {
            addSystemMessage(`${data.agent_name} ha dejado la conversación`);
            setAgentName(null);
        });

        websocketService.on(WEBSOCKET_EVENTS.CONVERSATION_ESCALATED, (data) => {
            setIsEscalated(true);
            addSystemMessage('Conversación escalada. Un agente se unirá pronto...');
        });

        websocketService.on(WEBSOCKET_EVENTS.ERROR, (error) => {
            console.error('WebSocket error:', error);
        });
    };

    const handleSendMessage = async (messageText) => {
        if (!messageText.trim() || !conversationId) return;

        const tempId = generateId();
        const userMessage = {
            id: tempId,
            text: messageText,
            isUser: true,
            timestamp: new Date().toISOString(),
            status: MESSAGE_STATUS.SENDING
        };

        // Agregar mensaje del usuario inmediatamente
        setMessages(prev => [...prev, userMessage]);

        try {
            // Enviar mensaje a la API
            const response = await chatApi.sendMessage(conversationId, messageText);

            // Actualizar estado del mensaje
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === tempId
                        ? { ...msg, status: MESSAGE_STATUS.SENT, id: response.message_id || tempId }
                        : msg
                )
            );

            // Agregar respuesta del bot si viene en la respuesta
            if (response.response) {
                addBotMessage(response.response, response.metadata);
            }
        } catch (error) {
            console.error('Error enviando mensaje:', error);

            // Marcar mensaje como error
            setMessages(prev =>
                prev.map(msg =>
                    msg.id === tempId ? { ...msg, status: MESSAGE_STATUS.ERROR } : msg
                )
            );

            addSystemMessage('Error al enviar el mensaje. Por favor intenta nuevamente.');
        }
    };

    const addBotMessage = (text, metadata = {}) => {
        const botMessage = {
            id: generateId(),
            text,
            isUser: false,
            timestamp: new Date().toISOString(),
            metadata
        };
        setMessages(prev => [...prev, botMessage]);
    };

    const addSystemMessage = (text) => {
        const systemMessage = {
            id: generateId(),
            text,
            isUser: false,
            isSystem: true,
            timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, systemMessage]);
    };

    const handleTyping = (typing) => {
        setIsTyping(typing);
        if (websocketService.isConnected()) {
            websocketService.sendTyping(typing);
        }
    };

    const handleEscalate = async (escalationData) => {
        try {
            await chatApi.escalateToAgent(conversationId, escalationData);
            setShowEscalationModal(false);
            setIsEscalated(true);
            addSystemMessage('Tu conversación ha sido escalada. Un agente te atenderá pronto.');
        } catch (error) {
            console.error('Error escalando:', error);
            throw error;
        }
    };

    const toggleWidget = () => {
        setIsOpen(!isOpen);
        if (!isOpen) {
            setUnreadCount(0);
        }
    };

    const toggleMinimize = () => {
        setIsMinimized(!isMinimized);
    };

    const handleClose = async () => {
        if (conversationId) {
            try {
                await chatApi.endConversation(conversationId);
            } catch (error) {
                console.error('Error cerrando conversación:', error);
            }
        }

        // Limpiar estado
        setMessages([]);
        setConversationId(null);
        setIsEscalated(false);
        setAgentName(null);
        setIsOpen(false);

        // Limpiar localStorage
        saveToStorage('conversationId', null);
        saveToStorage('messages', []);
    };

    return (
        <>
            {/* Widget Toggle Button */}
            {!isOpen && (
                <button
                    className="chat-widget-toggle"
                    onClick={toggleWidget}
                    aria-label="Abrir chat"
                >
                    💬
                    {unreadCount > 0 && (
                        <span className="unread-badge">{unreadCount}</span>
                    )}
                </button>
            )}

            {/* Chat Widget Window */}
            {isOpen && (
                <div className={`chat-widget-window ${isMinimized ? 'minimized' : ''}`}>
                    {/* Header */}
                    <div className="chat-widget-header">
                        <div className="header-info">
                            <div className="header-avatar">🏦</div>
                            <div className="header-text">
                                <h3>{config.headerText || 'Chat Bancario'}</h3>
                                <span className="status-indicator">
                  {isConnected ? (
                      <>
                          <span className="status-dot online"></span>
                          {agentName ? `${agentName} - En línea` : 'En línea'}
                      </>
                  ) : (
                      <>
                          <span className="status-dot offline"></span>
                          Desconectado
                      </>
                  )}
                </span>
                            </div>
                        </div>

                        <div className="header-actions">
                            {config.enableEscalation && !isEscalated && (
                                <button
                                    className="header-button"
                                    onClick={() => setShowEscalationModal(true)}
                                    title="Escalar a agente humano"
                                >
                                    👤
                                </button>
                            )}

                            <button
                                className="header-button"
                                onClick={toggleMinimize}
                                title={isMinimized ? 'Maximizar' : 'Minimizar'}
                            >
                                {isMinimized ? '🔼' : '🔽'}
                            </button>

                            <button
                                className="header-button"
                                onClick={handleClose}
                                title="Cerrar chat"
                            >
                                ✕
                            </button>
                        </div>
                    </div>

                    {/* Messages Area */}
                    {!isMinimized && (
                        <>
                            <div className="chat-widget-messages" ref={chatContainerRef}>
                                {messages.length === 0 ? (
                                    <div className="empty-state">
                                        <div className="empty-icon">💬</div>
                                        <p>¡Hola! ¿En qué puedo ayudarte hoy?</p>
                                    </div>
                                ) : (
                                    messages.map((message) => (
                                        <MessageBubble
                                            key={message.id}
                                            message={message.text}
                                            isUser={message.isUser}
                                            timestamp={message.timestamp}
                                            status={message.status}
                                            attachments={message.attachments}
                                        />
                                    ))
                                )}

                                {agentTyping && (
                                    <TypingIndicator
                                        show={agentTyping}
                                        agentName={agentName}
                                    />
                                )}

                                <div ref={messagesEndRef} />
                            </div>

                            {/* Input Area */}
                            <InputArea
                                onSendMessage={handleSendMessage}
                                onTyping={handleTyping}
                                disabled={!isConnected}
                                placeholder={config.placeholderText || 'Escribe tu mensaje...'}
                            />

                            {/* Powered By (opcional) */}
                            {config.showBranding && (
                                <div className="chat-widget-footer">
                                    <span>Powered by ChatBot AI</span>
                                </div>
                            )}
                        </>
                    )}
                </div>
            )}

            {/* Escalation Modal */}
            <EscalationModal
                isOpen={showEscalationModal}
                onClose={() => setShowEscalationModal(false)}
                onEscalate={handleEscalate}
                conversationId={conversationId}
            />
        </>
    );
};

export default ChatWidget;