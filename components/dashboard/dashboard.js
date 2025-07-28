// Dashboard Component
class Dashboard {
    constructor() {
        this.currentPet = null;
        this.init();
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
        document.getElementById('bmi-value').textContent = bmi.value;
        const bmiStatus = document.getElementById('bmi-status');
        bmiStatus.textContent = bmi.status;
        bmiStatus.className = `metric-status ${bmi.level}`;

        // Update BCS
        document.getElementById('bcs-value').textContent = bcs.value;
        const bcsStatus = document.getElementById('bcs-status');
        bcsStatus.textContent = bcs.status;
        bcsStatus.className = `metric-status ${bcs.level}`;

        // Update MER
        document.getElementById('mer-value').textContent = `${mer.value} kcal`;
        const merStatus = document.getElementById('mer-status');
        merStatus.textContent = mer.status;
        merStatus.className = `metric-status ${mer.level}`;

        // Update Risk Assessment
        document.getElementById('risk-value').textContent = riskAssessment.level;
        const riskStatus = document.getElementById('risk-status');
        riskStatus.textContent = riskAssessment.status;
        riskStatus.className = `metric-status ${riskAssessment.level}`;
    }

    calculateBMI(pet) {
        // BMI calculation for pets (simplified)
        const heightInM = pet.height / 100;
        const bmi = pet.weight / (heightInM * heightInM);
        
        let status, level;
        if (pet.species === 'dog') {
            if (bmi < 15) {
                status = 'Underweight';
                level = 'warning';
            } else if (bmi <= 25) {
                status = 'Healthy Weight';
                level = 'normal';
            } else if (bmi <= 30) {
                status = 'Overweight';
                level = 'warning';
            } else {
                status = 'Obese';
                level = 'danger';
            }
        } else { // cat
            if (bmi < 18) {
                status = 'Underweight';
                level = 'warning';
            } else if (bmi <= 27) {
                status = 'Healthy Weight';
                level = 'normal';
            } else if (bmi <= 32) {
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
        const bmi = pet.weight / ((pet.height / 100) * (pet.height / 100));
        let bcs;
        
        if (pet.species === 'dog') {
            if (bmi < 15) bcs = 3;
            else if (bmi <= 20) bcs = 4;
            else if (bmi <= 25) bcs = 5;
            else if (bmi <= 30) bcs = 6;
            else bcs = 7;
        } else {
            if (bmi < 18) bcs = 3;
            else if (bmi <= 22) bcs = 4;
            else if (bmi <= 27) bcs = 5;
            else if (bmi <= 32) bcs = 6;
            else bcs = 7;
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
        let rer; // Resting Energy Requirement
        
        if (pet.weight < 2) {
            rer = 70 * Math.pow(pet.weight, 0.75);
        } else {
            rer = (30 * pet.weight) + 70;
        }

        // Activity factor (assuming moderate activity)
        let activityFactor = 1.6;
        
        // Adjust for age
        const age = this.getAgeInYears(pet.birthdate);
        if (age < 1) {
            activityFactor = 2.0; // Growing
        } else if (age > 7) {
            activityFactor = 1.4; // Senior
        }

        const mer = rer * activityFactor;

        return {
            value: Math.round(mer),
            status: 'Daily requirement',
            level: 'info'
        };
    }

    assessDiseaseRisk(pet) {
        const conditions = pet.conditions || [];
        const age = this.getAgeInYears(pet.birthdate);
        const bmi = pet.weight / ((pet.height / 100) * (pet.height / 100));
        
        let riskScore = 0;
        
        // Age factor
        if (age > 7) riskScore += 2;
        else if (age > 3) riskScore += 1;
        
        // Weight factor
        if (pet.species === 'dog') {
            if (bmi > 30) riskScore += 3;
            else if (bmi > 25) riskScore += 1;
        } else {
            if (bmi > 32) riskScore += 3;
            else if (bmi > 27) riskScore += 1;
        }
        
        // Existing conditions
        riskScore += conditions.length;
        
        let level, status, riskLevel;
        if (riskScore <= 2) {
            level = 'Low';
            status = 'Low risk profile';
            riskLevel = 'normal';
        } else if (riskScore <= 4) {
            level = 'Moderate';
            status = 'Monitor closely';
            riskLevel = 'warning';
        } else {
            level = 'High';
            status = 'Requires attention';
            riskLevel = 'danger';
        }

        return {
            level,
            status,
            level: riskLevel
        };
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
            
            if (activities.length > 0) {
                content += '<h4>Recent Activities:</h4>';
                activities.slice(0, 3).forEach(activity => {
                    content += `
                        <div class="info-item">
                            <span class="info-label">${activity.name}:</span>
                            <span class="info-value">${activity.duration}min, ${activity.frequency}</span>
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
                            <span class="info-value">${food.quantity}g, ${food.frequency}</span>
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
        if (!this.currentPet) return;

        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/reports', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    petId: this.currentPet.id,
                    reportType: 'health_summary'
                })
            });

            if (response.ok) {
                const report = await response.json();
                this.showSuccess('Health report generated successfully!');
                
                // Navigate to reports page
                window.navbarComponent.navigateTo('reports');
                
                // Refresh reports list
                if (window.reportsComponent) {
                    window.reportsComponent.loadReports();
                }
            } else {
                const result = await response.json();
                this.showError(result.message || 'Failed to generate report');
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

    getAgeInYears(birthdate) {
        const birth = new Date(birthdate);
        const now = new Date();
        return Math.floor((now - birth) / (1000 * 60 * 60 * 24 * 365));
    }

    showError(message) {
        console.error('Error:', message);
        // Implement toast notifications here
    }

    showSuccess(message) {
        console.log('Success:', message);
        // Implement toast notifications here
    }
}

// Initialize dashboard component
window.dashboardComponent = new Dashboard();