// Test suite for Auth component functionality
const { describe, test, expect, beforeEach } = require('@jest/globals');

describe('Auth Component', () => {
    let auth;

    beforeEach(() => {
        // Create fresh Auth instance using the real component
        auth = new Auth();
    });

    describe('login', () => {
        test('should return success for valid admin credentials', () => {
            // Arrange
            const username = 'admin';
            const password = 'password123';

            // Act
            const result = auth.login(username, password);

            // Assert
            expect(result.success).toBe(true);
            expect(result.message).toBe('Login successful');
            expect(result.user.username).toBe('admin');
            expect(result.user.role).toBe('admin');
        });

        test('should return success for valid user credentials', () => {
            // Arrange
            const username = 'user';
            const password = 'user123';

            // Act
            const result = auth.login(username, password);

            // Assert
            expect(result.success).toBe(true);
            expect(result.message).toBe('Login successful');
            expect(result.user.username).toBe('user');
            expect(result.user.role).toBe('user');
        });

        test('should return error for invalid credentials', () => {
            // Arrange
            const username = 'invalid';
            const password = 'wrongpass';

            // Act
            const result = auth.login(username, password);

            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Invalid username or password');
        });

        test('should return error for empty username', () => {
            // Arrange
            const username = '';
            const password = 'password123';

            // Act
            const result = auth.login(username, password);

            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Username and password are required');
        });

        test('should return error for empty password', () => {
            // Arrange
            const username = 'admin';
            const password = '';

            // Act
            const result = auth.login(username, password);

            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Username and password are required');
        });

        test('should return error for missing credentials', () => {
            // Act
            const result = auth.login();

            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Username and password are required');
        });
    });

    describe('logout', () => {
        test('should logout successfully', () => {
            // Arrange
            auth.login('admin', 'password123'); // First login

            // Act
            const result = auth.logout();

            // Assert
            expect(result.success).toBe(true);
            expect(result.message).toBe('Logout successful');
            expect(auth.isAuthenticated).toBe(false);
            expect(auth.currentUser).toBe(null);
        });
    });

    describe('isValidEmail', () => {
        test('should return true for valid email', () => {
            // Act & Assert
            expect(auth.isValidEmail('test@example.com')).toBe(true);
            expect(auth.isValidEmail('user.name@domain.co.uk')).toBe(true);
        });

        test('should return false for invalid email', () => {
            // Act & Assert
            expect(auth.isValidEmail('invalid-email')).toBe(false);
            expect(auth.isValidEmail('test@')).toBe(false);
            expect(auth.isValidEmail('@domain.com')).toBe(false);
        });
    });

    describe('showAuthModal', () => {
        test('should show login modal', () => {
            // Act
            const result = auth.showAuthModal('login');

            // Assert
            expect(result.modalVisible).toBe(true);
            expect(result.mode).toBe('login');
            expect(result.className).toBe('active');
        });

        test('should show register modal', () => {
            // Act
            const result = auth.showAuthModal('register');

            // Assert
            expect(result.modalVisible).toBe(true);
            expect(result.mode).toBe('register');
            expect(result.className).toBe('active');
        });
    });

    describe('hideAuthModal', () => {
        test('should hide modal', () => {
            // Act
            const result = auth.hideAuthModal();

            // Assert
            expect(result.modalVisible).toBe(false);
            expect(result.formsReset).toBe(true);
            expect(result.className).toBe('');
        });
    });
});
