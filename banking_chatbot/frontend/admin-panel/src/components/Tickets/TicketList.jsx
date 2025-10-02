// frontend/admin-panel/src/components/Tickets/TicketList.jsx
import React from 'react';
import '../../styles/components/TicketList.css';

const TicketList = ({ tickets, selectedTicket, onSelectTicket }) => {
    const getPriorityColor = (priority) => {
        const colors = {
            low: '#4CAF50',
            medium: '#FF9800',
            high: '#F44336',
            urgent: '#9C27B0'
        };
        return colors[priority] || '#9e9e9e';
    };

    const getStatusColor = (status) => {
        const colors = {
            open: '#f093fb',
            in_progress: '#4facfe',
            waiting: '#feca57',
            resolved: '#43e97b',
            closed: '#95a5a6'
        };
        return colors[status] || '#9e9e9e';
    };

    const formatDate = (date) => {
        const d = new Date(date);
        const today = new Date();
        const diffTime = Math.abs(today - d);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            return d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
        } else if (diffDays === 1) {
            return 'Ayer';
        } else if (diffDays < 7) {
            return `Hace ${diffDays} días`;
        } else {
            return d.toLocaleDateString('es-ES', { day: '2-digit', month: 'short' });
        }
    };

    if (!tickets || tickets.length === 0) {
        return (
            <div className="ticket-list-empty">
                <div className="empty-icon">🎫</div>
                <h3>No hay tickets</h3>
                <p>No se encontraron tickets con los filtros aplicados</p>
            </div>
        );
    }

    return (
        <div className="ticket-list">
            {tickets.map((ticket) => (
                <div
                    key={ticket.id}
                    className={`ticket-item ${selectedTicket?.id === ticket.id ? 'selected' : ''}`}
                    onClick={() => onSelectTicket(ticket)}
                >
                    <div className="ticket-item-header">
                        <span className="ticket-id">#{ticket.id}</span>
                        <span
                            className="priority-dot"
                            style={{ background: getPriorityColor(ticket.priority) }}
                            title={ticket.priority}
                        ></span>
                    </div>

                    <h4 className="ticket-title">{ticket.title || ticket.description}</h4>

                    <div className="ticket-meta">
            <span className="ticket-category">
              {ticket.category}
            </span>
                        <span
                            className="ticket-status"
                            style={{ background: getStatusColor(ticket.status) }}
                        >
              {ticket.status}
            </span>
                    </div>

                    <div className="ticket-footer">
                        <div className="ticket-customer">
              <span className="customer-avatar">
                {ticket.customerName?.charAt(0) || '?'}
              </span>
                            <span className="customer-name">{ticket.customerName || 'Cliente'}</span>
                        </div>
                        <span className="ticket-time">{formatDate(ticket.createdAt)}</span>
                    </div>

                    {ticket.assignedTo && (
                        <div className="ticket-assigned">
                            <span className="assigned-icon">👤</span>
                            <span className="assigned-name">{ticket.assignedTo}</span>
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
};

export default TicketList;