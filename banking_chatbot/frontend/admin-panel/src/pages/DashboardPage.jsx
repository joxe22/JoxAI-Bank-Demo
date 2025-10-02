// frontend/admin-panel/src/pages/DashboardPage.jsx
import React, { useState } from "react";
import MetricsCards from "../components/Dashboard/MetricsCards";
import ChartsSection from "../components/Dashboard/ChartsSection";
import Modal from "../components/Common/Modal"
import "../styles/pages/DashboardPage.css";

const DashboardPage = () => {
    const [timeRange, setTimeRange] = useState('today');

    const metrics = {
        totalTickets: 150,
        activeChats: 23,
        avgResponseTime: "2.5m",
        satisfaction: 4.5,
        newTickets: 12,
        resolvedTickets: 45
    };

    const chartData = {
        conversations: {
            today: [65, 78, 90, 81, 56, 55, 40],
            week: [120, 150, 180, 165, 200, 190, 210],
            month: [850, 920, 780, 1100, 950, 1200, 1300, 1250, 1400, 1350, 1500, 1600]
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

            <MetricsCards metrics={metrics} loading={false} />
            <ChartsSection data={chartData} timeRange={timeRange} />
        </div>
    );
};

export default DashboardPage;
