from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
import uuid
import json

from app.db import get_db
from app.models import User, Analysis, Roadmap
from app.schemas import (
    UploadResponse, AnalysisResponse, RoadmapResponse,
    ProgressUpdateRequest, ProgressUpdateResponse, DashboardMetrics,
    ChatRequest, ChatResponse
)
from app.services import AnalysisService
# # from app.services.chatbot_service import ChatbotService

router = APIRouter()
analysis_service = AnalysisService()
# # chatbot_service = ChatbotService()


@router.post("/upload", response_model=UploadResponse)
async def upload_documents(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
    email: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload resume and job description for analysis
    """
    session_id = str(uuid.uuid4())[:8]
    
    resume_content = await resume.read()
    jd_content = await job_description.read()
    
    try:
        resume_text = resume_content.decode('utf-8')
    except:
        resume_text = str(resume_content, errors='ignore')
    
    try:
        jd_text = jd_content.decode('utf-8')
    except:
        jd_text = str(jd_content, errors='ignore')
    
    user = db.query(User).filter(User.email == email).first() if email else None
    if not user:
        user = User(email=email, name=email.split('@')[0] if email else f"user_{session_id}")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    analysis = Analysis(
        user_id=user.id,
        session_id=session_id,
        resume_text=resume_text[:5000],
        job_description_text=jd_text[:5000],
        status="uploaded"
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    return UploadResponse(
        session_id=session_id,
        status="uploaded",
        message="Documents uploaded successfully. Use session_id to retrieve analysis."
    )


@router.get("/analyze/{session_id}", response_model=AnalysisResponse)
async def analyze_documents(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Perform complete skill gap analysis
    """
    analysis = db.query(Analysis).filter(Analysis.session_id == session_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if analysis.status == "analyzed":
        return AnalysisResponse(
            session_id=session_id,
            status="analyzed",
            user_skills=json.loads(analysis.user_skills or "[]"),
            required_skills=json.loads(analysis.required_skills or "[]"),
            skill_gaps=json.loads(analysis.skill_gaps or "[]"),
            strong_skills=analysis.strong_skills or [],
            weak_skills=analysis.weak_skills or [],
            reasoning_trace=json.loads(analysis.reasoning_trace or "[]")
        )
    
    if not analysis.resume_text or not analysis.job_description_text:
        raise HTTPException(status_code=400, detail="Missing resume or job description")
    
    analysis_response, priorities = analysis_service.analyze(
        resume_text=analysis.resume_text,
        jd_text=analysis.job_description_text
    )
    
    analysis.user_skills = [s.dict() for s in analysis_response.user_skills]
    analysis.required_skills = [s.dict() for s in analysis_response.required_skills]
    analysis.skill_gaps = [s.dict() for s in analysis_response.skill_gaps]
    analysis.strong_skills = analysis_response.strong_skills
    analysis.weak_skills = analysis_response.weak_skills
    analysis.reasoning_trace = [s.dict() for s in analysis_response.reasoning_trace]
    analysis.status = "analyzed"
    
    db.commit()
    
    analysis_response.session_id = session_id
    return analysis_response


@router.get("/roadmap/{session_id}", response_model=RoadmapResponse)
async def generate_roadmap(
    session_id: str,
    fast_track: bool = False,
    db: Session = Depends(get_db)
):
    """
    Generate personalized learning roadmap
    """
    analysis = db.query(Analysis).filter(Analysis.session_id == session_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if analysis.status != "analyzed":
        raise HTTPException(status_code=400, detail="Analysis not complete. Call /analyze first.")
    
    roadmap = db.query(Roadmap).filter(Roadmap.analysis_id == analysis.id).first()
    
    if roadmap and not fast_track:
        # Handle both string and list types (depends on SQLAlchemy version)
        learning_path = roadmap.learning_path
        if isinstance(learning_path, str):
            learning_path = json.loads(learning_path or "[]")
        
        milestones = roadmap.milestones
        if isinstance(milestones, str):
            milestones = json.loads(milestones or "[]")
        
        return RoadmapResponse(
            session_id=session_id,
            target_role=roadmap.target_role or "Target Role",
            learning_path=learning_path,
            milestones=milestones,
            estimated_total_hours=roadmap.estimated_total_hours,
            fast_track_available=roadmap.fast_track_mode,
            reasoning_trace=[]
        )
    
    from app.ai import PriorityScore
    
    mock_priorities = []
    for gap in (analysis.skill_gaps or [])[:10]:
        mock_priorities.append(PriorityScore(
            skill=gap.get('skill', ''),
            raw_priority=gap.get('priority', 0.5),
            gap_component=gap.get('gap_score', 0.5),
            importance_component=0.5,
            dependency_component=1.0,
            learning_efficiency=0.7,
            final_priority=gap.get('priority', 0.5),
            reasoning=[gap.get('reasoning', '')]
        ))
    
    roadmap_response = analysis_service.generate_roadmap(
        resume_text=analysis.resume_text or "",
        jd_text=analysis.job_description_text or "",
        priorities=mock_priorities,
        fast_track=fast_track
    )
    
    # Convert milestones to dictionaries for JSON serialization
    milestones_data = []
    for m in roadmap_response.milestones:
        if hasattr(m, 'dict'):
            milestones_data.append(m.dict())
        elif isinstance(m, dict):
            milestones_data.append(m)
    
    roadmap = Roadmap(
        analysis_id=analysis.id,
        user_id=analysis.user_id,
        learning_path=[s.dict() if hasattr(s, 'dict') else s for s in roadmap_response.learning_path],
        milestones=milestones_data,
        estimated_total_hours=roadmap_response.estimated_total_hours,
        target_role=roadmap_response.target_role,
        fast_track_mode=fast_track
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)
    
    roadmap_response.session_id = session_id
    return roadmap_response


@router.post("/progress/{session_id}", response_model=ProgressUpdateResponse)
async def update_progress(
    session_id: str,
    update: ProgressUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update learning progress for adaptive roadmap
    """
    analysis = db.query(Analysis).filter(Analysis.session_id == session_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Session not found")
    
    response = analysis_service.update_progress(
        skill_name=update.skill_name,
        completion_percentage=update.completion_percentage,
        current_level=0.0,
        time_spent_hours=update.time_spent_hours or 0,
        assessment_score=update.assessment_score if update.assessment_score is not None else None
    )
    
    return response


@router.get("/dashboard/{session_id}", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get dashboard metrics for session
    """
    analysis = db.query(Analysis).filter(Analysis.session_id == session_id).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Session not found")
    
    roadmap = db.query(Roadmap).filter(Roadmap.analysis_id == analysis.id).first()
    
    user_skills_count = len(json.loads(analysis.user_skills or "[]"))
    skill_gaps_count = len(json.loads(analysis.skill_gaps or "[]"))
    strong_skills_count = len(analysis.strong_skills or [])
    
    return DashboardMetrics(
        total_skills_analyzed=user_skills_count + skill_gaps_count,
        skills_gap_count=skill_gaps_count,
        strong_skills_count=strong_skills_count,
        estimated_learning_hours=roadmap.estimated_total_hours if roadmap else 0,
        progress_percentage=roadmap.progress_percentage if roadmap else 0
    )


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "AI-Adaptive Onboarding Engine"}


# # @router.post("/chat/{session_id}", response_model=ChatResponse)
# # async def chat_with_mentor(
# #     session_id: str,
# #     chat_request: ChatRequest,
# #     db: Session = Depends(get_db)
# # ):
# #     """
# #     AI Chatbot - Conversational learning mentor
# #     """
# #     analysis = db.query(Analysis).filter(Analysis.session_id == session_id).first()
# #     roadmap = db.query(Roadmap).filter(Roadmap.analysis_id == analysis.id).first() if analysis else None
# #     
# #     # Prepare analysis data
# #     analysis_data = None
# #     if analysis:
# #         analysis_data = {
# #             'skill_gaps': json.loads(analysis.skill_gaps or "[]"),
# #             'strong_skills': analysis.strong_skills or [],
# #             'weak_skills': analysis.weak_skills or [],
# #             'user_skills': json.loads(analysis.user_skills or "[]")
# #         }
# #     
# #     # Prepare roadmap data
# #     roadmap_data = None
# #     if roadmap:
# #         learning_path = roadmap.learning_path
# #         if isinstance(learning_path, str):
# #             learning_path = json.loads(learning_path or "[]")
# #         milestones = roadmap.milestones
# #         if isinstance(milestones, str):
# #             milestones = json.loads(milestones or "[]")
# #         
# #         roadmap_data = {
# #             'learning_path': learning_path,
# #             'milestones': milestones,
# #             'estimated_total_hours': roadmap.estimated_total_hours,
# #             'target_role': roadmap.target_role
# #         }
# #     
# #     # Get chatbot response
# #     response = chatbot_service.get_response(
# #         user_message=chat_request.message,
# #         session_id=session_id,
# #         analysis_data=analysis_data,
# #         roadmap_data=roadmap_data
# #     )
# #     
# #     return response
