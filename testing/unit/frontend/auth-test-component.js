// Auth component simplified for testing (without DOM dependencies)
class Auth {
    constructor() {
        this.isAuthenticated = false;
        this.currentUser = null;
        this.users = []; // Mock user database
    }

    showAuthModal(mode = 'login') {
        return {
            modalVisible: true,
            mode: mode,
            className: 'active'
        };
    }

    hideAuthModal() {
        return {
            modalVisible: false,
            formsReset: true,
            className: ''
        };
    }

    async handleLogin(email, password) {
        if (!email || !password) {
            throw new Error('Email and password are required');
        }
        
        if (email === 'test@example.com' && password === 'Password123!') {
            this.isAuthenticated = true;
            this.currentUser = { email, id: 1 };
            return {
                success: true,
                user: this.currentUser,
                token: 'mock-jwt-token'
            };
        } else {
            throw new Error('Invalid credentials');
        }
    }

    async handleRegister(email, password, confirmPassword, name) {
        if (!email || !password || !confirmPassword || !name) {
            throw new Error('All fields are required');
        }

        if (password !== confirmPassword) {
            throw new Error('Passwords do not match');
        }

        if (password.length < 8) {
            throw new Error('Password must be at least 8 characters long');
        }

        if (!this.isValidEmail(email)) {
            throw new Error('Please enter a valid email address');
        }

        // Check if user already exists
        if (this.users.find(u => u.email === email)) {
            throw new Error('Email already registered');
        }

        // Create new user
        const newUser = {
            id: this.users.length + 1,
            email: email,
            name: name,
            created_at: new Date().toISOString()
        };

        this.users.push(newUser);
        this.isAuthenticated = true;
        this.currentUser = newUser;

        return {
            success: true,
            user: newUser,
            token: 'mock-jwt-token'
        };
    }

    // Main login method (used in tests)
    login(username, password) {
        // Validation
        if (!username || !password) {
            return {
                success: false,
                message: 'Username and password are required'
            };
        }

        if (username.trim() === '' || password.trim() === '') {
            return {
                success: false,
                message: 'Username and password cannot be empty'
            };
        }

        // Mock authentication
        if (username === 'admin' && password === 'password123') {
            this.currentUser = {
                id: 1,
                username: 'admin',
                email: 'admin@petmonitor.com',
                role: 'admin'
            };
            this.isAuthenticated = true;
            
            return {
                success: true,
                message: 'Login successful',
                user: this.currentUser
            };
        } else if (username === 'user' && password === 'user123') {
            this.currentUser = {
                id: 2,
                username: 'user',
                email: 'user@petmonitor.com',
                role: 'user'
            };
            this.isAuthenticated = true;
            
            return {
                success: true,
                message: 'Login successful',
                user: this.currentUser
            };
        }

        return {
            success: false,
            message: 'Invalid username or password'
        };
    }

    logout() {
        this.currentUser = null;
        this.isAuthenticated = false;
        
        return {
            success: true,
            message: 'Logout successful'
        };
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    validatePassword(password) {
        const errors = [];
        
        if (password.length < 8) {
            errors.push('Password must be at least 8 characters long');
        }
        
        if (!/[A-Z]/.test(password)) {
            errors.push('Password must contain at least one uppercase letter');
        }
        
        if (!/[a-z]/.test(password)) {
            errors.push('Password must contain at least one lowercase letter');
        }
        
        if (!/[0-9]/.test(password)) {
            errors.push('Password must contain at least one number');
        }
        
        if (!/[!@#$%^&*]/.test(password)) {
            errors.push('Password must contain at least one special character (!@#$%^&*)');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    updateProfile(userId, profileData) {
        if (!this.isAuthenticated || !this.currentUser) {
            return {
                success: false,
                message: 'User not authenticated'
            };
        }
        
        if (this.currentUser.id !== userId) {
            return {
                success: false,
                message: 'Not authorized to update this profile'
            };
        }
        
        // Update current user data
        this.currentUser = { ...this.currentUser, ...profileData };
        
        return {
            success: true,
            message: 'Profile updated successfully',
            user: this.currentUser
        };
    }

    changePassword(currentPassword, newPassword) {
        if (!this.isAuthenticated) {
            return {
                success: false,
                message: 'User not authenticated'
            };
        }
        
        // Simulate password verification
        if (currentPassword !== 'currentPass123') {
            return {
                success: false,
                message: 'Current password is incorrect'
            };
        }
        
        const validation = this.validatePassword(newPassword);
        if (!validation.isValid) {
            return {
                success: false,
                message: validation.errors.join(', ')
            };
        }
        
        return {
            success: true,
            message: 'Password changed successfully'
        };
    }

    isLoggedIn() {
        return this.isAuthenticated && this.currentUser !== null;
    }

    getCurrentUser() {
        return this.currentUser;
    }

    // Additional validation methods
    validateLoginData(email, password) {
        const errors = [];
        
        if (!email) {
            errors.push('Email is required');
        } else if (!this.isValidEmail(email)) {
            errors.push('Please enter a valid email address');
        }
        
        if (!password) {
            errors.push('Password is required');
        } else if (password.length < 6) {
            errors.push('Password must be at least 6 characters long');
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    validateRegistrationData(name, email, password, confirmPassword) {
        const errors = [];
        
        if (!name || name.trim().length < 2) {
            errors.push('Name must be at least 2 characters long');
        }
        
        const emailValidation = this.validateLoginData(email, password);
        errors.push(...emailValidation.errors);
        
        if (password !== confirmPassword) {
            errors.push('Passwords do not match');
        }
        
        const passwordValidation = this.validatePassword(password);
        if (!passwordValidation.isValid) {
            errors.push(...passwordValidation.errors);
        }
        
        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }
}

module.exports = Auth;
