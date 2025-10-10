// frontend/admin-panel/src/pages/CustomersPage.jsx
import React, { useState, useEffect } from 'react';
import customerService from '../services/customerService';
import '../styles/pages/CustomersPage.css';

const CustomersPage = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [statusFilter, setStatusFilter] = useState('all');

    useEffect(() => {
        loadCustomers();
    }, [statusFilter]);

    const loadCustomers = async () => {
        try {
            setLoading(true);
            setError(null);
            const params = {};
            if (statusFilter !== 'all') {
                params.status = statusFilter.toUpperCase();
            }
            const data = await customerService.getAllCustomers(params);
            setCustomers(data);
        } catch (error) {
            console.error('Error loading customers:', error);
            setError('Error al cargar clientes. Por favor, intente nuevamente.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (term) => {
        setSearchTerm(term);
        if (term.trim()) {
            try {
                setError(null);
                const results = await customerService.searchCustomers(term);
                setCustomers(results);
            } catch (error) {
                console.error('Error searching customers:', error);
                setError('Error al buscar clientes. Por favor, intente nuevamente.');
            }
        } else {
            loadCustomers();
        }
    };

    const filteredCustomers = customers;

    // Iconos modernos
    const icons = {
        customers: '👥',
        export: '📊',
        new: '✨',
        search: '🔍',
        view: '👀',
        edit: '✏️',
        active: '🟢',
        inactive: '⚫'
    };

    return (
        <div className="customers-page">
            <div className="page-header">
                <div className="header-left">
                    <h1>{icons.customers} Clientes</h1>
                    <p className="page-subtitle">Gestión de clientes y contactos</p>
                </div>
                <div className="header-right">
                    <button className="btn-secondary">
                        {icons.export} Exportar
                    </button>
                    <button className="btn-primary">
                        {icons.new} Nuevo Cliente
                    </button>
                </div>
            </div>

            <div className="customers-filters">
                <div className="search-box">
                    <span className="search-icon">{icons.search}</span>
                    <input
                        type="text"
                        placeholder="Buscar clientes..."
                        className="search-input"
                        value={searchTerm}
                        onChange={(e) => handleSearch(e.target.value)}
                    />
                </div>
                <select 
                    className="filter-select"
                    value={statusFilter}
                    onChange={(e) => setStatusFilter(e.target.value)}
                >
                    <option value="all">Todos los clientes</option>
                    <option value="active">Activos</option>
                    <option value="inactive">Inactivos</option>
                </select>
            </div>

            <div className="customers-table-container">
                {loading ? (
                    <div className="loading">Cargando clientes...</div>
                ) : error ? (
                    <div className="error">{error}</div>
                ) : customers.length === 0 ? (
                    <div className="no-data">No se encontraron clientes</div>
                ) : (
                    <table className="customers-table">
                        <thead>
                        <tr>
                            <th>Cliente</th>
                            <th>Email</th>
                            <th>Teléfono</th>
                            <th>Número de Cuenta</th>
                            <th>Tipo</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                        </thead>
                        <tbody>
                        {customers.map(customer => (
                            <tr key={customer.id}>
                                <td>
                                    <div className="customer-cell">
                                        <div className="customer-avatar">
                                            {customer.full_name?.split(' ').map(n => n[0]).join('') || '?'}
                                        </div>
                                        <span className="customer-name">{customer.full_name || 'N/A'}</span>
                                    </div>
                                </td>
                                <td className="customer-email">{customer.email || 'N/A'}</td>
                                <td className="customer-phone">{customer.phone || 'N/A'}</td>
                                <td className="customer-account">{customer.account_number || 'N/A'}</td>
                                <td className="customer-type">
                                    {customer.customer_type === 'INDIVIDUAL' ? 'Individual' : 'Empresa'}
                                </td>
                                <td>
                                    <span className={`status-badge ${customer.status?.toLowerCase() || 'active'}`}>
                                        {customer.status === 'ACTIVE' ? 'Activo' : 'Inactivo'}
                                    </span>
                                </td>
                                <td>
                                    <div className="action-buttons">
                                        <button className="btn-icon" title="Ver detalles">
                                            {icons.view}
                                        </button>
                                        <button className="btn-icon" title="Editar cliente">
                                            {icons.edit}
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default CustomersPage;