# BizFly Development Guide

## Quick Start

### One-Command Startup
```bash
./start.sh
```

This script handles everything:
- Environment setup
- Docker or manual deployment
- Database migrations
- Template seeding
- Service startup

## Development Commands

### Backend Development
```bash
cd backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest

# Run with hot reload
uvicorn main:app --reload

# Database operations
alembic upgrade head                    # Run migrations
alembic revision --autogenerate -m "description"  # Create migration
python scripts/seed_templates.py       # Seed templates
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Development server
npm run dev

# Run tests
npm test
npm run test:coverage

# Type checking
npm run typecheck

# Build for production
npm run build
```

### Docker Development
```bash
# Full stack with hot reload
docker-compose up --build

# Individual services
docker-compose up backend
docker-compose up frontend

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run commands in containers
docker-compose exec backend python scripts/seed_templates.py
docker-compose exec backend pytest
docker-compose exec frontend npm test
```

## Code Quality Standards

### Before Committing
1. Read `GAMEPLAN.md` for current standards
2. Run linting and type checking
3. Ensure tests pass
4. No dead code or unused imports
5. Follow naming conventions

### Backend Standards
```bash
# Code formatting
black .

# Type checking
mypy .

# Linting
ruff .

# Test coverage
pytest --cov=backend --cov-report=html
```

### Frontend Standards
```bash
# Type checking
npm run typecheck

# Linting
npm run lint

# Test coverage
npm run test:coverage
```

## Project Structure Principles

- **No Dead Code**: Every file serves a purpose
- **No Sequential Naming**: main.ts, main_new.ts patterns forbidden
- **Clear Modules**: Single responsibility per module
- **Test Isolation**: All tests in `/tests` directories
- **Type Safety**: 100% TypeScript/Python typing

## API Integration

### Environment Variables Required
```bash
GOOGLE_MAPS_API_KEY=your_google_maps_key
ANTHROPIC_API_KEY=your_anthropic_key
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://localhost:6379/0
```

### API Endpoints
- `GET /api/health/` - Health check
- `POST /api/businesses/search` - Search businesses
- `POST /api/research/{id}/start` - Start AI research
- `GET /api/templates/` - List templates
- `POST /api/websites/generate` - Generate website
- `GET /preview/{id}` - Preview generated website

## Testing Strategy

### Backend Tests
- Unit tests for business logic
- Integration tests for API endpoints
- Template generation tests
- Database operation tests

### Frontend Tests
- Component unit tests
- Store state tests
- API integration tests
- E2E user flows

## Deployment Options

### Production with Docker
```bash
docker-compose -f docker-compose.prod.yml up
```

### Manual Production
```bash
# Backend
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# Frontend
cd frontend
npm run build
npm start
```

## Adding New Features

### New Template
1. Create template class in `backend/templates/`
2. Add to `TemplateManager`
3. Add tests in `backend/tests/test_templates/`
4. Run seed script to add to database

### New API Endpoint
1. Add route to appropriate file in `backend/api/`
2. Create/update schemas in `backend/schemas/`
3. Add tests in `backend/tests/test_api/`
4. Update frontend service in `frontend/src/services/`

### New Frontend Component
1. Create component in `frontend/src/components/`
2. Add TypeScript types
3. Create tests in `frontend/tests/components/`
4. Update parent components as needed

## Troubleshooting

### Common Issues

**Docker Permission Errors**
```bash
sudo chown -R $USER:$USER .
```

**Database Connection Errors**
- Check PostgreSQL is running
- Verify connection string in .env
- Ensure database exists

**API Key Errors**
- Verify keys in .env file
- Check API quotas/limits
- Ensure keys have correct permissions

**Template Generation Fails**
- Check business research completed
- Verify template exists in database
- Check file permissions on output directory

### Development Logs
```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend

# Manual logs
tail -f backend.log
tail -f frontend.log

# Application logs in containers
docker-compose exec backend tail -f /var/log/app.log
```

## Performance Optimization

### Backend
- Redis caching for API responses
- Database query optimization
- Async/await for I/O operations
- Connection pooling

### Frontend  
- React Query for caching
- Lazy loading components
- Image optimization
- Code splitting

## Security Considerations

- API keys encrypted/secured
- Input validation on all endpoints
- CORS properly configured
- SQL injection prevention
- Rate limiting on API endpoints

Remember: **Clean Code > More Features**