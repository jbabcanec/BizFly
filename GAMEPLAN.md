# BizFly - Business Website Generation Platform
## Architecture & Development Standards

### 🎯 Project Vision
A professional, scalable platform that discovers businesses without websites and automatically generates beautiful, minimalistic websites using AI agents for research and content creation.

### 🚀 PRODUCTION READINESS STATUS

#### ✅ Completed Features
- **Authentication System**: JWT-based login with demo users
- **Modern UI**: Glass morphism, animations, responsive design
- **Dashboard**: Centralized workspace with tabs
- **Image Sourcing**: Multi-provider fallback system (Unsplash, Pexels, Picsum)
- **Website Storage**: Complete file management system
- **Static Serving**: Direct preview URLs for generated sites

#### 🔧 Production Requirements

##### Phase 1: Core Infrastructure (ACTIVE)
- [x] Authentication & user management
- [x] Basic dashboard interface
- [x] Template system foundation
- [ ] Google Places API integration
- [ ] Claude API for research
- [ ] Website preview server
- [ ] Export/download system

##### Phase 2: Website Management System
- [ ] **Live Preview Server**
  - Spin up isolated preview on port
  - Graceful teardown after timeout
  - Hot reload for edits
- [ ] **Code Editor Integration**
  - Monaco editor for HTML/CSS/JS
  - Live preview updates
  - Save/restore versions
- [ ] **Export Options**
  - ZIP download
  - GitHub deployment
  - Netlify/Vercel integration
  - FTP upload

##### Phase 3: Production Features
- [ ] User accounts & permissions
- [ ] Payment integration (Stripe)
- [ ] Custom domains
- [ ] SSL certificates
- [ ] Analytics dashboard
- [ ] White-label options

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
│   │   ├── image_service.py # Image sourcing system
│   │   ├── website_storage.py # Website file management
│   │   └── preview_server.py # Local preview servers
│   ├── templates/           # Website templates engine
│   ├── static/              # Static file serving
│   │   ├── websites/        # Generated sites
│   │   └── images/          # Cached images
│   └── tests/               # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── WebsiteManager.tsx # Website management UI
│   │   │   ├── CodeEditor.tsx     # Monaco editor wrapper
│   │   │   └── LivePreview.tsx    # Preview iframe
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API client services
│   │   ├── stores/         # State management
│   │   └── styles/         # Global styles
│   └── tests/              # Frontend tests
├── generated_websites/     # Website storage
│   ├── business_id/
│   │   ├── index.html
│   │   ├── styles.css
│   │   ├── script.js
│   │   ├── images/
│   │   └── metadata.json
│   └── versions/           # Version history
├── infrastructure/
│   ├── docker/             # Docker configurations
│   └── scripts/            # Deployment scripts
└── archive/                # Old prototype code
```

#### 3. Technology Stack
- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Next.js 14+ with TypeScript
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Cache**: Redis for session and API caching
- **AI Agents**: Claude API (Anthropic)
- **Search**: Google Places API
- **Images**: Unsplash, Pexels, Picsum (fallback)
- **Styling**: Tailwind CSS
- **Editor**: Monaco Editor
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
- Generates structured business profile
- Extracts: services, hours, reviews, specialties
- Stores findings in database as JSON

#### 3. Image Service (NEW)
```python
# Multi-provider system with fallbacks
1. Unsplash API (premium quality)
2. Pexels API (free stock)
3. Picsum Photos (lorem ipsum)
4. UI Avatars (logo generation)
```

#### 4. Website Storage System (NEW)
```python
# Complete file management
- Save website files to disk
- Create static serving symlinks
- Generate downloadable ZIPs
- Version control system
- Metadata tracking
```

#### 5. Preview Server System (PLANNED)
```python
# Dynamic preview servers
class PreviewServer:
    - Spin up on random port (8001-8999)
    - Serve single website
    - Auto-teardown after 30 minutes
    - WebSocket for live reload
    - Resource isolation
```

#### 6. Template System
- Professional, minimalistic templates
- Real image integration
- Industry-specific variations
- Component-based architecture
- Live preview system

#### 7. Website Generation Pipeline
```
Business Selected → AI Research → Image Sourcing → 
Template Selection → Content Injection → Save to Disk → 
Create Preview → Serve on Port
```

#### 8. Frontend Application
- **Dashboard**: Central control panel
- **Search Tab**: Find businesses
- **Templates Tab**: Browse designs
- **Websites Tab**: Manage generated sites
  - List view with previews
  - Code editor button
  - Preview button (opens in new tab)
  - Download ZIP
  - Deploy options

### 📋 Website Management UI Design

#### Websites Tab Interface
```typescript
interface WebsiteCard {
  businessName: string
  generatedAt: Date
  template: string
  previewImage: string
  status: 'draft' | 'published'
  actions: {
    preview: () => void    // Opens preview server
    edit: () => void       // Opens code editor
    download: () => void   // ZIP download
    deploy: () => void     // Deploy modal
    delete: () => void     // Confirm & delete
  }
}
```

#### Code Editor Modal
```typescript
interface CodeEditor {
  files: {
    'index.html': string
    'styles.css': string
    'script.js': string
  }
  activeFile: string
  livePreview: boolean
  actions: {
    save: () => void
    saveAs: () => void
    revert: () => void
    export: () => void
  }
}
```

### 🔄 Data Flow

1. **Search Phase**
   ```
   User Input → API → Google Places → Filter → Cache → Display
   ```

2. **Research Phase**
   ```
   Selected Business → AI Agent → Structured Data → Database
   ```

3. **Generation Phase**
   ```
   Business Data + Images + Template → Website Files → Storage → Preview
   ```

4. **Preview Phase** (NEW)
   ```
   Request Preview → Allocate Port → Start Server → Serve Files → Auto-Teardown
   ```

### 🎨 UI/UX Principles
- **Minimalistic**: Clean, uncluttered interface
- **Professional**: Business-appropriate design
- **Visual**: Card-based with preview images
- **Intuitive**: Clear user journey
- **Responsive**: Mobile-first approach
- **Fast**: Sub-second interactions
- **Interactive**: Live preview, inline editing

### 🔒 Security & Performance

#### Security
- API key encryption
- Rate limiting on preview servers
- Sandboxed preview environments
- Input validation
- CORS configuration
- SQL injection prevention
- XSS protection in generated sites

#### Performance
- Redis caching strategy
- Lazy loading images
- Preview server pooling
- Database query optimization
- Code splitting
- CDN for static assets

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

### 🚀 Deployment Strategy

#### Development
```bash
# One-command startup
./start.sh
# Access at localhost:3000
```

#### Production
```bash
# Docker Compose
docker-compose up -d
# Includes: app, db, redis, nginx
```

#### Scaling
- Horizontal scaling for preview servers
- CDN for generated websites
- Database read replicas
- Redis cluster for caching

### 📝 API Endpoints

#### Website Management
```
POST   /api/websites/generate     # Generate new website
GET    /api/websites              # List all websites
GET    /api/websites/{id}         # Get website details
PUT    /api/websites/{id}         # Update website
DELETE /api/websites/{id}         # Delete website
GET    /api/websites/{id}/download # Download ZIP
POST   /api/websites/{id}/preview  # Start preview server
DELETE /api/websites/{id}/preview  # Stop preview server
POST   /api/websites/{id}/deploy   # Deploy to service
```

### 🔄 Review Before Each Session
1. Is the code organized correctly?
2. Are preview servers cleaned up?
3. Are generated files organized?
4. Is image caching working?
5. Are all APIs responding?

### 📊 Success Metrics
- Website generation < 10 seconds
- Preview server startup < 2 seconds
- Image loading < 1 second
- 99.9% uptime for preview servers
- Zero data loss on generated sites

---

## Remember: User Experience > Technical Complexity

Every feature should be:
- **Intuitive**: No manual needed
- **Visual**: Show, don't tell
- **Fast**: Instant feedback
- **Reliable**: Always works
- **Beautiful**: Delight users