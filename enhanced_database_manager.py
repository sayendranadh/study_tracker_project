import sqlite3
import hashlib
import json
from datetime import date
from typing import Optional, List, Dict, Any

class EnhancedDatabaseManager:
    def __init__(self, db_name: str = "tracker.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection with Row factory"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def init_database(self):
        """Initialize all database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Subtopics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subtopics (
                    topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    topic_name TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    progress INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
            
            # Goals
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goals (
                    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    topic_id INTEGER,
                    goal_text TEXT NOT NULL,
                    is_completed INTEGER DEFAULT 0,
                    target_date DATE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (topic_id) REFERENCES subtopics (topic_id) ON DELETE SET NULL
                )
            ''')
            
            # Notes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    topic_id INTEGER,
                    note_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (topic_id) REFERENCES subtopics (topic_id) ON DELETE SET NULL
                )
            ''')
            
            # Exams
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exams (
                    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    topic_id INTEGER,
                    exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    questions TEXT NOT NULL,
                    user_answers TEXT,
                    score REAL,
                    total_questions INTEGER,
                    is_completed INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (topic_id) REFERENCES subtopics (topic_id) ON DELETE SET NULL
                )
            ''')
            
            # Tasks
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    task_text TEXT NOT NULL,
                    is_completed INTEGER DEFAULT 0,
                    due_date DATE,
                    priority TEXT DEFAULT 'medium',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
            
            # Code Snippets
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS code_snippets (
                    snippet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    language TEXT NOT NULL,
                    code TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
            
            # Activity Streak
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_streak (
                    streak_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    activity_date DATE NOT NULL,
                    activity_count INTEGER DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    UNIQUE(user_id, activity_date)
                )
            ''')
            
            # Practice Attempts
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS practice_attempts (
                    attempt_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    problem_id TEXT,
                    problem_title TEXT,
                    code TEXT,
                    language TEXT,
                    passed INTEGER,
                    total_questions INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, username: str, password: str, email: str) -> bool:
        """Create a new user"""
        password_hash = self.hash_password(password)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
        return True
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, username, password_hash, email FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
        return dict(result) if result else None
    
    # ==================== EXAM OPERATIONS ====================
    
    def create_exam(self, user_id: int, topic_id: int, questions: List[Dict]) -> int:
        """Create a new exam"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO exams (user_id, topic_id, questions, total_questions) VALUES (?, ?, ?, ?)",
                (user_id, topic_id, json.dumps(questions), len(questions))
            )
            return cursor.lastrowid
    
    def submit_exam(self, exam_id: int, user_answers: Dict[int, str]) -> bool:
        """Submit exam and calculate score"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT questions, total_questions FROM exams WHERE exam_id = ?", (exam_id,))
            result = cursor.fetchone()
            
            if not result:
                raise ValueError("Exam not found")
            
            questions = json.loads(result['questions'])
            total = result['total_questions']
            
            correct = sum(
                1 for idx, answer in user_answers.items()
                if 0 <= int(idx) < len(questions) and questions[int(idx)].get('correct_answer') == answer
            )
            
            score = (correct / total * 100) if total > 0 else 0
            
            cursor.execute(
                "UPDATE exams SET user_answers = ?, score = ?, is_completed = 1 WHERE exam_id = ?",
                (json.dumps(user_answers), score, exam_id)
            )
        return True
    
    def get_exam_history(self, user_id: int) -> List[Dict[str, Any]]:
        """Get completed exams for user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT e.exam_id, e.exam_date, e.score, e.total_questions, s.topic_name, s.subject
                FROM exams e
                LEFT JOIN subtopics s ON e.topic_id = s.topic_id
                WHERE e.user_id = ? AND e.is_completed = 1
                ORDER BY e.exam_date DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_exam_by_id(self, exam_id: int) -> Optional[Dict[str, Any]]:
        """Get exam details"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM exams WHERE exam_id = ?", (exam_id,))
            result = cursor.fetchone()
        
        if not result:
            return None
        
        exam = dict(result)
        exam['questions'] = json.loads(exam['questions'])
        exam['user_answers'] = json.loads(exam.get('user_answers') or '{}')
        return exam
    
    # ==================== TASK OPERATIONS ====================
    
    def add_task(self, user_id: int, task_text: str, due_date: str = None, priority: str = 'medium') -> bool:
        """Add a task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (user_id, task_text, due_date, priority) VALUES (?, ?, ?, ?)",
                (user_id, task_text, due_date, priority)
            )
        return True
    
    def get_tasks(self, user_id: int, include_completed: bool = True) -> List[Dict[str, Any]]:
        """Get tasks for user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM tasks WHERE user_id = ?"
            if not include_completed:
                query += " AND is_completed = 0"
            query += " ORDER BY due_date ASC, priority DESC, created_at DESC"
            cursor.execute(query, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def toggle_task(self, task_id: int) -> bool:
        """Toggle task completion"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE tasks 
                SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END,
                    completed_at = CASE WHEN is_completed = 0 THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE task_id = ?
            ''', (task_id,))
        return True
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (task_id,))
        return True
    
    # ==================== CODE SNIPPET OPERATIONS ====================
    
    def save_snippet(self, user_id: int, title: str, language: str, code: str, description: str = None) -> bool:
        """Save code snippet"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO code_snippets (user_id, title, language, code, description) VALUES (?, ?, ?, ?, ?)",
                (user_id, title, language, code, description)
            )
        return True
    
    def get_snippets(self, user_id: int, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get code snippets"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if language:
                cursor.execute(
                    "SELECT * FROM code_snippets WHERE user_id = ? AND language = ? ORDER BY created_at DESC",
                    (user_id, language)
                )
            else:
                cursor.execute(
                    "SELECT * FROM code_snippets WHERE user_id = ? ORDER BY created_at DESC",
                    (user_id,)
                )
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_snippet(self, snippet_id: int) -> bool:
        """Delete code snippet"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM code_snippets WHERE snippet_id = ?", (snippet_id,))
        return True
    
    # ==================== STREAK OPERATIONS ====================
    
    def update_streak(self, user_id: int) -> bool:
        """Update activity streak"""
        today = date.today().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activity_streak (user_id, activity_date, activity_count) 
                VALUES (?, ?, 1)
                ON CONFLICT(user_id, activity_date) 
                DO UPDATE SET activity_count = activity_count + 1
            ''', (user_id, today))
        return True
    
    def get_streak_data(self, user_id: int, days: int = 365) -> Dict[str, int]:
        """Get streak data"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT activity_date, activity_count 
                FROM activity_streak 
                WHERE user_id = ? 
                ORDER BY activity_date DESC 
                LIMIT ?
            ''', (user_id, days))
            return {row['activity_date']: row['activity_count'] for row in cursor.fetchall()}
    
    def get_current_streak(self, user_id: int) -> int:
        """Calculate consecutive streak"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT activity_date FROM activity_streak 
                WHERE user_id = ? 
                ORDER BY activity_date DESC
            ''', (user_id,))
            results = cursor.fetchall()
        
        if not results:
            return 0
        
        streak = 0
        current_date = date.today()
        
        for row in results:
            activity_date = date.fromisoformat(row['activity_date'])
            days_diff = (current_date - activity_date).days
            
            if days_diff <= 1:
                streak += 1
                current_date = activity_date
            else:
                break
        
        return streak
    
    # ==================== TOPIC/GOAL/NOTE OPERATIONS ====================
    
    def add_subtopic(self, user_id: int, topic_name: str, subject: str) -> bool:
        """Add subtopic"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO subtopics (user_id, topic_name, subject) VALUES (?, ?, ?)",
                (user_id, topic_name, subject)
            )
        return True
    
    def get_subtopics_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user subtopics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM subtopics WHERE user_id = ?", (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def update_subtopic_progress(self, topic_id: int, new_progress: int) -> bool:
        """Update subtopic progress"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE subtopics SET progress = ? WHERE topic_id = ?",
                (new_progress, topic_id)
            )
        return True
    
    def add_goal(self, user_id: int, goal_text: str, topic_id: int = None, target_date: str = None) -> bool:
        """Add goal"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO goals (user_id, topic_id, goal_text, target_date) VALUES (?, ?, ?, ?)",
                (user_id, topic_id, goal_text, target_date)
            )
        return True
    
    def get_goals_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user goals"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT g.*, COALESCE(s.topic_name, 'General') as topic_name
                FROM goals g 
                LEFT JOIN subtopics s ON g.topic_id = s.topic_id 
                WHERE g.user_id = ?
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def toggle_goal_completion(self, goal_id: int) -> bool:
        """Toggle goal completion"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE goals SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END WHERE goal_id = ?",
                (goal_id,)
            )
        return True
    
    def add_note(self, user_id: int, note_text: str, topic_id: int = None) -> bool:
        """Add note"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO notes (user_id, topic_id, note_text) VALUES (?, ?, ?)",
                (user_id, topic_id, note_text)
            )
        return True
    
    def get_notes_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user notes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT n.*, COALESCE(s.topic_name, 'General') as topic_name
                FROM notes n 
                LEFT JOIN subtopics s ON n.topic_id = s.topic_id 
                WHERE n.user_id = ? 
                ORDER BY n.created_at DESC
            ''', (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_note(self, note_id: int) -> bool:
        """Delete note"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE note_id = ?", (note_id,))
        return True
    
    # ==================== PRACTICE ATTEMPTS ====================
    
    def save_practice_attempt(self, user_id: int, problem_id: str, problem_title: str, 
                            code: str, language: str, passed: bool, total_questions: int) -> bool:
        """Save practice attempt"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO practice_attempts 
                (user_id, problem_id, problem_title, code, language, passed, total_questions) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, problem_id, problem_title, code, language, int(passed), total_questions))
        return True
    
    def get_practice_attempts_for_user(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent practice attempts"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM practice_attempts 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (user_id, limit))
            return [dict(r) for r in cursor.fetchall()]