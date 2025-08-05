import unittest
from unittest.mock import patch

# Imports del código a testear
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from backend.utils.auth_utils import hash_password, verify_password


class TestAuthUtils(unittest.TestCase):
    """Test cases for auth_utils utility functions"""
    
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        # Arrange
        password = "test_password_123"
        
        # Act
        hashed = hash_password(password)
        
        # Assert
        self.assertIsInstance(hashed, str)
        self.assertNotEqual(hashed, password)
        self.assertTrue(len(hashed) > 0)
        
    def test_hash_password_different_hashes(self):
        """Test that same password generates different hashes due to salt"""
        # Arrange
        password = "same_password"
        
        # Act
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Assert
        self.assertNotEqual(hash1, hash2)
        
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        # Arrange
        password = "my_secure_password"
        hashed = hash_password(password)
        
        # Act
        is_valid = verify_password(password, hashed)
        
        # Assert
        self.assertTrue(is_valid)
        
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        # Arrange
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        hashed = hash_password(correct_password)
        
        # Act
        is_valid = verify_password(wrong_password, hashed)
        
        # Assert
        self.assertFalse(is_valid)
        
    def test_verify_password_empty_password(self):
        """Test password verification with empty password"""
        # Arrange
        password = "non_empty_password"
        hashed = hash_password(password)
        empty_password = ""
        
        # Act
        is_valid = verify_password(empty_password, hashed)
        
        # Assert
        self.assertFalse(is_valid)
        
    def test_verify_password_special_characters(self):
        """Test password verification with special characters"""
        # Arrange
        password = "P@ssw0rd!#$%^&*()"
        hashed = hash_password(password)
        
        # Act
        is_valid = verify_password(password, hashed)
        
        # Assert
        self.assertTrue(is_valid)
        
    def test_verify_password_unicode_characters(self):
        """Test password verification with unicode characters"""
        # Arrange
        password = "contraseña_测试_🔒"
        hashed = hash_password(password)
        
        # Act
        is_valid = verify_password(password, hashed)
        
        # Assert
        self.assertTrue(is_valid)
        
    def test_hash_password_long_password(self):
        """Test hashing a very long password"""
        # Arrange
        password = "a" * 1000  # 1000 character password
        
        # Act
        hashed = hash_password(password)
        is_valid = verify_password(password, hashed)
        
        # Assert
        self.assertIsInstance(hashed, str)
        self.assertTrue(is_valid)
        
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case sensitive"""
        # Arrange
        password = "CaseSensitive"
        hashed = hash_password(password)
        wrong_case = "casesensitive"
        
        # Act
        is_valid = verify_password(wrong_case, hashed)
        
        # Assert
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
