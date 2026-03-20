"""
Job Description Parser - Extracts required skills and qualifications from JDs
"""
import re
from typing import List, Dict, Any
from collections import Counter
from dataclasses import dataclass


@dataclass
class ParsedJobDescription:
    title: str
    company: str
    required_skills: List[Dict[str, Any]]
    preferred_skills: List[str]
    qualifications: List[str]
    responsibilities: List[str]
    raw_text: str


class JobDescriptionParser:
    """
    Extracts structured information from job descriptions
    """
    
    def __init__(self):
        self.skill_keywords = self._load_skill_keywords()
        self.importance_patterns = {
            'required': [r'required', r'must have', r'essential', r'minimum', r'needed'],
            'preferred': [r'preferred', r'nice to have', r'bonus', r'plus', r'desirable'],
            'strong_preference': [r'strongly', r'extensive', r'expert', r'advanced']
        }
    
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        return {
            'technical': [
                'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
                'machine learning', 'data analysis', 'statistics', ' algorithms',
                'programming', 'software development', 'api', 'microservices',
                'cloud', 'devops', 'ci/cd', 'git', 'agile', 'scrum'
            ],
            'soft': [
                'communication', 'leadership', 'teamwork', 'problem-solving',
                'analytical', 'presentation', 'project management', 'stakeholder'
            ],
            'domain': [
                'finance', 'healthcare', 'e-commerce', 'marketing', 'retail',
                'manufacturing', 'logistics', 'telecommunications'
            ]
        }
    
    def parse(self, jd_text: str) -> ParsedJobDescription:
        """
        Main parsing function
        """
        cleaned_text = jd_text.lower()
        
        title = self._extract_job_title(jd_text)
        company = self._extract_company(cleaned_text)
        required_skills = self._extract_required_skills(jd_text)
        preferred_skills = self._extract_preferred_skills(jd_text)
        qualifications = self._extract_qualifications(cleaned_text)
        responsibilities = self._extract_responsibilities(cleaned_text)
        
        return ParsedJobDescription(
            title=title,
            company=company,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            qualifications=qualifications,
            responsibilities=responsibilities,
            raw_text=jd_text
        )
    
    def _extract_job_title(self, text: str) -> str:
        """Extract job title - usually in first line or near 'title' keyword"""
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
            if len(first_line) < 100 and not '@' in first_line:
                return first_line
        
        title_match = re.search(r'(?:position|title|role)[:\s]*(.+?)(?:\n|$)', text, re.IGNORECASE)
        if title_match:
            return title_match.group(1).strip()
        
        return "Unknown Position"
    
    def _extract_company(self, text: str) -> str:
        """Extract company name from JD"""
        company_patterns = [
            r'(?:company|organization|firm)[:\s]*(.+?)(?:\n|$)',
            r'(?:at|@)\s*(.+?)(?:\n|$)',
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Unknown Company"
    
    def _extract_required_skills(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract required skills with importance weights based on context
        """
        all_skills = []
        seen = set()
        
        text_lower = text.lower()
        
        for category, keywords in self.skill_keywords.items():
            for skill in keywords:
                if skill in text_lower:
                    if skill not in seen:
                        importance = self._calculate_importance(text_lower, skill)
                        frequency = text_lower.count(skill)
                        
                        all_skills.append({
                            'name': skill,
                            'category': category,
                            'importance': importance,
                            'frequency': frequency
                        })
                        seen.add(skill)
        
        all_skills.sort(key=lambda x: (x['importance'], x['frequency']), reverse=True)
        
        return all_skills
    
    def _calculate_importance(self, text: str, skill: str) -> float:
        """
        Calculate importance score based on:
        1. Mention in required/preferred sections
        2. Proximity to strong preference words
        3. Frequency of mention
        """
        importance = 0.5
        
        for indicator_type, patterns in self.importance_patterns.items():
            for pattern in patterns:
                context = rf'{pattern}.{{0,50}}{re.escape(skill)}|{re.escape(skill)}.{{0,50}}{pattern}'
                if re.search(context, text, re.IGNORECASE):
                    if indicator_type == 'required':
                        importance = max(importance, 0.9)
                    elif indicator_type == 'strong_preference':
                        importance = max(importance, 0.85)
                    elif indicator_type == 'preferred':
                        importance = max(importance, 0.7)
        
        skill_count = text.count(skill)
        if skill_count >= 3:
            importance = min(1.0, importance + 0.1)
        
        return importance
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract nice-to-have skills"""
        preferred = []
        
        preferred_section = re.search(
            r'(?:nice to have|bonus|plus|preferred|desired).*?(?=(?:required|responsibilities|about)|$)',
            text,
            re.IGNORECASE | re.DOTALL
        )
        
        if preferred_section:
            section_text = preferred_section.group().lower()
            
            for category, keywords in self.skill_keywords.items():
                for skill in keywords:
                    if skill in section_text and skill not in preferred:
                        preferred.append(skill)
        
        return preferred
    
    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract qualifications and requirements"""
        qualifications = []
        
        qual_pattern = r'(?:qualifications?|requirements?|minimum|education).*?(?=(?:responsibilities|about|the role)|$)'
        matches = re.findall(qual_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            lines = [l.strip() for l in match.split('\n') if l.strip() and len(l.strip()) > 10]
            qualifications.extend(lines[:5])
        
        return qualifications[:10]
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        
        resp_pattern = r'(?:responsibilities?|duties|what you\'ll do).*?(?=(?:qualifications?|requirements?|about)|$)'
        matches = re.findall(resp_pattern, text, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            lines = [l.strip() for l in match.split('\n') if l.strip() and len(l.strip()) > 15]
            responsibilities.extend(lines[:8])
        
        return responsibilities[:10]
