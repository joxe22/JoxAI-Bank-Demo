// WebSocket service para comunicación en tiempo real
const WS_BASE_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

class WebSocketService {
    constructor() {
        this.ws = null;
        this.conversationId = null;
        this.listeners = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.reconnectDelay = 3000;
        this.isIntentionalClose = false;
    }

    // Conectar al WebSocket
    connect(conversationId) {
        this.conversationId = conversationId;
        this.isIntentionalClose = false;

        const wsUrl = `${WS_BASE_URL}/ws/chat/${conversationId}`;

        try {
            this.ws = new WebSocket(wsUrl);
            this.setupEventHandlers();

            console.log(`Conectando WebSocket: ${wsUrl}`);
        } catch (error) {
            console.error('Error al conectar WebSocket:', error);
            this.handleReconnect();
        }
    }

    // Configurar manejadores de eventos
    setupEventHandlers() {
        this.ws.onopen = () => {
            console.log('WebSocket conectado');
            this.reconnectAttempts = 0;
            this.emit('connected');
        };

        this.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log('Mensaje WebSocket recibido:', data);

                // Emitir evento según tipo de mensaje
                if (data.type) {
                    this.emit(data.type, data);
                }

                // Emitir evento genérico de mensaje
                this.emit('message', data);
            } catch (error) {
                console.error('Error al parsear mensaje WebSocket:', error);
            }
        };

        this.ws.onerror = (error) => {
            console.error('Error en WebSocket:', error);
            this.emit('error', error);
        };

        this.ws.onclose = (event) => {
            console.log('WebSocket cerrado', event.code, event.reason);
            this.emit('disconnected', { code: event.code, reason: event.reason });

            // Intentar reconectar si no fue cierre intencional
            if (!this.isIntentionalClose && this.reconnectAttempts < this.maxReconnectAttempts) {
                this.handleReconnect();
            }
        };
    }

    // Manejar reconexión
    handleReconnect() {
        if (this.reconnectAttempts >= this.maxReconnectAttempts) {
            console.error('Máximo de intentos de reconexión alcanzado');
            this.emit('maxReconnectAttempts');
            return;
        }

        this.reconnectAttempts++;
        const delay = this.reconnectDelay * this.reconnectAttempts;

        console.log(`Intentando reconectar en ${delay}ms (intento ${this.reconnectAttempts})`);

        setTimeout(() => {
            if (this.conversationId) {
                this.connect(this.conversationId);
            }
        }, delay);
    }

    // Enviar mensaje
    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        } else {
            console.warn('WebSocket no está conectado');
        }
    }

    // Notificar que el usuario está escribiendo
    sendTyping(isTyping) {
        this.send({
            type: 'typing',
            is_typing: isTyping
        });
    }

    // Registrar listener para eventos
    on(event, callback) {
        if (!this.listeners[event]) {
            this.listeners[event] = [];
        }
        this.listeners[event].push(callback);
    }

    // Remover listener
    off(event, callback) {
        if (this.listeners[event]) {
            this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
        }
    }

    // Emitir evento a todos los listeners
    emit(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error en listener de evento ${event}:`, error);
                }
            });
        }
    }

    // Desconectar
    disconnect() {
        this.isIntentionalClose = true;
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.listeners = {};
    }

    // Verificar estado de conexión
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }
}

export default new WebSocketService();