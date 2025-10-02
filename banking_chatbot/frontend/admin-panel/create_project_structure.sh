#!/bin/bash

# Script para crear toda la estructura del proyecto Admin Panel
# Ejecutar desde: /frontend/admin-panel/

echo "🚀 Creando estructura de carpetas para Admin Panel..."

# Crear directorios principales
mkdir -p src/components/Common
mkdir -p src/components/Dashboard
mkdir -p src/components/Tickets
mkdir -p src/components/Analytics
mkdir -p src/components/Settings
mkdir -p src/pages
mkdir -p src/services
mkdir -p src/utils
mkdir -p src/styles/components
mkdir -p src/styles/pages

echo "✅ Carpetas creadas"

# Crear archivos placeholder para Pages
echo "📄 Creando archivos de Pages..."

cat > src/pages/LoginPage.jsx << 'EOF'
import React, { useState } from "react";
import "../styles/pages/LoginPage.css";

const LoginPage = () => {
  const [credentials, setCredentials] = useState({ email: "", password: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Login attempt:", credentials);
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <h1>JoxAI Bank Admin</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={credentials.email}
            onChange={(e) => setCredentials({...credentials, email: e.target.value})}
          />
          <input
            type="password"
            placeholder="Password"
            value={credentials.password}
            onChange={(e) => setCredentials({...credentials, password: e.target.value})}
          />
          <button type="submit">Login</button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
EOF

cat > src/pages/DashboardPage.jsx << 'EOF'
import React from "react";
import MetricsCards from "../components/Dashboard/MetricsCards";
import "../styles/pages/DashboardPage.css";

const DashboardPage = () => {
  const metrics = {
    totalTickets: 150,
    activeChats: 23,
    avgResponseTime: "2.5m",
    satisfaction: 4.5
  };

  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
      <MetricsCards metrics={metrics} loading={false} />
    </div>
  );
};

export default DashboardPage;
EOF

cat > src/pages/TicketsPage.jsx << 'EOF'
import React, { useState } from "react";
import "../styles/pages/TicketsPage.css";

const TicketsPage = () => {
  const [tickets] = useState([
    { id: 1, subject: "Consulta de saldo", status: "open", priority: "medium" },
    { id: 2, subject: "Transferencia fallida", status: "pending", priority: "high" }
  ]);

  return (
    <div className="tickets-page">
      <h1>Tickets</h1>
      <div className="tickets-list">
        {tickets.map(ticket => (
          <div key={ticket.id} className="ticket-card">
            <h3>{ticket.subject}</h3>
            <span className={`status ${ticket.status}`}>{ticket.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TicketsPage;
EOF

cat > src/pages/AnalyticsPage.jsx << 'EOF'
import React from "react";
import "../styles/pages/AnalyticsPage.css";

const AnalyticsPage = () => {
  return (
    <div className="analytics-page">
      <h1>Analytics</h1>
      <p>Análisis de conversaciones y rendimiento del chatbot</p>
    </div>
  );
};

export default AnalyticsPage;
EOF

cat > src/pages/SettingsPage.jsx << 'EOF'
import React from "react";
import "../styles/pages/SettingsPage.css";

const SettingsPage = () => {
  return (
    <div className="settings-page">
      <h1>Settings</h1>
      <p>Configuración del sistema y usuarios</p>
    </div>
  );
};

export default SettingsPage;
EOF

# Crear archivos CSS para Pages
echo "🎨 Creando archivos CSS de Pages..."

cat > src/styles/pages/LoginPage.css << 'EOF'
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.login-container h1 {
  margin-bottom: 1.5rem;
  text-align: center;
}

.login-container input {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.login-container button {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
EOF

cat > src/styles/pages/DashboardPage.css << 'EOF'
.dashboard-page {
  padding: 2rem;
}

.dashboard-page h1 {
  margin-bottom: 1.5rem;
}
EOF

cat > src/styles/pages/TicketsPage.css << 'EOF'
.tickets-page {
  padding: 2rem;
}

.tickets-list {
  display: grid;
  gap: 1rem;
  margin-top: 1rem;
}

.ticket-card {
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.status.open { background: #10b981; color: white; }
.status.pending { background: #f59e0b; color: white; }
EOF

cat > src/styles/pages/AnalyticsPage.css << 'EOF'
.analytics-page {
  padding: 2rem;
}
EOF

cat > src/styles/pages/SettingsPage.css << 'EOF'
.settings-page {
  padding: 2rem;
}
EOF

# Crear componente MetricsCards
echo "📦 Creando componentes..."

cat > src/components/Dashboard/MetricsCards.jsx << 'EOF'
import React from "react";
import "../../styles/components/MetricsCards.css";

const MetricsCards = ({ metrics, loading }) => {
  const cards = [
    { title: "Total Tickets", value: metrics.totalTickets, icon: "📊" },
    { title: "Active Chats", value: metrics.activeChats, icon: "💬" },
    { title: "Avg Response", value: metrics.avgResponseTime, icon: "⏱️" },
    { title: "Satisfaction", value: metrics.satisfaction, icon: "⭐" }
  ];

  if (loading) return <div>Loading...</div>;

  return (
    <div className="metrics-cards">
      {cards.map((card, index) => (
        <div key={index} className="metric-card">
          <div className="metric-icon">{card.icon}</div>
          <div className="metric-content">
            <h3>{card.title}</h3>
            <p className="metric-value">{card.value}</p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MetricsCards;
EOF

cat > src/styles/components/MetricsCards.css << 'EOF'
.metrics-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  font-size: 2rem;
}

.metric-content h3 {
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 0.5rem;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
}
EOF

echo "✅ Estructura completa creada!"
echo ""
echo "📁 Archivos creados:"
echo "  - 5 páginas (LoginPage, DashboardPage, TicketsPage, AnalyticsPage, SettingsPage)"
echo "  - 5 archivos CSS de páginas"
echo "  - 1 componente (MetricsCards)"
echo "  - 1 archivo CSS de componente"
echo ""
echo "🚀 Ahora ejecuta: npm run dev"