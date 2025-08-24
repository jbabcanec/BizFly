# 🚀 BizFly Production Deployment Guide

## 📋 AWS Deployment Checklist

### ✅ Codebase Audit Complete
- [x] Removed dead code and duplicates
- [x] Cleaned up empty directories
- [x] Organized file structure
- [x] Ray's Diner demo website generated
- [x] Environment variables configured

### 🔧 Pre-Deployment Requirements

#### AWS Services Needed
- [ ] **EC2 Instance** (t3.medium recommended)
- [ ] **RDS PostgreSQL** (db.t3.micro for start)
- [ ] **ElastiCache Redis** (cache.t3.micro)
- [ ] **S3 Bucket** for generated websites
- [ ] **CloudFront** for CDN
- [ ] **Application Load Balancer**
- [ ] **Route 53** for DNS
- [ ] **ACM Certificate** for SSL

#### API Keys Required
- [ ] Google Maps API Key
- [ ] Anthropic Claude API Key
- [ ] Unsplash API Key (optional)
- [ ] Pexels API Key (optional)

### 🏗️ Architecture Overview

```
Internet → Route 53 → ALB → EC2 (Docker Compose)
                             ├── Frontend (Next.js)
                             ├── Backend (FastAPI)
                             ├── PostgreSQL (RDS)
                             └── Redis (ElastiCache)
                           
Generated Websites → S3 → CloudFront → Users
```

## 📦 Deployment Methods

### Method 1: Docker Compose (Recommended)

1. **Launch EC2 Instance**
   ```bash
   # Amazon Linux 2023
   sudo yum update -y
   sudo yum install -y docker docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -a -G docker ec2-user
   ```

2. **Deploy Application**
   ```bash
   git clone https://github.com/jbabcanec/BizFly.git
   cd BizFly
   
   # Configure production environment
   cp .env.production .env
   nano .env  # Update with real credentials
   
   # Start services
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Setup SSL Certificate**
   ```bash
   # Using Let's Encrypt
   sudo yum install -y certbot
   sudo certbot certonly --standalone -d bizfly.ai -d api.bizfly.ai
   ```

### Method 2: AWS ECS (Scalable)

1. **Create ECS Cluster**
2. **Build and push Docker images to ECR**
3. **Create ECS Service definitions**
4. **Configure Application Load Balancer**
5. **Setup auto-scaling policies**

## 🌐 Domain Configuration

### DNS Records (Route 53)
```
A     bizfly.ai           → ALB IP
A     www.bizfly.ai       → ALB IP  
A     api.bizfly.ai       → ALB IP
CNAME preview.bizfly.ai   → ALB DNS
```

### SSL Certificate (ACM)
- Create certificate for `*.bizfly.ai`
- Validate via DNS
- Attach to Application Load Balancer

## 📊 Monitoring & Logging

### CloudWatch Metrics
- EC2 instance health
- Application response times  
- Error rates
- Database connections
- Redis memory usage

### Application Logs
```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🔒 Security Configuration

### Environment Variables
Update `.env.production` with:
- Strong JWT secret keys
- Secure database passwords
- Real API keys
- Production domain names

### Network Security
- VPC with private/public subnets
- Security groups allowing only necessary ports
- WAF protection for web traffic
- Private subnets for database/cache

### SSL/TLS
- Force HTTPS redirects
- HSTS headers
- Secure cookie flags

## 💰 Cost Estimation (Monthly)

### Minimal Setup
- EC2 t3.medium: ~$30
- RDS db.t3.micro: ~$15
- ElastiCache t3.micro: ~$15
- S3 storage (100GB): ~$2
- CloudFront: ~$5
- **Total: ~$67/month**

### Production Setup  
- EC2 t3.large: ~$60
- RDS db.t3.small: ~$25
- ElastiCache t3.small: ~$25
- Load Balancer: ~$20
- S3 + CloudFront: ~$10
- **Total: ~$140/month**

## 🚀 Deployment Commands

### Initial Deployment
```bash
# 1. Setup infrastructure
terraform apply

# 2. Deploy application
./deploy.sh production

# 3. Run database migrations
docker-compose exec backend alembic upgrade head

# 4. Create initial data
docker-compose exec backend python scripts/seed_templates.py
```

### Updates
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Health check
curl https://api.bizfly.ai/api/health/
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Multiple EC2 instances behind ALB
- Read replicas for PostgreSQL
- Redis cluster for caching
- Multiple preview server workers

### Performance Optimization
- CloudFront caching for generated websites
- Redis caching for API responses
- Database query optimization
- Image CDN for template assets

## 🔧 Maintenance Tasks

### Daily
- Monitor application logs
- Check system resources
- Verify backup completion

### Weekly
- Review security logs
- Update dependencies
- Performance analysis

### Monthly
- Security patches
- Cost optimization review
- Backup verification

## 🆘 Troubleshooting

### Common Issues

**Backend won't start**
```bash
# Check logs
docker-compose logs backend

# Verify database connection
docker-compose exec backend python -c "from models.database import engine; print(engine.execute('SELECT 1'))"
```

**Preview servers failing**
```bash
# Check port availability
netstat -tulpn | grep :80[0-9][0-9]

# Restart preview manager
docker-compose restart backend
```

**Database connection issues**
```bash
# Test RDS connection
docker-compose exec backend python -c "import psycopg2; psycopg2.connect('postgresql://user:pass@host:5432/db')"
```

## 📞 Support

For deployment support:
- Email: support@bizfly.ai
- Documentation: https://docs.bizfly.ai
- Status Page: https://status.bizfly.ai

---

## ✅ Ready for Production?

**Current Status**: 🟡 **READY WITH API KEYS**

- ✅ Codebase cleaned and organized
- ✅ Ray's Diner demo working
- ✅ Environment variables configured
- ✅ Docker Compose setup ready
- ✅ AWS architecture planned
- 🔧 **Need**: Real API keys for Google Maps, Claude
- 🔧 **Need**: AWS resources provisioned
- 🔧 **Need**: Domain and SSL setup

**Next Steps**:
1. Obtain API keys
2. Create AWS resources
3. Deploy to staging environment
4. Test end-to-end functionality
5. Deploy to production