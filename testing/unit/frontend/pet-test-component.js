// Pet component simplified for testing (without DOM dependencies)
class Pet {
    constructor() {
        this.currentPet = null;
        this.pets = [];
        this.currentPetForActivity = null;
    }

    calculateAge(birthdate) {
        const birth = new Date(birthdate);
        const now = new Date();
        const diffTime = Math.abs(now - birth);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays < 30) {
            return `${diffDays} days`;
        } else if (diffDays < 365) {
            const months = Math.floor(diffDays / 30);
            return `${months} month${months > 1 ? 's' : ''}`;
        } else {
            const years = Math.floor(diffDays / 365);
            const remainingMonths = Math.floor((diffDays % 365) / 30);
            if (remainingMonths > 0) {
                return `${years}y ${remainingMonths}m`;
            }
            return `${years} year${years > 1 ? 's' : ''}`;
        }
    }

    calculateAgeInYears(birthdate) {
        const today = new Date();
        const birth = new Date(birthdate);
        const diffTime = Math.abs(today - birth);
        return Math.floor(diffTime / (1000 * 60 * 60 * 24 * 365));
    }

    validatePetData(petData) {
        const errors = {};
        
        if (!petData.name || petData.name.trim() === '') {
            errors.name = 'Pet name is required';
        }
        
        if (!petData.species || petData.species.trim() === '') {
            errors.species = 'Species is required';
        }
        
        if (!petData.birthdate || petData.birthdate.trim() === '') {
            errors.birthdate = 'Birthdate is required';
        } else {
            const birthDate = new Date(petData.birthdate);
            const today = new Date();
            if (birthDate > today) {
                errors.birthdate = 'Birthdate cannot be in the future';
            }
        }
        
        if (petData.weight && (isNaN(petData.weight) || petData.weight <= 0)) {
            errors.weight = 'Weight must be a positive number';
        }
        
        if (petData.height && (isNaN(petData.height) || petData.height <= 0)) {
            errors.height = 'Height must be a positive number';
        }
        
        return {
            isValid: Object.keys(errors).length === 0,
            errors: errors
        };
    }

    formatPetForDisplay(pet) {
        if (!pet) return null;
        
        return {
            id: pet.id,
            name: pet.name,
            species: pet.species,
            breed: pet.breed || 'Unknown',
            age: this.calculateAge(pet.birthdate),
            weight: pet.weight ? `${pet.weight} kg` : 'Not specified',
            status: pet.is_active ? 'Active' : 'Inactive'
        };
    }

    filterPetsBySpecies(pets, species) {
        if (!pets || !Array.isArray(pets)) return [];
        if (!species) return pets;
        
        return pets.filter(pet => 
            pet.species && pet.species.toLowerCase() === species.toLowerCase()
        );
    }

    searchPets(pets, searchTerm) {
        if (!pets || !Array.isArray(pets)) return [];
        if (!searchTerm || searchTerm.trim() === '') return pets;
        
        const term = searchTerm.toLowerCase().trim();
        return pets.filter(pet => 
            (pet.name && pet.name.toLowerCase().includes(term)) ||
            (pet.species && pet.species.toLowerCase().includes(term)) ||
            (pet.breed && pet.breed.toLowerCase().includes(term))
        );
    }

    sortPets(pets, sortBy = 'name', order = 'asc') {
        if (!pets || !Array.isArray(pets)) return [];
        
        return [...pets].sort((a, b) => {
            let valueA, valueB;
            
            switch (sortBy) {
                case 'name':
                    valueA = a.name || '';
                    valueB = b.name || '';
                    break;
                case 'age':
                    valueA = this.calculateAgeInYears(a.birthdate);
                    valueB = this.calculateAgeInYears(b.birthdate);
                    break;
                case 'species':
                    valueA = a.species || '';
                    valueB = b.species || '';
                    break;
                case 'weight':
                    valueA = parseFloat(a.weight) || 0;
                    valueB = parseFloat(b.weight) || 0;
                    break;
                default:
                    valueA = a.name || '';
                    valueB = b.name || '';
            }
            
            if (typeof valueA === 'string') {
                valueA = valueA.toLowerCase();
                valueB = valueB.toLowerCase();
            }
            
            if (order === 'desc') {
                return valueA < valueB ? 1 : valueA > valueB ? -1 : 0;
            } else {
                return valueA > valueB ? 1 : valueA < valueB ? -1 : 0;
            }
        });
    }

    calculateBMI(weight, height) {
        if (!weight || !height || weight <= 0 || height <= 0) {
            return null;
        }
        
        // Convert height from cm to meters if necessary
        const heightInMeters = height > 3 ? height / 100 : height;
        const bmi = weight / (heightInMeters * heightInMeters);
        
        return parseFloat(bmi.toFixed(1));
    }

    getPetAgeCategory(birthdate) {
        const ageInYears = this.calculateAgeInYears(birthdate);
        
        if (ageInYears < 1) {
            return 'puppy';
        } else if (ageInYears >= 7) {
            return 'senior';
        } else {
            return 'adult';
        }
    }

    validateActivityData(activityData) {
        const errors = {};
        
        if (!activityData.type || activityData.type.trim() === '') {
            errors.type = 'Activity type is required';
        }
        
        if (!activityData.duration || activityData.duration <= 0) {
            errors.duration = 'Duration must be greater than 0';
        }
        
        if (!activityData.date || activityData.date.trim() === '') {
            errors.date = 'Date is required';
        } else {
            const activityDate = new Date(activityData.date);
            const today = new Date();
            if (activityDate > today) {
                errors.date = 'Activity date cannot be in the future';
            }
        }
        
        return {
            isValid: Object.keys(errors).length === 0,
            errors: errors
        };
    }

    calculateActivityCalories(activityType, duration, petWeight) {
        // Simplified calorie calculation
        const caloriesPerMinute = {
            'walking': 0.5,
            'running': 1.2,
            'playing': 0.8,
            'swimming': 1.5,
            'training': 0.6
        };
        
        const baseRate = caloriesPerMinute[activityType.toLowerCase()] || 0.5;
        const weightFactor = petWeight || 20; // Default weight
        
        return Math.round(baseRate * duration * (weightFactor / 20));
    }

    getPetHealthStatus(pet) {
        if (!pet) return 'unknown';
        
        const age = this.calculateAgeInYears(pet.birthdate);
        const bmi = this.calculateBMI(pet.weight, pet.height);
        
        let healthScore = 100;
        
        // Age factor
        if (age > 10) {
            healthScore -= 10;
        } else if (age < 1) {
            healthScore -= 5;
        }
        
        // BMI factor
        if (bmi) {
            if (bmi < 18 || bmi > 30) {
                healthScore -= 20;
            } else if (bmi < 20 || bmi > 25) {
                healthScore -= 10;
            }
        }
        
        // Medical conditions factor
        if (pet.conditions && pet.conditions.length > 0) {
            healthScore -= pet.conditions.length * 5;
        }
        
        if (healthScore >= 90) return 'excellent';
        if (healthScore >= 75) return 'good';
        if (healthScore >= 60) return 'fair';
        return 'poor';
    }

    addPet(petData) {
        const validation = this.validatePetData(petData);
        if (!validation.isValid) {
            return {
                success: false,
                errors: validation.errors
            };
        }
        
        const newPet = {
            id: this.pets.length + 1,
            ...petData,
            created_at: new Date().toISOString(),
            is_active: true
        };
        
        this.pets.push(newPet);
        
        return {
            success: true,
            pet: newPet
        };
    }

    updatePet(petId, updateData) {
        const petIndex = this.pets.findIndex(pet => pet.id === petId);
        if (petIndex === -1) {
            return {
                success: false,
                message: 'Pet not found'
            };
        }
        
        const validation = this.validatePetData({ ...this.pets[petIndex], ...updateData });
        if (!validation.isValid) {
            return {
                success: false,
                errors: validation.errors
            };
        }
        
        this.pets[petIndex] = { ...this.pets[petIndex], ...updateData };
        
        return {
            success: true,
            pet: this.pets[petIndex]
        };
    }

    deletePet(petId) {
        const petIndex = this.pets.findIndex(pet => pet.id === petId);
        if (petIndex === -1) {
            return {
                success: false,
                message: 'Pet not found'
            };
        }
        
        this.pets.splice(petIndex, 1);
        
        return {
            success: true,
            message: 'Pet deleted successfully'
        };
    }

    getPetById(petId) {
        return this.pets.find(pet => pet.id === petId) || null;
    }

    getAllPets() {
        return [...this.pets];
    }
}

module.exports = Pet;
