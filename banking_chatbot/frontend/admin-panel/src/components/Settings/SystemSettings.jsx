// frontend/admin-panel/src/components/Settings/SystemSettings.jsx
import React, { useState } from 'react';
import "../../styles/components/SystemSettings.css"

const SystemSettings = () => {
    const [settings, setSettings] = useState({
        // General
        systemName: 'ChatBot Bancario',
        systemEmail: 'support@banco.com',
        adminEmail: 'admin@banco.com',

        // Seguridad
        sessionTimeout: 30,
        maxLoginAttempts: 3,
        passwordMinLength: 8,
        requireStrongPassword: true,
        enableTwoFactor: false,
        enableIPWhitelist: false,
        ipWhitelist: '',

        // Notificaciones
        emailNotifications: true,
        slackNotifications: false,
        slackWebhook: '',
        notifyOnNewTicket: true,
        notifyOnEscalation: true,
        notifyOnHighPriority: true,

        // Base de Datos
        enableBackups: true,
        backupFrequency: 'daily',
        backupRetention: 30,

        // Logs
        enableAuditLog: true,
        logRetention: 90,
        logLevel: 'info',

        // Integrations
        enableWebhooks: false,
        webhookUrl: '',
        webhookEvents: [],

        // Performance
        cacheEnabled: true,
        cacheDuration: 3600,
        maxConcurrentConnections: 1000,
        rateLimitPerMinute: 60
    });

    const [activeSection, setActiveSection] = useState('general');

    const handleChange = (field, value) => {
        setSettings(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleSave = async () => {
        try {
            // Aquí iría la llamada a la API
            console.log('Guardando configuración:', settings);
            alert('Configuración guardada exitosamente');
        } catch (error) {
            console.error('Error guardando configuración:', error);
            alert('Error al guardar la configuración');
        }
    };

    const handleTestWebhook = () => {
        if (!settings.webhookUrl) {
            alert('Por favor ingresa una URL de webhook');
            return;
        }
        alert('Enviando webhook de prueba...');
        // Aquí iría la lógica de prueba
    };

    const handleExportSettings = () => {
        const dataStr = JSON.stringify(settings, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'system-settings.json';
        link.click();
    };

    return (
        <div className="system-settings">
            <div className="settings-header">
                <div className="header-left">
                    <h2>Configuración del Sistema</h2>
                    <p className="subtitle">Configuración avanzada y parámetros del sistema</p>
                </div>
                <div className="header-actions">
                    <button className="btn-secondary" onClick={handleExportSettings}>
                        📥 Exportar
                    </button>
                    <button className="btn-primary" onClick={handleSave}>
                        💾 Guardar Cambios
                    </button>
                </div>
            </div>

            <div className="settings-layout">
                {/* Sidebar Menu */}
                <div className="settings-sidebar">
                    <nav className="settings-nav">
                        <button
                            className={activeSection === 'general' ? 'active' : ''}
                            onClick={() => setActiveSection('general')}
                        >
                            🏢 General
                        </button>
                        <button
                            className={activeSection === 'security' ? 'active' : ''}
                            onClick={() => setActiveSection('security')}
                        >
                            🔒 Seguridad
                        </button>
                        <button
                            className={activeSection === 'notifications' ? 'active' : ''}
                            onClick={() => setActiveSection('notifications')}
                        >
                            🔔 Notificaciones
                        </button>
                        <button
                            className={activeSection === 'database' ? 'active' : ''}
                            onClick={() => setActiveSection('database')}
                        >
                            💾 Base de Datos
                        </button>
                        <button
                            className={activeSection === 'logs' ? 'active' : ''}
                            onClick={() => setActiveSection('logs')}
                        >
                            📋 Logs y Auditoría
                        </button>
                        <button
                            className={activeSection === 'integrations' ? 'active' : ''}
                            onClick={() => setActiveSection('integrations')}
                        >
                            🔗 Integraciones
                        </button>
                        <button
                            className={activeSection === 'performance' ? 'active' : ''}
                            onClick={() => setActiveSection('performance')}
                        >
                            ⚡ Performance
                        </button>
                    </nav>
                </div>

                {/* Settings Content */}
                <div className="settings-content">

                    {/* GENERAL */}
                    {activeSection === 'general' && (
                        <div className="settings-section">
                            <h3>Configuración General</h3>

                            <div className="form-group">
                                <label>Nombre del Sistema</label>
                                <input
                                    type="text"
                                    value={settings.systemName}
                                    onChange={(e) => handleChange('systemName', e.target.value)}
                                />
                            </div>

                            <div className="form-group">
                                <label>Email del Sistema</label>
                                <input
                                    type="email"
                                    value={settings.systemEmail}
                                    onChange={(e) => handleChange('systemEmail', e.target.value)}
                                />
                                <small>Email usado para enviar notificaciones automáticas</small>
                            </div>

                            <div className="form-group">
                                <label>Email del Administrador</label>
                                <input
                                    type="email"
                                    value={settings.adminEmail}
                                    onChange={(e) => handleChange('adminEmail', e.target.value)}
                                />
                                <small>Email para notificaciones críticas del sistema</small>
                            </div>
                        </div>
                    )}

                    {/* SECURITY */}
                    {activeSection === 'security' && (
                        <div className="settings-section">
                            <h3>Seguridad</h3>

                            <div className="form-group">
                                <label>Tiempo de Sesión (minutos)</label>
                                <input
                                    type="number"
                                    value={settings.sessionTimeout}
                                    onChange={(e) => handleChange('sessionTimeout', parseInt(e.target.value))}
                                    min="5"
                                    max="1440"
                                />
                                <small>Tiempo de inactividad antes de cerrar sesión automáticamente</small>
                            </div>

                            <div className="form-group">
                                <label>Intentos Máximos de Login</label>
                                <input
                                    type="number"
                                    value={settings.maxLoginAttempts}
                                    onChange={(e) => handleChange('maxLoginAttempts', parseInt(e.target.value))}
                                    min="1"
                                    max="10"
                                />
                            </div>

                            <div className="form-group">
                                <label>Longitud Mínima de Contraseña</label>
                                <input
                                    type="number"
                                    value={settings.passwordMinLength}
                                    onChange={(e) => handleChange('passwordMinLength', parseInt(e.target.value))}
                                    min="6"
                                    max="20"
                                />
                            </div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.requireStrongPassword}
                                        onChange={(e) => handleChange('requireStrongPassword', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Requerir Contraseña Fuerte
                                </label>
                                <small>Debe incluir mayúsculas, minúsculas, números y caracteres especiales</small>
                            </div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.enableTwoFactor}
                                        onChange={(e) => handleChange('enableTwoFactor', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Autenticación de Dos Factores
                                </label>
                            </div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.enableIPWhitelist}
                                        onChange={(e) => handleChange('enableIPWhitelist', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Habilitar Lista Blanca de IPs
                                </label>
                            </div>

                            {settings.enableIPWhitelist && (
                                <div className="form-group indent">
                                    <label>IPs Permitidas (una por línea)</label>
                                    <textarea
                                        value={settings.ipWhitelist}
                                        onChange={(e) => handleChange('ipWhitelist', e.target.value)}
                                        rows="5"
                                        placeholder="192.168.1.1&#10;10.0.0.0/8"
                                    />
                                </div>
                            )}
                        </div>
                    )}

                    {/* NOTIFICATIONS */}
                    {activeSection === 'notifications' && (
                        <div className="settings-section">
                            <h3>Notificaciones</h3>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.emailNotifications}
                                        onChange={(e) => handleChange('emailNotifications', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Notificaciones por Email
                                </label>
                            </div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.notifyOnNewTicket}
                                        onChange={(e) => handleChange('notifyOnNewTicket', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Notificar en Nuevos Tickets
                                </label>
                            </div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.notifyOnEscalation}
                                        onChange={(e) => handleChange('notifyOnEscalation', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Notificar en Escalaciones
                                </label>
                            </div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.notifyOnHighPriority}
                                        onChange={(e) => handleChange('notifyOnHighPriority', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Notificar en Tickets de Alta Prioridad
                                </label>
                            </div>

                            <div className="divider"></div>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.slackNotifications}
                                        onChange={(e) => handleChange('slackNotifications', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Notificaciones a Slack
                                </label>
                            </div>

                            {settings.slackNotifications && (
                                <div className="form-group indent">
                                    <label>Slack Webhook URL</label>
                                    <input
                                        type="url"
                                        value={settings.slackWebhook}
                                        onChange={(e) => handleChange('slackWebhook', e.target.value)}
                                        placeholder="https://hooks.slack.com/services/..."
                                    />
                                </div>
                            )}
                        </div>
                    )}

                    {/* DATABASE */}
                    {activeSection === 'database' && (
                        <div className="settings-section">
                            <h3>Base de Datos y Respaldos</h3>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.enableBackups}
                                        onChange={(e) => handleChange('enableBackups', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Habilitar Respaldos Automáticos
                                </label>
                            </div>

                            {settings.enableBackups && (
                                <>
                                    <div className="form-group indent">
                                        <label>Frecuencia de Respaldo</label>
                                        <select
                                            value={settings.backupFrequency}
                                            onChange={(e) => handleChange('backupFrequency', e.target.value)}
                                        >
                                            <option value="hourly">Cada hora</option>
                                            <option value="daily">Diario</option>
                                            <option value="weekly">Semanal</option>
                                            <option value="monthly">Mensual</option>
                                        </select>
                                    </div>

                                    <div className="form-group indent">
                                        <label>Retención de Respaldos (días)</label>
                                        <input
                                            type="number"
                                            value={settings.backupRetention}
                                            onChange={(e) => handleChange('backupRetention', parseInt(e.target.value))}
                                            min="1"
                                            max="365"
                                        />
                                    </div>
                                </>
                            )}

                            <div className="action-buttons">
                                <button className="btn-secondary">
                                    🗄️ Crear Respaldo Manual
                                </button>
                                <button className="btn-secondary">
                                    📥 Restaurar desde Respaldo
                                </button>
                            </div>
                        </div>
                    )}

                    {/* LOGS */}
                    {activeSection === 'logs' && (
                        <div className="settings-section">
                            <h3>Logs y Auditoría</h3>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.enableAuditLog}
                                        onChange={(e) => handleChange('enableAuditLog', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Habilitar Log de Auditoría
                                </label>
                                <small>Registra todas las acciones de los usuarios</small>
                            </div>

                            <div className="form-group">
                                <label>Nivel de Log</label>
                                <select
                                    value={settings.logLevel}
                                    onChange={(e) => handleChange('logLevel', e.target.value)}
                                >
                                    <option value="error">Solo Errores</option>
                                    <option value="warn">Warnings y Errores</option>
                                    <option value="info">Info, Warnings y Errores</option>
                                    <option value="debug">Debug (Todo)</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Retención de Logs (días)</label>
                                <input
                                    type="number"
                                    value={settings.logRetention}
                                    onChange={(e) => handleChange('logRetention', parseInt(e.target.value))}
                                    min="7"
                                    max="365"
                                />
                            </div>

                            <div className="action-buttons">
                                <button className="btn-secondary">
                                    📋 Ver Logs
                                </button>
                                <button className="btn-secondary">
                                    📥 Descargar Logs
                                </button>
                                <button className="btn-danger">
                                    🗑️ Limpiar Logs Antiguos
                                </button>
                            </div>
                        </div>
                    )}

                    {/* INTEGRATIONS */}
                    {activeSection === 'integrations' && (
                        <div className="settings-section">
                            <h3>Integraciones</h3>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.enableWebhooks}
                                        onChange={(e) => handleChange('enableWebhooks', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Habilitar Webhooks
                                </label>
                            </div>

                            {settings.enableWebhooks && (
                                <>
                                    <div className="form-group indent">
                                        <label>Webhook URL</label>
                                        <input
                                            type="url"
                                            value={settings.webhookUrl}
                                            onChange={(e) => handleChange('webhookUrl', e.target.value)}
                                            placeholder="https://api.example.com/webhook"
                                        />
                                    </div>

                                    <div className="form-group indent">
                                        <label>Eventos a Enviar</label>
                                        <div className="checkbox-group">
                                            {[
                                                { value: 'ticket.created', label: 'Ticket Creado' },
                                                { value: 'ticket.updated', label: 'Ticket Actualizado' },
                                                { value: 'ticket.closed', label: 'Ticket Cerrado' },
                                                { value: 'conversation.started', label: 'Conversación Iniciada' },
                                                { value: 'conversation.ended', label: 'Conversación Finalizada' }
                                            ].map(event => (
                                                <label key={event.value} className="checkbox-label">
                                                    <input
                                                        type="checkbox"
                                                        checked={settings.webhookEvents?.includes(event.value)}
                                                        onChange={(e) => {
                                                            const events = e.target.checked
                                                                ? [...(settings.webhookEvents || []), event.value]
                                                                : settings.webhookEvents.filter(ev => ev !== event.value);
                                                            handleChange('webhookEvents', events);
                                                        }}
                                                    />
                                                    {event.label}
                                                </label>
                                            ))}
                                        </div>
                                    </div>

                                    <button className="btn-secondary" onClick={handleTestWebhook}>
                                        🧪 Probar Webhook
                                    </button>
                                </>
                            )}
                        </div>
                    )}

                    {/* PERFORMANCE */}
                    {activeSection === 'performance' && (
                        <div className="settings-section">
                            <h3>Performance y Optimización</h3>

                            <div className="toggle-group">
                                <label className="toggle-label">
                                    <input
                                        type="checkbox"
                                        checked={settings.cacheEnabled}
                                        onChange={(e) => handleChange('cacheEnabled', e.target.checked)}
                                    />
                                    <span className="toggle-switch"></span>
                                    Habilitar Caché
                                </label>
                            </div>

                            {settings.cacheEnabled && (
                                <div className="form-group indent">
                                    <label>Duración del Caché (segundos)</label>
                                    <input
                                        type="number"
                                        value={settings.cacheDuration}
                                        onChange={(e) => handleChange('cacheDuration', parseInt(e.target.value))}
                                        min="60"
                                        max="86400"
                                    />
                                </div>
                            )}

                            <div className="form-group">
                                <label>Conexiones Concurrentes Máximas</label>
                                <input
                                    type="number"
                                    value={settings.maxConcurrentConnections}
                                    onChange={(e) => handleChange('maxConcurrentConnections', parseInt(e.target.value))}
                                    min="100"
                                    max="10000"
                                />
                            </div>

                            <div className="form-group">
                                <label>Rate Limit (requests por minuto)</label>
                                <input
                                    type="number"
                                    value={settings.rateLimitPerMinute}
                                    onChange={(e) => handleChange('rateLimitPerMinute', parseInt(e.target.value))}
                                    min="10"
                                    max="1000"
                                />
                            </div>

                            <div className="action-buttons">
                                <button className="btn-secondary">
                                    🗑️ Limpiar Caché
                                </button>
                                <button className="btn-secondary">
                                    🔄 Reiniciar Sistema
                                </button>
                            </div>
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
};

export default SystemSettings;