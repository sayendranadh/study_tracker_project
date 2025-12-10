"""
Unit Tests for Task Management
Tests task creation, retrieval, toggling, and deletion.
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


class TestTaskManagement(unittest.TestCase):
    """Test suite for task management operations."""
    
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
    
    # ========== ADD TASK TESTS ==========
    
    def test_add_task_success(self):
        """Test adding a task successfully."""
        success, message = self.app_logic.add_task(
            "Complete homework",
            "2025-12-31",
            "high"
        )
        
        self.assertTrue(success)
        self.assertEqual(message, "Task added successfully")
    
    def test_add_task_minimal_params(self):
        """Test adding task with only required parameters."""
        success, message = self.app_logic.add_task("Simple task")
        
        self.assertTrue(success)
        self.assertEqual(message, "Task added successfully")
    
    def test_add_task_no_user(self):
        """Test adding task fails without login."""
        self.app_logic.logout_user()
        success, message = self.app_logic.add_task("Task")
        
        self.assertFalse(success)
        self.assertEqual(message, "No user logged in")
    
    def test_add_task_empty_text(self):
        """Test adding task fails with empty text."""
        success, message = self.app_logic.add_task("   ")
        
        self.assertFalse(success)
        self.assertEqual(message, "Task text cannot be empty")
    
    # ========== GET TASKS TESTS ==========
    
    def test_get_tasks_empty(self):
        """Test getting tasks when none exist."""
        tasks = self.app_logic.get_tasks()
        
        self.assertEqual(len(tasks), 0)
        self.assertIsInstance(tasks, list)
    
    def test_get_tasks_multiple(self):
        """Test retrieving multiple tasks."""
        self.app_logic.add_task("Task 1")
        self.app_logic.add_task("Task 2")
        self.app_logic.add_task("Task 3")
        
        tasks = self.app_logic.get_tasks()
        
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]['task_text'], "Task 1")
        self.assertEqual(tasks[1]['task_text'], "Task 2")
        self.assertEqual(tasks[2]['task_text'], "Task 3")
    
    def test_get_tasks_exclude_completed(self):
        """Test filtering out completed tasks."""
        self.app_logic.add_task("Task 1")
        self.app_logic.add_task("Task 2")
        
        tasks = self.app_logic.get_tasks()
        self.app_logic.toggle_task(tasks[0]['task_id'])
        
        pending_tasks = self.app_logic.get_tasks(include_completed=False)
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0]['task_text'], "Task 2")
    
    def test_get_tasks_no_user(self):
        """Test getting tasks without login."""
        self.app_logic.logout_user()
        tasks = self.app_logic.get_tasks()
        
        self.assertEqual(len(tasks), 0)
    
    # ========== TOGGLE TASK TESTS ==========
    
    def test_toggle_task_complete(self):
        """Test toggling task to completed."""
        self.app_logic.add_task("Test task")
        tasks = self.app_logic.get_tasks()
        task_id = tasks[0]['task_id']
        
        self.assertEqual(tasks[0]['is_completed'], 0)
        
        success, message = self.app_logic.toggle_task(task_id)
        self.assertTrue(success)
        
        tasks = self.app_logic.get_tasks()
        self.assertEqual(tasks[0]['is_completed'], 1)
    
    def test_toggle_task_uncomplete(self):
        """Test toggling completed task back to pending."""
        self.app_logic.add_task("Test task")
        tasks = self.app_logic.get_tasks()
        task_id = tasks[0]['task_id']
        
        # Complete it
        self.app_logic.toggle_task(task_id)
        tasks = self.app_logic.get_tasks()
        self.assertEqual(tasks[0]['is_completed'], 1)
        
        # Uncomplete it
        success, message = self.app_logic.toggle_task(task_id)
        self.assertTrue(success)
        
        tasks = self.app_logic.get_tasks()
        self.assertEqual(tasks[0]['is_completed'], 0)
    
    def test_toggle_task_no_user(self):
        """Test toggling task without login."""
        self.app_logic.add_task("Task")
        tasks = self.app_logic.get_tasks()
        task_id = tasks[0]['task_id']
        
        self.app_logic.logout_user()
        
        success, message = self.app_logic.toggle_task(task_id)
        self.assertFalse(success)
        self.assertEqual(message, "No user logged in")
    
    # ========== DELETE TASK TESTS ==========
    
    def test_delete_task_success(self):
        """Test deleting a task."""
        self.app_logic.add_task("Task to delete")
        tasks = self.app_logic.get_tasks()
        self.assertEqual(len(tasks), 1)
        task_id = tasks[0]['task_id']
        
        success, message = self.app_logic.delete_task(task_id)
        self.assertTrue(success)
        self.assertEqual(message, "Task deleted successfully")
        
        tasks = self.app_logic.get_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_delete_task_no_user(self):
        """Test deleting task without login."""
        self.app_logic.add_task("Task")
        tasks = self.app_logic.get_tasks()
        task_id = tasks[0]['task_id']
        
        self.app_logic.logout_user()
        
        success, message = self.app_logic.delete_task(task_id)
        self.assertFalse(success)
        self.assertEqual(message, "No user logged in")
    
    # ========== TASK PRIORITY TESTS ==========
    
    def test_add_task_with_priority(self):
        """Test adding tasks with different priorities."""
        self.app_logic.add_task("High priority", priority="high")
        self.app_logic.add_task("Low priority", priority="low")
        self.app_logic.add_task("Medium priority", priority="medium")
        
        tasks = self.app_logic.get_tasks()
        
        self.assertEqual(len(tasks), 3)
        priorities = [t['priority'] for t in tasks]
        self.assertIn("high", priorities)
        self.assertIn("low", priorities)
        self.assertIn("medium", priorities)


if __name__ == "__main__":
    unittest.main(verbosity=2)