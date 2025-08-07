import unittest
from unittest.mock import Mock, patch
from datetime import date

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.services.activity_service import ActivityService
from backend.schemas.activity import ActivityCreate, FeedingCreate
from backend.models.relationships import Pet_activity, Pet_feeding


class TestActivityService(unittest.TestCase):
    """Test cases for ActivityService class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_db = Mock()
        
        self.sample_activity_data = ActivityCreate(
            pet_id=1,
            activity_id=1,
            frequency=3
        )
        
        self.sample_feeding_data = FeedingCreate(
            pet_id=1,
            feeding_id=1,
            frequency=2
        )
        
    @patch('backend.services.activity_service.ActivityRepository')
    @patch('backend.services.activity_service.Pet_activity')
    def test_create_pet_activity_success(self, mock_pet_activity_class, mock_activity_repo):
        """Test successful pet activity creation"""
        # Arrange
        mock_pet_activity_instance = Mock()
        mock_pet_activity_class.return_value = mock_pet_activity_instance
        mock_activity_repo.create_pet_activity.return_value = True
        
        # Act
        result = ActivityService.create_pet_activity(self.mock_db, self.sample_activity_data)
        
        # Assert
        mock_pet_activity_class.assert_called_once_with(
            pet_id=1,
            activity_id=1,
            weekly_frequency_activity=3
        )
        mock_activity_repo.create_pet_activity.assert_called_once_with(
            self.mock_db, mock_pet_activity_instance
        )
        self.assertTrue(result)
        
    @patch('backend.services.activity_service.ActivityRepository')
    @patch('backend.services.activity_service.Pet_feeding')
    def test_create_pet_feeding_success(self, mock_pet_feeding_class, mock_activity_repo):
        """Test successful pet feeding creation"""
        # Arrange
        mock_pet_feeding_instance = Mock()
        mock_pet_feeding_class.return_value = mock_pet_feeding_instance
        mock_activity_repo.create_pet_feeding.return_value = True
        
        # Act
        result = ActivityService.create_pet_feeding(self.mock_db, self.sample_feeding_data)
        
        # Assert
        mock_pet_feeding_class.assert_called_once_with(
            pet_id=1,
            feeding_id=1,
            daily_meal_frequency=2
        )
        mock_activity_repo.create_pet_feeding.assert_called_once_with(
            self.mock_db, mock_pet_feeding_instance
        )
        self.assertTrue(result)
        
    @patch('backend.services.activity_service.ActivityRepository')
    def test_get_activities_by_pet(self, mock_activity_repo):
        """Test retrieving activities by pet"""
        # Arrange
        mock_activities = [("Walking", 3), ("Playing", 5)]
        mock_activity_repo.get_activities_by_pet.return_value = mock_activities
        
        # Act
        result = ActivityService.get_activities_by_pet(self.mock_db, 1)
        
        # Assert
        mock_activity_repo.get_activities_by_pet.assert_called_once_with(self.mock_db, 1)
        self.assertEqual(result, mock_activities)
        
    @patch('backend.services.activity_service.ActivityRepository')
    def test_get_feedings_by_pet(self, mock_activity_repo):
        """Test retrieving feedings by pet"""
        # Arrange
        mock_feedings = [("Dry Food", 2), ("Wet Food", 1)]
        mock_activity_repo.get_feedings_by_pet.return_value = mock_feedings
        
        # Act
        result = ActivityService.get_feedings_by_pet(self.mock_db, 1)
        
        # Assert
        mock_activity_repo.get_feedings_by_pet.assert_called_once_with(self.mock_db, 1)
        self.assertEqual(result, mock_feedings)
        
    @patch('backend.services.activity_service.ActivityRepository')
    def test_get_all_activities(self, mock_activity_repo):
        """Test retrieving all activities"""
        # Arrange
        mock_activity1 = Mock()
        mock_activity1.name = "Walking"
        mock_activity2 = Mock()
        mock_activity2.name = "Playing"
        mock_activities = [mock_activity1, mock_activity2]
        mock_activity_repo.get_activities.return_value = mock_activities
        
        # Act
        result = ActivityService.get_all_activities(self.mock_db)
        
        # Assert
        mock_activity_repo.get_activities.assert_called_once_with(self.mock_db)
        self.assertEqual(result, mock_activities)
        
    @patch('backend.services.activity_service.ActivityRepository')
    def test_get_all_feedings(self, mock_activity_repo):
        """Test retrieving all feedings"""
        # Arrange
        mock_feeding1 = Mock()
        mock_feeding1.name = "Dry Food"
        mock_feeding2 = Mock()
        mock_feeding2.name = "Wet Food"
        mock_feedings = [mock_feeding1, mock_feeding2]
        mock_activity_repo.get_feedings.return_value = mock_feedings
        
        # Act
        result = ActivityService.get_all_feedings(self.mock_db)
        
        # Assert
        mock_activity_repo.get_feedings.assert_called_once_with(self.mock_db)
        self.assertEqual(result, mock_feedings)


if __name__ == '__main__':
    unittest.main()
