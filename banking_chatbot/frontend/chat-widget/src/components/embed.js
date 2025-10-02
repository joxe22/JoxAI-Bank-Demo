/**
 * Chat Widget Embed Script
 *
 * Uso:
 * <script>
 *   window.chatbotConfig = {
 *     apiUrl: 'http://localhost:8000',
 *     primaryColor: '#1976d2',
 *     headerText: 'Chat Bancario',
 *     welcomeMessage: '¡Hola! ¿En qué puedo ayudarte?',
 *     autoOpen: false,
 *     enableEscalation: true,
 *     showBranding: true
 *   };
 * </script>
 * <script src="https://tu-dominio.com/embed.js"></script>
 */

(function() {
    'use strict';

    // Evitar múltiples inicializaciones
    if (window.__chatbot_initialized) {
        console.warn('Chat widget ya está inicializado');
        return;
    }
    window.__chatbot_initialized = true;

    // Configuración por defecto
    const defaultConfig = {
        apiUrl: 'http://localhost:8000',
        wsUrl: 'ws://localhost:8000',
        primaryColor: '#1976d2',
        headerText: 'Chat Bancario',
        welcomeMessage: '¡Hola! ¿En qué puedo ayudarte hoy?',
        placeholderText: 'Escribe tu mensaje...',
        position: 'bottom-right',
        autoOpen: false,
        enableFileUpload: true,
        enableEscalation: true,
        soundEnabled: true,
        showBranding: false
    };

    // Merge con configuración del usuario
    const config = {
        ...defaultConfig,
        ...(window.chatbotConfig || {})
    };

    // Crear contenedor para el widget
    const createWidgetContainer = () => {
        const container = document.createElement('div');
        container.id = 'chatbot-widget-root';
        document.body.appendChild(container);
        return container;
    };

    // Inyectar estilos CSS
    const injectStyles = () => {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = `${config.apiUrl}/widget/styles.css`;
        document.head.appendChild(link);

        // Estilos inline para posicionamiento
        const style = document.createElement('style');
        style.textContent = `
      #chatbot-widget-root {
        position: fixed;
        z-index: 9999;
      }
      
      #chatbot-widget-root.position-bottom-right {
        bottom: 0;
        right: 0;
      }
      
      #chatbot-widget-root.position-bottom-left {
        bottom: 0;
        left: 0;
      }
      
      #chatbot-widget-root.position-top-right {
        top: 0;
        right: 0;
      }
      
      #chatbot-widget-root.position-top-left {
        top: 0;
        left: 0;
      }
    `;
        document.head.appendChild(style);
    };

    // Cargar y montar el widget React
    const loadWidget = () => {
        const container = createWidgetContainer();
        container.className = `position-${config.position}`;

        // Cargar React y el widget
        const script = document.createElement('script');
        script.src = `${config.apiUrl}/widget/bundle.js`;
        script.async = true;

        script.onload = () => {
            if (window.ChatWidget) {
                window.ChatWidget.render(container, config);
                console.log('Chat widget inicializado correctamente');
            } else {
                console.error('Error: ChatWidget no encontrado en el bundle');
            }
        };

        script.onerror = () => {
            console.error('Error cargando el script del chat widget');
        };

        document.body.appendChild(script);
    };

    // API pública para interactuar con el widget
    window.chatbot = {
        open: () => {
            if (window.ChatWidget && window.ChatWidget.instance) {
                window.ChatWidget.instance.open();
            }
        },

        close: () => {
            if (window.ChatWidget && window.ChatWidget.instance) {
                window.ChatWidget.instance.close();
            }
        },

        toggle: () => {
            if (window.ChatWidget && window.ChatWidget.instance) {
                window.ChatWidget.instance.toggle();
            }
        },

        sendMessage: (message) => {
            if (window.ChatWidget && window.ChatWidget.instance) {
                window.ChatWidget.instance.sendMessage(message);
            }
        },

        setUser: (userData) => {
            if (window.ChatWidget && window.ChatWidget.instance) {
                window.ChatWidget.instance.setUser(userData);
            }
        },

        on: (event, callback) => {
            if (window.ChatWidget && window.ChatWidget.instance) {
                window.ChatWidget.instance.on(event, callback);
            }
        },

        destroy: () => {
            const container = document.getElementById('chatbot-widget-root');
            if (container) {
                container.remove();
            }
            window.__chatbot_initialized = false;
        }
    };

    // Inicializar cuando el DOM esté listo
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            injectStyles();
            loadWidget();
        });
    } else {
        injectStyles();
        loadWidget();
    }

    // Eventos globales
    window.addEventListener('message', (event) => {
        // Manejar mensajes entre frames si es necesario
        if (event.data && event.data.type === 'chatbot') {
            console.log('Mensaje del chatbot:', event.data);
        }
    });

    console.log('Chat widget embed script cargado', {
        config,
        version: '1.0.0'
    });

})();