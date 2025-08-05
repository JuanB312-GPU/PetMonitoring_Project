// Pet Component
class Pet {
    constructor() {
        this.currentPetForActivity = null;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        // Add pet button
        const addPetBtn = document.getElementById('add-pet-btn');
        if (addPetBtn) {
            addPetBtn.addEventListener('click', () => {
                this.showPetModal();
            });
        }

        // Pet modal controls
        const petModal = document.getElementById('pet-modal');
        const activityModal = document.getElementById('activity-modal');
        const foodModal = document.getElementById('food-modal');
        
        // Close buttons
        document.querySelectorAll('.modal .close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                modal.classList.remove('active');
            });
        });

        // Close modals on outside click
        [petModal, activityModal, foodModal].forEach(modal => {
            if (modal) {
                modal.addEventListener('click', (e) => {
                    if (e.target === modal) {
                        modal.classList.remove('active');
                    }
                });
            }
        });

        // Form submissions
        document.getElementById('pet-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handlePetRegistration(e.target);
        });

        document.getElementById('activity-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleActivityAdd(e.target);
        });

        document.getElementById('food-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleFoodAdd(e.target);
        });
    }

    showPetModal() {
        const petModal = document.getElementById('pet-modal');
        petModal.classList.add('active');
    }

    hidePetModal() {
        const petModal = document.getElementById('pet-modal');
        petModal.classList.remove('active');
        document.getElementById('pet-form').reset();
    }

    async handlePetRegistration(form) {
        const formData = new FormData(form);

        // Validate species and breed selection
        if (formData.get('species') === "0") {
            this.showErrorFront('Please select a species.');
            return;
        }
        if (formData.get('breed') === "0") {
            this.showErrorFront('Please select a breed.');
            return;
        }
        
        // Get selected conditions and vaccines
        const conditions = Array.from(document.getElementById('pet-conditions').selectedOptions)
            .map(option => option.value);
        const vaccines = Array.from(document.getElementById('pet-vaccines').selectedOptions)
            .map(option => option.value);
        
        const userData = JSON.parse(localStorage.getItem('userData'));

        const petData = {
            name: formData.get('name'),
            user_id: userData.user_id, // Assuming user ID is stored in localStorage
            species: formData.get('species'),
            breed: formData.get('breed'),  
            birthdate: formData.get('birthdate'),
            height: parseFloat(formData.get('height')),
            weight: parseFloat(formData.get('weight')),
            conditions: conditions.map(id => parseInt(id)),
            vaccines: vaccines.map(id => parseInt(id))
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        this.setLoading(submitBtn, true);

        console.log(JSON.stringify(petData));
        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/pets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(petData)
            });

            const result = await response.json();

            if (response.ok) {
                this.hidePetModal();
                this.showSuccess('Pet registered successfully!');
                // Reload the complete pet list after a short delay
                // to ensure the database transaction is completed
                setTimeout(() => {
                    if (window.app && window.app.loadUserPets) {
                        window.app.loadUserPets();
                    }
                }, 500); // 500ms delay
            } else {
                this.showError(result.message || 'Failed to register pet');
            }
        } catch (error) {
            console.error('Pet registration error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(submitBtn, false);
        }
    }

    addPetCard(pet) {
        const petsContainer = document.getElementById('pets-container');
        const addPetCard = document.getElementById('add-pet-btn');
        
        const petCard = this.createPetCard(pet);
        petsContainer.insertBefore(petCard, addPetCard);
    }

    createPetCard(pet) {
        const card = document.createElement('div');
        card.className = 'pet-card';
        card.dataset.petId = pet.id;
        
        const age = this.calculateAge(pet.birthdate);
        const conditions = pet.conditions || [];
        const vaccines = pet.vaccines || [];

        card.innerHTML = `
            <div class="pet-card-header">
                <div class="pet-card-name">${pet.name}</div>
                <div class="pet-card-species">${pet.species.charAt(0).toUpperCase() + pet.species.slice(1)} • ${pet.breed}</div>
            </div>
            <div class="pet-card-body">
                <div class="pet-info">
                    <div class="pet-info-item">
                        <div class="pet-info-label">Age</div>
                        <div class="pet-info-value">${age}</div>
                    </div>
                    <div class="pet-info-item">
                        <div class="pet-info-label">Weight</div>
                        <div class="pet-info-value">${pet.weight} kg</div>
                    </div>
                    <div class="pet-info-item">
                        <div class="pet-info-label">Height</div>
                        <div class="pet-info-value">${pet.height} cm</div>
                    </div>
                </div>
                
                ${conditions.length > 0 ? `
                    <div class="pet-conditions">
                        <h4>Medical Conditions</h4>
                        <div class="conditions-list">
                            ${conditions.map(condition => `
                                <span class="condition-tag">${condition.replace('_', ' ').toUpperCase()}</span>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
                
                ${vaccines.length > 0 ? `
                    <div class="pet-vaccines">
                        <h4>Vaccines</h4>
                        <div class="vaccines-list">
                            ${vaccines.map(vaccine => `
                                <span class="vaccine-tag">${vaccine.replace('_', ' ').toUpperCase()}</span>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}
                
                <div class="pet-actions">
                    <button class="btn btn-secondary" onclick="window.petComponent.showActivityModal('${pet.id}')">Add Activity</button>
                    <button class="btn btn-secondary" onclick="window.petComponent.showFoodModal('${pet.id}')">Add Food</button>
                </div>
            </div>
        `;

        // Add click handler for card (excluding action buttons)
        card.addEventListener('click', (e) => {
            if (!e.target.closest('.pet-actions')) {
                this.navigateToDashboard(pet);
            }
        });

        return card;
    }

    showActivityModal(petId) {
        this.currentPetForActivity = petId;
        document.getElementById('activity-modal').classList.add('active');
    }

    showFoodModal(petId) {
        this.currentPetForActivity = petId;
        document.getElementById('food-modal').classList.add('active');
    }

    async handleActivityAdd(form) {
        const formData = new FormData(form);
        const activityData = {
            pet_id: this.currentPetForActivity,
            activity_id: formData.get('name'),
            frequency: formData.get('frequency'),
        };
        console.log('Activity Data:', activityData);

        const submitBtn = form.querySelector('button[type="submit"]');
        this.setLoading(submitBtn, true);

        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/activities', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(activityData)
            });

            if (response.ok) {
                document.getElementById('activity-modal').classList.remove('active');
                form.reset();
                this.showSuccess('Activity added successfully!');
            } else {
                const result = await response.json();
                this.showError(result.message || 'Failed to add activity');
            }
        } catch (error) {
            console.error('Activity add error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(submitBtn, false);
        }
    }

    async handleFoodAdd(form) {
        const formData = new FormData(form);
        const foodData = {
            pet_id: this.currentPetForActivity,
            feeding_id: formData.get('name'),
            frequency: formData.get('frequency'),
        };

        const submitBtn = form.querySelector('button[type="submit"]');
        this.setLoading(submitBtn, true);

        try {
            const token = localStorage.getItem('authToken');
            const response = await fetch('/api/foods', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(foodData)
            });

            if (response.ok) {
                document.getElementById('food-modal').classList.remove('active');
                form.reset();
                this.showSuccess('Food added successfully!');
            } else {
                const result = await response.json();
                this.showError(result.message || 'Failed to add food');
            }
        } catch (error) {
            console.error('Food add error:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.setLoading(submitBtn, false);
        }
    }

    navigateToDashboard(pet) {
        // Set the selected pet in navbar
        const petSelector = document.getElementById('pet-selector');
        if (petSelector) {
            petSelector.value = pet.id;
            window.navbarComponent.selectPet(pet.id.toString());
        }
        
        // Navigate to dashboard
        window.navbarComponent.navigateTo('home');
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
        console.error('Error:', message);
        // Implement toast notifications here
    }

    showSuccess(message) {
        console.log('Success:', message);
        // Implement toast notifications here
    }

    showErrorFront(message) {
        // Remove existing error messages
        this.clearErrors();
        
        // Create error element
        const errorElement = document.createElement('div');
        errorElement.className = 'form-error';
        errorElement.textContent = message;
        
        // Insert at the top of modal body
        const modalBody = document.querySelector('#pet-modal .modal-body');
        modalBody.insertBefore(errorElement, modalBody.firstChild);
    }

    clearErrors() {
        document.querySelectorAll('.form-error').forEach(error => {
            error.remove();
        });
    }

    async loadVaccines() {
        try {
            const response = await fetch('/vaccines');
            const vaccines = await response.json();

            console.log('Vaccines:', vaccines);

            const select = document.getElementById('pet-vaccines');
            select.innerHTML = ''; // Clear existing options

              vaccines.forEach(vaccines => {
            const option = document.createElement('option');
            option.value = vaccines.vaccine_id;
            option.textContent = vaccines.name;
            select.appendChild(option);
        });

        } catch (error) {
            console.error('Error loading vaccines:', error);
        }
    }

    async loadMedicalConditions() {
    try {
        const response = await fetch('/conditions');
        const conditions = await response.json();

        const select = document.getElementById('pet-conditions');
        select.innerHTML = ''; // Clear existing options

        console.log('Conditions:', conditions);

        conditions.forEach(condition => {
            const option = document.createElement('option');
            option.value = condition.mc_id;
            option.textContent = condition.name;
            select.appendChild(option);
        });

        } catch (error) {
            console.error('Error loading conditions:', error);
        }
    }

    async loadSpecies() {
        try {
            const response = await fetch('/species');
            const species = await response.json();

            const select = document.getElementById('pet-species');
            select.innerHTML = ''; // Clear existing options
            const option = document.createElement('option');
            option.value = "0";
            option.textContent = 'Select Species';
            select.appendChild(option);

            species.forEach(species => {
                const option = document.createElement('option');
                option.value = species.species_id;
                option.textContent = species.name;
                select.appendChild(option);
            });

        } catch (error) {
            console.error('Error loading species:', error);
        }
    }

   async setupBreedSelector() {
    const speciesSelect = document.getElementById('pet-species');   
    const breedSelect = document.getElementById('pet-breed');

    speciesSelect.addEventListener('change', async () => {
        const speciesId = speciesSelect.value;

        // Clear previous breeds
        breedSelect.innerHTML = '';

        if (!speciesId || speciesId === "0") {
            // If no species selected, show default option
            const option = document.createElement('option');
            option.value = "0";
            option.textContent = 'Select a species first';
            breedSelect.appendChild(option);
            return;
        }

        try { 
            const response = await fetch(`/breeds/${speciesId}`);
            const breeds = await response.json();

            const defaultOption = document.createElement('option');
            defaultOption.value = "0";
            defaultOption.textContent = 'Select Breed';
            breedSelect.appendChild(defaultOption);

            breeds.forEach(breed => {
                const option = document.createElement('option');
                option.value = breed.breed_id;
                option.textContent = breed.name;
                breedSelect.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching breeds:', error);
        }
    });}

    async loadActivities() {
        try {
            const response = await fetch('/activities');
            const activities = await response.json();

            const select = document.getElementById('activity-name');
            select.innerHTML = ''; // Clear existing options

            activities.forEach(activity => {
                const option = document.createElement('option');
                option.value = activity.activity_id;
                option.textContent = activity.name;
                select.appendChild(option);
            });

        } catch (error) {
            console.error('Error loading activities:', error);
        }
    }

    async loadFeedings() {
        try {
            const response = await fetch('/feedings');
            const feedings = await response.json();

            const select = document.getElementById('food-name');
            select.innerHTML = ''; // Clear existing options

            feedings.forEach(food => {
                const option = document.createElement('option');
                option.value = food.feeding_id;
                option.textContent = food.name;
                select.appendChild(option);
            });

        } catch (error) {
            console.error('Error loading feedings:', error);
        }
    }

}

// Initialize when the page is ready
window.addEventListener('DOMContentLoaded', () => {
    window.petComponent.loadMedicalConditions();
    window.petComponent.loadVaccines();
    window.petComponent.loadSpecies();
    window.petComponent.setupBreedSelector();
    window.petComponent.loadActivities();
    window.petComponent.loadFeedings();
});

// Initialize pet component
window.petComponent = new Pet();