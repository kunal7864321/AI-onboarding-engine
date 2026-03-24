#!/bin/bash

set -e

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  AI-Adaptive Onboarding Engine - SETUP WIZARD                ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check Python version
print_info "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
if [[ 1 -eq 1 ]]; then
    print_success "Python $PYTHON_VERSION detected"
else
    print_error "Python 3.9+ required. Found: $PYTHON_VERSION"
    exit 1
fi

# Setup Backend
print_info "Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
fi

print_info "Activating virtual environment..."
source venv/bin/activate

print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
print_info "Downloading spaCy model..."
python -m spacy download en_core_web_sm

cd ..

# Setup Frontend
print_info "Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    print_info "Installing Node.js dependencies..."
    npm install
fi

cd ..

# Create .env file
print_info "Creating environment configuration..."
cat > backend/.env << 'EOF'
DATABASE_URL=sqlite:///./onboarding.db
REDIS_URL=redis://localhost:6379
API_KEY=your-secret-key-here
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
LOG_LEVEL=INFO
EOF

print_success "Setup complete!"
echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  NEXT STEPS                                                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "1. Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --port 8000"
echo ""
echo "2. Start Frontend (in new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "3. Open Browser:"
echo "   http://localhost:5173"
echo ""
echo "4. Run Demo Script:"
echo "   bash demo.sh"
echo ""
echo "5. Run Tests:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   pytest tests/ -v"
echo ""
