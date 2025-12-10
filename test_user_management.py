"""
Unit Tests for User Management
Tests user registration, login, and logout functionality.
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import MagicMock

# Add project directory to path
sys.path.insert(0, os.path.abspath('.'))

# Mock torch and transformers to avoid dependency issues
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()

from enhanced_app_logic import EnhancedAppLogic
from enhanced_database_manager import EnhancedDatabaseManager


class TestUserManagement(unittest.TestCase):
    """Test suite for user management operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_db_fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        self.app_logic = EnhancedAppLogic()
        self.app_logic.db_manager = EnhancedDatabaseManager(db_name=self.test_db_path)
        
        self.test_username = "testuser"
        self.test_password = "testpass123"
        self.test_email = "test@example.com"
    
    def tearDown(self):
        """Clean up test fixtures."""
        try:
            os.close(self.test_db_fd)
            os.unlink(self.test_db_path)
        except Exception:
            pass
    
    # ========== REGISTRATION TESTS ==========
    
    def test_register_user_success(self):
        """Test successful user registration."""
        success, message = self.app_logic.register_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        self.assertTrue(success)
        self.assertEqual(message, "User registered successfully")
    
    def test_register_user_short_username(self):
        """Test registration fails with short username."""
        success, message = self.app_logic.register_user(
            "ab",
            self.test_password,
            self.test_email
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Username must be at least 3 characters long")
    
    def test_register_user_short_password(self):
        """Test registration fails with short password."""
        success, message = self.app_logic.register_user(
            self.test_username,
            "12345",
            self.test_email
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Password must be at least 6 characters long")
    
    def test_register_user_invalid_email(self):
        """Test registration fails with invalid email."""
        success, message = self.app_logic.register_user(
            self.test_username,
            self.test_password,
            "invalidemail"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Please enter a valid email address")
    
    def test_register_user_duplicate_username(self):
        """Test registration fails with duplicate username."""
        self.app_logic.register_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        success, message = self.app_logic.register_user(
            self.test_username,
            "different_pass",
            "different@example.com"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Username already exists")
    
    # ========== LOGIN TESTS ==========
    
    def test_login_user_success(self):
        """Test successful login."""
        self.app_logic.register_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        success, message = self.app_logic.login_user(
            self.test_username,
            self.test_password
        )
        
        self.assertTrue(success)
        self.assertEqual(message, "Login successful")
        self.assertIsNotNone(self.app_logic.current_user)
    
    def test_login_user_wrong_password(self):
        """Test login fails with wrong password."""
        self.app_logic.register_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        success, message = self.app_logic.login_user(
            self.test_username,
            "wrongpassword"
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Invalid password")
        self.assertIsNone(self.app_logic.current_user)
    
    def test_login_user_nonexistent(self):
        """Test login fails with non-existent username."""
        success, message = self.app_logic.login_user(
            "nonexistent",
            self.test_password
        )
        
        self.assertFalse(success)
        self.assertEqual(message, "Username not found")
        self.assertIsNone(self.app_logic.current_user)
    
    # ========== LOGOUT TESTS ==========
    
    def test_logout_user(self):
        """Test user logout."""
        self.app_logic.register_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        self.app_logic.login_user(self.test_username, self.test_password)
        
        self.assertIsNotNone(self.app_logic.current_user)
        
        self.app_logic.logout_user()
        
        self.assertIsNone(self.app_logic.current_user)
    
    def test_get_current_user(self):
        """Test getting current user."""
        self.assertIsNone(self.app_logic.get_current_user())
        
        self.app_logic.register_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        self.app_logic.login_user(self.test_username, self.test_password)
        
        current_user = self.app_logic.get_current_user()
        self.assertIsNotNone(current_user)
        self.assertEqual(current_user['username'], self.test_username)
    
    def test_password_hashing(self):
        """Test that passwords are hashed."""
        self.app_logic.register_user("testuser", "password123", "test@test.com")
        
        user = self.app_logic.db_manager.get_user_by_username("testuser")
        
        self.assertNotEqual(user['password_hash'], "password123")
        self.assertTrue(len(user['password_hash']) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)