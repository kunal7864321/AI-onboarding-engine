"""
Skill Extractor - Core NLP engine for extracting and normalizing skills
"""
from typing import List, Dict, Any, Set, Optional
import re
from collections import Counter


class SkillExtractor:
    """
    Unified skill extraction engine that combines resume and JD parsing
    with skill normalization and level estimation
    """
    
    def __init__(self, skills_taxonomy: Optional[Dict] = None):
        self.skills_taxonomy = skills_taxonomy or self._get_default_taxonomy()
        self.skill_aliases = self._load_aliases()
        self.categories = self._get_categories()
    
    def _get_default_taxonomy(self) -> Dict:
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go',
                'rust', 'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'sql',
                'html', 'css', 'bash', 'shell', 'perl', 'haskell', 'elixir', 'lua'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js',
                'express', 'fastapi', 'rails', 'laravel', 'flutter', 'tensorflow',
                'pytorch', 'scikit-learn', 'pandas', 'numpy', 'scipy', 'keras'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite',
                'oracle', 'sql server', 'dynamodb', 'cassandra', 'neo4j', 'mariadb'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'amazon web services',
                'heroku', 'digitalocean', 'firebase'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'github actions',
                'gitlab', 'jira', 'datadog', 'prometheus', 'grafana', 'elk stack'
            ],
            'ml_ai': [
                'machine learning', 'deep learning', 'nlp', 'computer vision',
                'neural networks', 'reinforcement learning', 'transformers',
                'llm', 'generative ai', 'bert', 'gpt', 'xgboost', 'random forest'
            ],
            'data_engineering': [
                'spark', 'hadoop', 'kafka', 'airflow', 'dbt', 'snowflake', 'bigquery',
                'databricks', 'etl', 'data pipeline', 'data warehouse', 'data lake'
            ],
            'soft_skills': [
                'leadership', 'communication', 'problem solving', 'teamwork',
                'project management', 'agile', 'scrum', 'critical thinking',
                'presentation', 'analytical thinking', 'time management'
            ]
        }
    
    def _load_aliases(self) -> Dict[str, str]:
        return {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'ml': 'machine learning',
            'dl': 'deep learning',
            'aws': 'amazon web services',
            'react.js': 'react',
            'reactjs': 'react',
            'node': 'node.js',
            'nodejs': 'node.js',
            'postgres': 'postgresql',
            'mongo': 'mongodb',
            'vue.js': 'vue',
            'vuejs': 'vue',
            'cnn': 'computer vision',
            'nlp': 'natural language processing',
        }
    
    def _get_categories(self) -> List[str]:
        return list(self.skills_taxonomy.keys())
    
    def extract_skills_from_text(
        self, 
        text: str,
        source_type: str = 'resume'
    ) -> List[Dict[str, Any]]:
        """
        Extract skills from raw text with confidence scores
        """
        text_lower = text.lower()
        found_skills = []
        seen = set()
        
        for category, skills in self.skills_taxonomy.items():
            for skill in skills:
                skill_lower = skill.lower()
                
                if skill_lower in text_lower:
                    normalized = self._normalize_skill(skill_lower)
                    
                    if normalized not in seen:
                        confidence = self._calculate_confidence(
                            text_lower, 
                            skill_lower, 
                            source_type
                        )
                        
                        found_skills.append({
                            'name': normalized,
                            'original_name': skill,
                            'category': category,
                            'confidence': confidence,
                            'source': source_type
                        })
                        seen.add(normalized)
        
        for alias, normalized in self.skill_aliases.items():
            if alias in text_lower and normalized not in seen:
                confidence = self._calculate_confidence(text_lower, alias, source_type)
                
                found_skills.append({
                    'name': normalized,
                    'original_name': alias,
                    'category': self._get_skill_category(normalized),
                    'confidence': confidence * 0.9,
                    'source': source_type
                })
                seen.add(normalized)
        
        return sorted(found_skills, key=lambda x: x['confidence'], reverse=True)
    
    def _normalize_skill(self, skill: str) -> str:
        """Normalize skill names to canonical form"""
        return self.skill_aliases.get(skill, skill)
    
    def _get_skill_category(self, skill: str) -> str:
        """Find category for a normalized skill"""
        skill_lower = skill.lower()
        
        for category, skills in self.skills_taxonomy.items():
            if skill_lower in [s.lower() for s in skills]:
                return category
        
        return 'uncategorized'
    
    def _calculate_confidence(
        self, 
        text: str, 
        skill: str,
        source_type: str
    ) -> float:
        """
        Calculate confidence score for skill extraction
        """
        base_confidence = 0.7
        
        count = text.count(skill)
        if count >= 3:
            base_confidence += 0.15
        elif count >= 2:
            base_confidence += 0.1
        
        skill_patterns = [
            rf'\b{re.escape(skill)}\b\s+(?:experience|proficient|expertise)',
            rf'{re.escape(skill)}\s*\(\d+\+?\s*years?\)',
            rf'(?:proficient|expert|advanced)\s+(?:in|with)\s+{re.escape(skill)}'
        ]
        
        for pattern in skill_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                base_confidence += 0.1
                break
        
        if source_type == 'resume':
            section_patterns = [
                r'skills?[:\s]',
                r'technical\s+skills?[:\s]',
                r'core\s+competencies?[:\s]'
            ]
            for pattern in section_patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    base_confidence += 0.05
                    break
        
        return min(1.0, base_confidence)
    
    def merge_skills(
        self,
        resume_skills: List[Dict],
        jd_skills: List[Dict]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Merge skills from resume and JD into unified structure
        """
        merged = {}
        
        for skill_data in resume_skills:
            name = skill_data['name']
            merged[name] = {
                'name': name,
                'category': skill_data.get('category', 'uncategorized'),
                'resume_level': skill_data.get('confidence', 0.5) * 5,
                'resume_confidence': skill_data.get('confidence', 0.5),
                'in_resume': True,
                'in_jd': False,
                'jd_importance': 0
            }
        
        for skill_data in jd_skills:
            name = skill_data['name']
            
            if name in merged:
                merged[name]['in_jd'] = True
                merged[name]['jd_importance'] = skill_data.get('importance', 0.5)
            else:
                merged[name] = {
                    'name': name,
                    'category': skill_data.get('category', 'uncategorized'),
                    'resume_level': 0,
                    'resume_confidence': 0,
                    'in_resume': False,
                    'in_jd': True,
                    'jd_importance': skill_data.get('importance', 0.5)
                }
        
        return merged
