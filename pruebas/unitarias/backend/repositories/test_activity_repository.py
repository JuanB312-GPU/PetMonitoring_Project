import unittest
from unittest.mock import Mock, patch

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.repositories.activity_repository import ActivityRepository


class TestActivityRepository(unittest.TestCase):
    """Test cases for ActivityRepository class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        
    @patch('backend.repositories.activity_repository.Activity')
    def test_get_activities(self, mock_activity):
        """Test retrieving all activities"""
        # Arrange
        mock_activity1 = Mock()
        mock_activity1.name = "Walking"
        mock_activity2 = Mock()
        mock_activity2.name = "Playing"
        
        self.mock_db.query.return_value.all.return_value = [mock_activity1, mock_activity2]
        
        # Act
        result = ActivityRepository.get_activities(self.mock_db)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_activity)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mock_activity1)
        self.assertEqual(result[1], mock_activity2)
        
    @patch('backend.repositories.activity_repository.Feeding')
    def test_get_feedings(self, mock_feeding):
        """Test retrieving all feedings"""
        # Arrange
        mock_feeding1 = Mock()
        mock_feeding1.name = "Dry Food"
        mock_feeding2 = Mock()
        mock_feeding2.name = "Wet Food"
        
        self.mock_db.query.return_value.all.return_value = [mock_feeding1, mock_feeding2]
        
        # Act
        result = ActivityRepository.get_feedings(self.mock_db)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_feeding)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], mock_feeding1)
        self.assertEqual(result[1], mock_feeding2)
        
    @patch('backend.repositories.activity_repository.Activity')
    def test_get_activity_by_id_found(self, mock_activity):
        """Test retrieving activity by ID when found"""
        # Arrange
        mock_activity_instance = Mock()
        mock_activity_instance.activity_id = 1
        mock_activity_instance.name = "Walking"
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_activity_instance
        
        # Act
        result = ActivityRepository.get_activity_by_id(self.mock_db, 1)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_activity)
        self.assertEqual(result, mock_activity_instance)
        
    @patch('backend.repositories.activity_repository.Activity')
    def test_get_activity_by_id_not_found(self, mock_activity):
        """Test retrieving activity by ID when not found"""
        # Arrange
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = ActivityRepository.get_activity_by_id(self.mock_db, 999)
        
        # Assert
        self.mock_db.query.assert_called_once_with(mock_activity)
        self.assertIsNone(result)
        
    @patch('backend.repositories.activity_repository.Pet_activity')
    @patch('backend.repositories.activity_repository.Activity')
    def test_get_activities_by_pet(self, mock_activity, mock_pet_activity):
        """Test retrieving activities for a specific pet"""
        # Arrange
        mock_result = [("Walking", 3), ("Playing", 5)]
        
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = mock_result
        
        # Act
        result = ActivityRepository.get_activities_by_pet(self.mock_db, 1)
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("Walking", 3))
        self.assertEqual(result[1], ("Playing", 5))
        
    @patch('backend.repositories.activity_repository.Pet_feeding')
    @patch('backend.repositories.activity_repository.Feeding')
    def test_get_feedings_by_pet(self, mock_feeding, mock_pet_feeding):
        """Test retrieving feedings for a specific pet"""
        # Arrange
        mock_result = [("Dry Food", 2), ("Wet Food", 1)]
        
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = mock_result
        
        # Act
        result = ActivityRepository.get_feedings_by_pet(self.mock_db, 1)
        
        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ("Dry Food", 2))
        self.assertEqual(result[1], ("Wet Food", 1))
        
    @patch('backend.repositories.activity_repository.Pet_activity')
    def test_create_pet_activity_success(self, mock_pet_activity_class):
        """Test successful creation of pet activity"""
        # Arrange
        mock_pet_activity = Mock()
        
        # Act
        result = ActivityRepository.create_pet_activity(self.mock_db, mock_pet_activity)
        
        # Assert
        self.mock_db.add.assert_called_once_with(mock_pet_activity)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(mock_pet_activity)
        self.assertTrue(result)
        
    @patch('backend.repositories.activity_repository.Pet_feeding')
    def test_create_pet_feeding_success(self, mock_pet_feeding_class):
        """Test successful creation of pet feeding"""
        # Arrange
        mock_pet_feeding = Mock()
        
        # Act
        result = ActivityRepository.create_pet_feeding(self.mock_db, mock_pet_feeding)
        
        # Assert
        self.mock_db.add.assert_called_once_with(mock_pet_feeding)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(mock_pet_feeding)
        self.assertTrue(result)
        
    def test_get_activities_by_pet_empty_result(self):
        """Test retrieving activities for pet with no activities"""
        # Arrange
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
        
        # Act
        result = ActivityRepository.get_activities_by_pet(self.mock_db, 999)
        
        # Assert
        self.assertEqual(result, [])
        
    def test_get_feedings_by_pet_empty_result(self):
        """Test retrieving feedings for pet with no feedings"""
        # Arrange
        self.mock_db.query.return_value.join.return_value.filter.return_value.all.return_value = []
        
        # Act
        result = ActivityRepository.get_feedings_by_pet(self.mock_db, 999)
        
        # Assert
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
