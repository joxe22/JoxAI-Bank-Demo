// frontend/admin-panel/src/components/Tickets/TicketDetail.jsx
import React, { useState } from 'react';
import '../../styles/components/TicketDetails.css';

const TicketDetail = ({ ticket, onUpdate, onClose }) => {
    const [status, setStatus] = useState(ticket?.status || 'open');
    const [priority, setPriority] = useState(ticket?.priority || 'medium');
    const [assignedTo, setAssignedTo] = useState(ticket?.assignedTo || '');
    const [notes, setNotes] = useState('');
    const [showNotesForm, setShowNotesForm] = useState(false);

    const statusOptions = [
        { value: 'open', label: 'Abierto', color: '#f093fb' },
        { value: 'in_progress', label: 'En Progreso', color: '#4facfe' },
        { value: 'waiting', label: 'Esperando', color: '#feca57' },
        { value: 'resolved', label: 'Resuelto', color: '#43e97b' },
        { value: 'closed', label: 'Cerrado', color: '#95a5a6' }
    ];

    const priorityOptions = [
        { value: 'low', label: 'Baja', color: '#4CAF50' },
        { value: 'medium', label: 'Media', color: '#FF9800' },
        { value: 'high', label: 'Alta', color: '#F44336' },
        { value: 'urgent', label: 'Urgente', color: '#9C27B0' }
    ];

    const agents = [
        { id: 1, name: 'Juan Pérez' },
        { id: 2, name: 'María García' },
        { id: 3, name: 'Carlos López' },
        { id: 4, name: 'Ana Martínez' }
    ];

    const handleSave = async () => {
        try {
            await onUpdate({
                id: ticket.id,
                status,
                priority,
                assignedTo
            });
            alert('Ticket actualizado correctamente');
        } catch (error) {
            console.error('Error actualizando ticket:', error);
            alert('Error al actualizar el ticket');
        }
    };

    const handleAddNote = () => {
        if (notes.trim()) {
            // Aquí iría la lógica para agregar la nota
            console.log('Agregar nota:', notes);
            setNotes('');
            setShowNotesForm(false);
        }
    };

    const formatDate = (date) => {
        return new Date(date).toLocaleString('es-ES', {
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (!ticket) {
        return (
            <div className="ticket-detail-empty">
                <p>Selecciona un ticket para ver los detalles</p>
            </div>
        );
    }

    return (
        <div className="ticket-detail">
            <div className="ticket-detail-header">
                <div className="header-left">
                    <h2 className="ticket-id">#{ticket.id}</h2>
                    <span className="ticket-category">{ticket.category}</span>
                </div>
                <button className="close-button" onClick={onClose}>✕</button>
            </div>

            <div className="ticket-detail-body">
                {/* Información Principal */}
                <section className="detail-section">
                    <h3 className="section-title">Información del Ticket</h3>

                    <div className="info-grid">
                        <div className="info-item">
                            <label>Estado</label>
                            <select
                                value={status}
                                onChange={(e) => setStatus(e.target.value)}
                                className="status-select"
                            >
                                {statusOptions.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="info-item">
                            <label>Prioridad</label>
                            <select
                                value={priority}
                                onChange={(e) => setPriority(e.target.value)}
                                className="priority-select"
                            >
                                {priorityOptions.map(option => (
                                    <option key={option.value} value={option.value}>
                                        {option.label}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="info-item">
                            <label>Asignado a</label>
                            <select
                                value={assignedTo}
                                onChange={(e) => setAssignedTo(e.target.value)}
                                className="agent-select"
                            >
                                <option value="">Sin asignar</option>
                                {agents.map(agent => (
                                    <option key={agent.id} value={agent.id}>
                                        {agent.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="info-item">
                            <label>Creado</label>
                            <span className="info-value">{formatDate(ticket.createdAt)}</span>
                        </div>

                        <div className="info-item">
                            <label>Última actualización</label>
                            <span className="info-value">{formatDate(ticket.updatedAt)}</span>
                        </div>

                        <div className="info-item">
                            <label>Cliente</label>
                            <span className="info-value">{ticket.customerName}</span>
                        </div>
                    </div>
                </section>

                {/* Descripción */}
                <section className="detail-section">
                    <h3 className="section-title">Descripción</h3>
                    <div className="description-box">
                        <p>{ticket.description || 'Sin descripción'}</p>
                    </div>
                </section>

                {/* Notas Internas */}
                <section className="detail-section">
                    <div className="section-header">
                        <h3 className="section-title">Notas Internas</h3>
                        <button
                            className="btn-add-note"
                            onClick={() => setShowNotesForm(!showNotesForm)}
                        >
                            + Agregar Nota
                        </button>
                    </div>

                    {showNotesForm && (
                        <div className="notes-form">
              <textarea
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Escribe una nota interna..."
                  rows="4"
                  className="notes-textarea"
              />
                            <div className="notes-actions">
                                <button
                                    className="btn btn-secondary"
                                    onClick={() => {
                                        setShowNotesForm(false);
                                        setNotes('');
                                    }}
                                >
                                    Cancelar
                                </button>
                                <button
                                    className="btn btn-primary"
                                    onClick={handleAddNote}
                                >
                                    Guardar Nota
                                </button>
                            </div>
                        </div>
                    )}

                    <div className="notes-list">
                        {ticket.notes && ticket.notes.length > 0 ? (
                            ticket.notes.map((note, index) => (
                                <div key={index} className="note-item">
                                    <div className="note-header">
                                        <strong>{note.author}</strong>
                                        <span className="note-date">{formatDate(note.date)}</span>
                                    </div>
                                    <p className="note-content">{note.content}</p>
                                </div>
                            ))
                        ) : (
                            <p className="empty-notes">No hay notas internas</p>
                        )}
                    </div>
                </section>

                {/* Historial */}
                <section className="detail-section">
                    <h3 className="section-title">Historial</h3>
                    <div className="timeline">
                        {ticket.history && ticket.history.map((event, index) => (
                            <div key={index} className="timeline-item">
                                <div className="timeline-marker"></div>
                                <div className="timeline-content">
                                    <p className="timeline-text">{event.text}</p>
                                    <span className="timeline-date">{formatDate(event.date)}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>
            </div>

            <div className="ticket-detail-footer">
                <button className="btn btn-secondary" onClick={onClose}>
                    Cancelar
                </button>
                <button className="btn btn-primary" onClick={handleSave}>
                    Guardar Cambios
                </button>
            </div>
        </div>
    );
};

export default TicketDetail;