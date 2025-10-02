// frontend/admin-panel/src/components/Common/Modal.jsx
import React, { useEffect } from 'react';
import '../../styles/components/Modal.css';

const Modal = ({
                   isOpen,
                   onClose,
                   title,
                   children,
                   footer,
                   size = 'medium',
                   closeOnBackdrop = true
               }) => {
    useEffect(() => {
        if (isOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }

        return () => {
            document.body.style.overflow = 'unset';
        };
    }, [isOpen]);

    useEffect(() => {
        const handleEscape = (e) => {
            if (e.key === 'Escape' && isOpen) {
                onClose();
            }
        };

        document.addEventListener('keydown', handleEscape);
        return () => document.removeEventListener('keydown', handleEscape);
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    const sizeClasses = {
        small: 'modal-small',
        medium: 'modal-medium',
        large: 'modal-large',
        full: 'modal-full'
    };

    const handleBackdropClick = (e) => {
        if (e.target === e.currentTarget && closeOnBackdrop) {
            onClose();
        }
    };

    return (
        <div className="modal-backdrop" onClick={handleBackdropClick}>
            <div className={`modal-container ${sizeClasses[size]}`}>
                <div className="modal-header">
                    <h2 className="modal-title">{title}</h2>
                    <button
                        className="modal-close-btn"
                        onClick={onClose}
                        aria-label="Cerrar modal"
                    >
                        ✕
                    </button>
                </div>

                <div className="modal-body">
                    {children}
                </div>

                {footer && (
                    <div className="modal-footer">
                        {footer}
                    </div>
                )}
            </div>
        </div>
    );
};

export default Modal;