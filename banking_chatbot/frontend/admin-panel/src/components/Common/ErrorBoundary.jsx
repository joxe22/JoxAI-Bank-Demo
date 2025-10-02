// frontend/admin-panel/src/components/Common/ErrorBoundary.jsx
import React, { Component } from 'react';
import '../../styles/components/ErrorBoundary.css';

class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null
        };
    }

    static getDerivedStateFromError(error) {
        return { hasError: true };
    }

    componentDidCatch(error, errorInfo) {
        console.error('Error capturado por ErrorBoundary:', error, errorInfo);

        this.setState({
            error,
            errorInfo
        });

        // Aquí podrías enviar el error a un servicio de logging
        // logErrorToService(error, errorInfo);
    }

    handleReload = () => {
        window.location.reload();
    };

    handleGoHome = () => {
        window.location.href = '/';
    };

    render() {
        if (this.state.hasError) {
            return (
                <div className="error-boundary">
                    <div className="error-container">
                        <div className="error-icon">⚠️</div>
                        <h1 className="error-title">¡Oops! Algo salió mal</h1>
                        <p className="error-message">
                            Ha ocurrido un error inesperado. Nuestro equipo ha sido notificado.
                        </p>

                        {process.env.NODE_ENV === 'development' && this.state.error && (
                            <details className="error-details">
                                <summary>Detalles del error (solo en desarrollo)</summary>
                                <pre className="error-stack">
                  {this.state.error.toString()}
                                    {this.state.errorInfo && this.state.errorInfo.componentStack}
                </pre>
                            </details>
                        )}

                        <div className="error-actions">
                            <button
                                className="btn btn-primary"
                                onClick={this.handleReload}
                            >
                                Recargar Página
                            </button>
                            <button
                                className="btn btn-secondary"
                                onClick={this.handleGoHome}
                            >
                                Ir al Inicio
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;