// frontend/admin-panel/src/pages/CustomersPage.jsx
import React, { useState } from 'react';
import '../styles/pages/CustomersPage.css';

const CustomersPage = () => {
    const [customers] = useState([
        {
            id: 1,
            name: 'Juan Pérez',
            email: 'juan.perez@email.com',
            phone: '+1 809-555-0123',
            totalConversations: 15,
            lastContact: '2024-01-15',
            status: 'active'
        },
        {
            id: 2,
            name: 'María García',
            email: 'maria.garcia@email.com',
            phone: '+1 809-555-0456',
            totalConversations: 8,
            lastContact: '2024-01-14',
            status: 'active'
        },
        {
            id: 3,
            name: 'Carlos Rodríguez',
            email: 'carlos.rodriguez@email.com',
            phone: '+1 809-555-0789',
            totalConversations: 3,
            lastContact: '2024-01-10',
            status: 'inactive'
        },
        {
            id: 4,
            name: 'Ana López',
            email: 'ana.lopez@email.com',
            phone: '+1 809-555-0321',
            totalConversations: 22,
            lastContact: '2024-01-16',
            status: 'active'
        }
    ]);

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
                    />
                </div>
                <select className="filter-select">
                    <option value="all">Todos los clientes</option>
                    <option value="active">Activos</option>
                    <option value="inactive">Inactivos</option>
                </select>
            </div>

            <div className="customers-table-container">
                <table className="customers-table">
                    <thead>
                    <tr>
                        <th>Cliente</th>
                        <th>Email</th>
                        <th>Teléfono</th>
                        <th>Conversaciones</th>
                        <th>Último Contacto</th>
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
                                        {customer.name.split(' ').map(n => n[0]).join('')}
                                    </div>
                                    <span className="customer-name">{customer.name}</span>
                                </div>
                            </td>
                            <td className="customer-email">{customer.email}</td>
                            <td className="customer-phone">{customer.phone}</td>
                            <td className="customer-conversations">
                                <strong>{customer.totalConversations}</strong>
                            </td>
                            <td className="customer-last-contact">{customer.lastContact}</td>
                            <td>
                                <span className={`status-badge ${customer.status}`}>
                                    {customer.status === 'active' ? 'Activo' : 'Inactivo'}
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
            </div>
        </div>
    );
};

export default CustomersPage;