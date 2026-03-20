from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=True)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="user", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(String(100), unique=True, index=True)
    
    # Parsed data
    resume_text = Column(Text, nullable=True)
    job_description_text = Column(Text, nullable=True)
    resume_file_path = Column(String(500), nullable=True)
    jd_file_path = Column(String(500), nullable=True)
    
    # Extracted skills
    user_skills = Column(JSON, default=list)  # List of {skill, level, confidence}
    required_skills = Column(JSON, default=list)  # List of {skill, level, importance}
    
    # Gap analysis results
    skill_gaps = Column(JSON, default=list)  # List of {skill, gap_score, priority}
    strong_skills = Column(JSON, default=list)
    weak_skills = Column(JSON, default=list)
    
    # Status tracking
    status = Column(String(50), default="uploaded")  # uploaded, parsed, analyzed, roadmap_generated
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Reasoning trace
    reasoning_trace = Column(JSON, default=list)
    
    user = relationship("User", back_populates="analyses")
    roadmap = relationship("Roadmap", back_populates="analysis", uselist=False)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    category = Column(String(100), index=True)  # programming, soft_skill, domain, tool
    subcategory = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    proficiency_scale = Column(JSON, default={"min": 0, "max": 5})
    dependencies = Column(JSON, default=list)  # List of skill names this depends on
    related_skills = Column(JSON, default=list)
    industry_importance = Column(Float, default=0.5)
    metadata_ = Column('metadata', JSON, default=dict)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    provider = Column(String(100))
    description = Column(Text)
    duration_hours = Column(Float)
    difficulty_level = Column(String(50))  # beginner, intermediate, advanced
    skills_covered = Column(JSON, default=list)  # List of skill names
    prerequisites = Column(JSON, default=list)
    url = Column(String(500), nullable=True)
    rating = Column(Float, nullable=True)
    is_free = Column(Boolean, default=False)
    metadata_ = Column('metadata', JSON, default=dict)


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analyses.id"), unique=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Roadmap data
    learning_path = Column(JSON, default=list)  # Ordered list of {skill, courses, duration, order}
    estimated_total_hours = Column(Float, default=0)
    milestones = Column(JSON, default=list)
    
    # Progress tracking
    current_position = Column(Integer, default=0)
    completed_skills = Column(JSON, default=list)
    in_progress_skill = Column(String(100), nullable=True)
    progress_percentage = Column(Float, default=0.0)
    
    # Settings
    fast_track_mode = Column(Boolean, default=False)
    target_role = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    analysis = relationship("Analysis", back_populates="roadmap")
    user = relationship("User", back_populates="roadmaps")
    progress_updates = relationship("ProgressUpdate", back_populates="roadmap", cascade="all, delete-orphan")


class ProgressUpdate(Base):
    __tablename__ = "progress_updates"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    
    skill_name = Column(String(100), nullable=False)
    completion_percentage = Column(Float)  # 0.0 to 1.0
    time_spent_hours = Column(Float)
    assessment_score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    
    # Updated skill levels
    new_skill_level = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    roadmap = relationship("Roadmap", back_populates="progress_updates")
