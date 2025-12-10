"""
Unit Tests for Topic/Subtopic Management
Tests topic creation, progress tracking, and retrieval.
"""

import unittest
import sys
import os
import tempfile
from unittest.mock import MagicMock

# Add project directory to path
sys.path.insert(0, os.path.abspath('.'))

# Mock torch and transformers
sys.modules['torch'] = MagicMock()
sys.modules['transformers'] = MagicMock()

from enhanced_app_logic import EnhancedAppLogic
from enhanced_database_manager import EnhancedDatabaseManager


class TestTopicManagement(unittest.TestCase):
    """Test suite for topic/subtopic management operations."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_db_fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        self.app_logic = EnhancedAppLogic()
        self.app_logic.db_manager = EnhancedDatabaseManager(db_name=self.test_db_path)
        
        # Register and login a test user
        self.app_logic.register_user("testuser", "testpass123", "test@example.com")
        self.app_logic.login_user("testuser", "testpass123")
    
    def tearDown(self):
        """Clean up test fixtures."""
        try:
            os.close(self.test_db_fd)
            os.unlink(self.test_db_path)
        except Exception:
            pass
    
    # ========== ADD SUBTOPIC TESTS ==========
    
    def test_add_subtopic_success(self):
        """Test adding a subtopic successfully."""
        success, message = self.app_logic.add_subtopic(
            "Python Basics",
            "Computer Science"
        )
        
        self.assertTrue(success)
        self.assertEqual(message, "Topic added successfully")
    
    def test_add_subtopic_no_user(self):
        """Test adding subtopic fails without login."""
        self.app_logic.logout_user()
        success, message = self.app_logic.add_subtopic("Python", "CS")
        
        self.assertFalse(success)
        self.assertEqual(message, "No user logged in")
    
    def test_add_subtopic_empty_topic_name(self):
        """Test adding subtopic fails with empty topic name."""
        success, message = self.app_logic.add_subtopic("", "Subject")
        
        self.assertFalse(success)
        self.assertEqual(message, "Topic name and subject cannot be empty")
    
    def test_add_subtopic_empty_subject(self):
        """Test adding subtopic fails with empty subject."""
        success, message = self.app_logic.add_subtopic("Topic", "")
        
        self.assertFalse(success)
        self.assertEqual(message, "Topic name and subject cannot be empty")
    
    def test_add_subtopic_whitespace_only(self):
        """Test adding subtopic fails with whitespace-only fields."""
        success, message = self.app_logic.add_subtopic("   ", "   ")
        
        self.assertFalse(success)
        self.assertEqual(message, "Topic name and subject cannot be empty")
    
    # ========== GET SUBTOPICS TESTS ==========
    
    def test_get_user_subtopics_empty(self):
        """Test getting subtopics when none exist."""
        subtopics = self.app_logic.get_user_subtopics()
        
        self.assertEqual(len(subtopics), 0)
        self.assertIsInstance(subtopics, list)
    
    def test_get_user_subtopics_multiple(self):
        """Test retrieving multiple subtopics."""
        self.app_logic.add_subtopic("Topic 1", "Subject 1")
        self.app_logic.add_subtopic("Topic 2", "Subject 2")
        self.app_logic.add_subtopic("Topic 3", "Subject 3")
        
        subtopics = self.app_logic.get_user_subtopics()
        
        self.assertEqual(len(subtopics), 3)
        self.assertEqual(subtopics[0]['topic_name'], "Topic 1")
        self.assertEqual(subtopics[0]['subject'], "Subject 1")
        self.assertEqual(subtopics[1]['topic_name'], "Topic 2")
        self.assertEqual(subtopics[2]['topic_name'], "Topic 3")
    
    def test_get_user_subtopics_no_user(self):
        """Test getting subtopics without login."""
        self.app_logic.logout_user()
        subtopics = self.app_logic.get_user_subtopics()
        
        self.assertEqual(len(subtopics), 0)
    
    def test_get_user_subtopics_default_progress(self):
        """Test that new subtopics have 0% progress."""
        self.app_logic.add_subtopic("New Topic", "Subject")
        subtopics = self.app_logic.get_user_subtopics()
        
        self.assertEqual(subtopics[0]['progress'], 0)
    
    # ========== UPDATE PROGRESS TESTS ==========
    
    def test_update_topic_progress_success(self):
        """Test updating topic progress."""
        self.app_logic.add_subtopic("Test Topic", "Test Subject")
        subtopics = self.app_logic.get_user_subtopics()
        topic_id = subtopics[0]['topic_id']
        
        success, message = self.app_logic.update_topic_progress(topic_id, 75)
        self.assertTrue(success)
        self.assertEqual(message, "Progress updated successfully")
        
        subtopics = self.app_logic.get_user_subtopics()
        self.assertEqual(subtopics[0]['progress'], 75)
    
    def test_update_topic_progress_zero(self):
        """Test updating progress to 0%."""
        self.app_logic.add_subtopic("Test Topic", "Test Subject")
        subtopics = self.app_logic.get_user_subtopics()
        topic_id = subtopics[0]['topic_id']
        
        success, message = self.app_logic.update_topic_progress(topic_id, 0)
        self.assertTrue(success)
        
        subtopics = self.app_logic.get_user_subtopics()
        self.assertEqual(subtopics[0]['progress'], 0)
    
    def test_update_topic_progress_hundred(self):
        """Test updating progress to 100%."""
        self.app_logic.add_subtopic("Test Topic", "Test Subject")
        subtopics = self.app_logic.get_user_subtopics()
        topic_id = subtopics[0]['topic_id']
        
        success, message = self.app_logic.update_topic_progress(topic_id, 100)
        self.assertTrue(success)
        
        subtopics = self.app_logic.get_user_subtopics()
        self.assertEqual(subtopics[0]['progress'], 100)
    
    def test_update_topic_progress_below_range(self):
        """Test updating progress fails with value < 0."""
        self.app_logic.add_subtopic("Test Topic", "Test Subject")
        subtopics = self.app_logic.get_user_subtopics()
        topic_id = subtopics[0]['topic_id']
        
        success, message = self.app_logic.update_topic_progress(topic_id, -10)
        
        self.assertFalse(success)
        self.assertEqual(message, "Progress must be between 0 and 100")
    
    def test_update_topic_progress_above_range(self):
        """Test updating progress fails with value > 100."""
        self.app_logic.add_subtopic("Test Topic", "Test Subject")
        subtopics = self.app_logic.get_user_subtopics()
        topic_id = subtopics[0]['topic_id']
        
        success, message = self.app_logic.update_topic_progress(topic_id, 150)
        
        self.assertFalse(success)
        self.assertEqual(message, "Progress must be between 0 and 100")
    
    def test_update_topic_progress_no_user(self):
        """Test updating progress fails without login."""
        self.app_logic.add_subtopic("Test Topic", "Test Subject")
        subtopics = self.app_logic.get_user_subtopics()
        topic_id = subtopics[0]['topic_id']
        
        self.app_logic.logout_user()
        
        success, message = self.app_logic.update_topic_progress(topic_id, 50)
        self.assertFalse(success)
        self.assertEqual(message, "No user logged in")
    
    # ========== CALCULATE PROGRESS TESTS ==========
    
    def test_calculate_total_progress_empty(self):
        """Test calculating progress with no topics."""
        progress = self.app_logic.calculate_total_progress()
        
        self.assertEqual(progress, 0.0)
    
    def test_calculate_total_progress_single(self):
        """Test calculating progress with single topic."""
        self.app_logic.add_subtopic("Topic 1", "Subject 1")
        subtopics = self.app_logic.get_user_subtopics()
        self.app_logic.update_topic_progress(subtopics[0]['topic_id'], 60)
        
        progress = self.app_logic.calculate_total_progress()
        
        self.assertEqual(progress, 60.0)
    
    def test_calculate_total_progress_multiple(self):
        """Test calculating average progress across multiple topics."""
        self.app_logic.add_subtopic("Topic 1", "Subject 1")
        self.app_logic.add_subtopic("Topic 2", "Subject 2")
        self.app_logic.add_subtopic("Topic 3", "Subject 3")
        
        subtopics = self.app_logic.get_user_subtopics()
        self.app_logic.update_topic_progress(subtopics[0]['topic_id'], 50)
        self.app_logic.update_topic_progress(subtopics[1]['topic_id'], 100)
        self.app_logic.update_topic_progress(subtopics[2]['topic_id'], 25)
        
        progress = self.app_logic.calculate_total_progress()
        
        # Average of 50, 100, 25 = 58.333...
        self.assertAlmostEqual(progress, 58.333, places=2)
    
    def test_calculate_total_progress_no_user(self):
        """Test calculating progress without login."""
        self.app_logic.logout_user()
        progress = self.app_logic.calculate_total_progress()
        
        self.assertEqual(progress, 0.0)
    
    # ========== USER ISOLATION TESTS ==========
    
    def test_subtopics_user_isolation(self):
        """Test that users can't see each other's subtopics."""
        # Add subtopic for user 1
        self.app_logic.add_subtopic("User1 Topic", "Subject")
        user1_topics = len(self.app_logic.get_user_subtopics())
        self.app_logic.logout_user()
        
        # Register and login as user 2
        self.app_logic.register_user("user2", "pass123", "user2@test.com")
        self.app_logic.login_user("user2", "pass123")
        user2_topics = len(self.app_logic.get_user_subtopics())
        
        self.assertEqual(user1_topics, 1)
        self.assertEqual(user2_topics, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)