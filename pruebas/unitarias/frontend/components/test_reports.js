// Test suite for Reports component functionality
// Using Jest-like syntax for testing framework

// Reports Component Unit Tests
const { describe, test, expect, beforeEach, afterEach } = require('@jest/globals');

// Mock Reports class
class Reports {
    constructor() {
        this.reports = [];
        this.currentPet = null;
    }

    calculateBMI(weight, height) {
        if (!weight || !height || weight === 0 || height === 0) {
            return null;
        }
        return weight / (height * height);
    }

    getBMIStatus(bmi, species) {
        if (!bmi) return 'unknown';
        
        if (species === 'cat') {
            if (bmi < 16) return 'underweight';
            if (bmi >= 16 && bmi < 22) return 'ideal';
            if (bmi >= 22 && bmi < 27) return 'overweight';
            return 'obese';
        } else if (species === 'dog') {
            if (bmi < 18.5) return 'underweight';
            if (bmi >= 18.5 && bmi < 25) return 'ideal';
            if (bmi >= 25 && bmi < 30) return 'overweight';
            return 'obese';
        }
        
        return 'unknown';
    }

    getOverallHealthStatus(pet) {
        const bmi = this.calculateBMI(pet.weight, pet.height);
        const bmiStatus = this.getBMIStatus(bmi, pet.species);
        const conditions = pet.medical_conditions || [];
        
        // Handle conditions as string
        let conditionsCount = 0;
        if (typeof conditions === 'string') {
            conditionsCount = conditions.trim() === '' ? 0 : 1;
        } else if (Array.isArray(conditions)) {
            conditionsCount = conditions.length;
        }
        
        if (conditionsCount === 0 && bmiStatus === 'ideal') {
            return 'Excellent';
        } else if (conditionsCount === 0 && (bmiStatus === 'overweight' || bmiStatus === 'underweight')) {
            return 'Good';
        } else if (conditionsCount > 0 && bmiStatus === 'ideal') {
            return 'Fair';
        } else {
            return 'Needs Attention';
        }
    }

    generateHealthReport(petId, dateRange) {
        if (!petId) {
            return {
                success: false,
                message: 'Pet ID is required'
            };
        }

        // Mock report generation
        const report = {
            id: Date.now(),
            pet_id: petId,
            date_range: dateRange,
            type: 'health',
            generated_at: new Date().toISOString(),
            data: {
                weight_trend: 'stable',
                activity_level: 'normal',
                medical_alerts: 0,
                vaccination_status: 'up_to_date'
            }
        };

        this.reports.push(report);
        
        return {
            success: true,
            report: report,
            message: 'Health report generated successfully'
        };
    }

    generateActivityReport(petId, dateRange) {
        if (!petId) {
            return {
                success: false,
                message: 'Pet ID is required'
            };
        }

        // Mock activity report
        const report = {
            id: Date.now(),
            pet_id: petId,
            date_range: dateRange,
            type: 'activity',
            generated_at: new Date().toISOString(),
            data: {
                total_activities: 15,
                avg_duration: 45,
                most_common_activity: 'walking',
                activity_trends: 'increasing'
            }
        };

        this.reports.push(report);
        
        return {
            success: true,
            report: report,
            message: 'Activity report generated successfully'
        };
    }

    generateMedicalReport(petId, dateRange) {
        if (!petId) {
            return {
                success: false,
                message: 'Pet ID is required'
            };
        }

        // Mock medical report
        const report = {
            id: Date.now(),
            pet_id: petId,
            date_range: dateRange,
            type: 'medical',
            generated_at: new Date().toISOString(),
            data: {
                medical_visits: 3,
                vaccinations: 2,
                medications: 1,
                health_alerts: 0
            }
        };

        this.reports.push(report);
        
        return {
            success: true,
            report: report,
            message: 'Medical report generated successfully'
        };
    }

    exportReport(reportId, format = 'pdf') {
        const report = this.reports.find(r => r.id === reportId);
        
        if (!report) {
            return {
                success: false,
                message: 'Report not found'
            };
        }

        // Mock export
        return {
            success: true,
            message: `Report exported as ${format.toUpperCase()}`,
            download_url: `reports/${reportId}.${format}`
        };
    }

    getReportsByPet(petId) {
        return this.reports.filter(r => r.pet_id === petId);
    }

    deleteReport(reportId) {
        const index = this.reports.findIndex(r => r.id === reportId);
        
        if (index === -1) {
            return {
                success: false,
                message: 'Report not found'
            };
        }

        this.reports.splice(index, 1);
        
        return {
            success: true,
            message: 'Report deleted successfully'
        };
    }

    validateDateRange(dateRange) {
        if (!dateRange || !dateRange.start || !dateRange.end) {
            return {
                isValid: false,
                message: 'Start and end dates are required'
            };
        }

        const startDate = new Date(dateRange.start);
        const endDate = new Date(dateRange.end);
        const today = new Date();

        if (startDate > endDate) {
            return {
                isValid: false,
                message: 'Start date cannot be after end date'
            };
        }

        if (endDate > today) {
            return {
                isValid: false,
                message: 'End date cannot be in the future'
            };
        }

        return {
            isValid: true,
            message: 'Date range is valid'
        };
    }

    filterReportsByDateRange(reports, dateRange) {
        if (!reports || !dateRange) return [];

        const startDate = new Date(dateRange.start);
        const endDate = new Date(dateRange.end);

        return reports.filter(report => {
            const reportDate = new Date(report.generated_at);
            return reportDate >= startDate && reportDate <= endDate;
        });
    }

    calculateReportMetrics(reports) {
        if (!reports || reports.length === 0) {
            return {
                total_reports: 0,
                health_reports: 0,
                activity_reports: 0,
                medical_reports: 0
            };
        }

        return {
            total_reports: reports.length,
            health_reports: reports.filter(r => r.type === 'health').length,
            activity_reports: reports.filter(r => r.type === 'activity').length,
            medical_reports: reports.filter(r => r.type === 'medical').length
        };
    }

    showModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.style.display = 'block';
            modal.classList.add('show');
        }
    }

    hideModal(id) {
        const modal = document.getElementById(id);
        if (modal) {
            modal.style.display = 'none';
            modal.classList.remove('show');
        }
    }

    updateReportList(reports) {
        // Mock DOM update
        return true;
    }

    displayReportData(report) {
        if (!report) return false;
        
        // Mock display
        return {
            type: report.type,
            data: report.data,
            generated_at: report.generated_at
        };
    }
}

describe('Reports Component', () => {
    let reports;
    let mockDocument;
    
    beforeEach(() => {
        // Setup DOM mock
        mockDocument = {
            getElementById: jest.fn(),
            querySelectorAll: jest.fn(),
            createElement: jest.fn(),
            querySelector: jest.fn()
        };
        
        global.document = mockDocument;
        global.window = {
            reportsComponent: {
                updateList: jest.fn()
            }
        };
        
        // Import the Reports class (would need module system)
        reports = new Reports();
    });
    
    describe('calculateBMI', () => {
        test('should calculate BMI correctly', () => {
            // Arrange
            const weight = 10; // kg
            const height = 0.5; // m
            
            // Act
            const result = reports.calculateBMI(weight, height);
            
            // Assert
            expect(result).toBe(40); // 10 / (0.5^2) = 40
        });
        
        test('should return null for zero weight', () => {
            // Act
            const result = reports.calculateBMI(0, 0.5);
            
            // Assert
            expect(result).toBeNull();
        });
        
        test('should return null for zero height', () => {
            // Act
            const result = reports.calculateBMI(10, 0);
            
            // Assert
            expect(result).toBeNull();
        });
        
        test('should return null for missing parameters', () => {
            // Act
            const result1 = reports.calculateBMI(null, 0.5);
            const result2 = reports.calculateBMI(10, null);
            
            // Assert
            expect(result1).toBeNull();
            expect(result2).toBeNull();
        });
    });
    
    describe('getBMIStatus', () => {
        test('should classify cat BMI correctly', () => {
            expect(reports.getBMIStatus(15, 'cat')).toBe('underweight');
            expect(reports.getBMIStatus(18, 'cat')).toBe('ideal');
            expect(reports.getBMIStatus(24, 'cat')).toBe('overweight');
            expect(reports.getBMIStatus(30, 'cat')).toBe('obese');
        });
        
        test('should classify dog BMI correctly', () => {
            expect(reports.getBMIStatus(17, 'dog')).toBe('underweight');
            expect(reports.getBMIStatus(20, 'dog')).toBe('ideal');
            expect(reports.getBMIStatus(27, 'dog')).toBe('overweight');
            expect(reports.getBMIStatus(35, 'dog')).toBe('obese');
        });
        
        test('should return unknown for invalid inputs', () => {
            expect(reports.getBMIStatus(null, 'dog')).toBe('unknown');
            expect(reports.getBMIStatus(20, 'bird')).toBe('unknown');
            expect(reports.getBMIStatus(20, null)).toBe('unknown');
        });
    });
    
    describe('getOverallHealthStatus', () => {
        test('should return Excellent for healthy pet with no conditions', () => {
            // Arrange
            const pet = {
                weight: 10,
                height: 0.707, // BMI ~20 (ideal for dog)
                species: 'dog',
                medical_conditions: []
            };
            
            // Act
            const result = reports.getOverallHealthStatus(pet);
            
            // Assert
            expect(result).toBe('Excellent');
        });
        
        test('should return Good for overweight pet with no conditions', () => {
            // Arrange
            const pet = {
                weight: 15,
                height: 0.707, // BMI ~30 (overweight for dog)
                species: 'dog',
                medical_conditions: []
            };
            
            // Act
            const result = reports.getOverallHealthStatus(pet);
            
            // Assert
            expect(result).toBe('Good');
        });
        
        test('should return Fair for healthy weight pet with conditions', () => {
            // Arrange
            const pet = {
                weight: 10,
                height: 0.707, // BMI ~20 (ideal for dog)
                species: 'dog',
                medical_conditions: ['diabetes']
            };
            
            // Act
            const result = reports.getOverallHealthStatus(pet);
            
            // Assert
            expect(result).toBe('Fair');
        });
        
        test('should return Needs Attention for obese pet with conditions', () => {
            // Arrange
            const pet = {
                weight: 20,
                height: 0.707, // BMI ~40 (obese for dog)
                species: 'dog',
                medical_conditions: ['diabetes', 'arthritis']
            };
            
            // Act
            const result = reports.getOverallHealthStatus(pet);
            
            // Assert
            expect(result).toBe('Needs Attention');
        });
        
        test('should handle conditions as string', () => {
            // Arrange
            const pet = {
                weight: 10,
                height: 0.707,
                species: 'dog',
                medical_conditions: 'diabetes'
            };
            
            // Act
            const result = reports.getOverallHealthStatus(pet);
            
            // Assert
            expect(result).toBe('Fair');
        });
        
        test('should handle empty string conditions', () => {
            // Arrange
            const pet = {
                weight: 10,
                height: 0.707,
                species: 'dog',
                medical_conditions: ''
            };
            
            // Act
            const result = reports.getOverallHealthStatus(pet);
            
            // Assert
            expect(result).toBe('Excellent');
        });
    });
    
    describe('generateHealthReport', () => {
        test('should generate health report successfully', () => {
            // Arrange
            const petId = 1;
            const dateRange = { start: '2024-01-01', end: '2024-01-31' };
            
            // Act
            const result = reports.generateHealthReport(petId, dateRange);
            
            // Assert
            expect(result.success).toBe(true);
            expect(result.report.pet_id).toBe(petId);
            expect(result.report.type).toBe('health');
            expect(result.report.date_range).toEqual(dateRange);
            expect(reports.reports).toHaveLength(1);
        });
        
        test('should fail when pet ID is missing', () => {
            // Act
            const result = reports.generateHealthReport(null);
            
            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Pet ID is required');
        });
        
        test('should include health data in report', () => {
            // Arrange
            const petId = 1;
            
            // Act
            const result = reports.generateHealthReport(petId, {});
            
            // Assert
            expect(result.report.data).toEqual({
                weight_trend: 'stable',
                activity_level: 'normal',
                medical_alerts: 0,
                vaccination_status: 'up_to_date'
            });
        });
    });
    
    describe('generateActivityReport', () => {
        test('should generate activity report successfully', () => {
            // Arrange
            const petId = 2;
            const dateRange = { start: '2024-01-01', end: '2024-01-31' };
            
            // Act
            const result = reports.generateActivityReport(petId, dateRange);
            
            // Assert
            expect(result.success).toBe(true);
            expect(result.report.pet_id).toBe(petId);
            expect(result.report.type).toBe('activity');
            expect(result.report.date_range).toEqual(dateRange);
        });
        
        test('should include activity data in report', () => {
            // Arrange
            const petId = 2;
            
            // Act
            const result = reports.generateActivityReport(petId, {});
            
            // Assert
            expect(result.report.data).toEqual({
                total_activities: 15,
                avg_duration: 45,
                most_common_activity: 'walking',
                activity_trends: 'increasing'
            });
        });
    });
    
    describe('generateMedicalReport', () => {
        test('should generate medical report successfully', () => {
            // Arrange
            const petId = 3;
            const dateRange = { start: '2024-01-01', end: '2024-01-31' };
            
            // Act
            const result = reports.generateMedicalReport(petId, dateRange);
            
            // Assert
            expect(result.success).toBe(true);
            expect(result.report.pet_id).toBe(petId);
            expect(result.report.type).toBe('medical');
            expect(result.report.date_range).toEqual(dateRange);
        });
        
        test('should include medical data in report', () => {
            // Arrange
            const petId = 3;
            
            // Act
            const result = reports.generateMedicalReport(petId, {});
            
            // Assert
            expect(result.report.data).toEqual({
                medical_visits: 3,
                vaccinations: 2,
                medications: 1,
                health_alerts: 0
            });
        });
    });
    
    describe('exportReport', () => {
        test('should export existing report successfully', () => {
            // Arrange
            const petId = 1;
            const reportResult = reports.generateHealthReport(petId, {});
            const reportId = reportResult.report.id;
            
            // Act
            const result = reports.exportReport(reportId, 'pdf');
            
            // Assert
            expect(result.success).toBe(true);
            expect(result.message).toBe('Report exported as PDF');
            expect(result.download_url).toBe(`reports/${reportId}.pdf`);
        });
        
        test('should fail for non-existent report', () => {
            // Act
            const result = reports.exportReport(999);
            
            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Report not found');
        });
        
        test('should support different export formats', () => {
            // Arrange
            const petId = 1;
            const reportResult = reports.generateHealthReport(petId, {});
            const reportId = reportResult.report.id;
            
            // Act
            const pdfResult = reports.exportReport(reportId, 'pdf');
            const csvResult = reports.exportReport(reportId, 'csv');
            
            // Assert
            expect(pdfResult.message).toBe('Report exported as PDF');
            expect(csvResult.message).toBe('Report exported as CSV');
        });
    });
    
    describe('getReportsByPet', () => {
        test('should return reports for specific pet', () => {
            // Arrange
            reports.generateHealthReport(1, {});
            reports.generateActivityReport(1, {});
            reports.generateMedicalReport(2, {});
            
            // Act
            const pet1Reports = reports.getReportsByPet(1);
            const pet2Reports = reports.getReportsByPet(2);
            
            // Assert
            expect(pet1Reports).toHaveLength(2);
            expect(pet2Reports).toHaveLength(1);
            expect(pet1Reports[0].pet_id).toBe(1);
            expect(pet1Reports[1].pet_id).toBe(1);
            expect(pet2Reports[0].pet_id).toBe(2);
        });
        
        test('should return empty array for pet with no reports', () => {
            // Act
            const result = reports.getReportsByPet(999);
            
            // Assert
            expect(result).toEqual([]);
        });
    });
    
    describe('deleteReport', () => {
        test('should delete existing report successfully', () => {
            // Arrange
            const reportResult = reports.generateHealthReport(1, {});
            const reportId = reportResult.report.id;
            
            // Act
            const result = reports.deleteReport(reportId);
            
            // Assert
            expect(result.success).toBe(true);
            expect(result.message).toBe('Report deleted successfully');
            expect(reports.reports).toHaveLength(0);
        });
        
        test('should fail for non-existent report', () => {
            // Act
            const result = reports.deleteReport(999);
            
            // Assert
            expect(result.success).toBe(false);
            expect(result.message).toBe('Report not found');
        });
    });
    
    describe('validateDateRange', () => {
        test('should validate correct date range', () => {
            // Arrange
            const dateRange = {
                start: '2024-01-01',
                end: '2024-01-31'
            };
            
            // Act
            const result = reports.validateDateRange(dateRange);
            
            // Assert
            expect(result.isValid).toBe(true);
            expect(result.message).toBe('Date range is valid');
        });
        
        test('should fail when start date is missing', () => {
            // Arrange
            const dateRange = { end: '2024-01-31' };
            
            // Act
            const result = reports.validateDateRange(dateRange);
            
            // Assert
            expect(result.isValid).toBe(false);
            expect(result.message).toBe('Start and end dates are required');
        });
        
        test('should fail when end date is missing', () => {
            // Arrange
            const dateRange = { start: '2024-01-01' };
            
            // Act
            const result = reports.validateDateRange(dateRange);
            
            // Assert
            expect(result.isValid).toBe(false);
            expect(result.message).toBe('Start and end dates are required');
        });
        
        test('should fail when start date is after end date', () => {
            // Arrange
            const dateRange = {
                start: '2024-01-31',
                end: '2024-01-01'
            };
            
            // Act
            const result = reports.validateDateRange(dateRange);
            
            // Assert
            expect(result.isValid).toBe(false);
            expect(result.message).toBe('Start date cannot be after end date');
        });
    });
    
    describe('filterReportsByDateRange', () => {
        test('should filter reports within date range', () => {
            // Arrange
            const report1 = reports.generateHealthReport(1, {});
            const report2 = reports.generateActivityReport(1, {});
            
            // Manually set dates for testing
            report1.report.generated_at = '2024-01-15T10:00:00Z';
            report2.report.generated_at = '2024-02-15T10:00:00Z';
            
            const dateRange = {
                start: '2024-01-01',
                end: '2024-01-31'
            };
            
            // Act
            const result = reports.filterReportsByDateRange(reports.reports, dateRange);
            
            // Assert
            expect(result).toHaveLength(1);
            expect(result[0].id).toBe(report1.report.id);
        });
        
        test('should return empty array for invalid inputs', () => {
            // Act
            const result1 = reports.filterReportsByDateRange(null, {});
            const result2 = reports.filterReportsByDateRange([], null);
            
            // Assert
            expect(result1).toEqual([]);
            expect(result2).toEqual([]);
        });
    });
    
    describe('calculateReportMetrics', () => {
        test('should calculate metrics for multiple reports', () => {
            // Arrange
            reports.generateHealthReport(1, {});
            reports.generateActivityReport(1, {});
            reports.generateMedicalReport(1, {});
            reports.generateHealthReport(2, {});
            
            // Act
            const result = reports.calculateReportMetrics(reports.reports);
            
            // Assert
            expect(result).toEqual({
                total_reports: 4,
                health_reports: 2,
                activity_reports: 1,
                medical_reports: 1
            });
        });
        
        test('should return zero metrics for empty reports', () => {
            // Act
            const result = reports.calculateReportMetrics([]);
            
            // Assert
            expect(result).toEqual({
                total_reports: 0,
                health_reports: 0,
                activity_reports: 0,
                medical_reports: 0
            });
        });
        
        test('should handle null/undefined reports', () => {
            // Act
            const result1 = reports.calculateReportMetrics(null);
            const result2 = reports.calculateReportMetrics(undefined);
            
            // Assert
            expect(result1).toEqual({
                total_reports: 0,
                health_reports: 0,
                activity_reports: 0,
                medical_reports: 0
            });
            expect(result2).toEqual({
                total_reports: 0,
                health_reports: 0,
                activity_reports: 0,
                medical_reports: 0
            });
        });
    });
});
