import requests
import json
import random
from typing import List, Dict, Any, Optional

class OllamaIntegration:
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama integration"""
        self.base_url = base_url
        self.model = "mistral"

    def check_connection(self) -> bool:
        """Check if Ollama is running"""
        response = requests.get(f"{self.base_url}/api/tags", timeout=5)
        return response.status_code == 200

    def generate_exam(self, topic: str, subject: str, count: int = 20, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """Generate objective-type exam questions using Ollama"""
        if not self.check_connection():
            raise ConnectionError("Ollama is not running. Please start Ollama service.")

        prompt = f"""Generate {count} multiple-choice questions about {topic} in {subject}.
Difficulty level: {difficulty}

For each question, provide:
1. The question text
2. Four options (A, B, C, D)
3. The correct answer (A, B, C, or D)
4. A brief explanation

Format your response as JSON array with this structure:
[
  {{
    "question": "Question text here?",
    "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
    "correct_answer": "A",
    "explanation": "Explanation here"
  }}
]

Make sure questions are diverse, accurate, and test understanding rather than just memorization.
Ensure all {count} questions are unique and cover different aspects of {topic}."""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "top_p": 0.9}
            },
            timeout=400
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code}")

        result = response.json()
        generated_text = result.get('response', '')
        questions = self._parse_questions(generated_text)

        # Re-generate if not enough valid questions
        if len(questions) < count:
            additional = self.generate_exam(topic, subject, count - len(questions), difficulty)
            questions.extend(additional)

        # Shuffle each question’s options
        for q in questions:
            self._shuffle_question_options(q)

        return questions[:count]

    def _parse_questions(self, text: str) -> List[Dict[str, Any]]:
        """Parse questions from Ollama response"""
        start = text.find('[')
        end = text.rfind(']') + 1

        if start != -1 and end > start:
            json_text = text[start:end]
            questions = json.loads(json_text)
            return [q for q in questions if self._validate_question(q)]
        return []

    def _validate_question(self, question: Dict[str, Any]) -> bool:
        """Validate question structure"""
        required_fields = ['question', 'options', 'correct_answer', 'explanation']
        if not all(field in question for field in required_fields):
            return False
        if len(question['options']) != 4:
            return False
        if question['correct_answer'] not in ['A', 'B', 'C', 'D']:
            return False
        return True

    def _shuffle_question_options(self, question: Dict[str, Any]):
        """Shuffle options and update correct answer"""
        correct_idx = ord(question['correct_answer']) - ord('A')
        correct_text = question['options'][correct_idx]
        random.shuffle(question['options'])
        new_idx = question['options'].index(correct_text)
        question['correct_answer'] = chr(ord('A') + new_idx)

    def generate_study_guide(self, topic: str, subject: str) -> str:
        """Generate a comprehensive study guide for a topic"""
        if not self.check_connection():
            raise ConnectionError("Ollama is not running. Please start Ollama service.")

        prompt = f"""Create a comprehensive study guide for {topic} in {subject}.

Include:
1. Key Concepts (5-7 main points)
2. Important Definitions
3. Common Mistakes to Avoid
4. Practice Tips
5. Related Topics to Explore

Make it clear, concise, and student-friendly."""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code}")

        return response.json().get('response', '')

    def explain_concept(self, concept: str, context: str = "") -> str:
        """Get AI explanation for a specific concept"""
        if not self.check_connection():
            raise ConnectionError("Ollama is not running. Please start Ollama service.")

        prompt = f"""Explain the concept of "{concept}" in simple terms.
{"Context: " + context if context else ""}

Provide:
1. A clear definition
2. A simple example
3. Why it's important

Keep the explanation concise and easy to understand."""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code}")

        return response.json().get('response', '')

    def generate_code_practice(self, topic: str, difficulty: str = 'easy', language: str = 'python') -> Optional[Dict[str, Any]]:
        """Generate a coding practice problem using Ollama."""
        if not self.check_connection():
            raise ConnectionError("Ollama is not running. Please start Ollama service.")

        prompt = f"""Create a single coding practice problem about {topic} targeting {difficulty} difficulty for the {language} programming language.

Return a JSON object with the following fields:
- title: short title string
- description: one-paragraph problem description
- template: a runnable {language} program template that reads from stdin and prints the answer
- tests: an array of objects with fields 'input' (string) and 'expected' (string)

Make sure tests are deterministic and there are at least 3 tests. Output only the JSON object, without extra explanation."""

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2}
            },
            timeout=60
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ollama API error: {response.status_code}")

        text = response.json().get('response', '')
        start = text.find('{')
        end = text.rfind('}') + 1

        if start == -1 or end <= start:
            return None

        data = json.loads(text[start:end])

        if not all(k in data for k in ('title', 'description', 'template', 'tests')):
            return None

        valid_tests = []
        for t in data.get('tests', []):
            if isinstance(t, dict) and 'input' in t and 'expected' in t:
                valid_tests.append({'input': str(t['input']), 'expected': str(t['expected'])})

        data['tests'] = valid_tests
        return data
