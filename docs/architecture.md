# AI-Adaptive Onboarding Engine - Technical Architecture

## Overview
This document describes the complete technical architecture of the AI-Adaptive Onboarding Engine, a hackathon-winning project for IISc Bangalore.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │  Upload  │ │Dashboard │ │ SkillGap │ │ Roadmap  │         │
│  │  Page    │ │  Page    │ │  Page    │ │  Page    │         │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘         │
│                          │                                     │
│                     Recharts UI                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI)                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     API Routes                            │  │
│  │  /upload  /analyze  /roadmap  /progress  /dashboard    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   Services Layer                          │  │
│  │  AnalysisService  │  RoadmapGenerator  │  AdaptiveEngine │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    AI/ML Layer                           │  │
│  │  ResumeParser  │  JDParser  │  GapAnalyzer  │  Priority │  │
│  │  DependencyGraph  │  SkillExtractor  │  AdaptiveEngine   │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                 Database (SQLAlchemy)                    │  │
│  │  Users  │  Analysis  │  Skills  │  Courses  │  Roadmaps │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## AI/ML Pipeline

### 1. Resume Parser (`resume_parser.py`)
**Purpose:** Extract structured information from resumes

**Features:**
- Pattern matching for personal info (email, phone, LinkedIn)
- Skills extraction using taxonomy
- Proficiency estimation based on context
- Experience and education parsing

**Output:**
```python
ParsedResume:
  - personal_info: Dict[str, str]
  - skills: List[Dict[str, Any]]
  - experience: List[Dict[str, Any]]
  - education: List[Dict[str, Any]]
  - skill_proficiencies: Dict[str, float]
```

### 2. Job Description Parser (`jd_parser.py`)
**Purpose:** Extract requirements from job descriptions

**Features:**
- Job title and company extraction
- Required skills identification with importance weights
- Preferred skills categorization
- Qualification and responsibility extraction

**Key Innovation:**
Importance calculation based on:
- Keyword proximity ("required", "must have", "strong")
- Frequency of mention
- Section context

### 3. Skill Extractor (`skill_extractor.py`)
**Purpose:** Unified skill extraction and normalization

**Features:**
- Skill alias handling (JS → JavaScript)
- Category classification
- Confidence scoring
- Cross-source merging (resume + JD)

**Algorithm:**
1. Pattern matching against taxonomy
2. Alias normalization
3. Confidence calculation based on context
4. Merge with importance weights from JD

### 4. Gap Analyzer (`gap_analyzer.py`)
**Purpose:** Identify and quantify skill gaps

**Gap Score Formula:**
```
gap_score = (required_level - current_level) / 5.0
```

**Skill Categorization:**
- **Strong:** current_level ≥ required_level
- **Weak:** 0 < gap < required_level
- **Missing:** skill not in resume

### 5. Priority Engine (`priority_engine.py`) - **CORE INNOVATION**
**Purpose:** Rank skills by learning priority

**Priority Formula:**
```
final_priority = (
    (gap_score × W_gap) + 
    (importance × W_importance) + 
    (dependency_satisfaction × W_dependency)
) × learning_efficiency
```

**Where:**
- W_gap = 0.40 (weight for skill gap)
- W_importance = 0.35 (weight for job importance)
- W_dependency = 0.25 (weight for dependency satisfaction)

**Learning Efficiency:**
```
learning_efficiency = (gap_score / complexity) × dependency_bonus
```

**Why This Works:**
1. Prioritizes large gaps (need to learn a lot)
2. Considers job importance (must-have vs nice-to-have)
3. Rewards satisfied dependencies (can learn efficiently)
4. Accounts for skill complexity (harder skills take longer)

### 6. Dependency Graph (`dependency_graph.py`)
**Purpose:** Manage skill learning order

**Algorithm:** Topological Sort with Cycle Breaking

**Features:**
- Graph construction from skill dependencies
- Learning order calculation
- Prerequisite validation
- Cycle detection and resolution

**Example Dependencies:**
```
React → JavaScript, HTML, CSS
Machine Learning → Python, Statistics
Deep Learning → Machine Learning
```

### 7. Adaptive Engine (`adaptive_engine.py`)
**Purpose:** Real-time roadmap adaptation

**Progress Update Formula:**
```
new_level = current_level + (learning_gain × completion × assessment_factor)

where:
  learning_gain = 0.8 (configurable rate)
  assessment_factor = 1.0-1.2 based on test scores
```

**Recomputation Triggers:**
- Skill completion ≥ 20%
- Significant time deviation
- User feedback indicating difficulty

**Key Features:**
- Learning velocity calculation
- Completion time prediction
- Difficulty detection
- Insight generation

## Data Models

### User
```python
User:
  - id: int
  - email: str
  - name: str
  - created_at: datetime
```

### Analysis
```python
Analysis:
  - id: int
  - user_id: int
  - session_id: str
  - resume_text: str
  - job_description_text: str
  - user_skills: JSON
  - required_skills: JSON
  - skill_gaps: JSON
  - strong_skills: JSON
  - weak_skills: JSON
  - reasoning_trace: JSON
  - status: str
```

### Roadmap
```python
Roadmap:
  - id: int
  - analysis_id: int
  - user_id: int
  - learning_path: JSON
  - milestones: JSON
  - estimated_total_hours: float
  - progress_percentage: float
  - fast_track_mode: bool
```

## API Endpoints

### POST `/api/v1/upload`
Upload resume and job description
- Input: Multipart form (resume file, JD file, email)
- Output: session_id for tracking

### GET `/api/v1/analyze/{session_id}`
Perform skill gap analysis
- Output: Complete analysis with reasoning trace

### GET `/api/v1/roadmap/{session_id}`
Generate learning roadmap
- Query params: fast_track (bool)
- Output: Ordered learning path with courses

### POST `/api/v1/progress/{session_id}`
Update learning progress
- Input: skill_name, completion_percentage, time_spent, assessment_score
- Output: New skill level, roadmap update decision

### GET `/api/v1/dashboard/{session_id}`
Get dashboard metrics
- Output: Key metrics for UI display

## Frontend Architecture

### State Management (Zustand)
```typescript
interface AppState {
  sessionId: string | null;
  analysis: AnalysisResponse | null;
  roadmap: RoadmapResponse | null;
  isLoading: boolean;
  error: string | null;
}
```

### Pages
1. **UploadPage** - File upload with drag-drop
2. **Dashboard** - Metrics overview with charts
3. **SkillGap** - Detailed gap visualization
4. **Roadmap** - Timeline and milestones
5. **ReasoningPanel** - AI decision explanation

### Key Libraries
- **React Router** - Navigation
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Tailwind CSS** - Styling

## Key Innovations

### 1. Zero Hallucination
- Skills grounded in real taxonomy
- Courses from curated catalog only
- No generated content

### 2. Explainable AI
- Every decision has reasoning
- Step-by-step trace visible
- Formula transparency

### 3. Adaptive Learning
- Real-time roadmap updates
- Progress-based adaptation
- Difficulty detection

### 4. Cross-Domain Scalability
- Works for tech + non-tech
- Extensible skill taxonomy
- Universal algorithms

## Performance Considerations

### Backend
- Async/await for I/O operations
- Connection pooling for database
- Caching for skill lookups

### Frontend
- Lazy loading for pages
- Memoization for expensive computations
- Optimistic UI updates

## Security

- File upload validation
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Input sanitization

## Scalability

- Stateless API design
- Database connection pooling
- Horizontal scaling ready
- Redis caching compatible

## Testing Strategy

- Unit tests for AI modules
- Integration tests for API
- E2E tests for critical flows
- Mock data for reproducibility

## Future Enhancements

1. **AI Mentor Chatbot** - Conversational guidance
2. **Gamification** - XP and badges
3. **Multi-Role Comparison** - Career path switching
4. **Industry Benchmarks** - Resume scoring
5. **Real-time Collaboration** - Team learning

## Conclusion

This architecture demonstrates production-ready engineering with:
- Clean separation of concerns
- Original, well-documented algorithms
- Comprehensive AI reasoning
- Beautiful, functional UI

The system is designed to win hackathons by combining technical sophistication with real-world usability.
