# AI-Adaptive Onboarding Engine

> An intelligent onboarding system that analyzes resumes and job descriptions to create **personalized learning roadmaps** with **real-time adaptation** and **explainable AI reasoning**.

## 🎯 Project Overview
This project demonstrates a production-ready AI system for corporate learning and development, featuring smart resume parsing, multi-dimensional gap analysis, and an original priority algorithm to rank skills based on gap, importance, and dependencies.

## ⚙️ Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Download the NLP model: `python -m spacy download en_core_web_sm`
5. Run the server: `uvicorn app.main:app --reload --port 8000`

### Frontend Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

## 📦 Dependencies

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion
- Zustand

**Backend:**
- FastAPI (Python 3.11)
- SQLAlchemy
- PostgreSQL / SQLite
- Redis
- spaCy (`en_core_web_sm`)

## 🧠 Skill-Gap Analysis Logic

The core logic for skill-gap analysis and roadmap generation relies on extracting proficiencies from the user's resume and comparing them against the core requirements parsed from the given job description.

The differences are measured and fed into our **Priority Engine**, which ranks what the user should learn first using the following formula:
`final_priority = (gap_score × 0.40) + (importance × 0.35) + (dependency × 0.25)`

- **Gap Score (40%)**: The numerical difference between the user's current proficiency and the job's requirement.
- **Importance (35%)**: How critical the specific skill is for the role (e.g., core skill vs. nice-to-have).
- **Dependencies (25%)**: Whether prerequisite foundational skills have been met (calculated via our Logic-Based Dependency Graph).
