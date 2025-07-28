// Authentication Component
class Auth {
    constructor() {
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        // Modal controls
        const authModal = document.getElementById('auth-modal');
        const loginBtn = document.getElementById('login-btn');
        const registerBtn = document.getElementById('register-btn');
        const closeButtons = authModal.querySelectorAll('.close');

        loginBtn.addEventListener('click', () => {
            this.showAuthModal('login');
        });

        registerBtn.addEventListener('click', () => {
            this.showAuthModal('register');
        });

        closeButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.hideAuthModal();
            });
        });

        // Close modal on outside click
        authModal.addEventListener('click', (e) => {
            if (e.target === authModal) {
                this.hideAuthModal();
            }
        });

        // Form submissions
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin(e.target);
        });

        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleRegister(e.target);
        });
    }

    showAuthModal(type) {
        const authModal = document.getElementById('auth-modal');
        const modalTitle = document.getElementById('modal-title');
        const loginForm = document.getElementById('login-form');
        const registerForm = document.getElementById('register-form');

        if (type === 'login') {
            modalTitle.textContent = 'Login';
            loginForm.classList.remove('hidden');
            registerForm.classList.add('hidden');
        } else {
            modalTitle.textContent = 'Register';
            loginForm.classList.add('hidden');
            registerForm.classList.remove('hidden');
        }

        authModal.classList.add('active');
    }

    hideAuthModal() {
        const authModal = document.getElementById('auth-modal');
        authModal.classList.remove('active');
        
        // Clear forms
        document.getElementById('login-form').reset();
        document.getElementById('register-form').reset();
        this.clearErrors();
    }

    async handleLogin(form) {
        const formData = new FormData(form);
        const loginData = {
            email: formData.get('email'),
            password: formData.get('password')
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        this.setLoading(submitBtn, true);
        this.clearErrors();

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            });

            const result = await response.json();

            if (response.ok) {
                // Store auth data
                localStorage.setItem('authToken', result.token);
                localStorage.setItem('userData', JSON.stringify(result.user));
                
                // Update UI
                window.navbarComponent.updateAuthState(result.user);
                this.hideAuthModal();
                this.showUserContent(result.user);
                
                this.showSuccess('Login successful!');
            } else {
                this.showError(result.detail || 'Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(submitBtn, false);
        }
    }

    async handleRegister(form) {
        const formData = new FormData(form);
        const registerData = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            password: formData.get('password'),
            confirmPassword: formData.get('confirmPassword')
        };

        // Validate passwords match
        if (registerData.password !== registerData.confirmPassword) {
            this.showError('Passwords do not match');
            return;
        }

        const submitBtn = form.querySelector('button[type="submit"]');
        this.setLoading(submitBtn, true);
        this.clearErrors();

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(registerData)
            });

            const result = await response.json();

            if (response.ok) {
                // Store auth data
                localStorage.setItem('authToken', result.token);
                localStorage.setItem('userData', JSON.stringify(result.user));
                // Update UI
                window.navbarComponent.updateAuthState(result.user);
                this.hideAuthModal();
                this.showUserContent(result.user, true);
                
                this.showSuccess('Registration successful!');
            } else {
                this.showError(result.detail || 'Registration failed');
            }
        } catch (error) {
            console.error('Registration error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(submitBtn, false);
        }
    }

    showUserContent(user, register = false) {
        document.getElementById('guest-content').classList.add('hidden');
        document.getElementById('user-content').classList.remove('hidden');
        
        const welcomeMessage = document.getElementById('welcome-message');
        if (register) {welcomeMessage.textContent = `Welcome new pet lover, ${user.name}!`;}
        else{welcomeMessage.textContent = `Welcome back, ${user.name}!`;}
    }

    setLoading(button, loading) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            button.disabled = false;
        }
    }

    showError(message) {
        // Remove existing error messages
        this.clearErrors();
        
        // Create error element
        const errorElement = document.createElement('div');
        errorElement.className = 'form-error';
        errorElement.textContent = message;
        
        // Insert at the top of modal body
        const modalBody = document.querySelector('#auth-modal .modal-body');
        modalBody.insertBefore(errorElement, modalBody.firstChild);
    }

    showSuccess(message) {
        // Create success notification (you could implement a toast system here)
        console.log('Success:', message);
    }

    clearErrors() {
        document.querySelectorAll('.form-error').forEach(error => {
            error.remove();
        });
    }
}

// Initialize auth component
window.authComponent = new Auth();