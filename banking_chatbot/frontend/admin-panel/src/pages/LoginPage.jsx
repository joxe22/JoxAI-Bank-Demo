import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import authService from "../services/authService";
import "../styles/pages/LoginPage.css";

const LoginPage = () => {
    const [credentials, setCredentials] = useState({ email: "", password: "" });
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setLoading(true);

        try {
            const result = await authService.login(credentials.email, credentials.password);

            if (result.success) {
                // Login exitoso - redirigir al dashboard
                navigate("/dashboard");
            } else {
                // Mostrar error
                setError(result.message || "Error al iniciar sesión");
            }
        } catch (err) {
            setError("Error de conexión. Por favor intenta de nuevo.");
            console.error("Login error:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            <div className="login-container">
                <h1>JoxAI Bank Admin</h1>

                {error && (
                    <div className="error-message">
                        {error}
                    </div>
                )}

                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={credentials.email}
                        onChange={(e) => setCredentials({...credentials, email: e.target.value})}
                        required
                        disabled={loading}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={credentials.password}
                        onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                        required
                        disabled={loading}
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? "Iniciando sesión..." : "Login"}
                    </button>
                </form>

                {/* Credentials para desarrollo */}
                <div className="dev-credentials">
                    <small>
                        <strong>Desarrollo:</strong> admin@joxai.com / admin123
                    </small>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;