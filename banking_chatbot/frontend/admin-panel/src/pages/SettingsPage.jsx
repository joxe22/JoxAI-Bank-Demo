// frontend/admin-panel/src/pages/SettingsPage.jsx
import React, { useState, useEffect } from "react";
import settingsService from "../services/settingsService";
import "../styles/pages/SettingsPage.css";
import BotConfiguration from "../components/Settings/BotConfiguration.jsx";
import SystemSettings from "../components/Settings/SystemSettings.jsx";
import UserManagement from "../components/Settings/UserManagement.jsx";

const SettingsPage = () => {
    const [activeTab, setActiveTab] = useState('system');
    const [botConfig, setBotConfig] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (activeTab === 'bot') {
            loadBotConfiguration();
        }
    }, [activeTab]);

    const loadBotConfiguration = async () => {
        try {
            setLoading(true);
            setError(null);
            const config = await settingsService.getBotConfiguration();
            setBotConfig(config);
        } catch (error) {
            console.error('Error loading bot configuration:', error);
            setError('Error al cargar la configuración del bot');
            setBotConfig({
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
            });
        } finally {
            setLoading(false);
        }
    };

    const handleSaveBotConfig = async (config) => {
        try {
            setError(null);
            await settingsService.setBotConfiguration(config);
            setBotConfig(config);
            return Promise.resolve();
        } catch (error) {
            console.error('Error saving bot configuration:', error);
            setError('Error al guardar la configuración del bot');
            throw error;
        }
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

                {activeTab === 'system' && (
                    <SystemSettings />
                )}

                {activeTab === 'bot' && (
                    loading ? (
                        <div className="loading">Cargando configuración del bot...</div>
                    ) : (
                        <BotConfiguration
                            config={botConfig}
                            onSave={handleSaveBotConfig}
                        />
                    )
                )}

                {activeTab === 'users' && (
                    <UserManagement />
                )}
            </div>
        </div>
    );
};

export default SettingsPage;
