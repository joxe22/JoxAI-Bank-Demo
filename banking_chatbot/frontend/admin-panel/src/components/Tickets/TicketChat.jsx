// frontend/admin-panel/src/components/Tickets/TicketChat.jsx
import React, { useState, useRef, useEffect } from 'react';
import '../../styles/components/TicketChat.css';

const TicketChat = ({ ticketId, messages: initialMessages, onSendMessage }) => {
    const [messages, setMessages] = useState(initialMessages || []);
    const [newMessage, setNewMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const messagesEndRef = useRef(null);
    const chatContainerRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();

        if (!newMessage.trim()) return;

        const message = {
            id: Date.now(),
            text: newMessage,
            sender: 'agent',
            senderName: 'Tú',
            timestamp: new Date().toISOString(),
            read: false
        };

        setMessages([...messages, message]);
        setNewMessage('');

        try {
            await onSendMessage?.(ticketId, newMessage);
        } catch (error) {
            console.error('Error enviando mensaje:', error);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage(e);
        }
    };

    const formatTime = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString('es-ES', {
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    const formatDate = (timestamp) => {
        const date = new Date(timestamp);
        const today = new Date();
        const yesterday = new Date(today);
        yesterday.setDate(yesterday.getDate() - 1);

        if (date.toDateString() === today.toDateString()) {
            return 'Hoy';
        } else if (date.toDateString() === yesterday.toDateString()) {
            return 'Ayer';
        } else {
            return date.toLocaleDateString('es-ES', {
                day: '2-digit',
                month: 'short'
            });
        }
    };

    const groupMessagesByDate = (messages) => {
        const groups = {};

        messages.forEach(message => {
            const date = formatDate(message.timestamp);
            if (!groups[date]) {
                groups[date] = [];
            }
            groups[date].push(message);
        });

        return groups;
    };

    const messageGroups = groupMessagesByDate(messages);

    return (
        <div className="ticket-chat">
            <div className="chat-header">
                <div className="header-info">
                    <h3>Chat del Ticket #{ticketId}</h3>
                    <span className="chat-status">
            <span className="status-dot online"></span>
            Cliente en línea
          </span>
                </div>
                <div className="header-actions">
                    <button className="icon-button" title="Adjuntar archivo">
                        📎
                    </button>
                    <button className="icon-button" title="Buscar en chat">
                        🔍
                    </button>
                    <button className="icon-button" title="Más opciones">
                        ⋮
                    </button>
                </div>
            </div>

            <div className="chat-messages" ref={chatContainerRef}>
                {Object.entries(messageGroups).map(([date, msgs]) => (
                    <div key={date}>
                        <div className="date-divider">
                            <span>{date}</span>
                        </div>

                        {msgs.map((message) => (
                            <div
                                key={message.id}
                                className={`message ${message.sender === 'agent' ? 'message-sent' : 'message-received'}`}
                            >
                                {message.sender !== 'agent' && (
                                    <div className="message-avatar">
                                        <span>{message.senderName?.charAt(0) || 'C'}</span>
                                    </div>
                                )}

                                <div className="message-content">
                                    {message.sender !== 'agent' && (
                                        <span className="message-sender">{message.senderName}</span>
                                    )}

                                    <div className="message-bubble">
                                        <p className="message-text">{message.text}</p>

                                        {message.attachments && message.attachments.length > 0 && (
                                            <div className="message-attachments">
                                                {message.attachments.map((attachment, idx) => (
                                                    <div key={idx} className="attachment">
                                                        📎 {attachment.name}
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>

                                    <div className="message-footer">
                                        <span className="message-time">{formatTime(message.timestamp)}</span>
                                        {message.sender === 'agent' && (
                                            <span className="message-status">
                        {message.read ? '✓✓' : '✓'}
                      </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                ))}

                {isTyping && (
                    <div className="message message-received">
                        <div className="message-avatar">
                            <span>C</span>
                        </div>
                        <div className="typing-indicator">
                            <span></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <form className="chat-input" onSubmit={handleSendMessage}>
                <button type="button" className="input-button" title="Emoji">
                    😊
                </button>

                <textarea
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Escribe un mensaje..."
                    className="message-textarea"
                    rows="1"
                />

                <button type="button" className="input-button" title="Adjuntar">
                    📎
                </button>

                <button
                    type="submit"
                    className="send-button"
                    disabled={!newMessage.trim()}
                >
                    ➤
                </button>
            </form>

            <div className="chat-info">
        <span className="info-text">
          💡 Presiona Enter para enviar, Shift+Enter para nueva línea
        </span>
            </div>
        </div>
    );
};

export default TicketChat;