// Test suite for Pet component functionality
const { describe, test, expect, beforeEach } = require('@jest/globals');

describe('Pet Component', () => {
    let pet;

    beforeEach(() => {
        // Create fresh Pet instance using the real component
        pet = new Pet();
    });

    describe('calculateAge', () => {
        test('should calculate age in days for very young pets', () => {
            // Arrange
            const recentDate = new Date();
            recentDate.setDate(recentDate.getDate() - 5);
            const birthdate = recentDate.toISOString().split('T')[0];

            // Act
            const result = pet.calculateAge(birthdate);

            // Assert
            expect(result).toMatch(/\d+ days/); // Accept any number of days
            expect(parseInt(result)).toBeGreaterThanOrEqual(4);
            expect(parseInt(result)).toBeLessThanOrEqual(7);
        });

        test('should calculate age in months for pets under 1 year', () => {
            // Arrange
            const recentDate = new Date();
            recentDate.setMonth(recentDate.getMonth() - 6);
            const birthdate = recentDate.toISOString().split('T')[0];

            // Act
            const result = pet.calculateAge(birthdate);

            // Assert
            expect(result).toBe('6 months');
        });

        test('should calculate age in years for older pets', () => {
            // Arrange
            const recentDate = new Date();
            recentDate.setFullYear(recentDate.getFullYear() - 3);
            const birthdate = recentDate.toISOString().split('T')[0];

            // Act
            const result = pet.calculateAge(birthdate);

            // Assert
            expect(result).toBe('3 years');
        });
    });

    describe('calculateAgeInYears', () => {
        test('should calculate age in years correctly', () => {
            // Arrange
            const birthdate = '2020-01-01';

            // Act
            const result = pet.calculateAgeInYears(birthdate);

            // Assert
            expect(result).toBe(4); // Assuming current date is 2024
        });
    });

    describe('validatePetData', () => {
        test('should return valid for complete pet data', () => {
            // Arrange
            const petData = {
                name: 'Buddy',
                species: 'Dog',
                birthdate: '2020-01-01',
                weight: 25,
                height: 60
            };

            // Act
            const result = pet.validatePetData(petData);

            // Assert
            expect(result.isValid).toBe(true);
            expect(Object.keys(result.errors)).toHaveLength(0);
        });

        test('should return invalid for missing name', () => {
            // Arrange
            const petData = {
                species: 'Dog',
                birthdate: '2020-01-01'
            };

            // Act
            const result = pet.validatePetData(petData);

            // Assert
            expect(result.isValid).toBe(false);
            expect(result.errors.name).toBe('Pet name is required');
        });

        test('should return invalid for future birthdate', () => {
            // Arrange
            const futureDate = new Date();
            futureDate.setFullYear(futureDate.getFullYear() + 1);
            const petData = {
                name: 'Buddy',
                species: 'Dog',
                birthdate: futureDate.toISOString().split('T')[0]
            };

            // Act
            const result = pet.validatePetData(petData);

            // Assert
            expect(result.isValid).toBe(false);
            expect(result.errors.birthdate).toBe('Birthdate cannot be in the future');
        });
    });

    describe('formatPetForDisplay', () => {
        test('should format pet data for display', () => {
            // Arrange
            const petData = {
                id: 1,
                name: 'Buddy',
                species: 'Dog',
                breed: 'Golden Retriever',
                birthdate: '2020-01-01',
                weight: 25,
                is_active: true
            };

            // Act
            const result = pet.formatPetForDisplay(petData);

            // Assert
            expect(result.id).toBe(1);
            expect(result.name).toBe('Buddy');
            expect(result.species).toBe('Dog');
            expect(result.breed).toBe('Golden Retriever');
            expect(result.weight).toBe('25 kg');
            expect(result.status).toBe('Active');
        });

        test('should return null for null pet', () => {
            // Act
            const result = pet.formatPetForDisplay(null);

            // Assert
            expect(result).toBe(null);
        });
    });

    describe('filterPetsBySpecies', () => {
        test('should filter pets by species', () => {
            // Arrange
            const pets = [
                { name: 'Buddy', species: 'Dog' },
                { name: 'Fluffy', species: 'Cat' },
                { name: 'Rex', species: 'Dog' }
            ];

            // Act
            const result = pet.filterPetsBySpecies(pets, 'Dog');

            // Assert
            expect(result).toHaveLength(2);
            expect(result[0].name).toBe('Buddy');
            expect(result[1].name).toBe('Rex');
        });

        test('should return all pets when no species filter', () => {
            // Arrange
            const pets = [
                { name: 'Buddy', species: 'Dog' },
                { name: 'Fluffy', species: 'Cat' }
            ];

            // Act
            const result = pet.filterPetsBySpecies(pets, null);

            // Assert
            expect(result).toHaveLength(2);
        });
    });

    describe('calculateBMI', () => {
        test('should calculate BMI correctly', () => {
            // Arrange
            const weight = 25; // kg
            const height = 60; // cm

            // Act
            const result = pet.calculateBMI(weight, height);

            // Assert
            expect(result).toBe(69.4); // 25 / (0.6 * 0.6) = 69.44
        });

        test('should return null for invalid inputs', () => {
            // Act
            const result = pet.calculateBMI(0, 60);

            // Assert
            expect(result).toBe(null);
        });
    });

    describe('addPet', () => {
        test('should add valid pet successfully', () => {
            // Arrange
            const petData = {
                name: 'Buddy',
                species: 'Dog',
                birthdate: '2020-01-01',
                weight: 25
            };

            // Act
            const result = pet.addPet(petData);

            // Assert
            expect(result.success).toBe(true);
            expect(result.pet.name).toBe('Buddy');
            expect(result.pet.id).toBe(1);
        });

        test('should reject invalid pet data', () => {
            // Arrange
            const petData = {
                species: 'Dog' // missing name
            };

            // Act
            const result = pet.addPet(petData);

            // Assert
            expect(result.success).toBe(false);
            expect(result.errors.name).toBe('Pet name is required');
        });
    });
});
