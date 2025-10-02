// frontend/admin-panel/src/components/Settings/BotConfiguration.jsx
import React, { useState } from 'react';
import "../../styles/components/BotConfiguration.css"

const BotConfiguration = ({ config, onSave }) => {
    const [formData, setFormData] = useState({
        botName: config?.botName || 'ChatBot Bancario',
        welcomeMessage: config?.welcomeMessage || '¡Hola! ¿En qué puedo ayudarte hoy?',
        primaryColor: config?.primaryColor || '#667eea',
        language: config?.language || 'es',
        timezone: config?.timezone || 'America/Santo_Domingo',
        maxConversationDuration: config?.maxConversationDuration || 30,
        autoEscalationEnabled: config?.autoEscalationEnabled || false,
        autoEscalationTimeout: config?.autoEscalationTimeout || 5,
        confidenceThreshold: config?.confidenceThreshold || 0.7,
        fallbackMessage: config?.fallbackMessage || 'Lo siento, no entendí tu consulta. ¿Podrías reformularla?',
        enableTypingIndicator: config?.enableTypingIndicator ?? true,
        enableFileUpload: config?.enableFileUpload ?? true,
        maxFileSize: config?.maxFileSize || 10,
        allowedFileTypes: config?.allowedFileTypes || 'image/*, .pdf, .doc, .docx',
        operatingHours: {
            enabled: config?.operatingHours?.enabled ?? false,
            start: config?.operatingHours?.start || '09:00',
            end: config?.operatingHours?.end || '18:00',
            days: config?.operatingHours?.days || ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
        },
        offlineMessage: config?.offlineMessage || 'Estamos fuera de horario. Nuestro horario es de lunes a viernes de 9:00 AM a 6:00 PM.',
        enableSentimentAnalysis: config?.enableSentimentAnalysis ?? true,
        enableSpellCheck: config?.enableSpellCheck ?? true,
        maxRetries: config?.maxRetries || 3
    });

    const [isSaving, setIsSaving] = useState(false);
    const [activeTab, setActiveTab] = useState('general');

    const handleChange = (field, value) => {
        setFormData(prev => ({
            ...prev,
            [field]: value
        }));
    };

    const handleNestedChange = (parent, field, value) => {
        setFormData(prev => ({
            ...prev,
            [parent]: {
                ...prev[parent],
                [field]: value
            }
        }));
    };

    const handleArrayChange = (parent, field, value) => {
        setFormData(prev => ({
            ...prev,
            [parent]: {
                ...prev[parent],
                [field]: value
            }
        }));
    };

    const handleSave = async () => {
        setIsSaving(true);
        try {
            await onSave(formData);
            alert('Configuración guardada exitosamente');
        } catch (error) {
            console.error('Error guardando configuración:', error);
            alert('Error al guardar la configuración');
        } finally {
            setIsSaving(false);
        }
    };

    const daysOfWeek = [
        { value: 'monday', label: 'Lunes' },
        { value: 'tuesday', label: 'Martes' },
        { value: 'wednesday', label: 'Miércoles' },
        { value: 'thursday', label: 'Jueves' },
        { value: 'friday', label: 'Viernes' },
        { value: 'saturday', label: 'Sábado' },
        { value: 'sunday', label: 'Domingo' }
    ];

    return (
        <div className="bot-configuration">
            <div className="config-header">
                <h2>Configuración del Bot</h2>
                <button
                    className="btn-save"
                    onClick={handleSave}
                    disabled={isSaving}
                >
                    {isSaving ? 'Guardando...' : 'Guardar Cambios'}
                </button>
            </div>

            <div className="config-tabs">
                <button
                    className={`tab ${activeTab === 'general' ? 'active' : ''}`}
                    onClick={() => setActiveTab('general')}
                >
                    General
                </button>
                <button
                    className={`tab ${activeTab === 'behavior' ? 'active' : ''}`}
                    onClick={() => setActiveTab('behavior')}
                >
                    Comportamiento
                </button>
                <button
                    className={`tab ${activeTab === 'hours' ? 'active' : ''}`}
                    onClick={() => setActiveTab('hours')}
                >
                    Horarios
                </button>
                <button
                    className={`tab ${activeTab === 'advanced' ? 'active' : ''}`}
                    onClick={() => setActiveTab('advanced')}
                >
                    Avanzado
                </button>
            </div>

            <div className="config-content">
                {/* TAB: General */}
                {activeTab === 'general' && (
                    <div className="config-section">
                        <h3>Configuración General</h3>

                        <div className="form-group">
                            <label>Nombre del Bot</label>
                            <input
                                type="text"
                                value={formData.botName}
                                onChange={(e) => handleChange('botName', e.target.value)}
                                placeholder="ChatBot Bancario"
                            />
                        </div>

                        <div className="form-group">
                            <label>Mensaje de Bienvenida</label>
                            <textarea
                                value={formData.welcomeMessage}
                                onChange={(e) => handleChange('welcomeMessage', e.target.value)}
                                rows="3"
                                placeholder="¡Hola! ¿En qué puedo ayudarte hoy?"
                            />
                        </div>

                        <div className="form-row">
                            <div className="form-group">
                                <label>Color Principal</label>
                                <div className="color-input-group">
                                    <input
                                        type="color"
                                        value={formData.primaryColor}
                                        onChange={(e) => handleChange('primaryColor', e.target.value)}
                                    />
                                    <input
                                        type="text"
                                        value={formData.primaryColor}
                                        onChange={(e) => handleChange('primaryColor', e.target.value)}
                                        placeholder="#667eea"
                                    />
                                </div>
                            </div>

                            <div className="form-group">
                                <label>Idioma</label>
                                <select
                                    value={formData.language}
                                    onChange={(e) => handleChange('language', e.target.value)}
                                >
                                    <option value="es">Español</option>
                                    <option value="en">English</option>
                                    <option value="pt">Português</option>
                                </select>
                            </div>
                        </div>

                        <div className="form-group">
                            <label>Zona Horaria</label>
                            <select
                                value={formData.timezone}
                                onChange={(e) => handleChange('timezone', e.target.value)}
                            >
                                <option value="America/Santo_Domingo">Santo Domingo (GMT-4)</option>
                                <option value="America/New_York">New York (GMT-5)</option>
                                <option value="America/Los_Angeles">Los Angeles (GMT-8)</option>
                                <option value="Europe/Madrid">Madrid (GMT+1)</option>
                            </select>
                        </div>
                    </div>
                )}

                {/* TAB: Comportamiento */}
                {activeTab === 'behavior' && (
                    <div className="config-section">
                        <h3>Configuración de Comportamiento</h3>

                        <div className="form-group">
                            <label>Mensaje de Fallback</label>
                            <textarea
                                value={formData.fallbackMessage}
                                onChange={(e) => handleChange('fallbackMessage', e.target.value)}
                                rows="3"
                                placeholder="Mensaje cuando el bot no entiende"
                            />
                            <small>Mensaje mostrado cuando el bot no puede responder con confianza</small>
                        </div>

                        <div className="form-group">
                            <label>Umbral de Confianza</label>
                            <input
                                type="range"
                                min="0"
                                max="1"
                                step="0.05"
                                value={formData.confidenceThreshold}
                                onChange={(e) => handleChange('confidenceThreshold', parseFloat(e.target.value))}
                            />
                            <span className="range-value">{(formData.confidenceThreshold * 100).toFixed(0)}%</span>
                            <small>Nivel mínimo de confianza para responder automáticamente</small>
                        </div>

                        <div className="form-group">
                            <label>Duración Máxima de Conversación (minutos)</label>
                            <input
                                type="number"
                                value={formData.maxConversationDuration}
                                onChange={(e) => handleChange('maxConversationDuration', parseInt(e.target.value))}
                                min="5"
                                max="120"
                            />
                            <small>Tiempo máximo antes de cerrar una conversación inactiva</small>
                        </div>

                        <div className="form-group">
                            <label>Intentos Máximos de Reintento</label>
                            <input
                                type="number"
                                value={formData.maxRetries}
                                onChange={(e) => handleChange('maxRetries', parseInt(e.target.value))}
                                min="1"
                                max="10"
                            />
                            <small>Número de veces que el bot intenta entender antes de escalar</small>
                        </div>

                        <div className="toggle-group">
                            <label className="toggle-label">
                                <input
                                    type="checkbox"
                                    checked={formData.autoEscalationEnabled}
                                    onChange={(e) => handleChange('autoEscalationEnabled', e.target.checked)}
                                />
                                <span className="toggle-switch"></span>
                                Escalación Automática
                            </label>
                            <small>Escalar automáticamente a agente humano después de cierto tiempo</small>
                        </div>

                        {formData.autoEscalationEnabled && (
                            <div className="form-group indent">
                                <label>Tiempo para Escalación Automática (minutos)</label>
                                <input
                                    type="number"
                                    value={formData.autoEscalationTimeout}
                                    onChange={(e) => handleChange('autoEscalationTimeout', parseInt(e.target.value))}
                                    min="1"
                                    max="30"
                                />
                            </div>
                        )}

                        <div className="toggle-group">
                            <label className="toggle-label">
                                <input
                                    type="checkbox"
                                    checked={formData.enableTypingIndicator}
                                    onChange={(e) => handleChange('enableTypingIndicator', e.target.checked)}
                                />
                                <span className="toggle-switch"></span>
                                Indicador de Escritura
                            </label>
                        </div>

                        <div className="toggle-group">
                            <label className="toggle-label">
                                <input
                                    type="checkbox"
                                    checked={formData.enableSentimentAnalysis}
                                    onChange={(e) => handleChange('enableSentimentAnalysis', e.target.checked)}
                                />
                                <span className="toggle-switch"></span>
                                Análisis de Sentimiento
                            </label>
                        </div>

                        <div className="toggle-group">
                            <label className="toggle-label">
                                <input
                                    type="checkbox"
                                    checked={formData.enableSpellCheck}
                                    onChange={(e) => handleChange('enableSpellCheck', e.target.checked)}
                                />
                                <span className="toggle-switch"></span>
                                Corrección Ortográfica
                            </label>
                        </div>
                    </div>
                )}

                {/* TAB: Horarios */}
                {activeTab === 'hours' && (
                    <div className="config-section">
                        <h3>Horario de Operación</h3>

                        <div className="toggle-group">
                            <label className="toggle-label">
                                <input
                                    type="checkbox"
                                    checked={formData.operatingHours.enabled}
                                    onChange={(e) => handleNestedChange('operatingHours', 'enabled', e.target.checked)}
                                />
                                <span className="toggle-switch"></span>
                                Habilitar Horario de Operación
                            </label>
                        </div>

                        {formData.operatingHours.enabled && (
                            <>
                                <div className="form-row">
                                    <div className="form-group">
                                        <label>Hora de Inicio</label>
                                        <input
                                            type="time"
                                            value={formData.operatingHours.start}
                                            onChange={(e) => handleNestedChange('operatingHours', 'start', e.target.value)}
                                        />
                                    </div>

                                    <div className="form-group">
                                        <label>Hora de Fin</label>
                                        <input
                                            type="time"
                                            value={formData.operatingHours.end}
                                            onChange={(e) => handleNestedChange('operatingHours', 'end', e.target.value)}
                                        />
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label>Días de Operación</label>
                                    <div className="days-selector">
                                        {daysOfWeek.map(day => (
                                            <label key={day.value} className="day-checkbox">
                                                <input
                                                    type="checkbox"
                                                    checked={formData.operatingHours.days.includes(day.value)}
                                                    onChange={(e) => {
                                                        const newDays = e.target.checked
                                                            ? [...formData.operatingHours.days, day.value]
                                                            : formData.operatingHours.days.filter(d => d !== day.value);
                                                        handleArrayChange('operatingHours', 'days', newDays);
                                                    }}
                                                />
                                                {day.label}
                                            </label>
                                        ))}
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label>Mensaje Fuera de Horario</label>
                                    <textarea
                                        value={formData.offlineMessage}
                                        onChange={(e) => handleChange('offlineMessage', e.target.value)}
                                        rows="3"
                                    />
                                </div>
                            </>
                        )}
                    </div>
                )}

                {/* TAB: Avanzado */}
                {activeTab === 'advanced' && (
                    <div className="config-section">
                        <h3>Configuración Avanzada</h3>

                        <div className="toggle-group">
                            <label className="toggle-label">
                                <input
                                    type="checkbox"
                                    checked={formData.enableFileUpload}
                                    onChange={(e) => handleChange('enableFileUpload', e.target.checked)}
                                />
                                <span className="toggle-switch"></span>
                                Permitir Carga de Archivos
                            </label>
                        </div>

                        {formData.enableFileUpload && (
                            <>
                                <div className="form-group indent">
                                    <label>Tamaño Máximo de Archivo (MB)</label>
                                    <input
                                        type="number"
                                        value={formData.maxFileSize}
                                        onChange={(e) => handleChange('maxFileSize', parseInt(e.target.value))}
                                        min="1"
                                        max="50"
                                    />
                                </div>

                                <div className="form-group indent">
                                    <label>Tipos de Archivo Permitidos</label>
                                    <input
                                        type="text"
                                        value={formData.allowedFileTypes}
                                        onChange={(e) => handleChange('allowedFileTypes', e.target.value)}
                                        placeholder="image/*, .pdf, .doc, .docx"
                                    />
                                    <small>Separar por comas</small>
                                </div>
                            </>
                        )}

                        <div className="alert alert-warning">
                            <span className="alert-icon">⚠️</span>
                            <div>
                                <strong>Atención:</strong> Los cambios en configuración avanzada pueden afectar el rendimiento del bot.
                                Asegúrate de probar en un ambiente de desarrollo primero.
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default BotConfiguration;