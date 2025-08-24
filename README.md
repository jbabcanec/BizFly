# BizFly - AI-Powered Business Website Generator

🚀 **BizFly** is a stunning, modern platform that discovers businesses without websites and generates beautiful, professional websites using AI-powered research and premium design templates.

![BizFly Dashboard](https://img.shields.io/badge/Status-Production%20Ready-brightgreen) ![Next.js](https://img.shields.io/badge/Next.js-14-black) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688) ![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)

## ✨ Features

### 🔐 **Secure Authentication System**
- **User Login**: Secure JWT-based authentication
- **Protected Dashboard**: Role-based access control
- **Demo Users**: 
  - Username: `floj` / Password: `7428`
  - Username: `drew` / Password: `philip`

### 🎨 **Stunning User Interface**
- **Modern Design**: Glass morphism, smooth animations, and professional gradients
- **Responsive Layout**: Perfect on desktop, tablet, and mobile
- **Centered Dashboard**: Clean, intuitive user experience
- **Interactive Elements**: Hover effects, micro-interactions, and smooth transitions

### 🤖 **AI-Powered Business Discovery**
- **Smart Search**: Find businesses in any location using Google Places API
- **Website Analysis**: Automatically identifies businesses without websites
- **AI Research**: Claude-powered agent researches business information
- **Intelligent Filtering**: Focus on businesses that need websites

### 🏗 **Professional Website Templates**
- **Minimal Professional**: Clean, modern design for service businesses
- **Modern Creative**: Bold design with animations and gradients  
- **Luxury Business**: Premium dark theme with gold accents for high-end businesses
- **Mobile-First**: All templates are fully responsive
- **SEO Optimized**: Built-in SEO best practices

### ⚡ **Instant Website Generation**
- **One-Click Generation**: AI-curated content with professional design
- **Live Preview**: Instant preview of generated websites
- **Custom Templates**: Easy template customization and extension
- **Export Ready**: Generated sites ready for deployment

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Google Maps API Key
- Anthropic Claude API Key

### One-Command Startup

**Option 1: Bash Script (Linux/Mac)**
```bash
./start.sh
```

**Option 2: Python Script (Cross-platform)**
```bash
python3 run.py
```

**Option 3: Docker Compose**
```bash
cp .env.example .env
# Edit .env with your API keys
docker-compose up
```

### Manual Installation

1. Clone and setup:
```bash
git clone https://github.com/jbabcanec/BizFly.git
cd bizfly
cp .env.example .env
# Edit .env with your API keys
```

2. Backend setup:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_templates.py
```

3. Frontend setup:
```bash
cd frontend
npm install
```

4. Start services:
```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal 2: Frontend  
cd frontend && npm run dev
```

## 🎯 Usage

### Authentication
1. **Login**: Go to http://localhost:3000 and click "Login"
2. **Demo Access**: Use provided demo credentials:
   - `floj` / `7428` or `drew` / `philip`
3. **Dashboard**: Access your personalized dashboard

### Website Generation Workflow
1. **Search**: Enter a location to discover local businesses
2. **Filter**: View businesses without existing websites
3. **Select**: Choose a business to generate a website for
4. **Research**: AI automatically researches business information
5. **Template**: Choose from professional templates
6. **Generate**: One-click website creation with AI content
7. **Preview**: View and customize your generated website
8. **Export**: Download or deploy your finished website

## 🖼 Screenshots

### Landing Page
Beautiful hero section with gradient animations and professional design

### Login Interface  
Secure, modern login form with glass morphism effects

### Dashboard
Centered layout with intuitive navigation and stunning visual elements

### Website Templates
Professional templates with live previews and customization options

## Project Structure

```
bizfly/
├── backend/            # FastAPI backend
│   ├── api/           # API endpoints
│   ├── agents/        # AI agents
│   ├── core/          # Core configuration
│   ├── models/        # Database models
│   ├── services/      # External services
│   └── templates/     # Website templates
├── frontend/          # Next.js frontend
│   └── src/
│       ├── components/  # React components
│       ├── pages/       # Next.js pages
│       ├── services/    # API client
│       └── stores/      # State management
└── archive/           # Prototype code
```

## API Documentation

Once running, API documentation is available at:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

## Development

### Code Quality Standards

- Read `GAMEPLAN.md` before making changes
- No dead code or sequential naming
- All tests in `/tests` folders
- Maintain clean module boundaries
- Follow TypeScript strict mode in frontend
- Python type hints required in backend

### Running Tests

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_MAPS_API_KEY` | Google Maps API key for business search | Yes |
| `ANTHROPIC_API_KEY` | Claude API key for AI research | Yes |
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `REDIS_URL` | Redis connection string | Yes |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes |

## 🎨 Design Features

### Modern UI/UX
- **Glass Morphism**: Translucent elements with backdrop blur
- **Smooth Animations**: Fade-in, slide-in, and floating animations
- **Professional Typography**: Inter font with perfect hierarchy
- **Color System**: Carefully crafted color palette with gradients
- **Interactive Elements**: Hover states and micro-interactions

### Responsive Design
- **Mobile-First**: Optimized for all screen sizes
- **Flexible Grids**: CSS Grid and Flexbox layouts
- **Touch-Friendly**: Optimized for mobile interactions
- **Cross-Browser**: Compatible with all modern browsers

## 🔧 Technical Architecture

### Backend (FastAPI)
- **Modern Python**: FastAPI with async/await
- **Type Safety**: 100% Python type hints
- **API Documentation**: Auto-generated OpenAPI/Swagger docs
- **Database**: SQLAlchemy ORM with PostgreSQL
- **Authentication**: JWT tokens with secure password hashing

### Frontend (Next.js)
- **React 18**: Latest React features with hooks
- **TypeScript**: Strict type checking throughout
- **Tailwind CSS**: Utility-first styling with custom design system
- **State Management**: Zustand for clean state handling
- **API Integration**: Optimized API calls with error handling

### AI Integration
- **Claude API**: Advanced AI for business research
- **Content Generation**: Intelligent website content creation
- **Template Population**: AI-driven template customization

## License

MIT