import React from 'react';
import '../styles/MessageBubble.css';

const MessageBubble = ({ message, isUser, timestamp, status, attachments }) => {
    const formatTime = (date) => {
        const d = new Date(date);
        return d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    };

    const renderAttachment = (attachment) => {
        if (attachment.type === 'image') {
            return (
                <img
                    src={attachment.url}
                    alt={attachment.name}
                    className="message-attachment-image"
                />
            );
        }
        return (
            <a
                href={attachment.url}
                target="_blank"
                rel="noopener noreferrer"
                className="message-attachment-file"
            >
                📎 {attachment.name}
            </a>
        );
    };

    return (
        <div className={`message-bubble ${isUser ? 'user' : 'bot'}`}>
            <div className="message-content">
                {!isUser && (
                    <div className="bot-avatar">
                        <span>🏦</span>
                    </div>
                )}

                <div className="message-body">
                    <div className="message-text">
                        {message}
                    </div>

                    {attachments && attachments.length > 0 && (
                        <div className="message-attachments">
                            {attachments.map((attachment, idx) => (
                                <div key={idx}>
                                    {renderAttachment(attachment)}
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="message-footer">
                        <span className="message-time">{formatTime(timestamp)}</span>
                        {isUser && status && (
                            <span className={`message-status status-${status}`}>
                {status === 'sent' && '✓'}
                                {status === 'delivered' && '✓✓'}
                                {status === 'read' && '✓✓'}
                                {status === 'error' && '⚠'}
              </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MessageBubble;