"""
Skill Gap Analyzer - Identifies and quantifies skill gaps
"""
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class GapAnalysis:
    skill_name: str
    current_level: float
    required_level: float
    gap_score: float
    priority: float
    category: str
    reasoning: str


class GapAnalyzer:
    """
    Analyzes skill gaps between user capabilities and job requirements
    """
    
    def __init__(
        self,
        gap_weight: float = 0.4,
        importance_weight: float = 0.35,
        difficulty_weight: float = 0.25
    ):
        self.gap_weight = gap_weight
        self.importance_weight = importance_weight
        self.difficulty_weight = difficulty_weight
        
        self.level_descriptions = {
            0: "No knowledge",
            1: "Basic awareness",
            2: "Novice - Can perform simple tasks",
            3: "Intermediate - Can work independently",
            4: "Advanced - Can mentor others",
            5: "Expert - Industry recognized expert"
        }
    
    def analyze(
        self,
        user_skills: Dict[str, Dict[str, Any]],
        required_skills: List[Dict[str, Any]]
    ) -> Tuple[List[GapAnalysis], Dict[str, List[str]]]:
        """
        Main analysis function - computes gaps and categorizes skills
        """
        gaps = []
        categorized = {
            'missing': [],
            'weak': [],
            'strong': [],
            'excess': []
        }
        
        required_dict = {s['name']: s for s in required_skills}
        
        all_skills = set(user_skills.keys()) | set(required_dict.keys())
        
        for skill_name in all_skills:
            user_data = user_skills.get(skill_name, {})
            req_data = required_dict.get(skill_name, {})
            
            current_level = user_data.get('resume_level', 0)
            required_level = req_data.get('importance', 0.5) * 5 if req_data else 0
            importance = req_data.get('importance', 0.5) if req_data else 0.5
            
            in_resume = user_data.get('in_resume', False)
            in_jd = user_data.get('in_jd', False) if (skill_name in user_skills) else True
            
            if not in_jd and in_resume:
                categorized['excess'].append(skill_name)
                continue
            
            if not in_resume and required_level > 0:
                gap_score = 1.0
                reasoning = f"Skill '{skill_name}' is required but completely missing from resume"
                
                gaps.append(GapAnalysis(
                    skill_name=skill_name,
                    current_level=0,
                    required_level=required_level,
                    gap_score=gap_score,
                    priority=self._calculate_priority(gap_score, importance, 5),
                    category=user_data.get('category', 'uncategorized'),
                    reasoning=reasoning
                ))
                categorized['missing'].append(skill_name)
                
            elif current_level < required_level:
                gap_score = (required_level - current_level) / 5.0
                reasoning = self._generate_gap_reasoning(
                    skill_name, current_level, required_level, gap_score
                )
                
                gaps.append(GapAnalysis(
                    skill_name=skill_name,
                    current_level=current_level,
                    required_level=required_level,
                    gap_score=gap_score,
                    priority=self._calculate_priority(gap_score, importance, required_level),
                    category=user_data.get('category', 'uncategorized'),
                    reasoning=reasoning
                ))
                categorized['weak'].append(skill_name)
                
            else:
                categorized['strong'].append(skill_name)
        
        gaps.sort(key=lambda x: x.priority, reverse=True)
        
        return gaps, categorized
    
    def _calculate_priority(
        self,
        gap_score: float,
        importance: float,
        required_level: float
    ) -> float:
        """
        Calculate priority score using weighted formula:
        priority = (gap_score × importance_weight) + (importance × gap_weight) + (difficulty_bonus)
        """
        difficulty_factor = 1.0 + (required_level / 10.0)
        
        priority = (
            (gap_score * self.gap_weight) +
            (importance * self.importance_weight) +
            (difficulty_factor * self.difficulty_weight)
        )
        
        return round(priority, 3)
    
    def _generate_gap_reasoning(
        self,
        skill_name: str,
        current: float,
        required: float,
        gap: float
    ) -> str:
        """Generate human-readable reasoning for the gap"""
        current_desc = self.level_descriptions.get(int(current), f"Level {current}")
        required_desc = self.level_descriptions.get(int(required), f"Level {required}")
        
        if gap >= 0.8:
            severity = "critical gap"
        elif gap >= 0.5:
            severity = "significant gap"
        elif gap >= 0.3:
            severity = "moderate gap"
        else:
            severity = "minor gap"
        
        reasoning = (
            f"'{skill_name}' shows {severity}. "
            f"Current proficiency: {current_desc}. "
            f"Required for role: {required_desc}. "
            f"Gap of {gap*100:.0f}% needs to be addressed."
        )
        
        return reasoning
    
    def get_skill_statistics(
        self,
        gaps: List[GapAnalysis],
        categorized: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """Generate summary statistics"""
        total_required = sum(1 for g in gaps) + len(categorized['strong'])
        covered_skills = len(categorized['strong'])
        
        return {
            'total_required_skills': total_required,
            'covered_skills': covered_skills,
            'coverage_percentage': (covered_skills / total_required * 100) if total_required > 0 else 0,
            'missing_skills_count': len(categorized['missing']),
            'weak_skills_count': len(categorized['weak']),
            'strong_skills_count': len(categorized['strong']),
            'average_gap_score': sum(g.gap_score for g in gaps) / len(gaps) if gaps else 0,
            'total_priority_score': sum(g.priority for g in gaps),
            'critical_gaps': [g.skill_name for g in gaps if g.gap_score >= 0.8],
            'moderate_gaps': [g.skill_name for g in gaps if 0.3 <= g.gap_score < 0.8]
        }
