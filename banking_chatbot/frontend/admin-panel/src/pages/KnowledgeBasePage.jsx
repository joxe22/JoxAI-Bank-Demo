// frontend/admin-panel/src/pages/KnowledgeBasePage.jsx
import React, { useState } from 'react';
import '../styles/pages/KnowledgeBasePage.css';

const KnowledgeBasePage = () => {
    const [articles] = useState([
        {
            id: 1,
            title: 'Cómo realizar una transferencia bancaria',
            category: 'Transacciones',
            views: 1234,
            lastUpdated: '2024-01-15',
            status: 'published'
        },
        {
            id: 2,
            title: 'Requisitos para solicitar un préstamo',
            category: 'Préstamos',
            views: 892,
            lastUpdated: '2024-01-14',
            status: 'published'
        },
        {
            id: 3,
            title: 'Uso seguro de tarjetas de crédito',
            category: 'Tarjetas',
            views: 567,
            lastUpdated: '2024-01-13',
            status: 'draft'
        },
        {
            id: 4,
            title: 'Configuración de alertas de seguridad',
            category: 'Seguridad',
            views: 2341,
            lastUpdated: '2024-01-12',
            status: 'published'
        }
    ]);

    // Iconos modernos
    const icons = {
        knowledge: '📚',
        import: '📥',
        new: '✨',
        articles: '📄',
        views: '👁️',
        categories: '📂',
        search: '🔍',
        edit: '✏️',
        view: '👀',
        transaction: '💳',
        loan: '💰',
        card: '💳',
        security: '🛡️'
    };

    return (
        <div className="knowledge-base-page">
            <div className="page-header">
                <div className="header-left">
                    <h1>{icons.knowledge} Base de Conocimiento</h1>
                    <p className="page-subtitle">Artículos y documentación para el chatbot</p>
                </div>
                <div className="header-right">
                    <button className="btn-secondary">
                        {icons.import} Importar
                    </button>
                    <button className="btn-primary">
                        {icons.new} Nuevo Artículo
                    </button>
                </div>
            </div>

            <div className="knowledge-stats">
                <div className="stat-card">
                    <div className="stat-icon">{icons.articles}</div>
                    <div className="stat-content">
                        <span className="stat-label">Total Artículos</span>
                        <span className="stat-value">156</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">{icons.views}</div>
                    <div className="stat-content">
                        <span className="stat-label">Vistas Totales</span>
                        <span className="stat-value">12,450</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">{icons.categories}</div>
                    <div className="stat-content">
                        <span className="stat-label">Categorías</span>
                        <span className="stat-value">8</span>
                    </div>
                </div>
            </div>

            <div className="knowledge-filters">
                <div className="search-box">
                    <span className="search-icon">{icons.search}</span>
                    <input
                        type="text"
                        placeholder="Buscar artículos..."
                        className="search-input"
                    />
                </div>
                <select className="filter-select">
                    <option value="all">Todas las categorías</option>
                    <option value="transactions">Transacciones</option>
                    <option value="loans">Préstamos</option>
                    <option value="cards">Tarjetas</option>
                    <option value="security">Seguridad</option>
                </select>
            </div>

            <div className="articles-grid">
                {articles.map(article => (
                    <div key={article.id} className="article-card">
                        <div className="article-header">
                            <span className="article-category">{article.category}</span>
                            <span className={`status-badge ${article.status}`}>
                                {article.status === 'published' ? 'Publicado' : 'Borrador'}
                            </span>
                        </div>
                        <h3 className="article-title">{article.title}</h3>
                        <div className="article-footer">
                            <span className="article-views">{icons.views} {article.views} vistas</span>
                            <span className="article-date">Actualizado: {article.lastUpdated}</span>
                        </div>
                        <div className="article-actions">
                            <button className="btn-secondary btn-small">
                                {icons.edit} Editar
                            </button>
                            <button className="btn-secondary btn-small">
                                {icons.view} Ver
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default KnowledgeBasePage;