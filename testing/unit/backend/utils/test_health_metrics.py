import unittest
from unittest.mock import Mock, patch
from datetime import date

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.utils.health_metrics import (
    calculate_age,
    calculate_bmi,
    calculate_health_metrics
)


class TestHealthMetrics(unittest.TestCase):
    """Test cases for health_metrics utility functions"""
    
    def test_calculate_age_same_year(self):
        """Test age calculation for same year"""
        # Arrange
        today = date.today()
        birthdate = date(today.year, 1, 1)
        
        # Act
        age = calculate_age(birthdate)
        
        # Assert
        expected_age = 0 if today.month == 1 and today.day == 1 else 0
        self.assertEqual(age, 0)
        
    def test_calculate_age_previous_year(self):
        """Test age calculation for previous year"""
        # Arrange
        today = date.today()
        birthdate = date(today.year - 5, today.month, today.day)
        
        # Act
        age = calculate_age(birthdate)
        
        # Assert
        self.assertEqual(age, 5)
        
    def test_calculate_age_birthday_not_reached(self):
        """Test age calculation when birthday hasn't occurred this year"""
        # Arrange
        today = date.today()
        if today.month == 12:
            # If current month is December, use January for future birthday
            birthdate = date(today.year - 5, 1, 1)
            expected_age = 5
        else:
            # Use next month for future birthday
            birthdate = date(today.year - 5, today.month + 1, today.day)
            expected_age = 4
        
        # Act
        age = calculate_age(birthdate)
        
        # Assert
        self.assertEqual(age, expected_age)
        
    def test_calculate_bmi_valid_inputs(self):
        """Test BMI calculation with valid inputs"""
        # Arrange
        weight = 25.0  # kg
        height = 0.5   # meters
        
        # Act
        bmi = calculate_bmi(weight, height)
        
        # Assert
        expected_bmi = 25.0 / (0.5 ** 2)  # 100.0
        self.assertEqual(bmi, expected_bmi)
        
    def test_calculate_bmi_zero_height(self):
        """Test BMI calculation with zero height"""
        # Arrange
        weight = 25.0
        height = 0.0
        
        # Act
        bmi = calculate_bmi(weight, height)
        
        # Assert
        self.assertEqual(bmi, 0.0)
        
    def test_calculate_bmi_negative_height(self):
        """Test BMI calculation with negative height"""
        # Arrange
        weight = 25.0
        height = -0.5
        
        # Act
        bmi = calculate_bmi(weight, height)
        
        # Assert
        self.assertEqual(bmi, 0.0)
        
    def test_calculate_health_metrics_dog_healthy(self):
        """Test health metrics calculation for healthy dog"""
        # Arrange
        pet_data = {
            'weight': 25.0,
            'height': 1.0,  # 1 meter
            'age': 5,
            'species': 'dog'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 25.0)
        self.assertEqual(metrics['status'], 'Healthy')
        self.assertEqual(metrics['weight'], 25.0)
        self.assertEqual(metrics['height'], 1.0)
        self.assertEqual(metrics['age'], 5)
        
    def test_calculate_health_metrics_dog_underweight(self):
        """Test health metrics calculation for underweight dog"""
        # Arrange
        pet_data = {
            'weight': 10.0,
            'height': 1.0,
            'age': 3,
            'species': 'dog'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 10.0)
        self.assertEqual(metrics['status'], 'Underweight')
        
    def test_calculate_health_metrics_dog_overweight(self):
        """Test health metrics calculation for overweight dog"""
        # Arrange
        pet_data = {
            'weight': 28.0,
            'height': 1.0,
            'age': 7,
            'species': 'dog'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 28.0)
        self.assertEqual(metrics['status'], 'Overweight')
        
    def test_calculate_health_metrics_dog_obese(self):
        """Test health metrics calculation for obese dog"""
        # Arrange
        pet_data = {
            'weight': 35.0,
            'height': 1.0,
            'age': 8,
            'species': 'dog'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 35.0)
        self.assertEqual(metrics['status'], 'Obese')
        
    def test_calculate_health_metrics_cat_healthy(self):
        """Test health metrics calculation for healthy cat"""
        # Arrange
        pet_data = {
            'weight': 22.0,
            'height': 1.0,
            'age': 4,
            'species': 'cat'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 22.0)
        self.assertEqual(metrics['status'], 'Healthy')
        
    def test_calculate_health_metrics_cat_underweight(self):
        """Test health metrics calculation for underweight cat"""
        # Arrange
        pet_data = {
            'weight': 15.0,
            'height': 1.0,
            'age': 2,
            'species': 'cat'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 15.0)
        self.assertEqual(metrics['status'], 'Underweight')
        
    def test_calculate_health_metrics_cat_overweight(self):
        """Test health metrics calculation for overweight cat"""
        # Arrange
        pet_data = {
            'weight': 30.0,
            'height': 1.0,
            'age': 6,
            'species': 'cat'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 30.0)
        self.assertEqual(metrics['status'], 'Overweight')
        
    def test_calculate_health_metrics_cat_obese(self):
        """Test health metrics calculation for obese cat"""
        # Arrange
        pet_data = {
            'weight': 35.0,
            'height': 1.0,
            'age': 9,
            'species': 'cat'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 35.0)
        self.assertEqual(metrics['status'], 'Obese')
        
    def test_calculate_health_metrics_unknown_species(self):
        """Test health metrics calculation for unknown species"""
        # Arrange
        pet_data = {
            'weight': 20.0,
            'height': 1.0,
            'age': 3,
            'species': 'bird'
        }
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 20.0)
        self.assertEqual(metrics['status'], 'Unknown')
        
    def test_calculate_health_metrics_missing_data(self):
        """Test health metrics calculation with missing data"""
        # Arrange
        pet_data = {}
        
        # Act
        metrics = calculate_health_metrics(pet_data)
        
        # Assert
        self.assertEqual(metrics['bmi'], 0.0)
        self.assertEqual(metrics['status'], 'Unknown')
        self.assertEqual(metrics['weight'], 0.0)
        self.assertEqual(metrics['height'], 0.0)
        self.assertEqual(metrics['age'], 0)


if __name__ == '__main__':
    unittest.main()
