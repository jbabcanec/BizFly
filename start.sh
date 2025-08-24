#!/bin/bash

# BizFly - One-Command Startup Script
# This script sets up and runs the entire BizFly application

set -e

echo "🚀 Starting BizFly - Business Website Generation Platform"
echo "======================================================="

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_warning ".env file not found. Creating from template..."
    cp .env.example .env
    print_error "Please edit .env file with your API keys before running again:"
    print_error "- GOOGLE_MAPS_API_KEY"
    print_error "- ANTHROPIC_API_KEY"
    exit 1
fi

# Check for required environment variables
if ! grep -q "^GOOGLE_MAPS_API_KEY=.*[^[:space:]]" .env || ! grep -q "^ANTHROPIC_API_KEY=.*[^[:space:]]" .env; then
    print_error "Please set your API keys in .env file:"
    print_error "- GOOGLE_MAPS_API_KEY (from Google Cloud Console)"
    print_error "- ANTHROPIC_API_KEY (from Anthropic Console)"
    exit 1
fi

# Check if Docker is available
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    print_header "🐳 Using Docker for easy setup..."
    
    # Start with Docker Compose
    print_status "Building and starting services with Docker Compose..."
    docker-compose up --build -d
    
    print_status "Waiting for services to start..."
    sleep 10
    
    # Seed database with templates
    print_status "Seeding database with default templates..."
    docker-compose exec backend python scripts/seed_templates.py || print_warning "Template seeding skipped (may already exist)"
    
    print_header "✅ BizFly is running!"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "⚡ Backend API: http://localhost:8000"
    echo "📊 API Docs: http://localhost:8000/docs"
    echo ""
    echo "To stop: docker-compose down"
    echo "To view logs: docker-compose logs -f"
    
else
    print_header "🔧 Docker not found. Using manual setup..."
    
    # Check Python version
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3.11+ is required but not found"
        exit 1
    fi
    
    # Check Node.js version
    if ! command -v node &> /dev/null; then
        print_error "Node.js 18+ is required but not found"
        exit 1
    fi
    
    # Check for PostgreSQL and Redis
    print_warning "Make sure PostgreSQL and Redis are running:"
    print_warning "- PostgreSQL on localhost:5432"
    print_warning "- Redis on localhost:6379"
    
    # Setup backend
    print_header "🐍 Setting up backend..."
    
    if [ ! -d "backend/venv" ]; then
        print_status "Creating Python virtual environment..."
        cd backend
        python3 -m venv venv
        source venv/bin/activate
        print_status "Installing Python dependencies..."
        pip install -r requirements.txt
        cd ..
    else
        print_status "Activating existing virtual environment..."
        cd backend
        source venv/bin/activate
        cd ..
    fi
    
    # Run database migrations
    print_status "Running database migrations..."
    cd backend
    source venv/bin/activate
    alembic upgrade head || print_warning "Migration skipped (database may not be ready)"
    
    # Seed templates
    print_status "Seeding database with templates..."
    python scripts/seed_templates.py || print_warning "Template seeding skipped"
    cd ..
    
    # Setup frontend
    print_header "📦 Setting up frontend..."
    
    if [ ! -d "frontend/node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        cd frontend
        npm install
        cd ..
    else
        print_status "Node.js dependencies already installed"
    fi
    
    # Start services
    print_header "🚀 Starting services..."
    
    # Start backend in background
    print_status "Starting backend server..."
    cd backend
    source venv/bin/activate
    nohup uvicorn main:app --host 0.0.0.0 --port 8000 --reload > ../backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    
    # Start frontend in background
    print_status "Starting frontend server..."
    cd frontend
    nohup npm run dev > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for servers to start
    print_status "Waiting for servers to start..."
    sleep 5
    
    # Check if servers are running
    if curl -s http://localhost:8000/api/health/ > /dev/null; then
        BACKEND_STATUS="✅ Running"
    else
        BACKEND_STATUS="❌ Failed (check backend.log)"
    fi
    
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        FRONTEND_STATUS="✅ Running"
    else
        FRONTEND_STATUS="❌ Failed (check frontend.log)"
    fi
    
    print_header "🎉 BizFly Startup Complete!"
    echo ""
    echo "Backend:  $BACKEND_STATUS"
    echo "Frontend: $FRONTEND_STATUS"
    echo ""
    echo "🌐 Application: http://localhost:3000"
    echo "⚡ API: http://localhost:8000"
    echo "📊 API Docs: http://localhost:8000/docs"
    echo ""
    echo "📋 Logs:"
    echo "  Backend:  tail -f backend.log"
    echo "  Frontend: tail -f frontend.log"
    echo ""
    echo "🛑 To stop:"
    echo "  kill $BACKEND_PID $FRONTEND_PID"
    echo "  or use: pkill -f 'uvicorn\\|npm'"
    
    # Create stop script
    cat > stop.sh << EOF
#!/bin/bash
echo "Stopping BizFly services..."
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
pkill -f 'uvicorn' 2>/dev/null || true
pkill -f 'npm.*dev' 2>/dev/null || true
echo "Services stopped."
EOF
    chmod +x stop.sh
    echo "💡 Quick stop: ./stop.sh"
fi

echo ""
print_header "🎯 Ready to use BizFly!"
echo "1. Open http://localhost:3000"
echo "2. Search for businesses in any location"
echo "3. Select businesses without websites"
echo "4. Generate professional websites with AI"
echo ""
print_status "Happy website generating! 🚀"