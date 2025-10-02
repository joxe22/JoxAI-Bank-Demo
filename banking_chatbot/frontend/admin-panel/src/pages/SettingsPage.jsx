// frontend/admin-panel/src/pages/SettingsPage.jsx - MEJORADO
import React, { useState } from "react";
import "../styles/pages/SettingsPage.css";
import BotConfiguration from "../components/Settings/BotConfiguration.jsx";
import SystemSettings from "../components/Settings/SystemSettings.jsx";
import UserManagement from "../components/Settings/UserManagement.jsx";

const SettingsPage = () => {
    const [activeTab, setActiveTab] = useState('system');

    // Mock data para BotConfiguration
    const botConfig = {
        botName: 'ChatBot Bancario',
        welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
        primaryColor: '#667eea',
        language: 'es',
        timezone: 'America/Santo_Domingo',
        maxConversationDuration: 30,
        autoEscalationEnabled: false,
        autoEscalationTimeout: 5,
        confidenceThreshold: 0.7,
        fallbackMessage: 'Lo siento, no entendí tu consulta. ¿Podrías reformularla?',
        enableTypingIndicator: true,
        enableFileUpload: true,
        maxFileSize: 10,
        allowedFileTypes: 'image/*, .pdf, .doc, .docx',
        operatingHours: {
            enabled: false,
            start: '09:00',
            end: '18:00',
            days: ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        },
        offlineMessage: 'Estamos fuera de horario. Nuestro horario es de lunes a viernes de 9:00 AM a 6:00 PM.',
        enableSentimentAnalysis: true,
        enableSpellCheck: true,
        maxRetries: 3
    };

    const handleSaveBotConfig = async (config) => {
        console.log('Guardando configuración del bot:', config);
        // Aquí iría la llamada a la API para guardar la configuración
        return Promise.resolve();
    };

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    return (
        <div className="settings-page">
            <div className="settings-page-header">
                <h1>Configuración del Sistema</h1>
                <p>Gestiona la configuración del sistema, bot y usuarios</p>
            </div>

            <div className="settings-tabs">
                <button
                    className={`settings-tab ${activeTab === 'system' ? 'active' : ''}`}
                    onClick={() => handleTabClick('system')}
                    aria-label="Configuración del Sistema"
                >
                    <span className="tab-icon">⚙️</span>
                    Configuración del Sistema
                </button>
                <button
                    className={`settings-tab ${activeTab === 'bot' ? 'active' : ''}`}
                    onClick={() => handleTabClick('bot')}
                    aria-label="Configuración del Bot"
                >
                    <span className="tab-icon">🤖</span>
                    Configuración del Bot
                </button>
                <button
                    className={`settings-tab ${activeTab === 'users' ? 'active' : ''}`}
                    onClick={() => handleTabClick('users')}
                    aria-label="Gestión de Usuarios"
                >
                    <span className="tab-icon">👥</span>
                    Gestión de Usuarios
                </button>
            </div>

            <div className="settings-content">
                {activeTab === 'system' && (
                    <SystemSettings />
                )}

                {activeTab === 'bot' && (
                    <BotConfiguration
                        config={botConfig}
                        onSave={handleSaveBotConfig}
                    />
                )}

                {activeTab === 'users' && (
                    <UserManagement />
                )}
            </div>
        </div>
    );
};

export default SettingsPage;
