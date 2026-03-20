"""
Unit tests for Priority Engine
"""
import pytest
from app.ai.priority_engine import PriorityEngine
from dataclasses import dataclass


class TestPriorityEngine:
    def test_compute_priorities_empty_gaps(self):
        engine = PriorityEngine()
        gaps = []
        user_skills = {}
        dependency_graph = {}
        
        result = engine.compute_priorities(gaps, user_skills, dependency_graph)
        assert result == []

    def test_compute_priorities_basic(self):
        engine = PriorityEngine()
        
        @dataclass
        class MockGap:
            skill_name: str
            category: str
            gap_score: float
            current_level: float
            required_level: float
            priority: float
        
        gaps = [
            MockGap('Python', 'programming_languages', 0.8, 2.0, 5.0, 0.7),
            MockGap('React', 'frameworks_libraries', 0.9, 1.0, 5.0, 0.85),
        ]
        user_skills = {'Python': {'resume_level': 2.0}}
        dependency_graph = {'React': ['JavaScript']}
        
        result = engine.compute_priorities(gaps, user_skills, dependency_graph)
        assert len(result) == 2
        assert all(isinstance(r.final_priority, float) for r in result)

    def test_dependency_evaluation(self):
        engine = PriorityEngine()
        user_levels = {'JavaScript': 3.0, 'Python': 2.0}
        dependency_graph = {'React': ['JavaScript'], 'FastAPI': ['Python']}
        
        react_score = engine._evaluate_dependencies('React', dependency_graph, user_levels)
        assert react_score == 1.2
        
        ml_score = engine._evaluate_dependencies('ML', dependency_graph, user_levels)
        assert ml_score == 1.0

    def test_learning_efficiency_calculation(self):
        engine = PriorityEngine()
        
        efficiency = engine._calculate_learning_efficiency(0.8, 1.0, 1.2)
        assert 0 <= efficiency <= 1.0
        
        efficiency2 = engine._calculate_learning_efficiency(0.5, 2.5, 0.5)
        assert 0 <= efficiency2 <= 1.0

    def test_final_priority_computation(self):
        engine = PriorityEngine()
        
        priority = engine._compute_final_priority(0.8, 0.7, 1.2, 0.8)
        assert isinstance(priority, float)
        assert 0 <= priority <= 2.0
