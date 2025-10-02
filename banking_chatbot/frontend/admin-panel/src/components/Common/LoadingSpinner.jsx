// frontend/admin-panel/src/components/Common/LoadingSpinner.jsx
import React from 'react';
import '../../styles/components/LoadingSpinner.css';

const LoadingSpinner = ({ size = 'medium', message = '', fullScreen = false }) => {
    const sizeClasses = {
        small: 'spinner-small',
        medium: 'spinner-medium',
        large: 'spinner-large'
    };

    const spinner = (
        <div className={`loading-spinner ${sizeClasses[size]}`}>
            <div className="spinner-circle">
                <div className="spinner-inner"></div>
            </div>
            {message && <p className="spinner-message">{message}</p>}
        </div>
    );

    if (fullScreen) {
        return (
            <div className="loading-overlay">
                {spinner}
            </div>
        );
    }

    return spinner;
};

export default LoadingSpinner;