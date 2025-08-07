// Test suite for Dashboard component functionality
const { describe, test, expect, beforeEach, afterEach } = require('@jest/globals');

describe('Dashboard Component', () => {
    let dashboard;
    let mockDocument;
    
    beforeEach(() => {
        // Setup DOM mock
        mockDocument = {
            getElementById: jest.fn().mockReturnValue({
                textContent: '',
                innerHTML: '',
                className: '',
                style: {},
                classList: {
                    add: jest.fn(),
                    remove: jest.fn()
                }
            }),
            querySelectorAll: jest.fn()
        };
        
        global.document = mockDocument;
        global.window = {
            navbarComponent: {
                navigateTo: jest.fn()
            }
        };
        
        // Use the real Dashboard class loaded by setup.js
        dashboard = new Dashboard();
    });
    
    afterEach(() => {
        jest.clearAllMocks();
    });
    
    describe('calculateBMI', () => {
        test('should calculate BMI correctly for dogs', () => {
            // Arrange
            const pet = {
                species: 'dog',
                weight: 25,
                height: 50 // cm
            };
            
            // Act
            const result = dashboard.calculateBMI(pet);
            
            // Assert
            expect(result.value).toBe('100.0'); // 25 / (0.5^2) = 100
            expect(result.status).toBe('Obese');
            expect(result.level).toBe('danger');
        });
        
        test('should calculate BMI correctly for cats', () => {
            // Arrange
            const pet = {
                species: 'cat',
                weight: 5,
                height: 25 // cm
            };
            
            // Act
            const result = dashboard.calculateBMI(pet);
            
            // Assert
            expect(result.value).toBe('80.0'); // 5 / (0.25^2) = 80
            expect(result.status).toBe('Obese');
            expect(result.level).toBe('danger');
        });
    });

    describe('calculateBCS', () => {
        test('should calculate BCS for underweight dog', () => {
            // Arrange
            const pet = {
                species: 'dog',
                weight: 10,
                height: 100 // cm
            };
            
            // Act
            const result = dashboard.calculateBCS(pet);
            
            // Assert
            expect(result.value).toBe('3/9');
            expect(result.status).toBe('Underweight');
            expect(result.level).toBe('warning');
        });
    });

    describe('calculateMER', () => {
        test('should calculate MER for adult dog', () => {
            // Arrange
            const pet = {
                weight: 25,
                birthdate: '2020-01-01'
            };
            
            // Act
            const result = dashboard.calculateMER(pet);
            
            // Assert
            expect(result.value).toBe(1312); // RER = (30 * 25 + 70) = 820, MER = 820 * 1.6 = 1312
            expect(result.status).toBe('Daily requirement');
            expect(result.level).toBe('info');
        });
    });

    describe('calculateAge', () => {
        test('should calculate age in years and months correctly', () => {
            // Arrange
            const birthdate = '2020-06-15';
            
            // Mock current date to 2024-01-15
            const mockDate = new Date('2024-01-15');
            jest.spyOn(Date, 'now').mockReturnValue(mockDate.getTime());
            
            // Act
            const result = dashboard.calculateAge(birthdate);
            
            // Assert
            expect(result).toBe('3y 7m');
        });
        
        test('should calculate age for very young pet', () => {
            // Arrange
            const birthdate = '2024-01-01';
            
            // Mock current date to 2024-01-15
            const mockDate = new Date('2024-01-15');
            jest.spyOn(Date, 'now').mockReturnValue(mockDate.getTime());
            
            // Act
            const result = dashboard.calculateAge(birthdate);
            
            // Assert
            expect(result).toBe('14 days');
        });
    });
});
