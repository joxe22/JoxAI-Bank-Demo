import React from 'react';
import '../styles/TypingIndicator.css';

const TypingIndicator = ({ agentName, show }) => {
    if (!show) return null;

    return (
        <div className="typing-indicator-container">
            <div className="bot-avatar">
                <span>🏦</span>
            </div>

            <div className="typing-indicator">
                <div className="typing-dots">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                </div>
                {agentName && (
                    <span className="typing-text">{agentName} está escribiendo...</span>
                )}
            </div>
        </div>
    );
};

export default TypingIndicator;