// frontend/admin-panel/src/pages/DashboardPage.jsx
import React, { useState, useEffect } from "react";
import MetricsCards from "../components/Dashboard/MetricsCards";
import ChartsSection from "../components/Dashboard/ChartsSection";
import Modal from "../components/Common/Modal"
import analyticsService from "../services/analyticsService";
import "../styles/pages/DashboardPage.css";

const DashboardPage = () => {
    const [timeRange, setTimeRange] = useState('week');
    const [metrics, setMetrics] = useState({
        totalTickets: 0,
        activeChats: 0,
        avgResponseTime: "0m",
        satisfaction: 0,
        newTickets: 0,
        resolvedTickets: 0
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const chartData = {
        conversations: {
            today: [65, 78, 90, 81, 56, 55, 40],
            week: [120, 150, 180, 165, 200, 190, 210],
            month: [850, 920, 780, 1100, 950, 1200, 1300, 1250, 1400, 1350, 1500, 1600]
        }
    };

    useEffect(() => {
        fetchDashboardMetrics();
    }, [timeRange]);

    const fetchDashboardMetrics = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await analyticsService.getDashboardMetrics(timeRange);
            
            setMetrics({
                totalTickets: data.total_tickets || 0,
                activeChats: data.active_conversations || 0,
                avgResponseTime: "2.5m",
                satisfaction: 4.5,
                totalConversations: data.total_conversations || 0,
                totalCustomers: data.total_customers || 0,
                escalationRate: data.escalation_rate || 0
            });
        } catch (err) {
            console.error('Error fetching dashboard metrics:', err);
            setError('Failed to load dashboard metrics');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dashboard-page">
            <div className="dashboard-header">
                <div className="header-left">
                    <h1>Dashboard</h1>
                    <p>Resumen general del sistema y métricas</p>
                </div>
                <div className="header-controls">
                    <select
                        value={timeRange}
                        onChange={(e) => setTimeRange(e.target.value)}
                        className="time-range-select"
                    >
                        <option value="today">Hoy</option>
                        <option value="week">Esta Semana</option>
                        <option value="month">Este Mes</option>
                        <option value="year">Este Año</option>
                    </select>
                </div>
            </div>

            {error && (
                <div className="error-message" style={{
                    padding: '12px',
                    margin: '16px 0',
                    backgroundColor: '#fee',
                    color: '#c33',
                    borderRadius: '8px'
                }}>
                    {error}
                </div>
            )}

            <MetricsCards metrics={metrics} loading={loading} />
            <ChartsSection data={chartData} timeRange={timeRange} loading={loading} />
        </div>
    );
};

export default DashboardPage;
