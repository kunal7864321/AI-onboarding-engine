"""
Resume Parser - Extracts structured information from resumes using NLP
"""
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json


@dataclass
class ParsedResume:
    personal_info: Dict[str, str]
    skills: List[Dict[str, Any]]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    raw_text: str
    skill_proficiencies: Dict[str, float]


class ResumeParser:
    """
    Extracts structured information from resume text using pattern matching and NLP
    """
    
    def __init__(self, skills_taxonomy: Optional[Dict] = None):
        self.skills_taxonomy = skills_taxonomy or {}
        self.skill_patterns = self._load_skill_patterns()
        self.proficiency_indicators = {
            'expert': 5.0,
            'advanced': 4.5,
            'proficient': 4.0,
            'intermediate': 3.0,
            'familiar': 2.0,
            'beginner': 1.5,
            'novice': 1.0,
        }
    
    def _load_skill_patterns(self) -> Dict[str, List[str]]:
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 
                'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab',
                'sql', 'html', 'css', 'bash', 'shell', 'perl', 'haskell', 'elixir'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js',
                'express', 'fastapi', 'rails', 'laravel', 'flutter', 'react native'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
                'dynamodb', 'sqlite', 'oracle', 'sql server', 'neo4j'
            ],
            'cloud_devops': [
                'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins',
                'github actions', 'gitlab', 'jira', 'datadog', 'prometheus'
            ],
            'ml_ai': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras',
                'scikit-learn', 'nlp', 'computer vision', 'reinforcement learning',
                'transformers', 'hugging face', 'openai', 'llm', 'generative ai'
            ],
            'data_engineering': [
                'spark', 'hadoop', 'kafka', 'airflow', 'dbt', 'snowflake', 'bigquery',
                'databricks', 'etl', 'data pipeline', 'data warehouse', 'data lake'
            ],
            'soft_skills': [
                'leadership', 'communication', 'problem solving', 'teamwork', 
                'project management', 'agile', 'scrum', 'critical thinking'
            ]
        }
    
    def parse(self, resume_text: str) -> ParsedResume:
        """
        Main parsing function - extracts all resume information
        """
        cleaned_text = self._preprocess_text(resume_text)
        
        personal_info = self._extract_personal_info(cleaned_text)
        skills = self._extract_skills(cleaned_text)
        experience = self._extract_experience(cleaned_text)
        education = self._extract_education(cleaned_text)
        proficiencies = self._extract_proficiency_levels(cleaned_text, skills)
        
        return ParsedResume(
            personal_info=personal_info,
            skills=skills,
            experience=experience,
            education=education,
            raw_text=resume_text,
            skill_proficiencies=proficiencies
        )
    
    def _preprocess_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = text.lower()
        return text.strip()
    
    def _extract_personal_info(self, text: str) -> Dict[str, str]:
        info = {}
        
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            info['email'] = email_match.group()
        
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone_match:
            info['phone'] = phone_match.group()
        
        linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text)
        if linkedin_match:
            info['linkedin'] = linkedin_match.group()
        
        return info
    
    def _extract_skills(self, text: str) -> List[Dict[str, Any]]:
        """Extract skills using pattern matching against known taxonomy"""
        found_skills = []
        seen = set()
        
        for category, patterns in self.skill_patterns.items():
            for pattern in patterns:
                if pattern in text:
                    if pattern not in seen:
                        found_skills.append({
                            'name': pattern,
                            'category': category,
                            'confidence': 0.9 if len(pattern) > 5 else 0.7
                        })
                        seen.add(pattern)
        
        return found_skills
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """Extract work experience sections"""
        experience = []
        
        exp_pattern = r'(?:experience|work history|employment)[:\s]*([^•]+(?:\n[^•]+)*)'
        matches = re.findall(exp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches[:5]:
            lines = [l.strip() for l in match.split('\n') if l.strip()]
            if lines:
                experience.append({
                    'title': lines[0] if lines else 'Unknown',
                    'details': lines[1:4] if len(lines) > 1 else []
                })
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """Extract education information"""
        education = []
        
        edu_pattern = r'(?:education|academic|degree)[:\s]*([^•]+(?:\n[^•]+)*)'
        matches = re.findall(edu_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches[:3]:
            lines = [l.strip() for l in match.split('\n') if l.strip()]
            if lines:
                education.append({
                    'degree': lines[0] if lines else 'Unknown',
                    'details': lines[1:3] if len(lines) > 1 else []
                })
        
        return education
    
    def _extract_proficiency_levels(
        self, 
        text: str, 
        skills: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Estimate proficiency levels based on context clues
        """
        proficiencies = {}
        
        for skill in skills:
            skill_name = skill['name']
            
            for indicator, level in self.proficiency_indicators.items():
                pattern = rf'\b{indicator}\b.*\b{re.escape(skill_name)}\b|\b{re.escape(skill_name)}\b.*\b{indicator}\b'
                if re.search(pattern, text, re.IGNORECASE):
                    proficiencies[skill_name] = level
                    break
            
            if skill_name not in proficiencies:
                mentions = len(re.findall(rf'\b{re.escape(skill_name)}\b', text))
                years_match = re.search(
                    rf'{re.escape(skill_name)}.*?(\d+)\s*(?:year|yr)',
                    text,
                    re.IGNORECASE
                )
                
                if years_match:
                    years = int(years_match.group(1))
                    proficiencies[skill_name] = min(5.0, 1.0 + years * 0.8)
                elif mentions > 5:
                    proficiencies[skill_name] = 3.5
                elif mentions > 2:
                    proficiencies[skill_name] = 2.5
                else:
                    proficiencies[skill_name] = 2.0
        
        return proficiencies
