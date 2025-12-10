import json
import random
from typing import List, Dict, Any

class OfflineExamGenerator:
    """Lightweight template-based exam question generator"""
    
    def __init__(self):
        self.is_loaded = True
        self.question_templates = self._load_question_templates()
    
    def load_model(self):
        """Compatibility method - template generation is always ready"""
        print("✅ Offline exam generator ready")
        self.is_loaded = True
    
    def generate_exam(self, topic: str, subject: str, count: int = 20, difficulty: str = "medium") -> List[Dict[str, Any]]:
        """Generate exam questions using templates"""
        print(f"📝 Generating {count} {difficulty} questions about {topic}...")
        
        questions = []
        template_category = self._determine_category(subject)
        templates = self.question_templates.get(template_category, self.question_templates['general'])
        
        for i in range(count):
            template = templates[i % len(templates)]
            question = self._generate_question(topic, subject, difficulty, template)
            if question:
                self._shuffle_options(question)
                questions.append(question)
        
        print(f"✅ Generated {len(questions)} questions")
        return questions
    
    def _load_question_templates(self) -> Dict[str, List[Dict]]:
        """Load question templates by category"""
        return {
            'programming': [
                {
                    'template': 'What is the main purpose of {topic} in {subject}?',
                    'options_template': [
                        'To handle {topic} operations',
                        'To manage {topic} efficiently',
                        'To optimize {topic} performance',
                        'To implement {topic} functionality'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} is primarily used for handling specific operations in {subject}.'
                },
                {
                    'template': 'Which statement best describes {topic}?',
                    'options_template': [
                        'A fundamental concept in {subject}',
                        'An advanced technique',
                        'A debugging tool',
                        'A deprecated feature'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} represents a core concept in {subject}.'
                },
                {
                    'template': 'What is the key advantage of using {topic}?',
                    'options_template': [
                        'Improved code efficiency',
                        'Better code organization',
                        'Enhanced security',
                        'All of the above'
                    ],
                    'correct_idx': 3,
                    'explanation': '{topic} provides multiple benefits including efficiency, organization, and security.'
                },
                {
                    'template': 'When should you use {topic}?',
                    'options_template': [
                        'When working with {subject} applications',
                        'Only in production environments',
                        'Only for debugging',
                        'Never recommended'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} is appropriate when working with {subject} applications.'
                }
            ],
            'mathematics': [
                {
                    'template': 'What is the formula for calculating {topic}?',
                    'options_template': [
                        'Standard {topic} formula',
                        'Alternative {topic} method',
                        'Basic {topic} equation',
                        'Advanced {topic} calculation'
                    ],
                    'correct_idx': 0,
                    'explanation': 'The standard formula is commonly used for {topic} calculations.'
                },
                {
                    'template': 'Which concept is most related to {topic}?',
                    'options_template': [
                        'Core mathematical principle',
                        'Statistical method',
                        'Geometric theorem',
                        'Algebraic equation'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} is fundamentally based on core mathematical principles.'
                },
                {
                    'template': 'How is {topic} typically applied?',
                    'options_template': [
                        'In solving {subject} problems',
                        'Only in theoretical contexts',
                        'Rarely used in practice',
                        'Only for advanced students'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} is commonly applied in solving {subject} problems.'
                }
            ],
            'science': [
                {
                    'template': 'What is the primary function of {topic} in {subject}?',
                    'options_template': [
                        'Essential {subject} process',
                        'Supporting mechanism',
                        'Experimental technique',
                        'Theoretical concept'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} plays a crucial role in {subject} processes.'
                },
                {
                    'template': 'What role does {topic} play in {subject}?',
                    'options_template': [
                        'Central to understanding {subject}',
                        'Minor supporting role',
                        'Outdated concept',
                        'Only relevant in research'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} is central to understanding {subject}.'
                }
            ],
            'general': [
                {
                    'template': 'What is the most important aspect of {topic}?',
                    'options_template': [
                        'Fundamental principles',
                        'Practical applications',
                        'Historical development',
                        'Theoretical foundations'
                    ],
                    'correct_idx': 0,
                    'explanation': 'Understanding the fundamental principles is key to mastering {topic}.'
                },
                {
                    'template': 'Which statement about {topic} is correct?',
                    'options_template': [
                        'Essential for understanding {subject}',
                        'Only used in advanced contexts',
                        'Has limited applications',
                        'Being replaced by newer methods'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} remains essential for comprehensive understanding of {subject}.'
                },
                {
                    'template': 'Why is {topic} important in {subject}?',
                    'options_template': [
                        'Provides foundational knowledge',
                        'Rarely needed in practice',
                        'Only for academic purposes',
                        'Decreasing in relevance'
                    ],
                    'correct_idx': 0,
                    'explanation': '{topic} provides foundational knowledge in {subject}.'
                }
            ]
        }
    
    def _determine_category(self, subject: str) -> str:
        """Determine question category from subject"""
        subject_lower = subject.lower()
        
        if any(word in subject_lower for word in ['programming', 'coding', 'computer', 'software', 'python', 'java']):
            return 'programming'
        elif any(word in subject_lower for word in ['math', 'algebra', 'calculus', 'statistics', 'geometry']):
            return 'mathematics'
        elif any(word in subject_lower for word in ['science', 'physics', 'chemistry', 'biology']):
            return 'science'
        
        return 'general'
    
    def _generate_question(self, topic: str, subject: str, difficulty: str, template: Dict) -> Dict[str, Any]:
        """Generate question from template"""
        question_text = template['template'].format(topic=topic, subject=subject)
        
        options = []
        for opt_template in template['options_template']:
            option = opt_template.format(topic=topic, subject=subject)
            
            # Adjust for difficulty
            if difficulty == 'easy':
                option = option.replace('advanced', 'basic').replace('complex', 'simple')
            elif difficulty == 'hard':
                option = option.replace('basic', 'advanced').replace('simple', 'complex')
            
            options.append(option)
        
        correct_answer = chr(65 + template['correct_idx'])
        explanation = template['explanation'].format(topic=topic, subject=subject)
        
        return {
            'question': question_text,
            'options': options,
            'correct_answer': correct_answer,
            'explanation': explanation
        }
    
    def _shuffle_options(self, question: Dict[str, Any]):
        """Shuffle options and update correct answer"""
        correct_idx = ord(question['correct_answer']) - ord('A')
        correct_text = question['options'][correct_idx]
        
        random.shuffle(question['options'])
        
        new_idx = question['options'].index(correct_text)
        question['correct_answer'] = chr(ord('A') + new_idx)
    
    def check_connection(self) -> bool:
        """Check if generator is ready"""
        return self.is_loaded