import React, { useState, useRef } from 'react';
import '../styles/InputArea.css';

const InputArea = ({ onSendMessage, onTyping, disabled, placeholder }) => {
    const [message, setMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const fileInputRef = useRef(null);
    const typingTimeoutRef = useRef(null);

    const handleInputChange = (e) => {
        const value = e.target.value;
        setMessage(value);

        // Notificar que está escribiendo
        if (!isTyping && value.length > 0) {
            setIsTyping(true);
            onTyping?.(true);
        }

        // Clear timeout anterior
        if (typingTimeoutRef.current) {
            clearTimeout(typingTimeoutRef.current);
        }

        // Si deja de escribir por 2 segundos
        typingTimeoutRef.current = setTimeout(() => {
            setIsTyping(false);
            onTyping?.(false);
        }, 2000);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        if (message.trim() && !disabled) {
            onSendMessage(message.trim());
            setMessage('');
            setIsTyping(false);
            onTyping?.(false);

            if (typingTimeoutRef.current) {
                clearTimeout(typingTimeoutRef.current);
            }
        }
    };

    const handleKeyPress = (e) => {
        // Enviar con Enter, nueva línea con Shift+Enter
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    const handleFileSelect = (e) => {
        const file = e.target.files[0];
        if (file) {
            // Aquí se puede implementar la lógica de subida de archivos
            console.log('Archivo seleccionado:', file.name);
            // onSendFile(file);
        }
    };

    const triggerFileInput = () => {
        fileInputRef.current?.click();
    };

    return (
        <form className="input-area" onSubmit={handleSubmit}>
            <div className="input-container">
                <button
                    type="button"
                    className="attachment-button"
                    onClick={triggerFileInput}
                    disabled={disabled}
                    title="Adjuntar archivo"
                >
                    📎
                </button>

                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    style={{ display: 'none' }}
                    accept="image/*,.pdf,.doc,.docx"
                />

                <textarea
                    value={message}
                    onChange={handleInputChange}
                    onKeyPress={handleKeyPress}
                    placeholder={placeholder || "Escribe tu mensaje..."}
                    disabled={disabled}
                    className="message-input"
                    rows="1"
                    maxLength="1000"
                />

                <button
                    type="submit"
                    className="send-button"
                    disabled={disabled || !message.trim()}
                    title="Enviar mensaje"
                >
                    ➤
                </button>
            </div>

            {message.length > 900 && (
                <div className="character-count">
                    {message.length}/1000
                </div>
            )}
        </form>
    );
};

export default InputArea;