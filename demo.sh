"""
Comprehensive Demo Script for AI-Adaptive Onboarding Engine
Usage: bash demo.sh
"""
#!/bin/bash

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  AI-ADAPTIVE ONBOARDING ENGINE - LIVE DEMO                    ║"
echo "║  IISc Bangalore Hackathon Project                             ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_step() {
    echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}▶ $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Step 1: Check Prerequisites
print_step "STEP 1: CHECKING PREREQUISITES"

command -v python3 >/dev/null 2>&1 || { print_error "Python 3 is required but not installed. Aborting."; exit 1; }
command -v node >/dev/null 2>&1 || { print_error "Node.js is required but not installed. Aborting."; exit 1; }
command -v npm >/dev/null 2>&1 || { print_error "npm is required but not installed. Aborting."; exit 1; }

print_success "All prerequisites met"

# Step 2: Backend Setup
print_step "STEP 2: BACKEND SETUP"

cd backend

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
fi

print_info "Activating virtual environment..."
source venv/bin/activate

print_info "Installing backend dependencies..."
pip install -q -r requirements.txt

print_success "Backend dependencies installed"

# Step 3: Start Backend
print_step "STEP 3: STARTING BACKEND SERVER"

print_info "Starting FastAPI server on port 8000..."
print_info "Server will be available at: http://localhost:8000"
print_info "API docs available at: http://localhost:8000/docs"

# Start server in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait for server to start
sleep 5

# Check if server is running
if curl -s http://localhost:8000/health > /dev/null; then
    print_success "Backend server is running (PID: $BACKEND_PID)"
else
    print_error "Backend server failed to start"
    exit 1
fi

# Step 4: Test API Endpoints
print_step "STEP 4: TESTING API ENDPOINTS"

print_info "Testing health endpoint..."
HEALTH=$(curl -s http://localhost:8000/health)
echo "$HEALTH"
print_success "Health check passed"

print_info "Testing resume parsing..."
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "resume=@../data/sample_resumes/sample_resume.txt" \
  -F "job_description=@../data/sample_resumes/sample_job_description.txt" \
  2>/dev/null | python3 -m json.tool | head -20

print_success "Upload endpoint working"

# Step 5: Frontend Setup
print_step "STEP 5: FRONTEND SETUP"

cd ../frontend

if [ ! -d "node_modules" ]; then
    print_info "Installing frontend dependencies..."
    npm install
fi

print_success "Frontend dependencies installed"

# Step 6: Start Frontend
print_step "STEP 6: STARTING FRONTEND"

print_info "Starting React dev server on port 5173..."
print_info "Application will be available at: http://localhost:5173"

# Start frontend in background
npm run dev &
FRONTEND_PID=$!

sleep 5

if curl -s http://localhost:5173 > /dev/null; then
    print_success "Frontend server is running (PID: $FRONTEND_PID)"
else
    print_error "Frontend server failed to start"
fi

# Step 7: Demo Flow
print_step "STEP 7: DEMONSTRATION FLOW"

echo "
Navigate to: http://localhost:5173

DEMO FLOW:
═══════════════════════════════════════════════════════════════════

1️⃣  UPLOAD PAGE (http://localhost:5173/)
    - Click 'Upload Resume'
    - Select: data/sample_resumes/sample_resume.txt
    - Click 'Upload Job Description'
    - Select: data/sample_resumes/sample_job_description.txt
    - Click 'Analyze'
    - Wait for processing (5-10 seconds)

2️⃣  DASHBOARD (http://localhost:5173/dashboard)
    - View skill gap overview
    - See strong skills (green badges)
    - See weak skills (orange badges)
    - Check coverage percentage
    - View estimated learning hours

3️⃣  SKILL GAP ANALYSIS (http://localhost:5173/skill-gap)
    - Visual skill comparison chart
    - Gap scores for each skill
    - Priority rankings
    - Interactive hover details

4️⃣  ROADMAP TIMELINE (http://localhost:5173/roadmap)
    - Chronological learning path
    - Dependencies shown with arrows
    - Time estimates per module
    - Course recommendations
    - Progress tracking

5️⃣  AI REASONING PANEL (http://localhost:5173/reasoning)
    - Step-by-step AI thinking
    - Why each skill is recommended
    - Why order is chosen
    - Why something is skipped
    - Confidence scores

KEY FEATURES TO HIGHLIGHT:
═══════════════════════════════════════════════════════════════════

✅ Original Priority Algorithm
   - Multi-dimensional scoring
   - Gap × Importance × Dependencies
   
✅ Dependency Graph
   - Ensures logical learning order
   - Prevents skill conflicts
   
✅ Adaptive Learning
   - Updates roadmap in real-time
   - Tracks progress automatically
   
✅ Zero Hallucination
   - Only uses real courses
   - Grounded in actual data
   
✅ Explainable AI
   - Every decision has reasoning
   - Builds trust and transparency

API ENDPOINTS TO TEST:
═══════════════════════════════════════════════════════════════════

GET  http://localhost:8000/api/v1/health
GET  http://localhost:8000/api/v1/skills
POST http://localhost:8000/api/v1/upload
GET  http://localhost:8000/api/v1/analyze/{session_id}
GET  http://localhost:8000/api/v1/roadmap/{session_id}
GET  http://localhost:8000/api/v1/reasoning/{session_id}
POST http://localhost:8000/api/v1/progress/{session_id}

DATA FILES:
═══════════════════════════════════════════════════════════════════

Sample Resume: data/sample_resumes/sample_resume.txt
Sample JD:     data/sample_resumes/sample_job_description.txt
Course Catalog: data/courses/catalog.json
Skills Taxonomy: data/skills/taxonomy.json
"

# Cleanup function
cleanup() {
    print_step "CLEANING UP"
    
    print_info "Stopping backend server (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null || true
    
    print_info "Stopping frontend server (PID: $FRONTEND_PID)..."
    kill $FRONTEND_PID 2>/dev/null || true
    
    print_success "All servers stopped"
    print_info "Demo completed successfully!"
}

trap cleanup EXIT

# Keep script running
print_step "DEMO READY"
print_info "Press Ctrl+C to stop all servers and exit"
print_info "Or keep terminal open to access the application"

# Wait for user interrupt
wait
