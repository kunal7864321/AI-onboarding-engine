"""
Adaptive Learning Engine - Real-time roadmap adaptation based on progress
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class AdaptationResult:
    roadmap_updated: bool
    new_skill_level: float
    recomputed_path: List[Dict[str, Any]]
    reasoning: List[str]


class AdaptiveEngine:
    """
    Core innovation - Real-time learning path adaptation engine
    
    Key Features:
    1. Progress tracking with skill level updates
    2. Dynamic roadmap recomputation
    3. Learning efficiency optimization
    4. Feedback loop integration
    """
    
    def __init__(
        self,
        learning_gain_rate: float = 0.8,
        progress_threshold: float = 0.15,
        recompute_trigger: float = 0.2
    ):
        self.learning_gain_rate = learning_gain_rate
        self.progress_threshold = progress_threshold
        self.recompute_trigger = recompute_trigger
        
        self.progress_history: Dict[str, List[Dict]] = {}
    
    def update_progress(
        self,
        skill_name: str,
        completion_percentage: float,
        time_spent_hours: float,
        assessment_score: Optional[float] = None,
        current_level: float = 0.0
    ) -> AdaptationResult:
        """
        Update skill level based on learning progress
        
        Formula:
        new_level = current_level + (learning_gain × completion_percentage × assessment_factor)
        """
        assessment_factor = 1.0
        
        if assessment_score is not None:
            if assessment_score >= 90:
                assessment_factor = 1.2
            elif assessment_score >= 75:
                assessment_factor = 1.0
            elif assessment_score >= 60:
                assessment_factor = 0.8
            else:
                assessment_factor = 0.6
        
        learning_gain = self.learning_gain_rate * completion_percentage * assessment_factor
        
        new_level = min(5.0, current_level + learning_gain)
        
        actual_gain = new_level - current_level
        
        self._record_progress(
            skill_name, 
            completion_percentage, 
            time_spent_hours, 
            assessment_score,
            actual_gain
        )
        
        reasoning = [
            f"Updating '{skill_name}' proficiency:",
            f"- Current level: {current_level:.2f}/5.0",
            f"- Completion: {completion_percentage*100:.0f}%",
            f"- Assessment score: {assessment_score if assessment_score else 'N/A'}",
            f"- Learning gain: +{actual_gain:.2f}",
            f"- New level: {new_level:.2f}/5.0"
        ]
        
        should_recompute = completion_percentage >= self.recompute_trigger
        
        return AdaptationResult(
            roadmap_updated=should_recompute,
            new_skill_level=new_level,
            recomputed_path=[] if not should_recompute else [],
            reasoning=reasoning
        )
    
    def _record_progress(
        self,
        skill_name: str,
        completion: float,
        time_spent: float,
        assessment: Optional[float],
        gain: float
    ):
        """Record progress for analytics"""
        if skill_name not in self.progress_history:
            self.progress_history[skill_name] = []
        
        self.progress_history[skill_name].append({
            'timestamp': datetime.utcnow().isoformat(),
            'completion': completion,
            'time_spent': time_spent,
            'assessment': assessment,
            'gain': gain
        })
    
    def recompute_roadmap(
        self,
        current_roadmap: List[Dict[str, Any]],
        updated_skills: Dict[str, float],
        remaining_gaps: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Recompute roadmap based on updated skill levels
        
        Recomputation Triggers:
        1. Skill completion ≥ 20%
        2. Significant time deviation from estimate
        3. User feedback suggesting difficulty
        """
        recomputed = []
        updated_skill_set = set(updated_skills.keys())
        
        for step in current_roadmap:
            skill = step.get('skill_name')
            
            if skill in updated_skill_set:
                new_level = updated_skills[skill]
                target_level = step.get('target_level', 5.0)
                
                if new_level >= target_level:
                    step['status'] = 'completed'
                    step['completion'] = 1.0
                    continue
                
                remaining_gap = target_level - new_level
                step['completion'] = min(1.0, new_level / target_level)
                step['estimated_hours_remaining'] = step.get('estimated_hours', 10) * remaining_gap / 5.0
            
            recomputed.append(step)
        
        recomputed = self._optimize_order(recomputed, updated_skills)
        
        return recomputed
    
    def _optimize_order(
        self,
        roadmap: List[Dict[str, Any]],
        updated_skills: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Optimize remaining roadmap order based on current state"""
        remaining = [r for r in roadmap if r.get('status') != 'completed']
        completed = [r for r in roadmap if r.get('status') == 'completed']
        
        def get_priority(step):
            skill = step.get('skill_name', '')
            current_level = updated_skills.get(skill, 0)
            target_level = step.get('target_level', 5.0)
            gap = target_level - current_level
            
            efficiency = step.get('learning_efficiency', 0.5)
            
            return -(gap * efficiency)
        
        remaining.sort(key=get_priority)
        
        return completed + remaining
    
    def detect_learning_difficulties(
        self,
        skill_name: str,
        expected_time: float,
        actual_time: float,
        assessment_score: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Detect if user is struggling with a skill
        """
        time_ratio = actual_time / expected_time if expected_time > 0 else 1.0
        
        difficulties = []
        recommendations = []
        
        if time_ratio > 1.5:
            difficulties.append('Time overrun - taking longer than expected')
            recommendations.append('Consider additional practice exercises')
            recommendations.append('Break skill into smaller sub-skills')
        
        if assessment_score and assessment_score < 70:
            difficulties.append('Assessment score below threshold')
            recommendations.append('Review fundamental concepts')
            recommendations.append('Try alternative learning resources')
        
        if time_ratio > 2.0:
            difficulties.append('Significant time overrun')
            recommendations.append('Consider prerequisite knowledge gaps')
            recommendations.append('May need instructor-led training')
        
        return {
            'detected': len(difficulties) > 0,
            'difficulties': difficulties,
            'recommendations': recommendations,
            'time_ratio': time_ratio,
            'suggested_action': self._determine_action(difficulties)
        }
    
    def _determine_action(self, difficulties: List[str]) -> str:
        """Determine suggested action based on difficulties"""
        if not difficulties:
            return 'continue'
        
        if 'Significant time overrun' in difficulties:
            return 'reduce_scope'
        
        if 'Assessment score below threshold' in difficulties:
            return 'additional_practice'
        
        return 'monitor'
    
    def calculate_learning_velocity(
        self,
        skill_name: str
    ) -> float:
        """
        Calculate learning velocity (level increase per hour)
        """
        history = self.progress_history.get(skill_name, [])
        
        if len(history) < 2:
            return 0.0
        
        total_gain = sum(h['gain'] for h in history)
        total_time = sum(h['time_spent'] for h in history)
        
        if total_time == 0:
            return 0.0
        
        return total_gain / total_time
    
    def predict_completion_time(
        self,
        skill_name: str,
        current_level: float,
        target_level: float
    ) -> float:
        """
        Predict time to reach target level
        """
        velocity = self.calculate_learning_velocity(skill_name)
        
        if velocity <= 0:
            velocity = 0.2
        
        level_gain = target_level - current_level
        
        if level_gain <= 0:
            return 0.0
        
        return level_gain / velocity
    
    def generate_insights(
        self,
        progress_data: Dict[str, List[Dict]]
    ) -> List[Dict[str, Any]]:
        """
        Generate learning insights from progress data
        """
        insights = []
        
        for skill, history in progress_data.items():
            if not history:
                continue
            
            total_time = sum(h['time_spent'] for h in history)
            total_gain = sum(h['gain'] for h in history)
            avg_assessment = sum(h['assessment'] for h in history if h['assessment']) / max(1, len([h for h in history if h['assessment']]))
            
            velocity = total_gain / total_time if total_time > 0 else 0
            
            if velocity < 0.1:
                insights.append({
                    'type': 'struggle',
                    'skill': skill,
                    'message': f"Learning '{skill}' is taking longer than expected",
                    'metric': f"Velocity: {velocity:.3f} levels/hour"
                })
            elif velocity > 0.5:
                insights.append({
                    'type': 'success',
                    'skill': skill,
                    'message': f"Excellent progress on '{skill}'!",
                    'metric': f"Velocity: {velocity:.3f} levels/hour"
                })
            
            if avg_assessment > 0:
                if avg_assessment < 60:
                    insights.append({
                        'type': 'attention',
                        'skill': skill,
                        'message': f"Assessment scores for '{skill}' need improvement",
                        'metric': f"Avg score: {avg_assessment:.1f}%"
                    })
        
        return insights
