// frontend/admin-panel/src/components/Settings/UserManagement.jsx
import React, { useState } from 'react';
import '../../styles/components/UserManagement.css'

const UserManagement = () => {
    const [users, setUsers] = useState([
        {
            id: 1,
            name: 'Juan Pérez',
            email: 'juan.perez@banco.com',
            role: 'admin',
            status: 'active',
            lastLogin: '2024-01-15 14:30',
            createdAt: '2023-06-10'
        },
        {
            id: 2,
            name: 'María García',
            email: 'maria.garcia@banco.com',
            role: 'agent',
            status: 'active',
            lastLogin: '2024-01-15 13:45',
            createdAt: '2023-07-22'
        },
        {
            id: 3,
            name: 'Carlos López',
            email: 'carlos.lopez@banco.com',
            role: 'agent',
            status: 'active',
            lastLogin: '2024-01-14 18:20',
            createdAt: '2023-08-05'
        },
        {
            id: 4,
            name: 'Ana Martínez',
            email: 'ana.martinez@banco.com',
            role: 'supervisor',
            status: 'inactive',
            lastLogin: '2024-01-10 09:15',
            createdAt: '2023-09-12'
        }
    ]);

    const [showAddModal, setShowAddModal] = useState(false);
    const [showEditModal, setShowEditModal] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [filterRole, setFilterRole] = useState('all');
    const [filterStatus, setFilterStatus] = useState('all');

    const [newUser, setNewUser] = useState({
        name: '',
        email: '',
        role: 'agent',
        password: ''
    });

    const roles = [
        { value: 'admin', label: 'Administrador', color: '#9C27B0' },
        { value: 'supervisor', label: 'Supervisor', color: '#FF9800' },
        { value: 'agent', label: 'Agente', color: '#4CAF50' },
        { value: 'viewer', label: 'Observador', color: '#2196F3' }
    ];

    const permissions = {
        admin: ['Acceso completo', 'Gestión usuarios', 'Configuración sistema', 'Ver reportes', 'Gestionar tickets'],
        supervisor: ['Ver reportes', 'Gestionar tickets', 'Asignar agentes', 'Ver configuración'],
        agent: ['Ver tickets asignados', 'Responder conversaciones', 'Ver reportes básicos'],
        viewer: ['Ver reportes', 'Ver tickets', 'Solo lectura']
    };

    const filteredUsers = users.filter(user => {
        const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            user.email.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesRole = filterRole === 'all' || user.role === filterRole;
        const matchesStatus = filterStatus === 'all' || user.status === filterStatus;

        return matchesSearch && matchesRole && matchesStatus;
    });

    const handleAddUser = () => {
        if (!newUser.name || !newUser.email || !newUser.password) {
            alert('Por favor completa todos los campos');
            return;
        }

        const user = {
            id: users.length + 1,
            ...newUser,
            status: 'active',
            lastLogin: null,
            createdAt: new Date().toISOString().split('T')[0]
        };

        setUsers([...users, user]);
        setNewUser({ name: '', email: '', role: 'agent', password: '' });
        setShowAddModal(false);
        alert('Usuario agregado exitosamente');
    };

    const handleEditUser = () => {
        setUsers(users.map(u => u.id === selectedUser.id ? selectedUser : u));
        setShowEditModal(false);
        setSelectedUser(null);
        alert('Usuario actualizado exitosamente');
    };

    const handleDeleteUser = (userId) => {
        if (window.confirm('¿Estás seguro de eliminar este usuario?')) {
            setUsers(users.filter(u => u.id !== userId));
            alert('Usuario eliminado');
        }
    };

    const handleToggleStatus = (userId) => {
        setUsers(users.map(u =>
            u.id === userId
                ? { ...u, status: u.status === 'active' ? 'inactive' : 'active' }
                : u
        ));
    };

    const getRoleColor = (role) => {
        return roles.find(r => r.value === role)?.color || '#9e9e9e';
    };

    const getRoleLabel = (role) => {
        return roles.find(r => r.value === role)?.label || role;
    };

    return (
        <div className="user-management">
            <div className="management-header">
                <div className="header-left">
                    <h2>Gestión de Usuarios</h2>
                    <p className="subtitle">Administra los usuarios y sus permisos</p>
                </div>
                <button
                    className="btn-add-user"
                    onClick={() => setShowAddModal(true)}
                >
                    + Agregar Usuario
                </button>
            </div>

            {/* Filters */}
            <div className="filters-bar">
                <div className="search-box">
                    <span className="search-icon">🔍</span>
                    <input
                        type="text"
                        placeholder="Buscar por nombre o email..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <select
                    value={filterRole}
                    onChange={(e) => setFilterRole(e.target.value)}
                    className="filter-select"
                >
                    <option value="all">Todos los roles</option>
                    {roles.map(role => (
                        <option key={role.value} value={role.value}>{role.label}</option>
                    ))}
                </select>

                <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="filter-select"
                >
                    <option value="all">Todos los estados</option>
                    <option value="active">Activos</option>
                    <option value="inactive">Inactivos</option>
                </select>
            </div>

            {/* Users Table */}
            <div className="users-table-container">
                <table className="users-table">
                    <thead>
                    <tr>
                        <th>Usuario</th>
                        <th>Email</th>
                        <th>Rol</th>
                        <th>Estado</th>
                        <th>Último Acceso</th>
                        <th>Fecha Registro</th>
                        <th>Acciones</th>
                    </tr>
                    </thead>
                    <tbody>
                    {filteredUsers.map(user => (
                        <tr key={user.id}>
                            <td>
                                <div className="user-cell">
                                    <div className="user-avatar">
                                        {user.name.charAt(0)}
                                    </div>
                                    <span>{user.name}</span>
                                </div>
                            </td>
                            <td>{user.email}</td>
                            <td>
                  <span
                      className="role-badge"
                      style={{ background: getRoleColor(user.role) }}
                  >
                    {getRoleLabel(user.role)}
                  </span>
                            </td>
                            <td>
                                <button
                                    className={`status-toggle ${user.status}`}
                                    onClick={() => handleToggleStatus(user.id)}
                                >
                                    {user.status === 'active' ? 'Activo' : 'Inactivo'}
                                </button>
                            </td>
                            <td>{user.lastLogin || 'Nunca'}</td>
                            <td>{user.createdAt}</td>
                            <td>
                                <div className="action-buttons">
                                    <button
                                        className="btn-icon"
                                        onClick={() => {
                                            setSelectedUser({...user});
                                            setShowEditModal(true);
                                        }}
                                        title="Editar"
                                    >
                                        ✏️
                                    </button>
                                    <button
                                        className="btn-icon"
                                        onClick={() => handleDeleteUser(user.id)}
                                        title="Eliminar"
                                    >
                                        🗑️
                                    </button>
                                </div>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>

                {filteredUsers.length === 0 && (
                    <div className="empty-state">
                        <p>No se encontraron usuarios</p>
                    </div>
                )}
            </div>

            {/* Add User Modal */}
            {showAddModal && (
                <div className="modal-overlay" onClick={() => setShowAddModal(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Agregar Nuevo Usuario</h3>
                            <button className="modal-close" onClick={() => setShowAddModal(false)}>✕</button>
                        </div>

                        <div className="modal-body">
                            <div className="form-group">
                                <label>Nombre Completo</label>
                                <input
                                    type="text"
                                    value={newUser.name}
                                    onChange={(e) => setNewUser({...newUser, name: e.target.value})}
                                    placeholder="Juan Pérez"
                                />
                            </div>

                            <div className="form-group">
                                <label>Email</label>
                                <input
                                    type="email"
                                    value={newUser.email}
                                    onChange={(e) => setNewUser({...newUser, email: e.target.value})}
                                    placeholder="juan.perez@banco.com"
                                />
                            </div>

                            <div className="form-group">
                                <label>Rol</label>
                                <select
                                    value={newUser.role}
                                    onChange={(e) => setNewUser({...newUser, role: e.target.value})}
                                >
                                    {roles.map(role => (
                                        <option key={role.value} value={role.value}>{role.label}</option>
                                    ))}
                                </select>

                                <div className="permissions-preview">
                                    <strong>Permisos:</strong>
                                    <ul>
                                        {permissions[newUser.role]?.map((perm, idx) => (
                                            <li key={idx}>✓ {perm}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>

                            <div className="form-group">
                                <label>Contraseña Temporal</label>
                                <input
                                    type="password"
                                    value={newUser.password}
                                    onChange={(e) => setNewUser({...newUser, password: e.target.value})}
                                    placeholder="••••••••"
                                />
                                <small>El usuario deberá cambiar su contraseña en el primer acceso</small>
                            </div>
                        </div>

                        <div className="modal-footer">
                            <button className="btn-cancel" onClick={() => setShowAddModal(false)}>
                                Cancelar
                            </button>
                            <button className="btn-submit" onClick={handleAddUser}>
                                Agregar Usuario
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Edit User Modal */}
            {showEditModal && selectedUser && (
                <div className="modal-overlay" onClick={() => setShowEditModal(false)}>
                    <div className="modal-content" onClick={(e) => e.stopPropagation()}>
                        <div className="modal-header">
                            <h3>Editar Usuario</h3>
                            <button className="modal-close" onClick={() => setShowEditModal(false)}>✕</button>
                        </div>

                        <div className="modal-body">
                            <div className="form-group">
                                <label>Nombre Completo</label>
                                <input
                                    type="text"
                                    value={selectedUser.name}
                                    onChange={(e) => setSelectedUser({...selectedUser, name: e.target.value})}
                                />
                            </div>

                            <div className="form-group">
                                <label>Email</label>
                                <input
                                    type="email"
                                    value={selectedUser.email}
                                    onChange={(e) => setSelectedUser({...selectedUser, email: e.target.value})}
                                />
                            </div>

                            <div className="form-group">
                                <label>Rol</label>
                                <select
                                    value={selectedUser.role}
                                    onChange={(e) => setSelectedUser({...selectedUser, role: e.target.value})}
                                >
                                    {roles.map(role => (
                                        <option key={role.value} value={role.value}>{role.label}</option>
                                    ))}
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Estado</label>
                                <select
                                    value={selectedUser.status}
                                    onChange={(e) => setSelectedUser({...selectedUser, status: e.target.value})}
                                >
                                    <option value="active">Activo</option>
                                    <option value="inactive">Inactivo</option>
                                </select>
                            </div>
                        </div>

                        <div className="modal-footer">
                            <button className="btn-cancel" onClick={() => setShowEditModal(false)}>
                                Cancelar
                            </button>
                            <button className="btn-submit" onClick={handleEditUser}>
                                Guardar Cambios
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default UserManagement;