import React, { useState } from 'react';
import '../styles/EscalationModal.css';

const EscalationModal = ({ isOpen, onClose, onEscalate, conversationId }) => {
    const [category, setCategory] = useState('general');
    const [priority, setPriority] = useState('medium');
    const [description, setDescription] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const categories = [
        { value: 'general', label: 'Consulta General' },
        { value: 'technical', label: 'Problema Técnico' },
        { value: 'account', label: 'Gestión de Cuenta' },
        { value: 'transaction', label: 'Transacciones' },
        { value: 'loan', label: 'Préstamos/Créditos' },
        { value: 'card', label: 'Tarjetas' },
        { value: 'complaint', label: 'Reclamo' },
        { value: 'other', label: 'Otro' }
    ];

    const priorities = [
        { value: 'low', label: 'Baja', color: '#4CAF50' },
        { value: 'medium', label: 'Media', color: '#FF9800' },
        { value: 'high', label: 'Alta', color: '#F44336' },
        { value: 'urgent', label: 'Urgente', color: '#9C27B0' }
    ];

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            await onEscalate({
                conversationId,
                category,
                priority,
                description: description.trim()
            });

            // Reset form
            setCategory('general');
            setPriority('medium');
            setDescription('');
            onClose();
        } catch (error) {
            console.error('Error al escalar:', error);
            alert('Error al crear el ticket. Por favor intenta nuevamente.');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h3>Escalar a Agente Humano</h3>
                    <button className="modal-close" onClick={onClose}>✕</button>
                </div>

                <form onSubmit={handleSubmit} className="modal-body">
                    <div className="form-group">
                        <label htmlFor="category">Categoría</label>
                        <select
                            id="category"
                            value={category}
                            onChange={(e) => setCategory(e.target.value)}
                            required
                        >
                            {categories.map((cat) => (
                                <option key={cat.value} value={cat.value}>
                                    {cat.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="form-group">
                        <label htmlFor="priority">Prioridad</label>
                        <div className="priority-options">
                            {priorities.map((p) => (
                                <label
                                    key={p.value}
                                    className={`priority-option ${priority === p.value ? 'selected' : ''}`}
                                    style={{ borderColor: priority === p.value ? p.color : '#ddd' }}
                                >
                                    <input
                                        type="radio"
                                        name="priority"
                                        value={p.value}
                                        checked={priority === p.value}
                                        onChange={(e) => setPriority(e.target.value)}
                                    />
                                    <span style={{ color: p.color }}>●</span> {p.label}
                                </label>
                            ))}
                        </div>
                    </div>

                    <div className="form-group">
                        <label htmlFor="description">Motivo (opcional)</label>
                        <textarea
                            id="description"
                            value={description}
                            onChange={(e) => setDescription(e.target.value)}
                            placeholder="Describe brevemente el motivo de la escalación..."
                            rows="4"
                            maxLength="500"
                        />
                        <span className="character-count">{description.length}/500</span>
                    </div>

                    <div className="modal-footer">
                        <button
                            type="button"
                            className="btn-cancel"
                            onClick={onClose}
                            disabled={isSubmitting}
                        >
                            Cancelar
                        </button>
                        <button
                            type="submit"
                            className="btn-submit"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Escalando...' : 'Escalar Conversación'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EscalationModal;