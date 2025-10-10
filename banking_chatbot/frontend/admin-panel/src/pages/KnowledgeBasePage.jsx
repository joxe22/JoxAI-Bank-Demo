// frontend/admin-panel/src/pages/KnowledgeBasePage.jsx
import React, { useState, useEffect } from 'react';
import knowledgeService from '../services/knowledgeService';
import '../styles/pages/KnowledgeBasePage.css';

const KnowledgeBasePage = () => {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('all');
    const [categories, setCategories] = useState([]);

    useEffect(() => {
        loadCategories();
    }, []);

    useEffect(() => {
        loadArticles();
    }, [categoryFilter]);

    const loadCategories = async () => {
        try {
            const data = await knowledgeService.getCategories();
            setCategories(data);
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    };

    const loadArticles = async () => {
        try {
            setLoading(true);
            setError(null);
            const params = {};
            if (categoryFilter !== 'all') {
                params.category = categoryFilter;
            }
            const data = await knowledgeService.getAllArticles(params);
            setArticles(data);
        } catch (error) {
            console.error('Error loading articles:', error);
            setError('Error al cargar artículos. Por favor, intente nuevamente.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = async (term) => {
        setSearchTerm(term);
        if (term.trim()) {
            try {
                setError(null);
                const params = {};
                if (categoryFilter !== 'all') {
                    params.category = categoryFilter;
                }
                const results = await knowledgeService.searchArticles(term, params);
                setArticles(results);
            } catch (error) {
                console.error('Error searching articles:', error);
                setError('Error al buscar artículos. Por favor, intente nuevamente.');
            }
        } else {
            loadArticles();
        }
    };

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
                        <span className="stat-value">{articles.length}</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">{icons.views}</div>
                    <div className="stat-content">
                        <span className="stat-label">Artículos Activos</span>
                        <span className="stat-value">{articles.filter(a => a.is_active).length}</span>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon">{icons.categories}</div>
                    <div className="stat-content">
                        <span className="stat-label">Categorías</span>
                        <span className="stat-value">{new Set(articles.map(a => a.category)).size}</span>
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
                        value={searchTerm}
                        onChange={(e) => handleSearch(e.target.value)}
                    />
                </div>
                <select 
                    className="filter-select"
                    value={categoryFilter}
                    onChange={(e) => setCategoryFilter(e.target.value)}
                >
                    <option value="all">Todas las categorías</option>
                    {categories.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                    ))}
                </select>
            </div>

            <div className="articles-grid">
                {loading ? (
                    <div className="loading">Cargando artículos...</div>
                ) : error ? (
                    <div className="error">{error}</div>
                ) : articles.length === 0 ? (
                    <div className="no-data">No se encontraron artículos</div>
                ) : (
                    articles.map(article => (
                        <div key={article.id} className="article-card">
                            <div className="article-header">
                                <span className="article-category">{article.category || 'General'}</span>
                                <span className={`status-badge ${article.is_active ? 'published' : 'draft'}`}>
                                    {article.is_active ? 'Publicado' : 'Borrador'}
                                </span>
                            </div>
                            <h3 className="article-title">{article.title}</h3>
                            <div className="article-footer">
                                <span className="article-tags">
                                    {article.tags?.slice(0, 2).join(', ') || 'Sin etiquetas'}
                                </span>
                                <span className="article-date">
                                    {new Date(article.updated_at).toLocaleDateString('es-ES')}
                                </span>
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
                    ))
                )}
            </div>
        </div>
    );
};

export default KnowledgeBasePage;