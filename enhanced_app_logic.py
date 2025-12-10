import sqlite3
import hashlib
import json
import subprocess
import sys
import tempfile
import os
from datetime import datetime, date, timedelta
from pathlib import Path

class EnhancedAppLogic:
    def __init__(self, db_path="study_tracker.db"):
        self.db_path = db_path
        self.current_user_id = None
        self.init_database()
        self._init_ai_generators()
    
    def _init_ai_generators(self):
        """Initialize AI generators with fallback support"""
        # Try Ollama first
        self.ollama = None
        self.ollama_available = False
        try:
            from ollama_integration import OllamaIntegration
            self.ollama = OllamaIntegration()
            self.ollama_available = self.ollama.check_connection()
            if self.ollama_available:
                print("✅ Ollama connected successfully")
        except Exception as e:
            print(f"⚠️ Ollama not available: {e}")
        
        # Always load offline generators as fallback
        try:
            from offline_exam_generator import OfflineExamGenerator
            self.offline_exam_gen = OfflineExamGenerator()
            self.offline_exam_gen.load_model()
            print("✅ Offline exam generator loaded")
        except Exception as e:
            print(f"⚠️ Offline exam generator failed: {e}")
            self.offline_exam_gen = None
        
        try:
            from offline_coding_generator import OfflineCodingGenerator
            self.offline_coding_gen = OfflineCodingGenerator()
            self.offline_coding_gen.load_model()
            print("✅ Offline coding generator loaded")
        except Exception as e:
            print(f"⚠️ Offline coding generator failed: {e}")
            self.offline_coding_gen = None
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Subtopics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subtopics (
                topic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_name TEXT NOT NULL,
                subject TEXT,
                progress INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id INTEGER,
                goal_text TEXT NOT NULL,
                target_date DATE,
                is_completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (topic_id) REFERENCES subtopics (topic_id)
            )
        ''')
        
        # Notes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id INTEGER,
                note_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (topic_id) REFERENCES subtopics (topic_id)
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task_text TEXT NOT NULL,
                due_date DATE,
                priority TEXT DEFAULT 'medium',
                is_completed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Exams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS exams (
                exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                topic_id INTEGER,
                exam_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                score REAL,
                total_questions INTEGER,
                questions_data TEXT,
                user_answers TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (topic_id) REFERENCES subtopics (topic_id)
            )
        ''')
        
        # Study activity table (for streak tracking)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS study_activity (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_date DATE NOT NULL,
                activity_type TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash a password for storing"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                (username, password_hash, email)
            )
            
            conn.commit()
            conn.close()
            return True, "Account created successfully!"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def login_user(self, username, password):
        """Login a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute(
                "SELECT user_id FROM users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                self.current_user_id = result[0]
                self.log_activity("login")
                return True, "Login successful!"
            else:
                return False, "Invalid username or password"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def logout_user(self):
        """Logout current user"""
        self.current_user_id = None
    
    def get_current_user(self):
        """Get current user information"""
        if not self.current_user_id:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id, username, email FROM users WHERE user_id = ?",
            (self.current_user_id,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'email': result[2]
            }
        return None
    
    def log_activity(self, activity_type):
        """Log user activity for streak tracking"""
        if not self.current_user_id:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = date.today().strftime('%Y-%m-%d')
            
            # Check if already logged today
            cursor.execute(
                "SELECT activity_id FROM study_activity WHERE user_id = ? AND activity_date = ?",
                (self.current_user_id, today)
            )
            
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO study_activity (user_id, activity_date, activity_type) VALUES (?, ?, ?)",
                    (self.current_user_id, today, activity_type)
                )
                conn.commit()
            
            conn.close()
        except Exception:
            pass
    
    # ========== TOPICS ==========
    
    def add_subtopic(self, topic_name, subject):
        """Add a new topic"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        if not topic_name:
            return False, "Topic name is required"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO subtopics (user_id, topic_name, subject) VALUES (?, ?, ?)",
                (self.current_user_id, topic_name, subject)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("add_topic")
            return True, "Topic added successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user_subtopics(self):
        """Get all topics for current user"""
        if not self.current_user_id:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT topic_id, topic_name, subject, progress FROM subtopics WHERE user_id = ?",
            (self.current_user_id,)
        )
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'topic_id': r[0],
                'topic_name': r[1],
                'subject': r[2],
                'progress': r[3]
            }
            for r in results
        ]
    
    def update_topic_progress(self, topic_id, progress):
        """Update progress for a topic"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE subtopics SET progress = ? WHERE topic_id = ? AND user_id = ?",
                (progress, topic_id, self.current_user_id)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("update_progress")
            return True, "Progress updated!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def calculate_total_progress(self):
        """Calculate average progress across all topics"""
        topics = self.get_user_subtopics()
        if not topics:
            return 0
        
        total = sum(t['progress'] for t in topics)
        return total / len(topics)
    
    # ========== GOALS ==========
    
    def add_goal(self, goal_text, topic_id=None, target_date=None):
        """Add a new goal"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        if not goal_text:
            return False, "Goal text is required"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO goals (user_id, topic_id, goal_text, target_date) VALUES (?, ?, ?, ?)",
                (self.current_user_id, topic_id, goal_text, target_date)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("add_goal")
            return True, "Goal added successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user_goals(self):
        """Get all goals for current user"""
        if not self.current_user_id:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT g.goal_id, g.goal_text, g.target_date, g.is_completed, s.topic_name
            FROM goals g
            LEFT JOIN subtopics s ON g.topic_id = s.topic_id
            WHERE g.user_id = ?
            ORDER BY g.is_completed, g.target_date
        ''', (self.current_user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'goal_id': r[0],
                'goal_text': r[1],
                'target_date': r[2],
                'is_completed': bool(r[3]),
                'topic_name': r[4] or 'General'
            }
            for r in results
        ]
    
    def toggle_goal(self, goal_id):
        """Toggle goal completion status"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE goals SET is_completed = NOT is_completed WHERE goal_id = ? AND user_id = ?",
                (goal_id, self.current_user_id)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("toggle_goal")
            return True, "Goal status updated!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ========== NOTES ==========
    
    def add_note(self, note_text, topic_id=None):
        """Add a new note"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        if not note_text:
            return False, "Note text is required"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO notes (user_id, topic_id, note_text) VALUES (?, ?, ?)",
                (self.current_user_id, topic_id, note_text)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("add_note")
            return True, "Note added successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_user_notes(self):
        """Get all notes for current user"""
        if not self.current_user_id:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT n.note_id, n.note_text, n.created_at, s.topic_name
            FROM notes n
            LEFT JOIN subtopics s ON n.topic_id = s.topic_id
            WHERE n.user_id = ?
            ORDER BY n.created_at DESC
        ''', (self.current_user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'note_id': r[0],
                'note_text': r[1],
                'created_at': r[2],
                'topic_name': r[3] or 'General'
            }
            for r in results
        ]
    
    def delete_note(self, note_id):
        """Delete a note"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM notes WHERE note_id = ? AND user_id = ?",
                (note_id, self.current_user_id)
            )
            
            conn.commit()
            conn.close()
            
            return True, "Note deleted!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ========== TASKS ==========
    
    def add_task(self, task_text, due_date=None, priority='medium'):
        """Add a new task"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        if not task_text:
            return False, "Task text is required"
        
        # Validate due_date
        if due_date and due_date != 'YYYY-MM-DD':
            try:
                datetime.strptime(due_date, '%Y-%m-%d')
            except ValueError:
                due_date = None
        else:
            due_date = None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO tasks (user_id, task_text, due_date, priority) VALUES (?, ?, ?, ?)",
                (self.current_user_id, task_text, due_date, priority)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("add_task")
            return True, "Task added successfully!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_tasks(self, include_completed=False):
        """Get tasks for current user"""
        if not self.current_user_id:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = '''
            SELECT task_id, task_text, due_date, priority, is_completed
            FROM tasks
            WHERE user_id = ?
        '''
        
        if not include_completed:
            query += " AND is_completed = 0"
        
        query += " ORDER BY is_completed, due_date"
        
        cursor.execute(query, (self.current_user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'task_id': r[0],
                'task_text': r[1],
                'due_date': r[2],
                'priority': r[3],
                'is_completed': bool(r[4])
            }
            for r in results
        ]
    
    def toggle_task(self, task_id):
        """Toggle task completion status"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE tasks SET is_completed = NOT is_completed WHERE task_id = ? AND user_id = ?",
                (task_id, self.current_user_id)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("toggle_task")
            return True, "Task status updated!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def delete_task(self, task_id):
        """Delete a task"""
        if not self.current_user_id:
            return False, "Not logged in"
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM tasks WHERE task_id = ? AND user_id = ?",
                (task_id, self.current_user_id)
            )
            
            conn.commit()
            conn.close()
            
            return True, "Task deleted!"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ========== EXAMS ==========
    
    def start_exam(self, topic_id, question_count=20, difficulty='medium'):
        """Generate and start an exam"""
        if not self.current_user_id:
            return False, "Not logged in", None
        
        # Get topic info
        topics = self.get_user_subtopics()
        topic = next((t for t in topics if t['topic_id'] == topic_id), None)
        
        if not topic:
            return False, "Topic not found", None
        
        # Generate questions with AI
        print(f"🔍 Generating {question_count} questions for {topic['topic_name']}...")
        questions = self.generate_exam_questions(
            topic['topic_name'],
            topic['subject'],
            question_count,
            difficulty
        )
        
        if not questions:
            return False, "Failed to generate questions", None
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO exams (user_id, topic_id, total_questions, questions_data) VALUES (?, ?, ?, ?)",
                (self.current_user_id, topic_id, len(questions), json.dumps(questions))
            )
            
            exam_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            self.log_activity("start_exam")
            print(f"✅ Exam created with ID: {exam_id}")
            return True, "Exam generated successfully!", exam_id
        except Exception as e:
            print(f"❌ Error creating exam: {e}")
            return False, f"Error: {str(e)}", None
    
    def generate_exam_questions(self, topic_name, subject, count, difficulty):
        """Generate exam questions using AI (Ollama) or fallback generators"""
        print(f"📝 Attempting to generate {count} questions...")
        
        # Try Ollama first (best quality)
        if self.ollama_available and self.ollama:
            try:
                print("🤖 Using Ollama AI for question generation...")
                questions = self.ollama.generate_exam(topic_name, subject, count, difficulty)
                if questions and len(questions) >= count:
                    print(f"✅ Ollama generated {len(questions)} questions")
                    return questions[:count]
            except Exception as e:
                print(f"⚠️ Ollama generation failed: {e}")
        
        # Try offline exam generator (template-based)
        if self.offline_exam_gen:
            try:
                print("📋 Using offline template generator...")
                questions = self.offline_exam_gen.generate_exam(topic_name, subject, count, difficulty)
                if questions and len(questions) >= count:
                    print(f"✅ Offline generator created {len(questions)} questions")
                    return questions[:count]
            except Exception as e:
                print(f"⚠️ Offline generator failed: {e}")
        
        # Final fallback
        print("⚠️ Using basic fallback generator...")
        return self._generate_fallback_questions(topic_name, subject, count, difficulty)
    
    def _generate_fallback_questions(self, topic_name, subject, count, difficulty):
        """Fallback question generator with basic templates"""
        import random
        
        questions = []
        
        question_templates = [
            "What is the primary purpose of {topic} in {subject}?",
            "Which of the following best describes {topic}?",
            "What is the key advantage of using {topic}?",
            "When should you apply {topic} in {subject}?",
            "Which concept is most related to {topic}?",
            "How does {topic} benefit {subject} applications?",
            "What is the most important aspect of {topic}?",
            "Which statement about {topic} is correct?",
            "Why is {topic} important in {subject}?",
            "What role does {topic} play in {subject}?"
        ]
        
        for i in range(count):
            template = question_templates[i % len(question_templates)]
            question_text = template.format(topic=topic_name, subject=subject)
            
            # Generate varied options based on difficulty
            if difficulty == 'easy':
                options = [
                    f"It is a fundamental concept in {subject}",
                    f"It is rarely used in practice",
                    f"It is only for advanced users",
                    f"It is being replaced by newer methods"
                ]
                correct_idx = 0
                explanation = f"{topic_name} is a fundamental concept in {subject} that forms the basis for understanding."
            elif difficulty == 'hard':
                options = [
                    f"Provides foundational understanding of {subject}",
                    f"Offers advanced optimization techniques",
                    f"Enables complex problem-solving approaches",
                    f"All of the above"
                ]
                correct_idx = 3
                explanation = f"{topic_name} encompasses multiple aspects including foundations, optimization, and problem-solving in {subject}."
            else:  # medium
                options = [
                    f"Essential for understanding {subject}",
                    f"Optional learning material",
                    f"Only needed in specific cases",
                    f"Deprecated in modern {subject}"
                ]
                correct_idx = 0
                explanation = f"{topic_name} is essential for a comprehensive understanding of {subject}."
            
            # Shuffle options
            correct_answer = options[correct_idx]
            random.shuffle(options)
            new_idx = options.index(correct_answer)
            
            question = {
                'question': question_text,
                'options': options,
                'correct_answer': chr(65 + new_idx),  # A, B, C, or D
                'explanation': explanation
            }
            questions.append(question)
        
        print(f"✅ Fallback generator created {len(questions)} questions")
        return questions
    
    def get_exam(self, exam_id):
        """Get exam details"""
        if not self.current_user_id:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT exam_id, questions_data FROM exams WHERE exam_id = ? AND user_id = ?",
            (exam_id, self.current_user_id)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'exam_id': result[0],
                'questions': json.loads(result[1])
            }
        return None
    
    def submit_exam(self, exam_id, answers):
        """Submit exam answers and calculate score"""
        if not self.current_user_id:
            return False, "Not logged in", 0
        
        exam = self.get_exam(exam_id)
        if not exam:
            return False, "Exam not found", 0
        
        # Calculate score
        correct = 0
        questions = exam['questions']
        
        for idx, question in enumerate(questions):
            user_answer = answers.get(idx, '')
            if user_answer == question['correct_answer']:
                correct += 1
        
        score = (correct / len(questions)) * 100
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE exams SET score = ?, user_answers = ? WHERE exam_id = ? AND user_id = ?",
                (score, json.dumps(answers), exam_id, self.current_user_id)
            )
            
            conn.commit()
            conn.close()
            
            self.log_activity("complete_exam")
            return True, "Exam submitted successfully!", score
        except Exception as e:
            return False, f"Error: {str(e)}", 0
    
    def validate_exam_answers(self, exam_id):
        """Get detailed results for an exam"""
        exam = self.get_exam(exam_id)
        if not exam:
            return None
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_answers FROM exams WHERE exam_id = ? AND user_id = ?",
            (exam_id, self.current_user_id)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if not result or not result[0]:
            return None
        
        user_answers = json.loads(result[0])
        questions = exam['questions']
        
        details = []
        correct_count = 0
        
        for idx, question in enumerate(questions):
            user_answer = user_answers.get(str(idx), 'Not answered')
            is_correct = user_answer == question['correct_answer']
            
            if is_correct:
                correct_count += 1
            
            details.append({
                'question_num': idx + 1,
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': question['correct_answer'],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })
        
        return {
            'total': len(questions),
            'correct': correct_count,
            'incorrect': len(questions) - correct_count,
            'details': details
        }
    
    def get_exam_history(self):
        """Get exam history for current user"""
        if not self.current_user_id:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.exam_id, e.exam_date, e.score, e.total_questions, s.topic_name, s.subject
            FROM exams e
            LEFT JOIN subtopics s ON e.topic_id = s.topic_id
            WHERE e.user_id = ? AND e.score IS NOT NULL
            ORDER BY e.exam_date DESC
        ''', (self.current_user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'exam_id': r[0],
                'exam_date': r[1],
                'score': r[2],
                'total_questions': r[3],
                'topic_name': r[4],
                'subject': r[5]
            }
            for r in results
        ]
    
    # ========== STREAK ==========
    
    def get_current_streak(self):
        """Calculate current study streak"""
        if not self.current_user_id:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT activity_date
            FROM study_activity
            WHERE user_id = ?
            ORDER BY activity_date DESC
        ''', (self.current_user_id,))
        
        dates = [r[0] for r in cursor.fetchall()]
        conn.close()
        
        if not dates:
            return 0
        
        streak = 0
        today = date.today()
        
        for i in range(len(dates)):
            expected_date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if expected_date in dates:
                streak += 1
            else:
                break
        
        return streak
    
    def get_streak_data(self):
        """Get activity data for visualization"""
        if not self.current_user_id:
            return {}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT activity_date, COUNT(*)
            FROM study_activity
            WHERE user_id = ?
            GROUP BY activity_date
        ''', (self.current_user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        return {r[0]: r[1] for r in results}
    
    # ========== CODE EXECUTION ==========
    
    def run_code(self, code, language='python', timeout=5):
        """Safely execute code in a subprocess"""
        if language != 'python':
            return False, "Only Python is supported"
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Run the code
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # Clean up
            os.unlink(temp_file)
            
            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr
            
            return True, output
        
        except subprocess.TimeoutExpired:
            try:
                os.unlink(temp_file)
            except:
                pass
            return False, "Error: Code execution timed out"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    # ========== CODING PRACTICE ==========
    
    def generate_coding_problem(self, topic, difficulty):
        """Generate a coding practice problem using AI or templates"""
        print(f"🔍 Generating coding problem: {topic} ({difficulty})...")
        
        # Try Ollama first
        if self.ollama_available and self.ollama:
            try:
                print("🤖 Using Ollama for coding problem generation...")
                problem = self.ollama.generate_code_practice(topic, difficulty, 'python')
                if problem and self._validate_coding_problem(problem):
                    print("✅ Ollama generated valid coding problem")
                    self.current_problem_test_cases = problem.get('tests', [])
                    return problem
            except Exception as e:
                print(f"⚠️ Ollama coding generation failed: {e}")
        
        # Try offline coding generator
        if self.offline_coding_gen:
            try:
                print("📋 Using offline coding problem generator...")
                problem = self.offline_coding_gen.generate_coding_problem(topic, difficulty)
                if problem and self._validate_coding_problem(problem):
                    print("✅ Offline generator created valid problem")
                    self.current_problem_test_cases = problem.get('test_cases', [])
                    return problem
            except Exception as e:
                print(f"⚠️ Offline coding generator failed: {e}")
        
        # Fallback to basic templates
        print("⚠️ Using basic fallback coding problems...")
        return self._generate_fallback_coding_problem(topic, difficulty)
    
    def _validate_coding_problem(self, problem):
        """Validate coding problem structure"""
        required = ['title', 'description', 'template']
        return all(key in problem for key in required)
    
    def _generate_fallback_coding_problem(self, topic, difficulty):
        """Generate a basic coding problem as fallback"""
        import random
        
        problems = {
            'easy': [
                {
                    'title': 'Sum of Array',
                    'description': 'Write a function that calculates the sum of all elements in an array.\n\nExample:\nInput: [1, 2, 3, 4, 5]\nOutput: 15',
                    'template': 'def array_sum(arr):\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    import sys\n    arr = eval(sys.stdin.read())\n    print(array_sum(arr))',
                    'test_cases': [
                        {'input': '[1, 2, 3, 4, 5]', 'expected': '15'},
                        {'input': '[10, 20]', 'expected': '30'},
                        {'input': '[0]', 'expected': '0'}
                    ]
                },
                {
                    'title': 'Reverse String',
                    'description': 'Write a function that reverses a string.\n\nExample:\nInput: "hello"\nOutput: "olleh"',
                    'template': 'def reverse_string(s):\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    import sys\n    s = sys.stdin.read().strip()\n    print(reverse_string(s))',
                    'test_cases': [
                        {'input': 'hello', 'expected': 'olleh'},
                        {'input': 'python', 'expected': 'nohtyp'},
                        {'input': 'a', 'expected': 'a'}
                    ]
                }
            ],
            'medium': [
                {
                    'title': 'Two Sum',
                    'description': 'Given an array of integers and a target, return indices of two numbers that add up to target.\n\nExample:\nInput: [2, 7, 11, 15], target=9\nOutput: [0, 1]',
                    'template': 'def two_sum(nums, target):\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    nums = eval(lines[0])\n    target = int(lines[1])\n    print(two_sum(nums, target))',
                    'test_cases': [
                        {'input': '[2, 7, 11, 15]\\n9', 'expected': '[0, 1]'},
                        {'input': '[3, 2, 4]\\n6', 'expected': '[1, 2]'},
                        {'input': '[3, 3]\\n6', 'expected': '[0, 1]'}
                    ]
                }
            ],
            'hard': [
                {
                    'title': 'Merge Sorted Arrays',
                    'description': 'Merge two sorted arrays into one sorted array.\n\nExample:\nInput: [1, 3, 5], [2, 4, 6]\nOutput: [1, 2, 3, 4, 5, 6]',
                    'template': 'def merge_sorted(arr1, arr2):\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    import sys\n    lines = sys.stdin.read().strip().split("\\n")\n    arr1 = eval(lines[0])\n    arr2 = eval(lines[1])\n    print(merge_sorted(arr1, arr2))',
                    'test_cases': [
                        {'input': '[1, 3, 5]\\n[2, 4, 6]', 'expected': '[1, 2, 3, 4, 5, 6]'},
                        {'input': '[1]\\n[2]', 'expected': '[1, 2]'},
                        {'input': '[]\\n[1, 2]', 'expected': '[1, 2]'}
                    ]
                }
            ]
        }
        
        problem_list = problems.get(difficulty, problems['easy'])
        selected = random.choice(problem_list)
        self.current_problem_test_cases = selected['test_cases']
        return selected
    
    def submit_coding_solution(self, code, language='python'):
        """Test the user's coding solution against test cases"""
        if not hasattr(self, 'current_problem_test_cases'):
            return {
                'passed': 0,
                'total': 0,
                'score': 0,
                'results': [{'test_case': 1, 'passed': False, 'expected': 'N/A', 'actual': 'No test cases available'}]
            }
        
        test_cases = self.current_problem_test_cases
        results = []
        passed_count = 0
        
        for i, test in enumerate(test_cases):
            try:
                # Create test code
                test_input = test['input']
                expected_output = test['expected']
                
                # Create temp file with code and test input
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    code_file = f.name
                
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
                    f.write(test_input)
                    input_file = f.name
                
                # Execute code with input
                with open(input_file, 'r') as inp:
                    result = subprocess.run(
                        [sys.executable, code_file],
                        stdin=inp,
                        capture_output=True,
                        text=True,
                        timeout=3
                    )
                
                # Cleanup
                os.unlink(code_file)
                os.unlink(input_file)
                
                if result.returncode == 0:
                    actual_output = result.stdout.strip()
                    is_correct = actual_output == expected_output
                    
                    if is_correct:
                        passed_count += 1
                    
                    results.append({
                        'test_case': i + 1,
                        'passed': is_correct,
                        'expected': expected_output,
                        'actual': actual_output,
                        'input': test_input[:50] + ('...' if len(test_input) > 50 else '')
                    })
                else:
                    results.append({
                        'test_case': i + 1,
                        'passed': False,
                        'expected': expected_output,
                        'actual': f"Error: {result.stderr[:100]}",
                        'input': test_input[:50] + ('...' if len(test_input) > 50 else '')
                    })
            
            except subprocess.TimeoutExpired:
                results.append({
                    'test_case': i + 1,
                    'passed': False,
                    'expected': test['expected'],
                    'actual': 'Timeout (>3s)',
                    'input': test['input'][:50] + ('...' if len(test['input']) > 50 else '')
                })
            except Exception as e:
                results.append({
                    'test_case': i + 1,
                    'passed': False,
                    'expected': test['expected'],
                    'actual': f'Error: {str(e)[:50]}',
                    'input': test.get('input', 'N/A')[:50]
                })
        
        score = (passed_count / len(test_cases)) * 100 if test_cases else 0
        
        # Log activity if all tests passed
        if passed_count == len(test_cases):
            self.log_activity("coding_practice")
        
        return {
            'passed': passed_count,
            'total': len(test_cases),
            'score': score,
            'results': results
        }
    
    def _extract_function_name(self, code):
        """Extract the function name from code"""
        for line in code.split('\n'):
            if line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0].strip()
                return func_name
        return 'unknown_function'