/**
 * 🚀 Punto de entrada del Chat Widget
 * Ubicación: frontend/chat-widget/src/main.jsx
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import ChatWidget from './components/ChatWidget.jsx'
import './styles/global.css'

// Renderizar el widget
ReactDOM.createRoot(document.getElementById('banking-chat-widget')).render(
    <React.StrictMode>
        <ChatWidget />
    </React.StrictMode>,
)