import unittest
from unittest.mock import Mock, patch
from datetime import date

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.models.pet import Pet


class TestPetModel(unittest.TestCase):
    """Test cases for Pet model class"""
    
    def test_calculate_age_same_year_before_birthday(self):
        """Test age calculation for same year before birthday"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is December 1, 2024 (hasn't happened yet)
            birthdate = date(2024, 12, 1)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert - Should be -1 (not born yet, but method handles this)
            self.assertEqual(age, -1)
            
    def test_calculate_age_same_year_after_birthday(self):
        """Test age calculation for same year after birthday"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is January 1, 2024 (already happened)
            birthdate = date(2024, 1, 1)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 0)
            
    def test_calculate_age_previous_year(self):
        """Test age calculation for pet born in previous year"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is July 15, 2023 (exactly 1 year ago)
            birthdate = date(2023, 7, 15)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 1)
            
    def test_calculate_age_multiple_years_birthday_passed(self):
        """Test age calculation for multiple years with birthday already passed"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is June 1, 2020 (birthday already passed this year)
            birthdate = date(2020, 6, 1)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 4)
            
    def test_calculate_age_multiple_years_birthday_not_passed(self):
        """Test age calculation for multiple years with birthday not yet passed"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is August 1, 2020 (birthday not yet passed this year)
            birthdate = date(2020, 8, 1)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 3)  # Not yet 4 because birthday hasn't occurred
            
    def test_calculate_age_leap_year_birthday(self):
        """Test age calculation for leap year birthday"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to March 1, 2024
            mock_date.today.return_value = date(2024, 3, 1)
            # Birthday is February 29, 2020 (leap year)
            birthdate = date(2020, 2, 29)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 4)
            
    def test_calculate_age_today_is_birthday(self):
        """Test age calculation when today is the birthday"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is July 15, 2021 (exactly 3 years ago)
            birthdate = date(2021, 7, 15)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 3)
            
    def test_calculate_age_new_year_edge_case(self):
        """Test age calculation around new year"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to January 1, 2024
            mock_date.today.return_value = date(2024, 1, 1)
            # Birthday is December 31, 2020
            birthdate = date(2020, 12, 31)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 3)
            
    def test_calculate_age_very_old_pet(self):
        """Test age calculation for very old pet"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is July 15, 2004 (20 years ago)
            birthdate = date(2004, 7, 15)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 20)
            
    def test_calculate_age_newborn_pet(self):
        """Test age calculation for newborn pet"""
        # Arrange
        with patch('backend.models.pet.date') as mock_date:
            # Set today to July 15, 2024
            mock_date.today.return_value = date(2024, 7, 15)
            # Birthday is today
            birthdate = date(2024, 7, 15)
            
            # Act
            age = Pet.calculate_age(birthdate)
            
            # Assert
            self.assertEqual(age, 0)


if __name__ == '__main__':
    unittest.main()
