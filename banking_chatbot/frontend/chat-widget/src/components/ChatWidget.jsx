import React, { useState, useEffect, useRef } from 'react';
import {
    MessageCircle,
    X,
    Send,
    Bot,
    User,
    TrendingUp,
    TrendingDown,
    Clock,
    Shield,
    ChevronRight,
    Minimize2,
    Maximize2
} from 'lucide-react';

// Hook personalizado para gestión del chat
const useChatWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [isMinimized, setIsMinimized] = useState(false);
    const [messages, setMessages] = useState([]);
    const [inputMessage, setInputMessage] = useState('');
    const [isTyping, setIsTyping] = useState(false);
    const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);

    // Métricas simuladas (en producción vendrían del API)
    const [metrics] = useState({
        responseTime: '-62%',
        nps: '+18',
        availability: '24/7',
        satisfaction: '85%'
    });

    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Simular respuesta del bot
    const simulateBotResponse = async (userMessage) => {
        setIsTyping(true);

        // Simular delay de procesamiento
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Respuestas simuladas basadas en keywords
        let botResponse = "¡Hola! Soy tu asistente bancario virtual. ¿En qué puedo ayudarte hoy?";

        const message = userMessage.toLowerCase();

        if (message.includes('saldo')) {
            botResponse = "Para consultar tu saldo, necesito verificar tu identidad por seguridad. Tu saldo actual es de $4,520.34. ¿Hay algo más en lo que pueda ayudarte?";
        } else if (message.includes('transferir') || message.includes('transferencia')) {
            botResponse = "Las transferencias se pueden realizar de manera segura a través de nuestra app móvil o banca en línea. ¿Te gustaría que te explique el proceso paso a paso?";
        } else if (message.includes('tarjeta')) {
            botResponse = "Ofrecemos tarjetas de crédito y débito con diferentes beneficios. ¿Buscas información sobre una tarjeta específica o quieres conocer nuestras opciones disponibles?";
        } else if (message.includes('préstamo') || message.includes('prestamo')) {
            botResponse = "Tenemos diferentes tipos de préstamos: personales, hipotecarios, y para vehículos. Las tasas varían según el tipo de préstamo y tu perfil crediticio.";
        } else if (message.includes('horario')) {
            botResponse = "Nuestros horarios de atención son: Lunes a Viernes de 8:00 AM a 6:00 PM, Sábados de 9:00 AM a 2:00 PM. La banca en línea está disponible 24/7.";
        }

        setIsTyping(false);

        const botMessage = {
            id: Date.now(),
            text: botResponse,
            sender: 'bot',
            timestamp: new Date(),
            confidence: 'high'
        };

        setMessages(prev => [...prev, botMessage]);
    };

    const sendMessage = async () => {
        if (!inputMessage.trim()) return;

        const userMessage = {
            id: Date.now(),
            text: inputMessage,
            sender: 'user',
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInputMessage('');

        // Simular respuesta del bot
        await simulateBotResponse(inputMessage);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    return {
        isOpen,
        setIsOpen,
        isMinimized,
        setIsMinimized,
        messages,
        inputMessage,
        setInputMessage,
        isTyping,
        metrics,
        sendMessage,
        handleKeyPress,
        sessionId
    };
};

// Componente de métricas
const MetricsCard = ({ metrics }) => (
    <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg p-3 text-white">
            <div className="flex items-center justify-between">
                <TrendingDown className="w-4 h-4" />
                <span className="text-xs opacity-75">Tiempo</span>
            </div>
            <div className="text-lg font-bold">{metrics.responseTime}</div>
        </div>

        <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg p-3 text-white">
            <div className="flex items-center justify-between">
                <TrendingUp className="w-4 h-4" />
                <span className="text-xs opacity-75">NPS</span>
            </div>
            <div className="text-lg font-bold">{metrics.nps}</div>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg p-3 text-white">
            <div className="flex items-center justify-between">
                <Clock className="w-4 h-4" />
                <span className="text-xs opacity-75">Disponible</span>
            </div>
            <div className="text-lg font-bold">{metrics.availability}</div>
        </div>

        <div className="bg-gradient-to-r from-orange-500 to-red-500 rounded-lg p-3 text-white">
            <div className="flex items-center justify-between">
                <Shield className="w-4 h-4" />
                <span className="text-xs opacity-75">Satisfacción</span>
            </div>
            <div className="text-lg font-bold">{metrics.satisfaction}</div>
        </div>
    </div>
);

// Componente de mensaje individual
const Message = ({ message, isTyping = false }) => {
    const isBot = message?.sender === 'bot' || isTyping;

    if (isTyping) {
        return (
            <div className="flex items-start space-x-3 mb-4">
                <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                        <Bot className="w-4 h-4 text-white" />
                    </div>
                </div>
                <div className="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 max-w-xs">
                    <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className={`flex items-start space-x-3 mb-4 ${!isBot ? 'flex-row-reverse space-x-reverse' : ''}`}>
            <div className="flex-shrink-0">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    isBot
                        ? 'bg-gradient-to-r from-blue-500 to-purple-500'
                        : 'bg-gradient-to-r from-gray-500 to-gray-600'
                }`}>
                    {isBot ? (
                        <Bot className="w-4 h-4 text-white" />
                    ) : (
                        <User className="w-4 h-4 text-white" />
                    )}
                </div>
            </div>
            <div className={`rounded-2xl px-4 py-3 max-w-xs ${
                isBot
                    ? 'bg-gray-100 rounded-tl-sm'
                    : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-tr-sm'
            }`}>
                <p className="text-sm leading-relaxed">{message.text}</p>
                {isBot && message.confidence && (
                    <div className="mt-2 pt-2 border-t border-gray-200">
            <span className={`text-xs px-2 py-1 rounded-full ${
                message.confidence === 'high' ? 'bg-green-100 text-green-700' :
                    message.confidence === 'medium' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-red-100 text-red-700'
            }`}>
              {message.confidence === 'high' ? 'Alta confianza' :
                  message.confidence === 'medium' ? 'Confianza media' :
                      'Baja confianza'}
            </span>
                    </div>
                )}
            </div>
        </div>
    );
};

// Componente principal del ChatWidget
const ChatWidget = () => {
    const {
        isOpen,
        setIsOpen,
        isMinimized,
        setIsMinimized,
        messages,
        inputMessage,
        setInputMessage,
        isTyping,
        metrics,
        sendMessage,
        handleKeyPress
    } = useChatWidget();

    // Mensaje inicial del bot
    useEffect(() => {
        if (messages.length === 0) {
            const welcomeMessage = {
                id: 1,
                text: "¡Hola! 👋 Soy tu asistente bancario virtual. Puedo ayudarte con consultas sobre saldos, transferencias, productos bancarios y más. ¿En qué puedo asistirte hoy?",
                sender: 'bot',
                timestamp: new Date(),
                confidence: 'high'
            };
            setMessages([welcomeMessage]);
        }
    }, []);

    return (
        <div className="fixed bottom-4 right-4 z-50">
            {/* Botón flotante para abrir el chat */}
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 flex items-center justify-center animate-bounce-subtle"
                >
                    <MessageCircle className="w-6 h-6 text-white" />
                    <div className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
                        <span className="text-xs text-white font-bold">!</span>
                    </div>
                </button>
            )}

            {/* Widget del chat */}
            {isOpen && (
                <div className={`bg-white rounded-2xl shadow-2xl border border-gray-200 transition-all duration-300 ${
                    isMinimized ? 'w-80 h-16' : 'w-96 h-[600px]'
                } animate-slide-in`}>

                    {/* Header del chat */}
                    <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-t-2xl">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                                <div className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
                                    <Bot className="w-4 h-4 text-white" />
                                </div>
                                <div>
                                    <h3 className="text-white font-semibold text-sm">JovAI Bank Assistant</h3>
                                    <p className="text-white text-xs opacity-75">En línea • Responde en segundos</p>
                                </div>
                            </div>

                            <div className="flex items-center space-x-2">
                                <button
                                    onClick={() => setIsMinimized(!isMinimized)}
                                    className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center hover:bg-opacity-30 transition-colors"
                                >
                                    {isMinimized ? (
                                        <Maximize2 className="w-4 h-4 text-white" />
                                    ) : (
                                        <Minimize2 className="w-4 h-4 text-white" />
                                    )}
                                </button>

                                <button
                                    onClick={() => setIsOpen(false)}
                                    className="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center hover:bg-opacity-30 transition-colors"
                                >
                                    <X className="w-4 h-4 text-white" />
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Contenido del chat */}
                    {!isMinimized && (
                        <>
                            {/* Métricas */}
                            <div className="p-4 border-b border-gray-100">
                                <MetricsCard metrics={metrics} />
                            </div>

                            {/* Área de mensajes */}
                            <div className="flex-1 p-4 overflow-y-auto custom-scrollbar h-96">
                                {messages.map((message) => (
                                    <Message key={message.id} message={message} />
                                ))}
                                {isTyping && <Message isTyping={true} />}
                            </div>

                            {/* Input para escribir mensajes */}
                            <div className="p-4 border-t border-gray-100">
                                <div className="flex items-end space-x-2">
                                    <div className="flex-1 relative">
                    <textarea
                        value={inputMessage}
                        onChange={(e) => setInputMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Escribe tu pregunta aquí..."
                        className="w-full px-4 py-3 border border-gray-200 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm max-h-20"
                        rows="1"
                    />
                                    </div>
                                    <button
                                        onClick={sendMessage}
                                        disabled={!inputMessage.trim() || isTyping}
                                        className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-md transition-all duration-200"
                                    >
                                        <Send className="w-4 h-4 text-white" />
                                    </button>
                                </div>

                                {/* Sugerencias rápidas */}
                                <div className="flex space-x-2 mt-3">
                                    {['Consultar saldo', 'Transferir dinero', 'Información de tarjetas'].map((suggestion, index) => (
                                        <button
                                            key={index}
                                            onClick={() => setInputMessage(suggestion)}
                                            className="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded-full text-xs text-gray-600 transition-colors"
                                        >
                                            {suggestion}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </>
                    )}
                </div>
            )}
        </div>
    );
};

export default ChatWidget;