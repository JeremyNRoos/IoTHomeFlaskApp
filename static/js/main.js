/* ============================================
   IoT Home Security System - Main JavaScript
   Utility functions and global event handlers
   ============================================ */

// Global configuration
const CONFIG = {
    updateInterval: 5000, // 5 seconds
    chartColors: {
        temperature: {
            border: 'rgb(255, 99, 132)',
            background: 'rgba(255, 99, 132, 0.1)'
        },
        humidity: {
            border: 'rgb(54, 162, 235)',
            background: 'rgba(54, 162, 235, 0.1)'
        }
    }
};

// Utility Functions
const Utils = {
    /**
     * Format a timestamp to a readable date/time string
     */
    formatTimestamp: function(timestamp) {
        const date = new Date(timestamp);
        return date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    /**
     * Format a date for display
     */
    formatDate: function(date) {
        const d = new Date(date);
        return d.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    /**
     * Show a toast notification
     */
    showNotification: function(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 90px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-lg);
            z-index: 9999;
            animation: slideIn 0.3s ease;
        `;

        // Set color based on type
        if (type === 'success') {
            notification.style.borderColor = 'var(--success-color)';
        } else if (type === 'error') {
            notification.style.borderColor = 'var(--danger-color)';
        } else if (type === 'warning') {
            notification.style.borderColor = 'var(--warning-color)';
        }

        document.body.appendChild(notification);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    },

    /**
     * Debounce function to limit API calls
     */
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Check if API is reachable
     */
    checkConnection: async function() {
        try {
            const response = await fetch('/api/system-status', { timeout: 5000 });
            return response.ok;
        } catch (error) {
            return false;
        }
    }
};

// API Helper Functions
const API = {
    /**
     * Generic fetch wrapper with error handling
     */
    fetch: async function(endpoint, options = {}) {
        try {
            const response = await fetch(endpoint, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    },

    /**
     * Get live sensor data
     */
    getLiveData: async function() {
        return await this.fetch('/api/live-data');
    },

    /**
     * Get historical data for a sensor
     */
    getHistoricalData: async function(sensor, date) {
        return await this.fetch(`/api/historical-data?sensor=${sensor}&date=${date}`);
    },

    /**
     * Control a device
     */
    controlDevice: async function(device, value) {
        return await this.fetch(`/api/control/${device}`, {
            method: 'POST',
            body: JSON.stringify({ value })
        });
    },

    /**
     * Get system status
     */
    getSystemStatus: async function() {
        return await this.fetch('/api/system-status');
    },

    /**
     * Get intrusion events
     */
    getIntrusions: async function(date) {
        return await this.fetch(`/api/intrusions?date=${date}`);
    }
};

// Animation definitions
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .loading {
        animation: spin 1s linear infinite;
    }

    .fade-in {
        animation: fadeIn 0.5s ease;
    }
`;
document.head.appendChild(style);

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('IoT Home Security System initialized');

    // Check connection status
    Utils.checkConnection().then(isConnected => {
        if (!isConnected) {
            Utils.showNotification('Warning: Unable to connect to backend', 'warning');
        }
    });

    // Add smooth scroll behavior to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to all buttons
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('no-loading')) {
                this.classList.add('loading');
                setTimeout(() => {
                    this.classList.remove('loading');
                }, 2000);
            }
        });
    });
});

// Export utilities for use in other scripts
window.Utils = Utils;
window.API = API;
window.CONFIG = CONFIG;

// Log when script is loaded
console.log('main.js loaded successfully');