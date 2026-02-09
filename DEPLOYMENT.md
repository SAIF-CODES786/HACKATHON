# Resume Screening System - Deployment Guide

## 🚀 Deployment Options

### Option 1: Docker Deployment (Recommended)

**Prerequisites:**
- Docker Desktop installed
- Docker Compose installed

**Steps:**

1. **Clone/Navigate to project**
```bash
cd HACKATHON
```

2. **Set environment variables**
```bash
# Create .env file
cat > .env << EOF
SECRET_KEY=$(openssl rand -hex 32)
DATABASE_URL=postgresql://resume_user:resume_password@postgres:5432/resume_screening
REDIS_URL=redis://redis:6379
ALLOWED_ORIGINS=http://localhost:3000
EOF
```

3. **Build and run containers**
```bash
docker-compose up --build
```

4. **Access application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

5. **Initialize database**
```bash
docker-compose exec backend python -c "from app.database import init_db; init_db()"
```

### Option 2: Heroku Deployment

**Backend (FastAPI):**

1. **Create Heroku app**
```bash
heroku create resume-screening-api
```

2. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

3. **Set environment variables**
```bash
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set ALLOWED_ORIGINS=https://your-frontend-url.com
```

4. **Deploy**
```bash
git subtree push --prefix backend heroku main
```

**Frontend (React):**

1. **Build for production**
```bash
cd frontend
npm run build
```

2. **Deploy to Vercel/Netlify**
```bash
# Vercel
vercel --prod

# Or Netlify
netlify deploy --prod --dir=dist
```

### Option 3: AWS Deployment

**Backend (EC2 + RDS):**

1. **Launch EC2 instance** (Ubuntu 22.04)
2. **Set up RDS PostgreSQL** database
3. **SSH into EC2**

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone repository
git clone <your-repo>
cd HACKATHON/backend

# Install Python packages
pip3 install -r requirements.txt -r requirements-enhanced.txt

# Set up systemd service
sudo nano /etc/systemd/system/resume-api.service
```

**Service file:**
```ini
[Unit]
Description=Resume Screening API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/HACKATHON/backend
Environment="DATABASE_URL=postgresql://user:pass@rds-endpoint/db"
ExecStart=/usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Frontend (S3 + CloudFront):**

1. **Build frontend**
```bash
npm run build
```

2. **Upload to S3**
```bash
aws s3 sync dist/ s3://your-bucket-name
```

3. **Configure CloudFront** for CDN

### Option 4: DigitalOcean App Platform

1. **Connect GitHub repository**
2. **Configure build settings:**
   - Backend: `backend/`
   - Build command: `pip install -r requirements.txt`
   - Run command: `uvicorn main:app --host 0.0.0.0`
   
3. **Add PostgreSQL database**
4. **Deploy**

## 🔧 Production Configuration

### Environment Variables

**Backend (.env):**
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>
ALLOWED_ORIGINS=https://yourdomain.com

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=noreply@yourdomain.com
SENDER_PASSWORD=<app-password>

# Redis (optional)
REDIS_URL=redis://localhost:6379

# App
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

**Frontend (.env):**
```env
VITE_API_URL=https://api.yourdomain.com
```

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Use HTTPS in production
- [ ] Enable CORS for specific domains only
- [ ] Set up rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable database SSL
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Enable logging and monitoring
- [ ] Set up backup strategy

### Performance Optimization

1. **Database:**
   - Add indexes on frequently queried fields
   - Use connection pooling
   - Enable query caching

2. **Backend:**
   - Enable Gzip compression
   - Use async operations
   - Implement Redis caching
   - Set up CDN for static files

3. **Frontend:**
   - Code splitting
   - Lazy loading
   - Image optimization
   - Browser caching

### Monitoring & Logging

**Sentry Integration:**
```python
# backend/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

**Application Logs:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

## 📊 Scaling Strategies

### Horizontal Scaling
- Use load balancer (Nginx, AWS ALB)
- Deploy multiple backend instances
- Shared PostgreSQL database
- Redis for session management

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Add database read replicas

### Caching Strategy
```python
# Example Redis caching
import redis

cache = redis.Redis(host='localhost', port=6379)

def get_candidates(job_id):
    cached = cache.get(f"candidates:{job_id}")
    if cached:
        return json.loads(cached)
    
    # Fetch from database
    candidates = db.query(Candidate).filter_by(job_id=job_id).all()
    cache.setex(f"candidates:{job_id}", 3600, json.dumps(candidates))
    return candidates
```

## 🔄 CI/CD Pipeline

**GitHub Actions (.github/workflows/deploy.yml):**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to production
        run: |
          # Your deployment commands
          ssh user@server 'cd /app && git pull && docker-compose up -d'
```

## 📱 Mobile App (Future)

Consider React Native for mobile version:
- Reuse API endpoints
- Share business logic
- Native camera for resume scanning

## 🌍 Multi-region Deployment

For global users:
- Deploy in multiple regions (US, EU, Asia)
- Use GeoDNS routing
- Replicate databases across regions
- CDN for static assets

---

**Need Help?** Check the troubleshooting guide or open an issue on GitHub.
