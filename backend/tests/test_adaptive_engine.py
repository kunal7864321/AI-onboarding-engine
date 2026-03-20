"""
Unit tests for Adaptive Engine
"""
import pytest
from app.ai.adaptive_engine import AdaptiveEngine


class TestAdaptiveEngine:
    def test_update_progress_basic(self):
        engine = AdaptiveEngine()
        
        result = engine.update_progress(
            skill_name='Python',
            completion_percentage=0.5,
            time_spent_hours=10,
            current_level=2.0
        )
        
        assert result.new_skill_level > 2.0
        assert len(result.reasoning) > 0

    def test_update_progress_with_assessment(self):
        engine = AdaptiveEngine()
        
        result = engine.update_progress(
            skill_name='ML',
            completion_percentage=0.8,
            time_spent_hours=20,
            assessment_score=90,
            current_level=3.0
        )
        
        assert result.new_skill_level > 3.0
        assert 'Assessment score: 90' in result.reasoning

    def test_update_progress_max_level(self):
        engine = AdaptiveEngine()
        
        result = engine.update_progress(
            skill_name='Python',
            completion_percentage=1.0,
            time_spent_hours=50,
            assessment_score=95,
            current_level=4.8
        )
        
        assert result.new_skill_level == 5.0

    def test_difficulty_detection(self):
        engine = AdaptiveEngine()
        
        result = engine.detect_learning_difficulties(
            skill_name='ML',
            expected_time=10,
            actual_time=20,
            assessment_score=55
        )
        
        assert result['detected'] == True
        assert len(result['difficulties']) > 0

    def test_learning_velocity(self):
        engine = AdaptiveEngine()
        
        engine.update_progress('Python', 0.5, 10, 80, 2.0)
        engine.update_progress('Python', 0.5, 10, 85, 2.5)
        
        velocity = engine.calculate_learning_velocity('Python')
        assert velocity > 0

    def test_completion_time_prediction(self):
        engine = AdaptiveEngine()
        
        engine.update_progress('ML', 0.5, 20, 85, 2.0)
        
        predicted_time = engine.predict_completion_time('ML', 3.0, 5.0)
        assert predicted_time >= 0
