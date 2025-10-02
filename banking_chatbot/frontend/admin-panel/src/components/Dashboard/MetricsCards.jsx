// frontend/admin-panel/src/components/Dashboard/MetricsCards.jsx - MEJORADO
import React from "react";
import "../../styles/components/MetricsCards.css";

const MetricsCards = ({ metrics, loading, timeRange }) => {
    const cards = [
        {
            title: "Total Tickets",
            value: metrics.totalTickets,
            icon: "📊",
            trend: "+12%",
            trendDirection: "up"
        },
        {
            title: "Active Chats",
            value: metrics.activeChats,
            icon: "💬",
            trend: "+5%",
            trendDirection: "up"
        },
        {
            title: "Avg Response",
            value: metrics.avgResponseTime,
            icon: "⏱️",
            trend: "-0.5m",
            trendDirection: "down"
        },
        {
            title: "Satisfaction",
            value: metrics.satisfaction,
            icon: "⭐",
            trend: "+0.2",
            trendDirection: "up"
        }
    ];

    const handleCardClick = (cardTitle) => {
        // Efecto de ripple ya está en CSS, aquí podemos agregar lógica adicional
        console.log(`Card clicked: ${cardTitle}`);
    };

    if (loading) {
        return (
            <div className="metrics-cards">
                {[1, 2, 3, 4].map((index) => (
                    <div key={index} className="metric-card skeleton">
                        <div className="skeleton-icon"></div>
                        <div className="metric-content">
                            <div className="skeleton-line short"></div>
                            <div className="skeleton-line" style={{width: '70%'}}></div>
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    return (
        <div className="metrics-cards">
            {cards.map((card, index) => (
                <div
                    key={index}
                    className="metric-card"
                    onClick={() => handleCardClick(card.title)}
                    role="button"
                    tabIndex={0}
                    aria-label={`Ver detalles de ${card.title}`}
                    onKeyPress={(e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            handleCardClick(card.title);
                        }
                    }}
                >
                    <div className="metric-icon">{card.icon}</div>
                    <div className="metric-content">
                        <h3>{card.title}</h3>
                        <p className="metric-value">{card.value}</p>
                        <div className={`metric-trend trend-${card.trendDirection}`}>
                            {card.trend}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default MetricsCards;