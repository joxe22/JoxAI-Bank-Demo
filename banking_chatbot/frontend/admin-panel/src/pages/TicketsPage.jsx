import React, { useState, useEffect } from 'react';
import TicketDetail from '../components/Tickets/TicketDetail';
import TicketChat from '../components/Tickets/TicketChat';
import TicketFilters from '../components/Tickets/TicketFilters';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import ticketService from '../services/ticketService';
import '../styles/pages/TicketsPage.css';

// Helper function to normalize backend data for frontend display
const normalizeTicket = (ticket) => {
    const statusMap = {
        'OPEN': 'open',
        'IN_PROGRESS': 'pending',
        'RESOLVED': 'resolved',
        'CLOSED': 'closed'
    };

    const priorityMap = {
        'HIGH': 'high',
        'MEDIUM': 'medium',
        'LOW': 'low'
    };

    return {
        ...ticket,
        status: statusMap[ticket.status] || ticket.status.toLowerCase(),
        priority: priorityMap[ticket.priority] || ticket.priority.toLowerCase(),
        createdAt: ticket.created_at || ticket.createdAt,
        assignedTo: ticket.assigned_to_name || ticket.assignedTo || (ticket.assigned_to ? `Agent ${ticket.assigned_to}` : null)
    };
};

// Componente TicketList interno
const TicketList = ({ tickets, selectedTicket, onSelectTicket }) => {
    if (!tickets || tickets.length === 0) {
        return (
            <div className="no-tickets">
                <div className="empty-icon">📋</div>
                <h3>No hay tickets</h3>
                <p>No se encontraron tickets con los filtros seleccionados</p>
            </div>
        );
    }

    return (
        <div className="tickets-list">
            {tickets.map(ticket => (
                <div
                    key={ticket.id}
                    className={`ticket-card ${selectedTicket?.id === ticket.id ? 'selected' : ''}`}
                    onClick={() => onSelectTicket(ticket)}
                >
                    <div className="ticket-header">
                        <h3 className="ticket-subject">{ticket.subject}</h3>
                        <span className={`status-badge status-${ticket.status}`}>
                            {ticket.status}
                        </span>
                    </div>

                    <div className="ticket-meta">
                        <span className={`priority-badge priority-${ticket.priority}`}>
                            {ticket.priority === 'high' && '🔴'}
                            {ticket.priority === 'medium' && '🟡'}
                            {ticket.priority === 'low' && '🟢'}
                            {ticket.priority}
                        </span>

                        {ticket.category && (
                            <span className="category-tag">{ticket.category}</span>
                        )}
                    </div>

                    {ticket.lastMessage && (
                        <p className="ticket-preview">{ticket.lastMessage}</p>
                    )}

                    <div className="ticket-footer">
                        <span className="ticket-date">
                            {new Date(ticket.createdAt || Date.now()).toLocaleDateString()}
                        </span>
                        {ticket.assignedTo && (
                            <span className="ticket-agent">👤 {ticket.assignedTo}</span>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
};

const TicketsPage = () => {
    const [tickets, setTickets] = useState([]);
    const [selectedTicket, setSelectedTicket] = useState(null);
    const [view, setView] = useState('detail'); // 'detail' o 'chat'
    const [isLoading, setIsLoading] = useState(true);
    const [filters, setFilters] = useState({
        status: 'all',
        priority: 'all',
        category: 'all',
        assignedTo: 'all',
        search: '',
        dateFrom: '',
        dateTo: '',
        sortBy: 'newest'
    });

    useEffect(() => {
        loadTickets();
    }, [filters]);

    const loadTickets = async () => {
        setIsLoading(true);
        try {
            const response = await ticketService.getTickets(filters);
            const normalizedTickets = (response.tickets || []).map(normalizeTicket);
            setTickets(normalizedTickets);
        } catch (error) {
            console.error('Error cargando tickets:', error);
            // En caso de error, usar datos mock para desarrollo
            setTickets([
                {
                    id: 1,
                    subject: "Consulta de saldo",
                    status: "open",
                    priority: "medium",
                    category: "Consultas",
                    createdAt: new Date().toISOString(),
                    lastMessage: "El cliente pregunta por su saldo disponible",
                    assignedTo: "Agent 1"
                },
                {
                    id: 2,
                    subject: "Transferencia fallida",
                    status: "pending",
                    priority: "high",
                    category: "Transacciones",
                    createdAt: new Date().toISOString(),
                    lastMessage: "Error al procesar transferencia internacional",
                    assignedTo: "Agent 2"
                },
                {
                    id: 3,
                    subject: "Actualización de datos",
                    status: "resolved",
                    priority: "low",
                    category: "Perfil",
                    createdAt: new Date().toISOString(),
                    lastMessage: "Cliente solicita cambio de dirección",
                    assignedTo: "Agent 1"
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSelectTicket = (ticket) => {
        setSelectedTicket(ticket);
        setView('detail');
    };

    const handleUpdateTicket = async (ticketData) => {
        try {
            await ticketService.updateTicket(ticketData.id, ticketData);
            // Actualizar la lista de tickets
            setTickets(tickets.map(t =>
                t.id === ticketData.id ? { ...t, ...ticketData } : t
            ));
            setSelectedTicket({ ...selectedTicket, ...ticketData });
        } catch (error) {
            console.error('Error actualizando ticket:', error);
            throw error;
        }
    };

    const handleCloseDetail = () => {
        setSelectedTicket(null);
        setView('detail');
    };

    const handleFilterChange = (newFilters) => {
        setFilters(newFilters);
    };

    const handleResetFilters = () => {
        setFilters({
            status: 'all',
            priority: 'all',
            category: 'all',
            assignedTo: 'all',
            search: '',
            dateFrom: '',
            dateTo: '',
            sortBy: 'newest'
        });
    };

    const handleSendMessage = async (ticketId, message) => {
        try {
            await ticketService.sendMessage(ticketId, message);
        } catch (error) {
            console.error('Error enviando mensaje:', error);
            throw error;
        }
    };

    return (
        <div className="tickets-page">
            <div className="page-header">
                <div className="header-left">
                    <h1>Tickets</h1>
                    <p className="page-subtitle">Gestión de tickets de soporte</p>
                </div>
                <div className="header-right">
                    <button className="btn-secondary">
                        Estadísticas
                    </button>
                    <button className="btn-primary">
                        + Crear Ticket
                    </button>
                </div>
            </div>

            <div className="tickets-content">
                {/* Filters Sidebar */}
                <div className="tickets-sidebar">
                    <TicketFilters
                        filters={filters}
                        onFilterChange={handleFilterChange}
                        onReset={handleResetFilters}
                    />
                </div>

                {/* Tickets List */}
                <div className="tickets-list-container">
                    {isLoading ? (
                        <LoadingSpinner size="medium" message="Cargando tickets..." />
                    ) : (
                        <TicketList
                            tickets={tickets}
                            selectedTicket={selectedTicket}
                            onSelectTicket={handleSelectTicket}
                        />
                    )}
                </div>

                {/* Ticket Detail/Chat */}
                <div className="tickets-detail-container">
                    {selectedTicket ? (
                        <>
                            <div className="detail-tabs">
                                <button
                                    className={`tab ${view === 'detail' ? 'active' : ''}`}
                                    onClick={() => setView('detail')}
                                >
                                    Detalles
                                </button>
                                <button
                                    className={`tab ${view === 'chat' ? 'active' : ''}`}
                                    onClick={() => setView('chat')}
                                >
                                    Chat
                                </button>
                            </div>

                            {view === 'detail' ? (
                                <TicketDetail
                                    ticket={selectedTicket}
                                    onUpdate={handleUpdateTicket}
                                    onClose={handleCloseDetail}
                                />
                            ) : (
                                <TicketChat
                                    ticketId={selectedTicket.id}
                                    messages={selectedTicket.messages || []}
                                    onSendMessage={handleSendMessage}
                                />
                            )}
                        </>
                    ) : (
                        <div className="no-ticket-selected">
                            <div className="empty-icon">🎫</div>
                            <h3>Selecciona un ticket</h3>
                            <p>Elige un ticket de la lista para ver sus detalles</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TicketsPage;
