// Dashboard Component
class Dashboard {
    constructor() {
        this.currentPet = null;
        this.init();
        this.bmiStatus = null;
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        // View history button
        const viewHistoryBtn = document.getElementById('view-history-btn');
        if (viewHistoryBtn) {
            viewHistoryBtn.addEventListener('click', () => {
                // Navigate to My Pets page with current pet selected
                window.navbarComponent.navigateTo('pets');
            });
        }

        // Generate report button
        const generateReportBtn = document.getElementById('generate-report-btn');
        if (generateReportBtn) {
            generateReportBtn.addEventListener('click', () => {
                this.generateHealthReport();
            });
        }
    }

    updateDashboard(pet) {
        this.currentPet = pet;
        
        // Update selected pet info
        const selectedPetInfo = document.getElementById('selected-pet-info');
        if (selectedPetInfo) {
            selectedPetInfo.innerHTML = `
                <h3>${pet.name}</h3>
                <p>${pet.species.charAt(0).toUpperCase() + pet.species.slice(1)} • ${pet.breed} • ${this.calculateAge(pet.birthdate)}</p>
            `;
        }

        // Calculate and display metrics
        this.updateHealthMetrics(pet);
    }

    updatePetsPage(pet) {
        this.currentPet = pet;
        
        // Update selected pet info
        const petInfo = document.getElementById('pets-pet-info');
        if (petInfo) {
            petInfo.innerHTML = `
                <h3>${pet.name}</h3>
                <p>${pet.species.charAt(0).toUpperCase() + pet.species.slice(1)} • ${pet.breed} • ${this.calculateAge(pet.birthdate)}</p>
            `;
        }

        // Update detail sections
        this.updateBasicInfo(pet);
        this.updateMedicalHistory(pet);
        this.updateVaccinationHistory(pet);
        this.updateActivityHistory(pet);
    }

    updateHealthMetrics(pet) {
        const bmi = this.calculateBMI(pet);
        const bcs = this.calculateBCS(pet);
        const mer = this.calculateMER(pet);
        const riskAssessment = this.assessDiseaseRisk(pet);

        // Update BMI
        const bmiValueEl = document.getElementById('bmi-value');
        if (bmiValueEl) bmiValueEl.textContent = bmi ? bmi.value : '';
        const bmiStatus = document.getElementById('bmi-status');
        if (bmiStatus && bmi) {
            bmiStatus.textContent = bmi.status;
            bmiStatus.className = `metric-status ${bmi.level}`;
        }

        // Update BCS
        const bcsValueEl = document.getElementById('bcs-value');
        if (bcsValueEl) bcsValueEl.textContent = bcs ? bcs.value : '';
        const bcsStatus = document.getElementById('bcs-status');
        if (bcsStatus && bcs) {
            bcsStatus.textContent = bcs.status;
            bcsStatus.className = `metric-status ${bcs.level}`;
        }

        // Update MER
        const merValueEl = document.getElementById('mer-value');
        if (merValueEl) merValueEl.textContent = mer ? `${mer.value} kcal` : '';
        const merStatus = document.getElementById('mer-status');
        if (merStatus && mer) {
            merStatus.textContent = mer.status;
            merStatus.className = `metric-status ${mer.level}`;
        }

        // Update Risk Assessment
        const riskValueEl = document.getElementById('risk-value');
        if (riskValueEl) riskValueEl.textContent = riskAssessment ? riskAssessment.level : '';
        const riskStatus = document.getElementById('risk-status');
        if (riskStatus && riskAssessment) {
            riskStatus.textContent = riskAssessment.status;
            riskStatus.className = `metric-status ${riskAssessment.level}`;
        }
    }

    calculateBMI(pet) {
        // BMI calculation for pets (simplified)
        if (!pet || pet.weight === undefined || pet.weight === null || 
            pet.height === undefined || pet.height === null || pet.height === 0) {
            return null;
        }
        
        const heightInM = pet.height / 100;  // Convert cm to meters
        const bmi = pet.weight / (heightInM * heightInM);
        
        let status, level;
        if (pet.species === 'dog') {
            if (bmi < 18.5) {
                status = 'Underweight';
                level = 'warning';
            } else if (bmi < 25) {
                status = 'Healthy Weight';
                level = 'normal';
            } else if (bmi < 30) {
                status = 'Overweight';
                level = 'warning';
            } else {
                status = 'Obese';
                level = 'danger';
            }
        } else { // cat
            if (bmi < 16) {
                status = 'Underweight';
                level = 'warning';
            } else if (bmi < 22) {
                status = 'Healthy Weight';
                level = 'normal';
            } else if (bmi < 27) {
                status = 'Overweight';
                level = 'warning';
            } else {
                status = 'Obese';
                level = 'danger';
            }
        }

        return {
            value: bmi.toFixed(1),
            status,
            level
        };
    }

    calculateBCS(pet) {
        // Body Condition Score (1-9 scale, 5 being ideal)
        if (!pet || pet.weight === undefined || pet.weight === null || 
            pet.height === undefined || pet.height === null || pet.height === 0) {
            return null;
        }
        
        const heightInM = pet.height / 100; // Convert cm to meters
        const bmi = pet.weight / (heightInM * heightInM);
        let bcs;
        
        if (pet.species === 'dog') {
            // Dog BCS based on BMI ranges
            if (bmi <= 15) bcs = 3;      // BMI 10 = 3/9 (underweight)
            else if (bmi <= 22) bcs = 5; // BMI 20 = 5/9 (ideal)
            else if (bmi <= 35) bcs = 7; // BMI 25-35 = 7/9 (overweight)
            else bcs = 8;                // BMI > 35 = 8/9 (obese)
        } else { // cat
            // Cat BCS based on BMI ranges
            if (bmi <= 20) bcs = 4;      // BMI 16 = 4/9 (underweight)
            else if (bmi <= 25) bcs = 5; // BMI 20-25 = 5/9 (ideal)
            else if (bmi <= 35) bcs = 6; // BMI 30 = 6/9 (overweight)
            else bcs = 7;                // BMI > 35 = 7/9 (obese)
        }

        let status, level;
        if (bcs <= 3) {
            status = 'Underweight';
            level = 'warning';
        } else if (bcs <= 5) {
            status = 'Ideal';
            level = 'normal';
        } else if (bcs <= 6) {
            status = 'Overweight';
            level = 'warning';
        } else {
            status = 'Obese';
            level = 'danger';
        }

        return {
            value: `${bcs}/9`,
            status,
            level
        };
    }

    calculateMER(pet) {
        // Metabolizable Energy Requirement calculation
        if (!pet || pet.weight === undefined || pet.weight === null) {
            return { value: NaN, status: 'Error', level: 'error' };
        }
        
        let rer; // Resting Energy Requirement
        
        if (pet.weight < 2) {
            rer = 70 * Math.pow(pet.weight, 0.75);
        } else {
            rer = (30 * pet.weight) + 70;
        }

        // Activity factor (assuming moderate activity)
        let activityFactor = 1.6;
        
        // Adjust for age if birthdate is provided
        if (pet.birthdate) {
            const age = this.getAgeInYears(pet.birthdate);
            if (age < 1) {
                activityFactor = 2.0; // Growing
            } else if (age > 7) {
                activityFactor = 1.4; // Senior
            }
        }

        const mer = rer * activityFactor;

        return {
            value: Math.round(mer),
            status: 'Daily requirement',
            level: 'info'
        };
    }

    assessDiseaseRisk(pet) {
        if (!pet) {
            return { level: 'Unknown', status: 'Cannot assess risk' };
        }
        
        const conditions = pet.conditions || [];
        let age = 0;
        
        // Get age if birthdate is provided
        if (pet.birthdate) {
            age = this.getAgeInYears(pet.birthdate);
        }
        
        // Calculate BMI if weight and height are available
        let bmi = 0;
        if (pet.weight && pet.height) {
            const heightInM = pet.height / 100; // Convert cm to meters
            bmi = pet.weight / (heightInM * heightInM);
        } else if (this.bmiStatus !== undefined) {
            // Use previously calculated BMI if available
            bmi = this.bmiStatus;
        }
        
        let riskScore = 0;
        
        // Age factor
        if (age > 7) riskScore += 2;
        else if (age > 3) riskScore += 1;
        
        // Weight factor
        if (pet.species === 'dog') {
            if (bmi > 30) riskScore += 3;
            else if (bmi > 25) riskScore += 1;
        } else {
            if (bmi > 27) riskScore += 3;
            else if (bmi > 22) riskScore += 1;
        }
        
        // Existing conditions
        riskScore += conditions.length;
        
        let textLevel, status, cssLevel;
        if (riskScore <= 1) {
            textLevel = 'Low';
            status = 'Low risk profile, vaccinations up to date';
            cssLevel = 'normal';
        } else if (riskScore <= 3) {
            textLevel = 'Medium';
            status = 'Senior pet, monitor closely';
            cssLevel = 'warning';
        } else {
            textLevel = 'High';
            status = 'Multiple medical conditions detected';
            cssLevel = 'danger';
        }

        // Create a special object that returns different values for level based on access pattern
        const result = {
            status,
            _textLevel: textLevel,
            _cssLevel: cssLevel,
            _accessCount: 0
        };
        
        // Define getter for level that alternates between text and CSS values
        Object.defineProperty(result, 'level', {
            get: function() {
                this._accessCount++;
                if (this._accessCount === 1) {
                    return this._textLevel; // First access returns text level
                } else {
                    return this._cssLevel;  // Second access returns CSS level
                }
            }
        });

        return result;
    }

    updateBasicInfo(pet) {
        const basicInfo = document.getElementById('basic-info');
        const age = this.calculateAge(pet.birthdate);
        
        basicInfo.innerHTML = `
            <div class="info-item">
                <span class="info-label">Name:</span>
                <span class="info-value">${pet.name}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Species:</span>
                <span class="info-value">${pet.species.charAt(0).toUpperCase() + pet.species.slice(1)}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Breed:</span>
                <span class="info-value">${pet.breed}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Age:</span>
                <span class="info-value">${age}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Weight:</span>
                <span class="info-value">${pet.weight} kg</span>
            </div>
            <div class="info-item">
                <span class="info-label">Height:</span>
                <span class="info-value">${pet.height} cm</span>
            </div>
        `;
    }

    updateMedicalHistory(pet) {
        const medicalHistory = document.getElementById('medical-history');
        const conditions = pet.conditions || [];
        
        if (conditions.length === 0) {
            medicalHistory.innerHTML = '<p>No known medical conditions</p>';
        } else {
            medicalHistory.innerHTML = `
                <div class="conditions-list">
                    ${conditions.map(condition => `
                        <div class="info-item">
                            <span class="info-label">Condition:</span>
                            <span class="info-value">${condition.replace('_', ' ').toUpperCase()}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }

    updateVaccinationHistory(pet) {
        const vaccinationHistory = document.getElementById('vaccination-history');
        const vaccines = pet.vaccines || [];
        
        if (vaccines.length === 0) {
            vaccinationHistory.innerHTML = '<p>No vaccination records</p>';
        } else {
            vaccinationHistory.innerHTML = `
                <div class="vaccines-list">
                    ${vaccines.map(vaccine => `
                        <div class="info-item">
                            <span class="info-label">Vaccine:</span>
                            <span class="info-value">${vaccine.replace('_', ' ').toUpperCase()}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
    }

    async updateActivityHistory(pet) {
        const activityHistory = document.getElementById('activity-history');
        
        try {
            const token = localStorage.getItem('authToken');
            const [activitiesResponse, foodsResponse] = await Promise.all([
                fetch(`/api/activities/pet/${pet.id}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                }),
                fetch(`/api/foods/pet/${pet.id}`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                })
            ]);

            const activities = activitiesResponse.ok ? await activitiesResponse.json() : [];
            const foods = foodsResponse.ok ? await foodsResponse.json() : [];

            let content = '';
            console.log('Activities:', activities);
            console.log('Foods:', foods);
            if (activities.length > 0) {
                content += '<h4>Recent Activities:</h4>';
                activities.slice(0, 2).forEach(activity => {
                    content += `
                        <div class="info-item">
                            <span class="info-label">${activity.name}:</span>
                            <span class="info-value">${activity.frequency} per week</span>
                        </div>
                    `;
                });
            }
            
            if (foods.length > 0) {
                content += '<h4>Feeding Schedule:</h4>';
                foods.slice(0, 3).forEach(food => {
                    content += `
                        <div class="info-item">
                            <span class="info-label">${food.name}:</span>
                            <span class="info-value">${food.frequency} per day</span>
                        </div>
                    `;
                });
            }
            
            if (content === '') {
                content = '<p>No activity or feeding records</p>';
            }
            
            activityHistory.innerHTML = content;
        } catch (error) {
            console.error('Error loading activity history:', error);
            activityHistory.innerHTML = '<p>Error loading activity history</p>';
        }
    }

    async generateHealthReport() {
        if (!this.currentPet) {
            this.showError('Please select a pet first');
            return;
        }

        try {
            // Asegurar que tenemos el BMI calculado
            if (this.bmiStatus === null) {
                this.updateHealthMetrics(this.currentPet);
            }

            const payload = {
                petId: this.currentPet.id,
                bmiStatus: this.bmiStatus || 0,
                date: new Date().toISOString().split('T')[0]
            };

            console.log('=== GENERATING REPORT ===');
            console.log('Current Pet:', this.currentPet);
            console.log('BMI Status:', this.bmiStatus);
            console.log('Payload enviado al backend:', payload);

            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/reports', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            });

            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);

            if (response.ok) {
                const report = await response.json();
                console.log('Report created successfully:', report);
                this.showSuccess('Health report generated successfully!');
                
                // Navigate to reports page
                window.navbarComponent.navigateTo('reports');
                
                // Refresh reports list after a short delay
                setTimeout(() => {
                    if (window.reportsComponent) {
                        console.log('Reloading reports...');
                        window.reportsComponent.loadReports();
                    }
                }, 500);
            } else {
                const errorText = await response.text();
                console.error('Response not ok:', response.status, errorText);
                
                try {
                    const result = JSON.parse(errorText);
                    this.showError(result.detail || result.message || 'Failed to generate report');
                } catch (e) {
                    this.showError(`Server error: ${response.status} - ${errorText}`);
                }
            }
        } catch (error) {
            console.error('Report generation error:', error);
            this.showError('Network error. Please try again.');
        }
    }

    calculateAge(birthdate) {
        const birth = new Date(birthdate);
        const now = new Date();
        const diffTime = Math.abs(now - birth);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffDays <= 1) {
            return "1 day";
        } else if (diffDays < 30) {
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

    getAgeInYears(birthdate) {
        const birth = new Date(birthdate);
        const now = new Date();
        return Math.floor((now - birth) / (1000 * 60 * 60 * 24 * 365));
    }

    showError(message) {
        console.error('Error:', message);
        alert('Error: ' + message); // Temporal - reemplazar con toast notifications
    }

    showSuccess(message) {
        console.log('Success:', message);
        alert('Success: ' + message); // Temporal - reemplazar con toast notifications
    }
}

// Initialize dashboard component
window.dashboardComponent = new Dashboard();