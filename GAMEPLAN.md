# BizFly - Business Website Generation Platform
## Architecture & Development Standards

### 🎯 Project Vision
A professional, scalable platform that discovers businesses without websites and automatically generates beautiful, minimalistic websites using AI agents for research and content creation.

### 📐 Core Architecture Principles

#### 1. Code Organization Standards
- **NO DEAD CODE**: Every file must serve a purpose
- **NO SEQUENTIAL NAMING**: No main.ts, main_new.ts patterns
- **CLEAR MODULE BOUNDARIES**: Each module has a single responsibility
- **EXPLICIT DEPENDENCIES**: All imports must be necessary
- **TEST ISOLATION**: All tests in dedicated `/tests` folders

#### 2. Directory Structure
```
bizfly/
├── backend/
│   ├── api/                 # FastAPI routes
│   ├── core/                # Core business logic
│   ├── agents/              # AI agent orchestration
│   ├── models/              # Database models
│   ├── services/            # External service integrations
│   ├── templates/           # Website templates engine
│   └── tests/               # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API client services
│   │   ├── stores/         # State management
│   │   └── styles/         # Global styles
│   └── tests/              # Frontend tests
├── shared/
│   ├── types/              # TypeScript type definitions
│   └── constants/          # Shared constants
├── infrastructure/
│   ├── docker/             # Docker configurations
│   └── scripts/            # Deployment scripts
└── archive/                # Old prototype code
```

#### 3. Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14+ with TypeScript
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for session and API caching
- **AI Agents**: Claude API (Anthropic)
- **Search**: Google Places API
- **Styling**: Tailwind CSS
- **Testing**: Pytest (backend), Jest + React Testing Library (frontend)
- **Container**: Docker + Docker Compose

### 🏗 System Components

#### 1. Business Discovery Service
- Searches Google Places API for businesses
- Filters by website presence
- Caches results in Redis
- Returns structured business data

#### 2. AI Research Agent
- Uses Claude to research business information
- Scrapes reviews, social media mentions
- Generates structured business profile
- Stores findings in PostgreSQL

#### 3. Template System
- Professional, minimalistic templates
- Industry-specific variations
- Component-based architecture
- Real-time preview system

#### 4. Website Generation Pipeline
- Selects appropriate template
- Populates with AI-researched content
- Generates static site files
- Deploys to localhost for preview

#### 5. Frontend Application
- Dashboard for search management
- Business selection interface
- Template preview and selection
- Generated website management

### 📋 Development Workflow

#### Before Every Feature
1. Read this GAMEPLAN.md
2. Review code organization standards
3. Check for existing similar code
4. Plan module boundaries

#### Code Quality Checklist
- [ ] No unused imports
- [ ] No commented-out code
- [ ] Clear, descriptive naming
- [ ] Type safety enforced
- [ ] Error handling implemented
- [ ] Tests written
- [ ] Documentation updated

#### Git Commit Standards
- Atomic commits (one logical change)
- Present tense commit messages
- Format: `type: description`
  - `feat:` New feature
  - `fix:` Bug fix
  - `refactor:` Code restructuring
  - `test:` Test additions/changes
  - `docs:` Documentation

### 🔄 Data Flow

1. **Search Phase**
   ```
   User Input → API → Google Places → Filter → Cache → Display
   ```

2. **Research Phase**
   ```
   Selected Business → AI Agent → Web Research → Data Extraction → Database
   ```

3. **Generation Phase**
   ```
   Business Data + Template → Content Generation → Site Assembly → Preview
   ```

### 🚀 Implementation Phases

#### Phase 1: Foundation (Current)
- Project structure setup
- Core API endpoints
- Database models
- Basic frontend shell

#### Phase 2: Discovery
- Google Places integration
- Search and filter logic
- Results caching
- UI for search management

#### Phase 3: AI Integration
- Claude API setup
- Research agent implementation
- Data organization system
- Content generation

#### Phase 4: Templates
- Template engine
- Industry templates
- Preview system
- Customization options

#### Phase 5: Generation
- Pipeline orchestration
- Local deployment
- Export functionality
- Website management

### 🔒 Security & Performance

#### Security
- API key encryption
- Rate limiting
- Input validation
- CORS configuration
- SQL injection prevention

#### Performance
- Redis caching strategy
- Database query optimization
- Lazy loading in frontend
- Image optimization
- Code splitting

### 📏 Quality Standards

#### Backend
- 100% type hints
- Docstrings for all public functions
- Maximum function length: 50 lines
- Maximum file length: 300 lines
- Test coverage minimum: 80%

#### Frontend
- TypeScript strict mode
- Component composition over inheritance
- Maximum component complexity: 150 lines
- Prop validation
- Accessibility standards (WCAG 2.1 AA)

### 🎨 UI/UX Principles
- **Minimalistic**: Clean, uncluttered interface
- **Professional**: Business-appropriate design
- **Intuitive**: Clear user journey
- **Responsive**: Mobile-first approach
- **Fast**: Sub-second interactions

### 📝 Documentation Requirements
- README.md for project overview
- API documentation (OpenAPI/Swagger)
- Component storybook
- Deployment guide
- NO unnecessary documentation files

### ⚠️ Anti-Patterns to Avoid
- Global state mutations
- Circular dependencies
- God objects/functions
- Magic numbers/strings
- Premature optimization
- Over-engineering

### 🔄 Review Before Each Session
1. Is the code organized correctly?
2. Are there any dead files to remove?
3. Is the naming consistent?
4. Are the tests in the right place?
5. Is the documentation current?

---

## Remember: Clean Code > More Features

Every line of code should be:
- **Necessary**: Serves a clear purpose
- **Clear**: Self-documenting
- **Maintainable**: Easy to modify
- **Tested**: Proven to work
- **Performant**: Efficient execution