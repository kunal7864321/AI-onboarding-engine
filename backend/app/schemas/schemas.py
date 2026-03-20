from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SkillLevel(BaseModel):
    skill: str
    level: float = Field(ge=0, le=5, description="Proficiency level 0-5")
    confidence: float = Field(ge=0, le=1, description="Confidence in extraction")
    source: Optional[str] = None


class RequiredSkill(BaseModel):
    skill: str
    required_level: float = Field(ge=0, le=5)
    importance: float = Field(ge=0, le=1, description="Weight in job requirements")
    frequency: int = Field(ge=1, description="Occurrences in JD")


class SkillGap(BaseModel):
    skill: str
    current_level: float
    required_level: float
    gap_score: float = Field(ge=0, description="Normalized gap 0-1")
    priority: float = Field(ge=0, description="Computed priority score")
    reasoning: str


class ReasoningStep(BaseModel):
    step_number: int
    title: str
    description: str
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    confidence: float = Field(ge=0, le=1)


class UploadRequest(BaseModel):
    resume_text: Optional[str] = None
    job_description_text: Optional[str] = None


class UploadResponse(BaseModel):
    session_id: str
    status: str
    message: str


class AnalysisResponse(BaseModel):
    session_id: str
    status: str
    
    user_skills: List[SkillLevel]
    required_skills: List[RequiredSkill]
    
    skill_gaps: List[SkillGap]
    strong_skills: List[str]
    weak_skills: List[str]
    
    reasoning_trace: List[ReasoningStep]
    
    metrics: Dict[str, Any] = Field(default_factory=dict)


class CourseInfo(BaseModel):
    title: str
    provider: str
    duration_hours: float
    difficulty: Optional[str] = 'intermediate'
    url: Optional[str] = None
    is_free: bool


class LearningStep(BaseModel):
    order: int
    skill: str
    target_level: float
    estimated_hours: float
    courses: List[CourseInfo]
    prerequisites_met: bool
    reasoning: str
    dependencies: List[str] = []


class Milestone(BaseModel):
    title: str
    skills: List[str]
    estimated_hours: float
    order: int


class RoadmapResponse(BaseModel):
    session_id: str
    target_role: str
    
    learning_path: List[LearningStep]
    milestones: List[Milestone]
    estimated_total_hours: float
    fast_track_available: bool
    
    reasoning_trace: List[ReasoningStep]


class ProgressUpdateRequest(BaseModel):
    skill_name: str
    completion_percentage: float = Field(ge=0, le=1)
    time_spent_hours: Optional[float] = None
    assessment_score: Optional[float] = Field(None, ge=0, le=100)
    feedback: Optional[str] = None


class ProgressUpdateResponse(BaseModel):
    updated_skill_level: float
    progress_percentage: float
    next_recommended_step: Optional[LearningStep]
    roadmap_updated: bool
    reasoning_trace: List[ReasoningStep]


class DashboardMetrics(BaseModel):
    total_skills_analyzed: int
    skills_gap_count: int
    strong_skills_count: int
    estimated_learning_hours: float
    progress_percentage: float


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    message: str
    type: str
    confidence: float
