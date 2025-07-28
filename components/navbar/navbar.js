// Navbar Component
class Navbar {
    constructor() {
        this.currentUser = null;
        this.currentPet = null;
        this.pets = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkAuthState();
    }

    bindEvents() {

        // Navigation links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const page = e.target.getAttribute('data-page');
                this.navigateTo(page);
            });
        });

        // Brand click (go to homepage)
        const navBrand = document.getElementById('nav-brand');
        if (navBrand) {
            navBrand.addEventListener('click', () => {
                this.navigateTo('home');
            });
        }

        // Pet selector
        const petSelector = document.getElementById('pet-selector');
        if (petSelector) {
            petSelector.addEventListener('change', (e) => {
                const petId = e.target.value;
                this.selectPet(petId);
            });
        }

        // Logout button
        const logoutBtn = document.getElementById('logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.logout();
            });
        }
    }

    navigateTo(page) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(p => {
            p.classList.remove('active');
        });

        // Show selected page
        const targetPage = document.getElementById(`${page}-page`) || document.getElementById('home-page');
        targetPage.classList.add('active');

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-page="${page}"]`)?.classList.add('active');

        // Update page content based on selected pet
        if (this.currentPet && (page === 'dashboard' || page === 'pets')) {
            this.updatePageContent(page);
        }
    }

    updatePageContent(page) {
        if (page === 'dashboard') {
            // Dashboard navigation
            if (this.currentPet) {
                window.dashboardComponent?.updateDashboard(this.currentPet);
            }
        } else if (page === 'pets') {
            // My Pets page
            if (this.currentPet) {
                window.dashboardComponent?.updatePetsPage(this.currentPet);
            }
        }
    }

    selectPet(petId) {
        if (!petId) {
            this.currentPet = null;
            // Clear dashboard metrics when no pet selected
            this.clearDashboardMetrics();
            return;
        }

        const pet = this.pets.find(p => p.id === parseInt(petId));
        if (pet) {
            this.currentPet = pet;
            // Update dashboard and pets pages
            if (window.dashboardComponent) {
                window.dashboardComponent.updateDashboard(pet);
                window.dashboardComponent.updatePetsPage(pet);
            }
        }
    }

    clearDashboardMetrics() {
        // Clear selected pet info
        const selectedPetInfo = document.getElementById('selected-pet-info');
        if (selectedPetInfo) {
            selectedPetInfo.innerHTML = '';
        }

        const petsPetInfo = document.getElementById('pets-pet-info');
        if (petsPetInfo) {
            petsPetInfo.innerHTML = '';
        }

        // Reset metric values
        const metrics = ['bmi-value', 'bcs-value', 'mer-value', 'risk-value'];
        const statuses = ['bmi-status', 'bcs-status', 'mer-status', 'risk-status'];
        
        metrics.forEach(metricId => {
            const element = document.getElementById(metricId);
            if (element) element.textContent = '-';
        });
        
        statuses.forEach(statusId => {
            const element = document.getElementById(statusId);
            if (element) {
                element.textContent = 'Select a pet to view metrics';
                element.className = 'metric-status';
            }
        });

        // Clear My Pets sections
        const sections = ['basic-info', 'medical-history', 'vaccination-history', 'activity-history'];
        sections.forEach(sectionId => {
            const element = document.getElementById(sectionId);
            if (element) {
                element.innerHTML = 'Select a pet to view details';
            }
        });
    }

    updateAuthState(user) {
        this.currentUser = user;
        const navAuth = document.getElementById('nav-auth');
        const navUser = document.getElementById('nav-user');

        if (user) {
            navAuth.classList.add('hidden');
            navUser.classList.remove('hidden');
            this.loadUserPets();
        } else {
            navAuth.classList.remove('hidden');
            navUser.classList.add('hidden');
            this.pets = [];
            this.currentPet = null;
            this.updatePetSelector();
        }
    }

    async loadUserPets() {
        try {
            const token = localStorage.getItem('authToken');

            const userData = JSON.parse(localStorage.getItem('userData'));
            const response = await fetch(`/api/pets?user_id=${userData.user_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (response.ok) {
                this.pets = await response.json();
                this.updatePetSelector();
            } else {
                console.error('Failed to load pets');
            }
        } catch (error) {
            console.error('Error loading pets:', error);
        }
    }

    updatePetSelector() {
        const petSelector = document.getElementById('pet-selector');
        if (!petSelector) return;

        petSelector.innerHTML = '<option value="">Select a Pet</option>';
        
        this.pets.forEach(pet => {
            const option = document.createElement('option');
            option.value = pet.id;
            option.textContent = pet.name;
            petSelector.appendChild(option);
        });

        // Select first pet if available and no pet currently selected
        if (this.pets.length > 0 && !this.currentPet) {
            petSelector.value = this.pets[0].id;
            this.selectPet(this.pets[0].id.toString());
        }
    }

    addPet(pet) {
        this.pets.push(pet);
        this.updatePetSelector();
        
        // Auto-select the newly added pet
        const petSelector = document.getElementById('pet-selector');
        if (petSelector) {
            petSelector.value = pet.id;
            this.selectPet(pet.id.toString());
        }
    }

    checkAuthState() {
        const token = localStorage.getItem('authToken');
        const userData = localStorage.getItem('userData');
        
        if (token && userData) {
            try {
                const user = JSON.parse(userData);
                this.updateAuthState(user);
            } catch (error) {
                console.error('Error parsing user data:', error);
                this.logout();
            }
        }
    }

    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        this.updateAuthState(null);
        this.navigateTo('home');
        
        // Show guest content
        document.getElementById('guest-content').classList.remove('hidden');
        document.getElementById('user-content').classList.add('hidden');
    }
}

// Initialize navbar component
window.navbarComponent = new Navbar();