"""
Roadmap Generator - Creates personalized learning roadmaps
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class LearningStep:
    order: int
    skill: str
    target_level: float
    estimated_hours: float
    courses: List[Dict[str, Any]]
    prerequisites_met: bool
    reasoning: str
    dependencies: List[str]
    difficulty: str
    category: str


class RoadmapGenerator:
    """
    Generates personalized learning roadmaps based on gap analysis and priorities
    """
    
    def __init__(self):
        self.course_catalog = self._load_course_catalog()
        self.skill_complexity = self._initialize_complexity()
        self.hours_per_level = 10
    
    def _load_course_catalog(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            'python': [
                {'title': 'Python for Everybody', 'provider': 'Coursera', 'hours': 32, 'level': 'beginner'},
                {'title': 'Python Crash Course', 'provider': 'Udemy', 'hours': 22, 'level': 'beginner'},
                {'title': 'Advanced Python Programming', 'provider': 'Pluralsight', 'hours': 18, 'level': 'advanced'},
            ],
            'javascript': [
                {'title': 'JavaScript Fundamentals', 'provider': 'freeCodeCamp', 'hours': 20, 'level': 'beginner'},
                {'title': 'Modern JavaScript', 'provider': 'Udemy', 'hours': 28, 'level': 'intermediate'},
            ],
            'react': [
                {'title': 'React - The Complete Guide', 'provider': 'Udemy', 'hours': 52, 'level': 'intermediate'},
                {'title': 'React for Beginners', 'provider': 'Wes Bos', 'hours': 30, 'level': 'beginner'},
            ],
            'machine learning': [
                {'title': 'Machine Learning by Stanford', 'provider': 'Coursera', 'hours': 60, 'level': 'intermediate'},
                {'title': 'Deep Learning Specialization', 'provider': 'Coursera', 'hours': 80, 'level': 'advanced'},
                {'title': 'Hands-On Machine Learning', 'provider': 'O\'Reilly', 'hours': 70, 'level': 'advanced'},
            ],
            'sql': [
                {'title': 'SQL for Data Science', 'provider': 'Coursera', 'hours': 20, 'level': 'beginner'},
                {'title': 'Advanced SQL', 'provider': 'Mode', 'hours': 15, 'level': 'advanced'},
            ],
            'docker': [
                {'title': 'Docker Mastery', 'provider': 'Udemy', 'hours': 25, 'level': 'intermediate'},
                {'title': 'Docker & Kubernetes', 'provider': 'Coursera', 'hours': 30, 'level': 'intermediate'},
            ],
            'aws': [
                {'title': 'AWS Certified Solutions Architect', 'provider': 'A Cloud Guru', 'hours': 45, 'level': 'intermediate'},
                {'title': 'AWS Fundamentals', 'provider': 'Coursera', 'hours': 15, 'level': 'beginner'},
            ],
            'data analysis': [
                {'title': 'Data Analysis with Python', 'provider': 'IBM', 'hours': 25, 'level': 'beginner'},
                {'title': 'Pandas for Data Analysis', 'provider': 'DataCamp', 'hours': 20, 'level': 'intermediate'},
            ],
            'deep learning': [
                {'title': 'Deep Learning by DeepLearning.AI', 'provider': 'Coursera', 'hours': 80, 'level': 'advanced'},
                {'title': 'Practical Deep Learning', 'provider': 'fast.ai', 'hours': 50, 'level': 'intermediate'},
            ],
            'statistics': [
                {'title': 'Statistics with R', 'provider': 'Duke', 'hours': 40, 'level': 'intermediate'},
                {'title': 'Probability and Statistics', 'provider': 'MIT OpenCourseWare', 'hours': 30, 'level': 'intermediate'},
            ],
            'leadership': [
                {'title': 'Leadership Skills', 'provider': 'LinkedIn Learning', 'hours': 8, 'level': 'beginner'},
                {'title': 'Strategic Leadership', 'provider': 'Coursera', 'hours': 15, 'level': 'advanced'},
            ],
            'communication': [
                {'title': 'Effective Communication', 'provider': 'LinkedIn Learning', 'hours': 6, 'level': 'beginner'},
                {'title': 'Business Writing', 'provider': 'Coursera', 'hours': 12, 'level': 'intermediate'},
            ]
        }
    
    def _initialize_complexity(self) -> Dict[str, float]:
        return {
            'soft_skills': 0.5,
            'programming_languages': 1.0,
            'databases': 1.2,
            'frameworks_libraries': 1.5,
            'devops_tools': 1.8,
            'cloud_platforms': 2.0,
            'data_engineering': 2.2,
            'ml_ai': 2.5
        }
    
    def generate_roadmap(
        self,
        gaps: List[Any],
        prioritized_skills: List[Any],
        dependency_graph: Any,
        user_current_skills: Dict[str, float],
        fast_track: bool = False
    ) -> Dict[str, Any]:
        """
        Generate complete learning roadmap
        """
        learning_path = []
        milestones = []
        total_hours = 0
        current_position = 0
        
        categories_seen = set()
        current_milestone = {
            'title': 'Foundation',
            'skills': [],
            'estimated_hours': 0,
            'order': 0
        }
        
        for idx, priority in enumerate(prioritized_skills):
            skill = priority.skill
            
            courses = self._find_courses(skill, fast_track)
            estimated_hours = self._calculate_hours(skill, priority, fast_track)
            
            dependencies = []
            if dependency_graph:
                try:
                    dependencies = dependency_graph.get_prerequisites(skill) if hasattr(dependency_graph, 'get_prerequisites') else []
                except:
                    dependencies = []
            
            prereqs_met = all(
                dep in user_current_skills and user_current_skills.get(dep, 0) >= 2.0
                for dep in dependencies
            ) if dependencies else True
            
            difficulty = self._determine_difficulty(skill, priority.final_priority)
            
            step = LearningStep(
                order=idx + 1,
                skill=skill,
                target_level=5.0,
                estimated_hours=estimated_hours,
                courses=courses,
                prerequisites_met=prereqs_met,
                reasoning=priority.reasoning[0] if priority.reasoning else f"Priority: {priority.final_priority:.3f}",
                dependencies=dependencies,
                difficulty=difficulty,
                category=priority.skill.split('_')[0] if hasattr(priority, 'skill') else 'technical'
            )
            
            learning_path.append(step)
            total_hours += estimated_hours
            current_position = idx
            
            category = self._get_skill_category(skill)
            if category and category not in ['soft_skills']:
                current_milestone['skills'].append(skill)
                current_milestone['estimated_hours'] += estimated_hours
                
                if len(current_milestone['skills']) >= 3:
                    milestones.append(current_milestone)
                    current_milestone = {
                        'title': f"{category.replace('_', ' ').title()} Mastery",
                        'skills': [],
                        'estimated_hours': 0,
                        'order': len(milestones)
                    }
        
        if current_milestone['skills']:
            milestones.append(current_milestone)
        
        if not milestones:
            milestones.append({
                'title': 'Learning Complete',
                'skills': [],
                'estimated_hours': 0,
                'order': 0
            })
        
        return {
            'learning_path': [self._step_to_dict(s) for s in learning_path],
            'milestones': milestones,
            'estimated_total_hours': total_hours,
            'current_position': current_position,
            'fast_track_available': fast_track,
            'summary': self._generate_summary(learning_path, total_hours, milestones)
        }
    
    def _find_courses(self, skill: str, fast_track: bool) -> List[Dict[str, Any]]:
        """Find relevant courses for a skill"""
        skill_lower = skill.lower()
        
        courses = self.course_catalog.get(skill_lower, [])
        
        if not courses:
            for skill_key, course_list in self.course_catalog.items():
                if skill_key in skill_lower or skill_lower in skill_key:
                    courses = course_list
                    break
        
        if not courses:
            courses = [{
                'title': f'{skill.title()} Fundamentals',
                'provider': 'Online Resource',
                'duration_hours': 15,
                'level': 'intermediate',
                'url': f'https://example.com/learn/{skill.lower().replace(" ", "-")}',
                'is_free': True,
                'difficulty': 'intermediate'
            }]
        
        if fast_track:
            courses = [c for c in courses if c.get('level') != 'beginner'][:2]
        else:
            courses = courses[:3]
        
        # Normalize course fields
        normalized_courses = []
        for course in courses:
            normalized = {
                'title': course.get('title', ''),
                'provider': course.get('provider', 'Online Resource'),
                'duration_hours': course.get('hours', course.get('duration_hours', 15)),
                'level': course.get('level', 'intermediate'),
                'difficulty': course.get('difficulty', course.get('level', 'intermediate')),
                'url': course.get('url'),
                'is_free': course.get('is_free', True)
            }
            normalized_courses.append(normalized)
        
        return normalized_courses
    
    def _calculate_hours(self, skill: str, priority: Any, fast_track: bool) -> float:
        """Estimate learning time for a skill"""
        base_hours = self.hours_per_level
        
        complexity = 1.0
        for cat, val in self.skill_complexity.items():
            if cat in skill.lower():
                complexity = val
                break
        
        gap_multiplier = 1.0 + (priority.gap_component * 0.5) if hasattr(priority, 'gap_component') else 1.0
        
        hours = base_hours * complexity * gap_multiplier
        
        if fast_track:
            hours *= 0.6
        
        return round(hours, 1)
    
    def _determine_difficulty(self, skill: str, priority: float) -> str:
        """Determine skill difficulty level"""
        for cat, val in self.skill_complexity.items():
            if cat in skill.lower():
                if val >= 2.0:
                    return 'advanced'
                elif val >= 1.5:
                    return 'intermediate'
                else:
                    return 'beginner'
        
        if priority > 0.8:
            return 'advanced'
        elif priority > 0.5:
            return 'intermediate'
        else:
            return 'beginner'
    
    def _get_skill_category(self, skill: str) -> Optional[str]:
        """Get category for a skill"""
        for cat in self.skill_complexity.keys():
            if cat in skill.lower():
                return cat
        return 'technical'
    
    def _step_to_dict(self, step: LearningStep) -> Dict[str, Any]:
        """Convert LearningStep to dictionary"""
        return {
            'order': step.order,
            'skill': step.skill,
            'target_level': step.target_level,
            'estimated_hours': step.estimated_hours,
            'courses': step.courses,
            'prerequisites_met': step.prerequisites_met,
            'reasoning': step.reasoning,
            'dependencies': step.dependencies,
            'difficulty': step.difficulty,
            'category': step.category
        }
    
    def _generate_summary(
        self,
        path: List[LearningStep],
        total_hours: float,
        milestones: List[Dict]
    ) -> str:
        """Generate roadmap summary"""
        skill_count = len(path)
        courses_count = sum(len(step.courses) for step in path)
        
        summary = (
            f"This roadmap covers {skill_count} skills across {len(milestones)} milestones. "
            f"Total estimated learning time: {total_hours:.0f} hours. "
            f"Includes {courses_count} curated courses and resources."
        )
        
        return summary
