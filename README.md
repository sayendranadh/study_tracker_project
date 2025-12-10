# 📚 Study Progress Tracker

A comprehensive desktop application for students to track their learning progress, take AI-generated exams, practice coding problems, and manage their study goals - all with an elegant Ubuntu-inspired interface.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## ✨ Features

### 🎯 Core Features
- **User Authentication**: Secure registration and login system with password hashing
- **Topic Management**: Create and track learning topics across different subjects
- **Smart Goals**: Set and track learning goals with optional deadlines
- **Note Taking**: Organize notes by topic with timestamps
- **Task Management**: To-do list with priorities and due dates
- **Learning Streak**: Track daily study activity with streak visualization

### 🎓 Advanced Learning Tools
- **AI-Powered Exams**: Generate custom multiple-choice exams using AI
  - Offline template-based generation (no internet required)
  - Optional Ollama integration for advanced question generation
  - Configurable question count and difficulty levels
  - Detailed results with explanations

- **Coding Practice**: LeetCode-style coding problems
  - Generate problems by topic and difficulty
  - Built-in code editor with syntax highlighting
  - Automated test case validation
  - Support for Python, JavaScript, and Bash

- **Code IDE**: Integrated development environment
  - Write and execute code directly in the app
  - Real-time output display
  - Support for multiple programming languages
  - Save and manage code snippets

### 📊 Progress Tracking
- **Dashboard**: Comprehensive overview of your learning journey
- **Grade Calculator**: Calculate required scores for target grades
- **Visual Streak Calendar**: 30-day activity visualization
- **Exam History**: Track all completed exams and scores
- **Progress Reports**: Subject-wise progress breakdown

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/study-progress-tracker.git
cd study-progress-tracker
```

2. **Create a virtual environment** (recommended)
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. **Install required dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python main_app.py
```

## 📦 Dependencies

### Required Packages
Create a `requirements.txt` file with:

```
torch>=2.0.0
transformers>=4.30.0
requests>=2.31.0
```

### Optional Dependencies
For enhanced AI features (Ollama integration):
- Install [Ollama](https://ollama.ai/) on your system
- Pull the Mistral model: `ollama pull mistral`

## 🎨 User Interface

The application features a modern Ubuntu Radiance-inspired theme with:
- Clean, minimalist design
- Intuitive navigation
- Color-coded sections for different features
- Responsive layout
- Smooth animations and transitions

### Color Scheme
- **Primary**: Ubuntu Orange (#e95420)
- **Secondary**: Ubuntu Purple (#762572)
- **Success**: Green (#38b44a)
- **Warning**: Amber (#efb73e)
- **Error**: Red (#df382c)

## 📖 Usage Guide

### First Time Setup

1. **Register an Account**
   - Launch the application
   - Fill in the "Create Account" form
   - Minimum requirements:
     - Username: 3+ characters
     - Password: 6+ characters
     - Valid email address

2. **Login**
   - Enter your credentials
   - Click "Sign In"

### Managing Topics

1. Navigate to "📚 Topics"
2. Add new topics with:
   - Topic name (e.g., "Python Functions")
   - Subject (e.g., "Programming")
3. Update progress (0-100%) as you learn
4. Track multiple topics across different subjects

### Taking Exams

1. Go to "🎓 Exams"
2. Select a topic from your list
3. Configure:
   - Number of questions (5-30)
   - Difficulty (easy/medium/hard)
4. Click "Generate Exam"
5. Answer all questions
6. Submit and view detailed results

### Coding Practice

1. Navigate to "⌨️ Coding Practice"
2. Generate a problem by topic
3. Write your solution in the editor
4. Run test cases to validate
5. View detailed results for each test

### Code IDE

1. Go to "💻 Code IDE"
2. Write code in the editor
3. Click "Run Code" to execute
4. View output in the console
5. Save useful snippets for later

### Setting Goals

1. Navigate to "🎯 Goals"
2. Add new goals with:
   - Goal description
   - Optional topic association
   - Optional target date
3. Toggle completion status
4. Track progress on dashboard

### Task Management

1. Go to "✅ Tasks"
2. Add tasks with:
   - Task description
   - Due date (optional)
   - Priority (low/medium/high)
3. Toggle completion
4. Delete completed tasks

## 🗄️ Database Schema

The application uses SQLite with the following tables:

- **users**: User accounts and credentials
- **subtopics**: Learning topics and progress
- **goals**: Learning goals and targets
- **notes**: Study notes
- **exams**: Generated exams and results
- **tasks**: To-do items
- **code_snippets**: Saved code
- **activity_streak**: Daily activity tracking
- **practice_attempts**: Coding practice history

## 🧠 AI Integration

### Offline Mode (Default)
- Template-based question generation
- No internet required
- Instant generation
- Pre-configured problem sets

### Ollama Integration (Optional)
- Advanced AI-powered question generation
- More natural and varied questions
- Requires Ollama installation
- Internet connection needed

To enable Ollama:
1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Run: `ollama pull mistral`
3. Ensure Ollama service is running
4. The app will automatically use Ollama when available

## 🔧 Configuration

### Customizing AI Models

In `offline_exam_generator.py`:
```python
# Change question templates
self.question_templates = self._load_question_templates()
```

In `ollama_integration.py`:
```python
# Change AI model
self.model = "mistral"  # or "llama2", "codellama", etc.
```

### Database Location

By default, the database is stored as `tracker.db` in the project directory. To change:

In `enhanced_database_manager.py`:
```python
def __init__(self, db_name: str = "your_custom_name.db"):
```

## 📊 Project Structure

```
study-progress-tracker/
│
├── main_app.py                    # Main GUI application
├── enhanced_app_logic.py          # Business logic layer
├── enhanced_database_manager.py   # Database operations
├── offline_exam_generator.py      # Template-based exam generation
├── offline_coding_generator.py    # Coding problem generation
├── ollama_integration.py          # Optional AI integration
├── tracker.db                     # SQLite database (auto-generated)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🎯 Key Features Explained

### Exam Generation Algorithm
1. Selects appropriate question templates based on subject
2. Fills templates with topic-specific content
3. Adjusts difficulty by modifying question complexity
4. Shuffles answer options to prevent pattern recognition
5. Generates unique explanations for each answer

### Streak Tracking System
- Automatically tracks daily activity
- Counts consecutive days of study
- Displays 30-day activity calendar
- Motivates consistent learning habits

### Code Execution Safety
- Runs code in temporary isolated files
- 5-second timeout limit
- Captures both stdout and stderr
- Automatic cleanup after execution
- Supports multiple programming languages

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide for Python code
- Add docstrings to all functions
- Test new features thoroughly
- Update documentation as needed

## 🐛 Known Issues

- Code execution limited to Python, JavaScript, and Bash
- Ollama integration requires local installation
- Large transformer models may be slow on older hardware

## 🔮 Future Enhancements

- [ ] Web-based version using Flask/Django
- [ ] Mobile app (React Native/Flutter)
- [ ] Cloud sync for multi-device access
- [ ] Collaborative study groups
- [ ] Spaced repetition flashcards
- [ ] Export to PDF/Excel
- [ ] More programming languages support
- [ ] Voice notes integration
- [ ] Calendar integration
- [ ] Study analytics dashboard

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Ubuntu design team for color scheme inspiration
- Ollama team for AI integration capabilities
- Hugging Face for transformer models
- The open-source community

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/study-progress-tracker/issues) page
2. Create a new issue with detailed information
3. Join our [Discussions](https://github.com/yourusername/study-progress-tracker/discussions)

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

---

**Happy Learning! 📚✨**

Made with ❤️ for students everywhere
