import unittest
from unittest.mock import Mock, patch

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.repositories.pet_repository import PetRepository


class TestPetRepository(unittest.TestCase):
    """Test cases for PetRepository class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        self.mock_pet = Mock()
        self.mock_pet.pet_id = 1
        self.mock_pet.name = "Buddy"
        self.mock_pet.user_id = 1
        
    def test_create_pet_success(self):
        """Test successful pet creation"""
        # Arrange
        # Mock pet is already set up in setUp
        
        # Act
        result = PetRepository.create(self.mock_db, self.mock_pet)
        
        # Assert
        self.mock_db.add.assert_called_once_with(self.mock_pet)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(self.mock_pet)
        self.assertEqual(result, self.mock_pet)
        
    @patch('backend.repositories.pet_repository.Pet')
    def test_get_user_pets_success(self, mock_pet_class):
        """Test successful retrieval of user pets"""
        # Arrange
        mock_pet1 = Mock()
        mock_pet1.name = "Buddy"
        mock_pet2 = Mock()
        mock_pet2.name = "Max"
        mock_pets = [mock_pet1, mock_pet2]
        
        self.mock_db.query.return_value.filter.return_value.all.return_value = mock_pets
        
        # Act
        result = PetRepository.get_user_pets(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_pet_class)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mock_pet1)
        self.assertEqual(result[1], mock_pet2)
        
    @patch('backend.repositories.pet_repository.Pet')
    def test_get_user_pets_no_pets(self, mock_pet_class):
        """Test retrieval when user has no pets"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Act
        result = PetRepository.get_user_pets(self.mock_db, 999)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_pet_class)
        self.assertEqual(result, [])
        
    @patch('backend.repositories.pet_repository.Pet')
    def test_get_pet_by_name_user_found(self, mock_pet_class):
        """Test finding pet by name and user when exists"""
        # Arrange
        mock_found_pet = Mock()
        mock_found_pet.name = "Buddy"
        mock_found_pet.user_id = 1
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_found_pet
        
        # Act
        result = PetRepository.get_pet_by_name_user(self.mock_db, "Buddy", 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_pet_class)
        self.assertEqual(result, mock_found_pet)
        
    @patch('backend.repositories.pet_repository.Pet')
    def test_get_pet_by_name_user_not_found(self, mock_pet_class):
        """Test finding pet by name and user when doesn't exist"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = PetRepository.get_pet_by_name_user(self.mock_db, "NonExistent", 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_pet_class)
        self.assertIsNone(result)
        
    @patch('backend.repositories.pet_repository.Species')
    def test_get_species_success(self, mock_species_class):
        """Test successful retrieval of all species"""
        # Arrange
        mock_species1 = Mock()
        mock_species1.name = "Dog"
        mock_species2 = Mock()
        mock_species2.name = "Cat"
        mock_species_list = [mock_species1, mock_species2]
        
        self.mock_db.query.return_value.all.return_value = mock_species_list
        
        # Act
        result = PetRepository.get_species(self.mock_db)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_species_class)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mock_species1)
        self.assertEqual(result[1], mock_species2)
        
    @patch('backend.repositories.pet_repository.Species')
    def test_get_species_by_id_found(self, mock_species_class):
        """Test retrieving species by ID when found"""
        # Arrange
        mock_species = Mock()
        mock_species.species_id = 1
        mock_species.name = "Dog"
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_species
        
        # Act
        result = PetRepository.get_species_by_id(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_species_class)
        self.assertEqual(result, mock_species)
        
    @patch('backend.repositories.pet_repository.Species')
    def test_get_species_by_id_not_found(self, mock_species_class):
        """Test retrieving species by ID when not found"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = PetRepository.get_species_by_id(self.mock_db, 999)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_species_class)
        self.assertIsNone(result)
        
    @patch('backend.repositories.pet_repository.Breed')
    def test_get_breeds_by_species_success(self, mock_breed_class):
        """Test successful retrieval of breeds by species"""
        # Arrange
        mock_breed1 = Mock()
        mock_breed1.name = "Golden Retriever"
        mock_breed2 = Mock()
        mock_breed2.name = "Labrador"
        mock_breeds = [mock_breed1, mock_breed2]
        
        self.mock_db.query.return_value.filter.return_value.all.return_value = mock_breeds
        
        # Act
        result = PetRepository.get_breeds_by_species(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_breed_class)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mock_breed1)
        self.assertEqual(result[1], mock_breed2)
        
    @patch('backend.repositories.pet_repository.Breed')
    def test_get_breeds_by_species_no_breeds(self, mock_breed_class):
        """Test retrieval of breeds when none exist for species"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.all.return_value = []
        
        # Act
        result = PetRepository.get_breeds_by_species(self.mock_db, 999)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_breed_class)
        self.assertEqual(result, [])
        
    @patch('backend.repositories.pet_repository.Breed')
    def test_get_breed_by_id_found(self, mock_breed_class):
        """Test retrieving breed by ID when found"""
        # Arrange
        mock_breed = Mock()
        mock_breed.breed_id = 1
        mock_breed.name = "Golden Retriever"
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_breed
        
        # Act
        result = PetRepository.get_breed_by_id(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_breed_class)
        self.assertEqual(result, mock_breed)
        
    @patch('backend.repositories.pet_repository.Breed')
    def test_get_breed_by_id_not_found(self, mock_breed_class):
        """Test retrieving breed by ID when not found"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = PetRepository.get_breed_by_id(self.mock_db, 999)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_breed_class)
        self.assertIsNone(result)
        
    def test_create_pet_with_database_error(self):
        """Test pet creation when database error occurs"""
        # Arrange
        self.mock_db.commit.side_effect = Exception("Database error")
        
        # Act & Assert
        with self.assertRaises(Exception):
            PetRepository.create(self.mock_db, self.mock_pet)
        
        self.mock_db.add.assert_called_once_with(self.mock_pet)
        self.mock_db.commit.assert_called_once()
        # refresh should not be called due to exception
        self.mock_db.refresh.assert_not_called()


if __name__ == '__main__':
    unittest.main()
