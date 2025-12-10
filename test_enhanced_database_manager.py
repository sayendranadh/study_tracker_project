"""
Unit Tests for EnhancedDatabaseManager Class
Tests database operations including user management, exam operations, and data integrity.
"""

import unittest
import os
import tempfile
import json
from datetime import date
import sys

# Add project directory to path
sys.path.insert(0, '/mnt/project')

from enhanced_database_manager import EnhancedDatabaseManager


class TestEnhancedDatabaseManager(unittest.TestCase):
    """
    Test suite for the EnhancedDatabaseManager class.
    Tests all major database operations with various scenarios.
    """
    
    def setUp(self):
        """
        Set up test fixtures.
        Creates a temporary database for each test to ensure isolation.
        """
        # Create a temporary database file
        self.test_db_fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        self.db_manager = EnhancedDatabaseManager(db_name=self.test_db_path)
        
        # Create a test user for most tests
        self.test_username = "testuser"
        self.test_password = "testpass123"
        self.test_email = "test@example.com"
        
        self.db_manager.create_user(
            self.test_username,
            self.test_password,
            self.test_email
        )
        
        self.test_user = self.db_manager.get_user_by_username(self.test_username)
        self.test_user_id = self.test_user['user_id']
    
    def tearDown(self):
        """
        Clean up after each test.
        Removes the temporary database file.
        """
        try:
            os.close(self.test_db_fd)
            os.unlink(self.test_db_path)
        except Exception:
            pass
    
    # ========== USER MANAGEMENT TESTS ==========
    
    def test_create_user_success(self):
        """Test successful user creation."""
        result = self.db_manager.create_user(
            "newuser",
            "password123",
            "newuser@example.com"
        )
        self.assertTrue(result)
        
        # Verify user exists
        user = self.db_manager.get_user_by_username("newuser")
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], "newuser")
        self.assertEqual(user['email'], "newuser@example.com")
    
    def test_create_user_duplicate_username(self):
        """Test that creating user with duplicate username raises error."""
        with self.assertRaises(Exception):
            self.db_manager.create_user(
                self.test_username,  # Duplicate username
                "different_password",
                "different@example.com"
            )
    
    def test_create_user_duplicate_email(self):
        """Test that creating user with duplicate email raises error."""
        with self.assertRaises(Exception):
            self.db_manager.create_user(
                "different_username",
                "password123",
                self.test_email  # Duplicate email
            )
    
    def test_get_user_by_username_exists(self):
        """Test retrieving an existing user."""
        user = self.db_manager.get_user_by_username(self.test_username)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], self.test_username)
        self.assertIn('user_id', user)
        self.assertIn('password_hash', user)
    
    def test_get_user_by_username_not_exists(self):
        """Test retrieving a non-existent user returns None."""
        user = self.db_manager.get_user_by_username("nonexistent_user")
        self.assertIsNone(user)
    
    def test_hash_password_consistency(self):
        """Test that hashing the same password produces the same hash."""
        hash1 = self.db_manager.hash_password("testpassword")
        hash2 = self.db_manager.hash_password("testpassword")
        self.assertEqual(hash1, hash2)
    
    def test_hash_password_different(self):
        """Test that different passwords produce different hashes."""
        hash1 = self.db_manager.hash_password("password1")
        hash2 = self.db_manager.hash_password("password2")
        self.assertNotEqual(hash1, hash2)
    
    # ========== SUBTOPIC TESTS ==========
    
    def test_add_subtopic_success(self):
        """Test adding a new subtopic."""
        result = self.db_manager.add_subtopic(
            self.test_user_id,
            "Python Basics",
            "Computer Science"
        )
        self.assertTrue(result)
        
        # Verify subtopic exists
        subtopics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        self.assertEqual(len(subtopics), 1)
        self.assertEqual(subtopics[0]['topic_name'], "Python Basics")
        self.assertEqual(subtopics[0]['subject'], "Computer Science")
    
    def test_get_subtopics_empty(self):
        """Test getting subtopics when none exist."""
        subtopics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        self.assertEqual(len(subtopics), 0)
    
    def test_update_subtopic_progress(self):
        """Test updating subtopic progress."""
        # Add a subtopic first
        self.db_manager.add_subtopic(
            self.test_user_id,
            "Data Structures",
            "Computer Science"
        )
        
        subtopics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        topic_id = subtopics[0]['topic_id']
        
        # Update progress
        result = self.db_manager.update_subtopic_progress(topic_id, 75)
        self.assertTrue(result)
        
        # Verify update
        subtopics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        self.assertEqual(subtopics[0]['progress'], 75)
    
    # ========== EXAM TESTS ==========
    
    def test_create_exam_success(self):
        """Test creating a new exam."""
        # Add a topic first
        self.db_manager.add_subtopic(
            self.test_user_id,
            "Arrays",
            "Data Structures"
        )
        
        topics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        topic_id = topics[0]['topic_id']
        
        # Create exam
        questions = [
            {
                'question': 'What is an array?',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'A',
                'explanation': 'Arrays are data structures'
            }
        ]
        
        exam_id = self.db_manager.create_exam(
            self.test_user_id,
            topic_id,
            questions
        )
        
        self.assertIsNotNone(exam_id)
        self.assertGreater(exam_id, 0)
    
    def test_submit_exam_calculates_score(self):
        """Test exam submission and score calculation."""
        # Create exam
        self.db_manager.add_subtopic(
            self.test_user_id,
            "Testing",
            "Software Engineering"
        )
        
        topics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        topic_id = topics[0]['topic_id']
        
        questions = [
            {
                'question': 'Q1?',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'A',
                'explanation': 'Explanation'
            },
            {
                'question': 'Q2?',
                'options': ['A', 'B', 'C', 'D'],
                'correct_answer': 'B',
                'explanation': 'Explanation'
            }
        ]
        
        exam_id = self.db_manager.create_exam(
            self.test_user_id,
            topic_id,
            questions
        )
        
        # Submit answers (1 correct, 1 incorrect)
        user_answers = {
            0: 'A',  # Correct
            1: 'C'   # Incorrect
        }
        
        result = self.db_manager.submit_exam(exam_id, user_answers)
        self.assertTrue(result)
        
        # Verify score
        exam = self.db_manager.get_exam_by_id(exam_id)
        self.assertEqual(exam['score'], 50.0)  # 1 out of 2 correct
        self.assertEqual(exam['is_completed'], 1)
    
    def test_get_exam_history(self):
        """Test retrieving exam history."""
        # Initially empty
        history = self.db_manager.get_exam_history(self.test_user_id)
        self.assertEqual(len(history), 0)
        
        # Create and submit an exam
        self.db_manager.add_subtopic(
            self.test_user_id,
            "History Topic",
            "Subject"
        )
        
        topics = self.db_manager.get_subtopics_by_user(self.test_user_id)
        topic_id = topics[0]['topic_id']
        
        questions = [{'question': 'Q?', 'options': ['A', 'B'], 'correct_answer': 'A', 'explanation': 'E'}]
        exam_id = self.db_manager.create_exam(self.test_user_id, topic_id, questions)
        self.db_manager.submit_exam(exam_id, {0: 'A'})
        
        # Verify history
        history = self.db_manager.get_exam_history(self.test_user_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['score'], 100.0)
    
    # ========== TASK TESTS ==========
    
    def test_add_task_success(self):
        """Test adding a new task."""
        result = self.db_manager.add_task(
            self.test_user_id,
            "Complete assignment",
            "2025-12-31",
            "high"
        )
        self.assertTrue(result)
        
        # Verify task exists
        tasks = self.db_manager.get_tasks(self.test_user_id)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['task_text'], "Complete assignment")
    
    def test_toggle_task_completion(self):
        """Test toggling task completion status."""
        # Add task
        self.db_manager.add_task(
            self.test_user_id,
            "Test task",
            None,
            "medium"
        )
        
        tasks = self.db_manager.get_tasks(self.test_user_id)
        task_id = tasks[0]['task_id']
        
        # Initially not completed
        self.assertEqual(tasks[0]['is_completed'], 0)
        
        # Toggle to completed
        self.db_manager.toggle_task(task_id)
        tasks = self.db_manager.get_tasks(self.test_user_id)
        self.assertEqual(tasks[0]['is_completed'], 1)
        
        # Toggle back to not completed
        self.db_manager.toggle_task(task_id)
        tasks = self.db_manager.get_tasks(self.test_user_id)
        self.assertEqual(tasks[0]['is_completed'], 0)
    
    def test_delete_task(self):
        """Test deleting a task."""
        # Add task
        self.db_manager.add_task(
            self.test_user_id,
            "Task to delete",
            None,
            "low"
        )
        
        tasks = self.db_manager.get_tasks(self.test_user_id)
        self.assertEqual(len(tasks), 1)
        task_id = tasks[0]['task_id']
        
        # Delete task
        result = self.db_manager.delete_task(task_id)
        self.assertTrue(result)
        
        # Verify deletion
        tasks = self.db_manager.get_tasks(self.test_user_id)
        self.assertEqual(len(tasks), 0)
    
    # ========== STREAK TESTS ==========
    
    def test_update_streak(self):
        """Test updating activity streak."""
        result = self.db_manager.update_streak(self.test_user_id)
        self.assertTrue(result)
        
        # Verify streak data
        streak_data = self.db_manager.get_streak_data(self.test_user_id)
        today = date.today().isoformat()
        self.assertIn(today, streak_data)
        self.assertGreaterEqual(streak_data[today], 1)
    
    def test_get_current_streak(self):
        """Test getting current streak count."""
        # Update streak for today
        self.db_manager.update_streak(self.test_user_id)
        
        # Get streak
        streak = self.db_manager.get_current_streak(self.test_user_id)
        self.assertEqual(streak, 1)
    
    # ========== CODE SNIPPET TESTS ==========
    
    def test_save_snippet(self):
        """Test saving a code snippet."""
        result = self.db_manager.save_snippet(
            self.test_user_id,
            "Hello World",
            "python",
            "print('Hello, World!')",
            "Basic Python print"
        )
        self.assertTrue(result)
        
        # Verify snippet
        snippets = self.db_manager.get_snippets(self.test_user_id)
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]['title'], "Hello World")
    
    def test_get_snippets_by_language(self):
        """Test filtering snippets by language."""
        # Add multiple snippets
        self.db_manager.save_snippet(
            self.test_user_id,
            "Python Code",
            "python",
            "print('Python')",
            None
        )
        
        self.db_manager.save_snippet(
            self.test_user_id,
            "JavaScript Code",
            "javascript",
            "console.log('JS')",
            None
        )
        
        # Get Python snippets only
        python_snippets = self.db_manager.get_snippets(self.test_user_id, "python")
        self.assertEqual(len(python_snippets), 1)
        self.assertEqual(python_snippets[0]['language'], "python")


class TestDatabaseIntegrity(unittest.TestCase):
    """
    Test suite for database integrity and edge cases.
    """
    
    def setUp(self):
        """Set up test database."""
        self.test_db_fd, self.test_db_path = tempfile.mkstemp(suffix='.db')
        self.db_manager = EnhancedDatabaseManager(db_name=self.test_db_path)
    
    def tearDown(self):
        """Clean up test database."""
        try:
            os.close(self.test_db_fd)
            os.unlink(self.test_db_path)
        except Exception:
            pass
    
    def test_foreign_key_cascade_delete(self):
        """Test that deleting a user cascades to related records."""
        # Create user
        self.db_manager.create_user("user1", "pass", "user1@test.com")
        user = self.db_manager.get_user_by_username("user1")
        user_id = user['user_id']
        
        # Add related data
        self.db_manager.add_subtopic(user_id, "Topic", "Subject")
        self.db_manager.add_task(user_id, "Task", None, "low")
        
        # Verify data exists
        self.assertEqual(len(self.db_manager.get_subtopics_by_user(user_id)), 1)
        self.assertEqual(len(self.db_manager.get_tasks(user_id)), 1)
        
        # Delete user (should cascade)
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        
        # Verify cascaded deletion
        self.assertEqual(len(self.db_manager.get_subtopics_by_user(user_id)), 0)
        self.assertEqual(len(self.db_manager.get_tasks(user_id)), 0)


if __name__ == "__main__":
    # Run all tests with verbose output
    unittest.main(verbosity=2)