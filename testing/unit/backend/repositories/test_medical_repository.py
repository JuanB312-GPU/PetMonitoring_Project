import unittest
from unittest.mock import Mock, patch

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.repositories.medical_repository import MedicalRepository


class TestMedicalRepository(unittest.TestCase):
    """Test cases for MedicalRepository class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        
    @patch('backend.repositories.medical_repository.Medical_condition')
    def test_get_medical_conditions(self, mock_medical_condition):
        """Test retrieving all medical conditions"""
        # Arrange
        mock_condition1 = Mock()
        mock_condition1.name = "Allergy"
        mock_condition2 = Mock()
        mock_condition2.name = "Diabetes"
        
        self.mock_db.query.return_value.all.return_value = [mock_condition1, mock_condition2]
        
        # Act
        result = MedicalRepository.get_medical_conditions(self.mock_db)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_medical_condition)
        self.assertEqual(len(result), 2)
        
    @patch('backend.repositories.medical_repository.Vaccine')
    def test_get_vaccines(self, mock_vaccine):
        """Test retrieving all vaccines"""
        # Arrange
        mock_vaccine1 = Mock()
        mock_vaccine1.name = "Rabies"
        mock_vaccine2 = Mock()
        mock_vaccine2.name = "DHPP"
        
        self.mock_db.query.return_value.all.return_value = [mock_vaccine1, mock_vaccine2]
        
        # Act
        result = MedicalRepository.get_vaccines(self.mock_db)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_vaccine)
        self.assertEqual(len(result), 2)
        
    @patch('backend.repositories.medical_repository.Medical_condition')
    def test_get_condition_by_id_found(self, mock_medical_condition):
        """Test retrieving medical condition by ID when found"""
        # Arrange
        mock_condition = Mock()
        mock_condition.mc_id = 1
        mock_condition.name = "Allergy"
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_condition
        
        # Act
        result = MedicalRepository.get_condition_by_id(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_medical_condition)
        self.assertEqual(result, mock_condition)
        
    @patch('backend.repositories.medical_repository.Medical_condition')
    def test_get_condition_by_id_not_found(self, mock_medical_condition):
        """Test retrieving medical condition by ID when not found"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = MedicalRepository.get_condition_by_id(self.mock_db, 999)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_medical_condition)
        self.assertIsNone(result)
        
    @patch('backend.repositories.medical_repository.Vaccine')
    def test_get_vaccine_by_id_found(self, mock_vaccine):
        """Test retrieving vaccine by ID when found"""
        # Arrange
        mock_vaccine_instance = Mock()
        mock_vaccine_instance.vaccine_id = 1
        mock_vaccine_instance.name = "Rabies"
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_vaccine_instance
        
        # Act
        result = MedicalRepository.get_vaccine_by_id(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_vaccine)
        self.assertEqual(result, mock_vaccine_instance)
        
    @patch('backend.repositories.medical_repository.Pet_medical_condition')
    @patch('backend.repositories.medical_repository.Medical_condition')
    def test_get_conditions_by_pet(self, mock_medical_condition, mock_pet_medical_condition):
        """Test retrieving conditions for a specific pet"""
        # Arrange
        mock_condition = Mock()
        mock_condition.name = "Allergy"
        
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_condition]
        
        # Act
        result = MedicalRepository.get_conditions_by_pet(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_medical_condition)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mock_condition)
        
    @patch('backend.repositories.medical_repository.Pet_vaccine')
    @patch('backend.repositories.medical_repository.Vaccine')
    def test_get_vaccines_by_pet(self, mock_vaccine, mock_pet_vaccine):
        """Test retrieving vaccines for a specific pet"""
        # Arrange
        mock_vaccine_instance = Mock()
        mock_vaccine_instance.name = "Rabies"
        
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = [mock_vaccine_instance]
        
        # Act
        result = MedicalRepository.get_vaccines_by_pet(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_vaccine)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], mock_vaccine_instance)
        
    @patch('backend.repositories.medical_repository.Species')
    def test_get_species(self, mock_species):
        """Test retrieving all species"""
        # Arrange
        mock_species_instance1 = Mock()
        mock_species_instance1.name = "Dog"
        mock_species_instance2 = Mock()
        mock_species_instance2.name = "Cat"
        
        self.mock_db.query.return_value.all.return_value = [mock_species_instance1, mock_species_instance2]
        
        # Act
        result = MedicalRepository.get_species(self.mock_db)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_species)
        self.assertEqual(len(result), 2)
        
    @patch('backend.repositories.medical_repository.Breed')
    def test_get_breeds_by_species(self, mock_breed):
        """Test retrieving breeds for a specific species"""
        # Arrange
        mock_breed_instance1 = Mock()
        mock_breed_instance1.name = "Golden Retriever"
        mock_breed_instance2 = Mock()
        mock_breed_instance2.name = "Labrador"
        
        self.mock_db.query.return_value.filter.return_value.all.return_value = [mock_breed_instance1, mock_breed_instance2]
        
        # Act
        result = MedicalRepository.get_breeds_by_species(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_breed)
        self.assertEqual(len(result), 2)
        
    @patch('backend.repositories.medical_repository.Pet_medical_condition')
    def test_create_pet_medical_condition_success(self, mock_pet_medical_condition_class):
        """Test successful creation of pet medical condition"""
        # Arrange
        mock_pet_condition = Mock()
        
        # Act
        result = MedicalRepository.create_pet_medical_condition(self.mock_db, mock_pet_condition)
        
        # Assert
        self.mock_db.add.assert_called_once_with(mock_pet_condition)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(mock_pet_condition)
        self.assertTrue(result)
        
    @patch('backend.repositories.medical_repository.Pet_vaccine')
    def test_create_pet_vaccine_success(self, mock_pet_vaccine_class):
        """Test successful creation of pet vaccine"""
        # Arrange
        mock_pet_vaccine = Mock()
        
        # Act
        result = MedicalRepository.create_pet_vaccine(self.mock_db, mock_pet_vaccine)
        
        # Assert
        self.mock_db.add.assert_called_once_with(mock_pet_vaccine)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(mock_pet_vaccine)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
