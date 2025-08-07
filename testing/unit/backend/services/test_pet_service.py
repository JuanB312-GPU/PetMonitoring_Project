import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import date, datetime
import pytest
from fastapi import HTTPException

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.services.pet_service import PetService
from backend.schemas.pet import PetCreate
from backend.models.pet import Pet
from backend.models.relationships import Pet_medical_condition, Pet_vaccine


class TestPetService(unittest.TestCase):
    """Test cases for PetService class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        self.sample_pet_data = PetCreate(
            name="Buddy",
            user_id=1,
            species=1,
            breed=1,
            birthdate=date(2020, 1, 1),
            height=50.0,
            weight=25.0,
            conditions=[1, 2],
            vaccines=[1]
        )
        
    @patch('backend.services.pet_service.PetRepository')
    @patch('backend.services.pet_service.Pet')
    def test_create_pet_success(self, mock_pet_class, mock_pet_repo):
        """Test successful pet creation"""
        # Arrange
        mock_pet_repo.get_pet_by_name_user.return_value = None
        mock_pet_class.calculate_age.return_value = 4
        
        mock_pet_instance = Mock()
        mock_pet_instance.pet_id = 1
        mock_pet_class.return_value = mock_pet_instance
        mock_pet_repo.create.return_value = mock_pet_instance
        
        # Act
        result = PetService.create_pet(self.mock_db, self.sample_pet_data)
        
        # Assert
        mock_pet_repo.get_pet_by_name_user.assert_called_once_with(
            self.mock_db, "Buddy", 1
        )
        mock_pet_class.calculate_age.assert_called_once_with(date(2020, 1, 1))
        mock_pet_repo.create.assert_called_once()
        self.mock_db.add.assert_called()
        self.mock_db.commit.assert_called_once()
        self.assertEqual(result, mock_pet_instance)
        
    @patch('backend.services.pet_service.PetRepository')
    def test_create_pet_already_exists(self, mock_pet_repo):
        """Test pet creation when pet already exists"""
        # Arrange
        existing_pet = Mock()
        mock_pet_repo.get_pet_by_name_user.return_value = existing_pet
        
        # Act & Assert
        with self.assertRaises(HTTPException) as context:
            PetService.create_pet(self.mock_db, self.sample_pet_data)
        
        self.assertEqual(context.exception.status_code, 409)
        self.assertEqual(context.exception.detail, "Pet with this name already exists")
        
    @patch('backend.services.pet_service.PetRepository')
    @patch('backend.services.pet_service.MedicalRepository')
    def test_get_user_pets_success(self, mock_medical_repo, mock_pet_repo):
        """Test successful retrieval of user pets"""
        # Arrange
        mock_pet = Mock()
        mock_pet.pet_id = 1
        mock_pet.name = "Buddy"
        mock_pet.species_id = 1
        mock_pet.breed_id = 1
        mock_pet.date_of_birth = date(2020, 1, 1)
        mock_pet.height = 50.0
        mock_pet.weight = 25.0
        
        mock_species = Mock()
        mock_species.name = "Dog"
        
        mock_breed = Mock()
        mock_breed.name = "Golden Retriever"
        
        mock_condition = Mock()
        mock_condition.name = "Allergy"
        
        mock_vaccine = Mock()
        mock_vaccine.name = "Rabies"
        
        mock_pet_repo.get_user_pets.return_value = [mock_pet]
        mock_pet_repo.get_species_by_id.return_value = mock_species
        mock_pet_repo.get_breed_by_id.return_value = mock_breed
        mock_medical_repo.get_conditions_by_pet.return_value = [mock_condition]
        mock_medical_repo.get_vaccines_by_pet.return_value = [mock_vaccine]
        
        # Act
        result = PetService.get_user_pets(self.mock_db, 1)
        
        # Assert
        self.assertEqual(len(result), 1)
        pet_data = result[0]
        self.assertEqual(pet_data["id"], 1)
        self.assertEqual(pet_data["name"], "Buddy")
        self.assertEqual(pet_data["species"], "Dog")
        self.assertEqual(pet_data["breed"], "Golden Retriever")
        self.assertEqual(pet_data["conditions"], ["Allergy"])
        self.assertEqual(pet_data["vaccines"], ["Rabies"])
        
    @patch('backend.services.pet_service.PetRepository')
    def test_get_user_pets_no_pets(self, mock_pet_repo):
        """Test retrieval when user has no pets"""
        # Arrange
        mock_pet_repo.get_user_pets.return_value = []
        
        # Act
        result = PetService.get_user_pets(self.mock_db, 1)
        
        # Assert
        self.assertEqual(result, [])
        
    @patch('backend.services.pet_service.PetRepository')
    @patch('backend.services.pet_service.MedicalRepository')
    def test_get_user_pets_with_none_values(self, mock_medical_repo, mock_pet_repo):
        """Test retrieval when some data is None"""
        # Arrange
        mock_pet = Mock()
        mock_pet.pet_id = 1
        mock_pet.name = "Buddy"
        mock_pet.species_id = 1
        mock_pet.breed_id = 1
        mock_pet.date_of_birth = date(2020, 1, 1)
        mock_pet.height = 50.0
        mock_pet.weight = 25.0
        
        mock_pet_repo.get_user_pets.return_value = [mock_pet]
        mock_pet_repo.get_species_by_id.return_value = None  # No species found
        mock_pet_repo.get_breed_by_id.return_value = None    # No breed found
        mock_medical_repo.get_conditions_by_pet.return_value = []
        mock_medical_repo.get_vaccines_by_pet.return_value = []
        
        # Act
        result = PetService.get_user_pets(self.mock_db, 1)
        
        # Assert
        self.assertEqual(len(result), 1)
        pet_data = result[0]
        self.assertEqual(pet_data["species"], "Unknown")
        self.assertEqual(pet_data["breed"], "Unknown")
        self.assertEqual(pet_data["conditions"], [])
        self.assertEqual(pet_data["vaccines"], [])


if __name__ == '__main__':
    unittest.main()
