// frontend/admin-panel/src/components/Tickets/TicketFilters.jsx
import React, { useState } from 'react';
import '../../styles/components/TicketFilters.css';

const TicketFilters = ({ filters, onFilterChange, onReset }) => {
    const [isExpanded, setIsExpanded] = useState(true);

    const statusOptions = [
        { value: 'all', label: 'Todos', count: 245 },
        { value: 'open', label: 'Abiertos', count: 45 },
        { value: 'in_progress', label: 'En Progreso', count: 30 },
        { value: 'waiting', label: 'Esperando', count: 15 },
        { value: 'resolved', label: 'Resueltos', count: 80 },
        { value: 'closed', label: 'Cerrados', count: 75 }
    ];

    const priorityOptions = [
        { value: 'all', label: 'Todas', color: '#9e9e9e' },
        { value: 'low', label: 'Baja', color: '#4CAF50' },
        { value: 'medium', label: 'Media', color: '#FF9800' },
        { value: 'high', label: 'Alta', color: '#F44336' },
        { value: 'urgent', label: 'Urgente', color: '#9C27B0' }
    ];

    const categoryOptions = [
        { value: 'all', label: 'Todas' },
        { value: 'general', label: 'General' },
        { value: 'technical', label: 'Técnico' },
        { value: 'account', label: 'Cuenta' },
        { value: 'transaction', label: 'Transacciones' },
        { value: 'loan', label: 'Préstamos' },
        { value: 'card', label: 'Tarjetas' },
        { value: 'complaint', label: 'Reclamo' }
    ];

    const agents = [
        { id: 'all', name: 'Todos los agentes' },
        { id: '1', name: 'Juan Pérez' },
        { id: '2', name: 'María García' },
        { id: '3', name: 'Carlos López' },
        { id: '4', name: 'Ana Martínez' },
        { id: 'unassigned', name: 'Sin asignar' }
    ];

    const handleFilterChange = (filterType, value) => {
        onFilterChange?.({
            ...filters,
            [filterType]: value
        });
    };

    const hasActiveFilters = () => {
        return Object.values(filters).some(value => value !== 'all' && value !== '');
    };

    return (
        <div className={`ticket-filters ${isExpanded ? 'expanded' : 'collapsed'}`}>
            <div className="filters-header">
                <div className="header-left">
                    <h3>Filtros</h3>
                    {hasActiveFilters() && (
                        <span className="active-filters-badge">
              {Object.values(filters).filter(v => v !== 'all' && v !== '').length}
            </span>
                    )}
                </div>

                <div className="header-right">
                    {hasActiveFilters() && (
                        <button className="clear-filters-btn" onClick={onReset}>
                            Limpiar
                        </button>
                    )}
                    <button
                        className="toggle-filters-btn"
                        onClick={() => setIsExpanded(!isExpanded)}
                    >
                        {isExpanded ? '▼' : '▶'}
                    </button>
                </div>
            </div>

            {isExpanded && (
                <div className="filters-content">
                    {/* Búsqueda */}
                    <div className="filter-group">
                        <label className="filter-label">Buscar</label>
                        <div className="search-input-wrapper">
                            <span className="search-icon">🔍</span>
                            <input
                                type="text"
                                placeholder="ID, cliente, descripción..."
                                value={filters.search || ''}
                                onChange={(e) => handleFilterChange('search', e.target.value)}
                                className="filter-search-input"
                            />
                        </div>
                    </div>

                    {/* Estado */}
                    <div className="filter-group">
                        <label className="filter-label">Estado</label>
                        <div className="filter-options">
                            {statusOptions.map(option => (
                                <button
                                    key={option.value}
                                    className={`filter-option ${filters.status === option.value ? 'active' : ''}`}
                                    onClick={() => handleFilterChange('status', option.value)}
                                >
                                    <span className="option-label">{option.label}</span>
                                    <span className="option-count">{option.count}</span>
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Prioridad */}
                    <div className="filter-group">
                        <label className="filter-label">Prioridad</label>
                        <div className="priority-filters">
                            {priorityOptions.map(option => (
                                <button
                                    key={option.value}
                                    className={`priority-option ${filters.priority === option.value ? 'active' : ''}`}
                                    onClick={() => handleFilterChange('priority', option.value)}
                                >
                  <span
                      className="priority-indicator"
                      style={{ background: option.color }}
                  ></span>
                                    {option.label}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Categoría */}
                    <div className="filter-group">
                        <label className="filter-label">Categoría</label>
                        <select
                            value={filters.category || 'all'}
                            onChange={(e) => handleFilterChange('category', e.target.value)}
                            className="filter-select"
                        >
                            {categoryOptions.map(option => (
                                <option key={option.value} value={option.value}>
                                    {option.label}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Agente Asignado */}
                    <div className="filter-group">
                        <label className="filter-label">Asignado a</label>
                        <select
                            value={filters.assignedTo || 'all'}
                            onChange={(e) => handleFilterChange('assignedTo', e.target.value)}
                            className="filter-select"
                        >
                            {agents.map(agent => (
                                <option key={agent.id} value={agent.id}>
                                    {agent.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Rango de Fechas */}
                    <div className="filter-group">
                        <label className="filter-label">Fecha de creación</label>
                        <div className="date-range">
                            <input
                                type="date"
                                value={filters.dateFrom || ''}
                                onChange={(e) => handleFilterChange('dateFrom', e.target.value)}
                                className="date-input"
                                placeholder="Desde"
                            />
                            <span className="date-separator">—</span>
                            <input
                                type="date"
                                value={filters.dateTo || ''}
                                onChange={(e) => handleFilterChange('dateTo', e.target.value)}
                                className="date-input"
                                placeholder="Hasta"
                            />
                        </div>
                    </div>

                    {/* Ordenar por */}
                    <div className="filter-group">
                        <label className="filter-label">Ordenar por</label>
                        <select
                            value={filters.sortBy || 'newest'}
                            onChange={(e) => handleFilterChange('sortBy', e.target.value)}
                            className="filter-select"
                        >
                            <option value="newest">Más recientes</option>
                            <option value="oldest">Más antiguos</option>
                            <option value="priority">Prioridad</option>
                            <option value="status">Estado</option>
                            <option value="updated">Última actualización</option>
                        </select>
                    </div>
                </div>
            )}
        </div>
    );
};

export default TicketFilters;