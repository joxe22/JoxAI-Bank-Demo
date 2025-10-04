// frontend/admin-panel/src/services/websocketService.js

// Detect WebSocket URL automatically - works in both dev and production
const getWsUrl = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const hostname = window.location.hostname;
    const port = window.location.port;
    
    // In production (served from same domain)
    if (hostname !== 'localhost' && hostname !== '127.0.0.1') {
        return `${protocol}//${hostname}${port ? ':' + port : ''}`;
    }
    // In development
    return import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
};

const WS_BASE_URL = getWsUrl();

class WebSocketService {
    constructor() {
        this.ws = null;
        this.listeners = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.isIntentionalClose = false;
        this.pingInterval = null;
    }

    // Connect to WebSocket
    connect(token = null) {
        this.isIntentionalClose = false;

        const authToken = token || localStorage.getItem('token');
        const wsUrl = `${WS_BASE_URL}/api/v1/conversations/ws/admin?token=${authToken}`;

        try {
            this.ws = new WebSocket(wsUrl);
            this.setupEventHandlers();
            this.startPingInterval();

            console.log('Connecting to Admin WebSocket...');
        } catch (error) {
            console.error('Error connecting to WebSocket:', error);
            this.handleReconnect();
        }
    }

    // Setup event handlers
    setupEventHandlers() {
        this.ws.onopen = () => {
            console.log('Admin WebSocket connected');
            this.reconnectAttempts = 0;
            // Send initial ping to keep connection alive
            this.send({ type: 'ping' });
            this.emit('connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log('WebSocket message received:', data);

                // Handle different message types
                if (data.type === 'pong') {
                    // Keep-alive response
                    return;
                }

                // Emit specific event
                if (data.type) {
                    this.emit(data.type, data);
                }

                // Emit general message event
                this.emit('message', data);
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.emit('error', error);
        };

        this.ws.onclose = (event) => {
            console.log('WebSocket closed', event.code, event.reason);
            this.stopPingInterval();
            this.emit('disconnected', { code: event.code, reason: event.reason });

            // Try to reconnect if not intentional close
            if (!this.isIntentionalClose && this.reconnectAttempts < this.maxReconnectAttempts) {
                this.handleReconnect();
            }
        };
    }

    // Handle reconnection
    handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            this.emit('maxReconnectAttempts');
            return;
        }

        this.reconnectAttempts++;
        const delay = this.reconnectDelay * this.reconnectAttempts;

        console.log(`Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

        setTimeout(() => {
            this.connect();
        }, delay);
    }

    // Start ping interval to keep connection alive
    startPingInterval() {
        this.pingInterval = setInterval(() => {
            if (this.isConnected()) {
                this.send({ type: 'ping' });
            }
        }, 30000); // Ping every 30 seconds
    }

    // Stop ping interval
    stopPingInterval() {
        if (this.pingInterval) {
            clearInterval(this.pingInterval);
            this.pingInterval = null;
        }
    }

    // Send message
    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket is not connected');
        }
    }

    // Subscribe to ticket updates
    subscribeToTicket(ticketId) {
        this.send({
            type: 'subscribe',
            channel: 'ticket',
            ticketId
        });
    }

    // Unsubscribe from ticket
    unsubscribeFromTicket(ticketId) {
        this.send({
            type: 'unsubscribe',
            channel: 'ticket',
            ticketId
        });
    }

    // Subscribe to real-time stats
    subscribeToStats() {
        this.send({
            type: 'subscribe',
            channel: 'stats'
        });
    }

    // Send typing indicator
    sendTyping(ticketId, isTyping) {
        this.send({
            type: 'typing',
            ticketId,
            isTyping
        });
    }

    // Register event listener
    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    // Remove event listener
    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    }

    // Emit event to all listeners
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in listener for event ${event}:`, error);
                }
            });
        }
    }

    // Check if connected
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    // Disconnect
    disconnect() {
        this.isIntentionalClose = true;
        this.stopPingInterval();
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.listeners = {};
    }
}

export default new WebSocketService();