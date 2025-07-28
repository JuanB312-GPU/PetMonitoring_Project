// Main Application
class App {
    constructor() {
        this.init();
    }

    init() {
        this.checkAuthenticationState();
        this.bindGlobalEvents();
    }

    checkAuthenticationState() {
        const token = localStorage.getItem('authToken');
        const userData = localStorage.getItem('userData');
        
        if (token && userData) {
            try {
                const user = JSON.parse(userData);
                this.showUserContent(user);
            } catch (error) {
                console.error('Error parsing user data:', error);
                this.logout();
            }
        } else {
            this.showGuestContent();
        }
    }

    showUserContent(user) {
        document.getElementById('guest-content').classList.add('hidden');
        document.getElementById('user-content').classList.remove('hidden');
        
        const welcomeMessage = document.getElementById('welcome-message');
        welcomeMessage.textContent = `Welcome back, ${user.name}!`;
        
        // Load user's pets
        this.loadUserPets();
    }

    showGuestContent() {
        document.getElementById('guest-content').classList.remove('hidden');
        document.getElementById('user-content').classList.add('hidden');
    }

    async loadUserPets() {
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/pets', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                const pets = await response.json();
                this.renderUserPets(pets);
            }
        } catch (error) {
            console.error('Error loading pets:', error);
        }
    }

    renderUserPets(pets) {
        const petsContainer = document.getElementById('pets-container');
        const addPetBtn = document.getElementById('add-pet-btn');
        
        // Clear existing pet cards (except add pet button)
        const existingCards = petsContainer.querySelectorAll('.pet-card');
        existingCards.forEach(card => card.remove());
        
        // Add pet cards
        pets.forEach(pet => {
            const petCard = window.petComponent.createPetCard(pet);
            petsContainer.insertBefore(petCard, addPetBtn);
        });
    }

    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        this.showGuestContent();
        window.navbarComponent.updateAuthState(null);
    }

    bindGlobalEvents() {
        // Handle keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // ESC key to close modals
            if (e.key === 'Escape') {
                const activeModal = document.querySelector('.modal.active');
                if (activeModal) {
                    activeModal.classList.remove('active');
                }
            }
        });

        // Handle form validation
        document.addEventListener('input', (e) => {
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT') {
                this.validateField(e.target);
            }
        });

        // Handle network errors globally
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
        });
    }

    validateField(field) {
        // Remove previous error styling
        field.classList.remove('error');
        
        // Basic validation
        if (field.hasAttribute('required') && !field.value.trim()) {
            field.classList.add('error');
            return false;
        }

        // Email validation
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                field.classList.add('error');
                return false;
            }
        }

        // Password confirmation
        if (field.name === 'confirmPassword') {
            const passwordField = document.querySelector('input[name="password"]');
            if (passwordField && field.value !== passwordField.value) {
                field.classList.add('error');
                return false;
            }
        }

        return true;
    }

    // Utility method for API calls
    async apiCall(url, options = {}) {
        const token = localStorage.getItem('authToken');
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(token && { 'Authorization': `Bearer ${token}` })
            }
        };

        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(url, finalOptions);
            
            // Handle unauthorized responses
            if (response.status === 401) {
                this.logout();
                throw new Error('Authentication required');
            }

            return response;
        } catch (error) {
            console.error('API call failed:', error);
            throw error;
        }
    }

    // Show notification (basic implementation)
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        Object.assign(notification.style, {
            position: 'fixed',
            top: '20px',
            right: '20px',
            padding: '12px 20px',
            borderRadius: '8px',
            color: 'white',
            fontWeight: '500',
            zIndex: '9999',
            opacity: '0',
            transition: 'opacity 0.3s ease'
        });

        // Set background color based on type
        const colors = {
            info: '#2563eb',
            success: '#22c55e',
            warning: '#f59e0b',
            error: '#ef4444'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Show notification
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 10);

        // Hide and remove notification
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});

// Add CSS for form validation
const style = document.createElement('style');
style.textContent = `
    .form-group input.error,
    .form-group select.error {
        border-color: var(--error-color);
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
    }
    
    .report-card {
        background: var(--surface-color);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: calc(var(--spacing-unit) * 3);
        margin-bottom: calc(var(--spacing-unit) * 3);
    }
    
    .report-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: calc(var(--spacing-unit) * 2);
    }
    
    .report-header h3 {
        margin: 0;
        font-size: 1.25rem;
        color: var(--text-primary);
    }
    
    .report-date {
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .report-body {
        margin-bottom: calc(var(--spacing-unit) * 3);
    }
    
    .report-metrics {
        margin-top: calc(var(--spacing-unit) * 2);
    }
    
    .metric-item {
        display: flex;
        justify-content: space-between;
        padding: calc(var(--spacing-unit) * 1) 0;
        border-bottom: 1px solid var(--border-color);
    }
    
    .metric-item:last-child {
        border-bottom: none;
    }
    
    .metric-label {
        font-weight: 500;
        color: var(--text-primary);
    }
    
    .metric-value {
        color: var(--text-secondary);
    }
    
    .report-actions {
        display: flex;
        gap: calc(var(--spacing-unit) * 2);
    }
    
    .report-actions .btn {
        flex: 1;
    }
    
    .report-details {
        max-height: 60vh;
        overflow-y: auto;
    }
    
    .report-section {
        margin-bottom: calc(var(--spacing-unit) * 4);
    }
    
    .report-section h3 {
        font-size: 1.25rem;
        margin-bottom: calc(var(--spacing-unit) * 2);
        color: var(--text-primary);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: calc(var(--spacing-unit) * 1);
    }
    
    @media (max-width: 768px) {
        .report-actions {
            flex-direction: column;
        }
        
        .report-header {
            flex-direction: column;
            gap: calc(var(--spacing-unit) * 1);
        }
    }
`;
document.head.appendChild(style);