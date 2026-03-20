"""
Analysis Service - Orchestrates the complete analysis pipeline
"""
from typing import Dict, List, Any, Tuple, Optional
from app.services.roadmap_generator import RoadmapGenerator
from app.ai import (
    ResumeParser, JobDescriptionParser, SkillExtractor,
    GapAnalyzer, PriorityEngine, DependencyGraph,
    AdaptiveEngine
)
from app.schemas import (
    SkillLevel, RequiredSkill, SkillGap, ReasoningStep,
    AnalysisResponse, RoadmapResponse, ProgressUpdateResponse, LearningStep
)


class AnalysisService:
    """
    Orchestrates the complete analysis pipeline:
    1. Parse resume and JD
    2. Extract and merge skills
    3. Analyze gaps
    4. Compute priorities
    5. Generate roadmap
    """
    
    def __init__(self):
        self.resume_parser = ResumeParser()
        self.jd_parser = JobDescriptionParser()
        self.skill_extractor = SkillExtractor()
        self.gap_analyzer = GapAnalyzer()
        self.priority_engine = PriorityEngine()
        self.dependency_graph = DependencyGraph()
        self.adaptive_engine = AdaptiveEngine()
        self.roadmap_generator = RoadmapGenerator()
    
    def analyze(
        self,
        resume_text: str,
        jd_text: str
    ) -> Tuple[AnalysisResponse, List[Any]]:
        """
        Main analysis pipeline
        """
        reasoning_trace = []
        
        reasoning_trace.append(ReasoningStep(
            step_number=1,
            title="Resume Parsing",
            description="Extracting structured information from resume",
            input_data={"text_length": len(resume_text)},
            output_data=None,
            confidence=0.9
        ))
        
        parsed_resume = self.resume_parser.parse(resume_text)
        resume_skills = self.skill_extractor.extract_skills_from_text(resume_text, 'resume')
        
        reasoning_trace.append(ReasoningStep(
            step_number=2,
            title="Job Description Parsing",
            description="Extracting requirements from job description",
            input_data={"text_length": len(jd_text)},
            output_data=None,
            confidence=0.9
        ))
        
        parsed_jd = self.jd_parser.parse(jd_text)
        jd_skills = self.skill_extractor.extract_skills_from_text(jd_text, 'jd')
        
        reasoning_trace.append(ReasoningStep(
            step_number=3,
            title="Skill Extraction & Matching",
            description="Merging skills from both sources",
            input_data={
                "resume_skills_count": len(resume_skills),
                "jd_skills_count": len(jd_skills)
            },
            output_data=None,
            confidence=0.85
        ))
        
        merged_skills = self.skill_extractor.merge_skills(resume_skills, jd_skills)
        
        reasoning_trace.append(ReasoningStep(
            step_number=4,
            title="Gap Analysis",
            description="Identifying skill gaps and categorizing skills",
            input_data={"total_skills": len(merged_skills)},
            output_data=None,
            confidence=0.88
        ))
        
        gaps, categorized = self.gap_analyzer.analyze(merged_skills, jd_skills)
        
        reasoning_trace.append(ReasoningStep(
            step_number=5,
            title="Dependency Graph Construction",
            description="Building skill dependency relationships",
            input_data={"skills_in_graph": len(merged_skills)},
            output_data=None,
            confidence=0.82
        ))
        
        categories = {s: data.get('category', 'uncategorized') for s, data in merged_skills.items()}
        dep_graph = self.dependency_graph.build_graph(
            skills=list(merged_skills.keys()),
            categories=categories
        )
        
        reasoning_trace.append(ReasoningStep(
            step_number=6,
            title="Priority Computation",
            description="Ranking skills by learning priority",
            input_data={"gaps_to_prioritize": len(gaps)},
            output_data=None,
            confidence=0.85
        ))
        
        user_levels = {
            s: data.get('resume_level', 0) 
            for s, data in merged_skills.items()
        }
        
        priorities = self.priority_engine.compute_priorities(
            gaps=gaps,
            user_skills=merged_skills,
            dependency_graph={s: [] for s in merged_skills.keys()}
        )
        
        optimized_priorities = self.priority_engine.optimize_learning_order(
            priorities=priorities,
            dependency_graph={s: self.dependency_graph.get_prerequisites(s) for s in merged_skills.keys()}
        )
        
        reasoning_trace.append(ReasoningStep(
            step_number=7,
            title="Analysis Complete",
            description="Skill gap analysis finished",
            input_data=None,
            output_data={
                "missing_skills": len(categorized['missing']),
                "weak_skills": len(categorized['weak']),
                "strong_skills": len(categorized['strong'])
            },
            confidence=0.9
        ))
        
        user_skill_levels = [
            SkillLevel(
                skill=s,
                level=data.get('resume_level', 0),
                confidence=data.get('resume_confidence', 0.5),
                source='resume'
            )
            for s, data in merged_skills.items()
            if data.get('in_resume', False)
        ]
        
        required_skills_list = [
            RequiredSkill(
                skill=s['name'],
                required_level=s.get('importance', 0.5) * 5,
                importance=s.get('importance', 0.5),
                frequency=s.get('frequency', 1)
            )
            for s in jd_skills
        ]
        
        skill_gaps = [
            SkillGap(
                skill=g.skill_name,
                current_level=g.current_level,
                required_level=g.required_level,
                gap_score=g.gap_score,
                priority=g.priority,
                reasoning=g.reasoning
            )
            for g in gaps
        ]
        
        return AnalysisResponse(
            session_id="",
            status="analyzed",
            user_skills=user_skill_levels,
            required_skills=required_skills_list,
            skill_gaps=skill_gaps,
            strong_skills=categorized['strong'],
            weak_skills=categorized['weak'],
            reasoning_trace=reasoning_trace,
            metrics={
                "coverage_percentage": (len(categorized['strong']) / max(1, len(merged_skills))) * 100,
                "total_gaps": len(gaps),
                "average_priority": sum(p.final_priority for p in priorities) / max(1, len(priorities))
            }
        ), priorities
    
    def generate_roadmap(
        self,
        resume_text: str,
        jd_text: str,
        priorities: List[Any],
        fast_track: bool = False
    ) -> RoadmapResponse:
        """
        Generate personalized learning roadmap
        """
        parsed_resume = self.resume_parser.parse(resume_text)
        parsed_jd = self.jd_parser.parse(jd_text)
        
        user_current_skills = parsed_resume.skill_proficiencies
        
        roadmap_data = self.roadmap_generator.generate_roadmap(
            gaps=[],
            prioritized_skills=priorities,
            dependency_graph=self.dependency_graph,
            user_current_skills=user_current_skills,
            fast_track=fast_track
        )
        
        learning_steps = [
            LearningStep(
                order=step['order'],
                skill=step['skill'],
                target_level=step['target_level'],
                estimated_hours=step['estimated_hours'],
                courses=step['courses'],
                prerequisites_met=step['prerequisites_met'],
                reasoning=step['reasoning'],
                dependencies=step['dependencies']
            )
            for step in roadmap_data['learning_path']
        ]
        
        reasoning_steps = [
            ReasoningStep(
                step_number=i + 1,
                title=f"Learning Step {i + 1}: {step['skill']}",
                description=step['reasoning'],
                input_data={"estimated_hours": step['estimated_hours']},
                output_data={"courses_count": len(step['courses'])},
                confidence=0.85
            )
            for i, step in enumerate(roadmap_data['learning_path'][:10])
        ]
        
        return RoadmapResponse(
            session_id="",
            target_role=parsed_jd.title,
            learning_path=learning_steps,
            milestones=roadmap_data['milestones'] if isinstance(roadmap_data['milestones'], list) else [],
            estimated_total_hours=roadmap_data['estimated_total_hours'],
            fast_track_available=fast_track,
            reasoning_trace=reasoning_steps
        )
    
    def update_progress(
        self,
        skill_name: str,
        completion_percentage: float,
        current_level: float,
        time_spent_hours: float = 0,
        assessment_score: Optional[float] = None
    ) -> ProgressUpdateResponse:
        """
        Update learning progress and trigger adaptive changes
        """
        result = self.adaptive_engine.update_progress(
            skill_name=skill_name,
            completion_percentage=completion_percentage,
            time_spent_hours=time_spent_hours,
            assessment_score=assessment_score,
            current_level=current_level
        )
        
        reasoning_steps = [
            ReasoningStep(
                step_number=1,
                title="Progress Update",
                description=r,
                input_data={"skill": skill_name, "completion": completion_percentage},
                output_data={"new_level": result.new_skill_level},
                confidence=0.9
            )
            for i, r in enumerate(result.reasoning)
        ]
        
        return ProgressUpdateResponse(
            updated_skill_level=result.new_skill_level,
            progress_percentage=completion_percentage,
            next_recommended_step=None,
            roadmap_updated=result.roadmap_updated,
            reasoning_trace=reasoning_steps
        )
