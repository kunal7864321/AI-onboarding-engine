"""
Priority Engine - Ranks skills based on multi-dimensional scoring
"""
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import math


@dataclass
class PriorityScore:
    skill: str
    raw_priority: float
    gap_component: float
    importance_component: float
    dependency_component: float
    learning_efficiency: float
    final_priority: float
    reasoning: List[str]


class PriorityEngine:
    """
    Core innovation - Multi-dimensional priority scoring engine
    
    Priority Formula:
    final_priority = (gap_score × W_gap) + (importance × W_importance) + (dependency_factor × W_dependency)
    
    Where:
    - W_gap = 0.40 (weight for skill gap)
    - W_importance = 0.35 (weight for job importance)
    - W_dependency = 0.25 (weight for dependency satisfaction)
    """
    
    def __init__(
        self,
        gap_weight: float = 0.40,
        importance_weight: float = 0.35,
        dependency_weight: float = 0.25
    ):
        self.gap_weight = gap_weight
        self.importance_weight = importance_weight
        self.dependency_weight = dependency_weight
        
        self.skill_complexity = self._initialize_complexity_map()
    
    def _initialize_complexity_map(self) -> Dict[str, float]:
        """Base complexity scores for common skill categories"""
        return {
            'programming_languages': 1.0,
            'soft_skills': 0.6,
            'frameworks_libraries': 1.5,
            'databases': 1.2,
            'cloud_platforms': 1.8,
            'devops_tools': 2.0,
            'ml_ai': 2.5,
            'data_engineering': 2.2
        }
    
    def compute_priorities(
        self,
        gaps: List[Any],
        user_skills: Dict[str, Dict],
        dependency_graph: Dict[str, List[str]]
    ) -> List[PriorityScore]:
        """
        Main priority computation - generates ranked skill list
        """
        user_levels = {s: data.get('resume_level', 0) for s, data in user_skills.items()}
        
        priorities = []
        
        for gap in gaps:
            skill = gap.skill_name
            category = gap.category
            
            gap_component = gap.gap_score
            importance_component = gap.priority - gap_component
            
            dependency_score = self._evaluate_dependencies(
                skill, 
                dependency_graph, 
                user_levels
            )
            
            complexity = self.skill_complexity.get(category, 1.0)
            learning_efficiency = self._calculate_learning_efficiency(
                gap_component, 
                complexity, 
                dependency_score
            )
            
            final_priority = self._compute_final_priority(
                gap_component,
                importance_component,
                dependency_score,
                learning_efficiency
            )
            
            reasoning = self._generate_reasoning(
                skill, gap, dependency_score, learning_efficiency
            )
            
            priorities.append(PriorityScore(
                skill=skill,
                raw_priority=gap.priority,
                gap_component=gap_component,
                importance_component=importance_component,
                dependency_component=dependency_score,
                learning_efficiency=learning_efficiency,
                final_priority=final_priority,
                reasoning=reasoning
            ))
        
        priorities.sort(key=lambda x: x.final_priority, reverse=True)
        
        return priorities
    
    def _evaluate_dependencies(
        self,
        skill: str,
        dependency_graph: Dict[str, List[str]],
        user_levels: Dict[str, float]
    ) -> float:
        """
        Evaluate if prerequisites are satisfied
        Returns 0.0-1.0 where 1.0 means all dependencies are met
        """
        dependencies = dependency_graph.get(skill, [])
        
        if not dependencies:
            return 1.0
        
        satisfied = sum(
            1 for dep in dependencies 
            if user_levels.get(dep, 0) >= 2.0
        )
        
        satisfaction_ratio = satisfied / len(dependencies)
        
        if satisfaction_ratio == 1.0:
            return 1.2
        elif satisfaction_ratio >= 0.5:
            return 0.8
        else:
            return 0.5
    
    def _calculate_learning_efficiency(
        self,
        gap_score: float,
        complexity: float,
        dependency_satisfaction: float
    ) -> float:
        """
        Calculate how efficiently this skill can be learned
        Higher efficiency = faster time to proficiency
        """
        base_efficiency = gap_score / complexity
        
        dependency_bonus = (dependency_satisfaction - 0.5) * 0.3
        
        efficiency = base_efficiency + dependency_bonus
        
        return max(0.1, min(1.0, efficiency))
    
    def _compute_final_priority(
        self,
        gap_component: float,
        importance_component: float,
        dependency_component: float,
        learning_efficiency: float
    ) -> float:
        """
        Final priority = weighted sum with efficiency boost
        """
        base_priority = (
            (gap_component * self.gap_weight) +
            (importance_component * self.importance_weight) +
            (dependency_component * self.dependency_weight)
        )
        
        efficiency_boost = 1.0 + (learning_efficiency * 0.2)
        
        final = base_priority * efficiency_boost
        
        return round(final, 4)
    
    def _generate_reasoning(
        self,
        skill: str,
        gap: Any,
        dependency_score: float,
        learning_efficiency: float
    ) -> List[str]:
        """Generate step-by-step reasoning for priority decision"""
        reasoning = []
        
        reasoning.append(
            f"Analyzing priority for '{skill}':"
        )
        
        reasoning.append(
            f"- Gap score: {gap.gap_score:.2f} "
            f"(current: {gap.current_level:.1f}/5 → required: {gap.required_level:.1f}/5)"
        )
        
        if dependency_score >= 1.0:
            reasoning.append(
                f"- Prerequisites: All dependencies satisfied (score: {dependency_score:.2f})"
            )
        else:
            reasoning.append(
                f"- Prerequisites: Some dependencies unmet (score: {dependency_score:.2f})"
            )
        
        reasoning.append(
            f"- Learning efficiency: {learning_efficiency:.2f} "
            f"({'High' if learning_efficiency > 0.7 else 'Medium' if learning_efficiency > 0.4 else 'Low'})"
        )
        
        reasoning.append(
            f"- Final priority score: {gap.priority:.3f} "
            f"(ranked {'high' if gap.priority > 0.7 else 'medium' if gap.priority > 0.4 else 'low'})"
        )
        
        return reasoning
    
    def optimize_learning_order(
        self,
        priorities: List[PriorityScore],
        dependency_graph: Dict[str, List[str]]
    ) -> List[PriorityScore]:
        """
        Optimize learning order based on dependencies
        Skills with unmet dependencies are deprioritized
        """
        optimized = []
        remaining = priorities.copy()
        
        while remaining:
            for i, priority in enumerate(remaining):
                deps = dependency_graph.get(priority.skill, [])
                
                if all(
                    dep in [p.skill for p in optimized] or
                    any(p.skill == dep for p in remaining if p.skill == dep)
                    for dep in deps
                ):
                    optimized.append(remaining.pop(i))
                    break
            else:
                optimized.append(remaining.pop(0))
        
        return optimized
