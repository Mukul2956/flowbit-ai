# Deployment Guide - FlowbitAI

## 🚀 Production Deployment

This guide covers deploying FlowbitAI to production environments using Vercel for frontend/backend and cloud hosting for the AI service.

## Prerequisites

- GitHub account and repository
- Vercel account
- Cloud hosting account (Render, Railway, Fly.io, or DigitalOcean)
- PostgreSQL database (hosted or local)
- Groq API key

---

## 1. Repository Setup

### GitHub Repository Structure
```
/FlowbitAI
├── apps/
│   ├── web/           # Deploy to Vercel
│   └── api/           # Deploy to Vercel  
├── services/
│   └── vanna/         # Deploy to cloud service
├── database/
│   └── seed.sql       # Database setup
└── docker-compose.yml # Local development
```

### Environment Files
Ensure you have the following environment files:

**apps/web/.env.local**
```bash
NEXT_PUBLIC_API_URL=https://your-app.vercel.app
NEXT_PUBLIC_AI_SERVER_URL=https://your-ai-service.onrender.com
```

**apps/api/.env**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/flowbit_ai
AI_SERVER_URL=https://your-ai-service.onrender.com
```

**services/vanna/.env**
```bash
DATABASE_URL=postgresql://user:pass@host:5432/flowbit_ai
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant
PORT=8000
ENVIRONMENT=production
```

---

## 2. Database Setup

### Option A: Cloud PostgreSQL (Recommended)

**Supabase (Free Tier)**
1. Create account at supabase.com
2. Create new project
3. Note connection string from Settings > Database
4. Run seed script via SQL Editor

**Railway PostgreSQL**
1. Create account at railway.app
2. Create new PostgreSQL service
3. Get connection details from service dashboard
4. Connect and run seed script

**Amazon RDS**
1. Create RDS PostgreSQL instance
2. Configure security groups
3. Connect and run seed script

### Option B: Local PostgreSQL with Docker

```bash
# Start PostgreSQL container
docker run --name flowbit-postgres \
  -e POSTGRES_DB=flowbit_ai \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=your_password \
  -p 5432:5432 \
  -d postgres:15

# Load seed data
docker exec -i flowbit-postgres psql -U postgres -d flowbit_ai < database/seed.sql
```

### Database URL Format
```bash
DATABASE_URL=postgresql://username:password@host:port/database_name

# Examples:
# Supabase: postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
# Railway: postgresql://postgres:xxx@containers-us-west-xxx.railway.app:6543/railway  
# Local: postgresql://postgres:password@localhost:5432/flowbit_ai
```

---

## 3. AI Service Deployment

### Option A: Render.com (Recommended)

1. **Create Render Account**
   - Sign up at render.com
   - Connect GitHub repository

2. **Create Web Service**
   - Choose "Web Service"
   - Connect repository
   - Set build command: `cd services/vanna && pip install -r requirements.txt`
   - Set start command: `python main.py`
   - Set environment variables

3. **Environment Variables**
   ```bash
   DATABASE_URL=your_postgresql_url
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=llama-3.1-8b-instant
   PORT=8000
   ENVIRONMENT=production
   ALLOWED_ORIGINS=https://your-app.vercel.app,https://*.vercel.app
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Note your service URL: `https://your-service-name.onrender.com`

### Option B: Railway.app

1. **Create Railway Account**
   - Sign up at railway.app
   - Connect GitHub repository

2. **Deploy Service**
   ```bash
   # Create new project
   railway login
   railway link your-project-id
   
   # Set environment variables
   railway variables:set DATABASE_URL=your_postgresql_url
   railway variables:set GROQ_API_KEY=your_groq_api_key
   
   # Deploy
   railway up --service services/vanna
   ```

### Option C: Fly.io

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Create fly.toml**
   ```toml
   app = "flowbit-ai-service"
   
   [build]
   dockerfile = "services/vanna/Dockerfile"
   
   [[services]]
   http_checks = []
   internal_port = 8000
   processes = ["app"]
   protocol = "tcp"
   script_checks = []
   
   [services.concurrency]
   hard_limit = 25
   soft_limit = 20
   type = "connections"
   
   [[services.ports]]
   force_https = true
   handlers = ["http"]
   port = 80
   
   [[services.ports]]
   handlers = ["tls", "http"]
   port = 443
   
   [env]
   PORT = "8000"
   ENVIRONMENT = "production"
   ```

3. **Deploy**
   ```bash
   fly auth login
   fly launch
   fly secrets set DATABASE_URL=your_postgresql_url
   fly secrets set GROQ_API_KEY=your_groq_api_key
   fly deploy
   ```

---

## 4. Vercel Deployment

### Frontend Deployment

1. **Connect Repository**
   - Go to vercel.com
   - Click "New Project"
   - Import GitHub repository
   - Set root directory to `apps/web`

2. **Build Configuration**
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": ".next",
     "installCommand": "npm install"
   }
   ```

3. **Environment Variables**
   ```bash
   NEXT_PUBLIC_API_URL=https://your-app.vercel.app
   NEXT_PUBLIC_AI_SERVER_URL=https://your-ai-service.onrender.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Note your frontend URL: `https://your-app.vercel.app`

### Backend API Deployment

1. **Create Second Vercel Project**
   - Click "New Project" again
   - Import same repository
   - Set root directory to `apps/api`

2. **Build Configuration**
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "dist",
     "installCommand": "npm install"
   }
   ```

3. **Environment Variables**
   ```bash
   DATABASE_URL=your_postgresql_url
   AI_SERVER_URL=https://your-ai-service.onrender.com
   ```

### Alternative: Monorepo Deployment

Deploy both frontend and backend in single Vercel project:

1. **Set Root Directory** to project root
2. **Configure vercel.json**
   ```json
   {
     "functions": {
       "apps/api/src/**/*.ts": {
         "maxDuration": 30
       }
     },
     "rewrites": [
       {
         "source": "/api/(.*)",
         "destination": "/apps/api/src/$1"
       },
       {
         "source": "/(.*)",
         "destination": "/apps/web/$1"
       }
     ]
   }
   ```

---

## 5. Domain Configuration

### Custom Domain Setup

1. **Add Domain in Vercel**
   - Go to project settings
   - Add custom domain
   - Configure DNS records

2. **Update Environment Variables**
   ```bash
   # Frontend
   NEXT_PUBLIC_API_URL=https://yourdomain.com
   
   # AI Service  
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

### SSL/HTTPS

- Vercel automatically provides SSL certificates
- Ensure all API calls use HTTPS in production
- Update CORS settings for your domain

---

## 6. Production Testing

### Health Checks

1. **Frontend**: `https://your-app.vercel.app`
2. **Backend API**: `https://your-app.vercel.app/api/health`
3. **AI Service**: `https://your-ai-service.onrender.com/health`

### Test Chat Functionality

```bash
# Test AI service directly
curl -X POST https://your-ai-service.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our total spending?"}'

# Test via backend API  
curl -X POST https://your-app.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How many invoices are pending?"}'
```

### Load Testing

```bash
# Install artillery for load testing
npm install -g artillery

# Create test script
cat > load-test.yml << EOF
config:
  target: https://your-app.vercel.app
  phases:
    - duration: 60
      arrivalRate: 10
scenarios:
  - name: "Chat queries"
    requests:
      - post:
          url: "/api/chat"
          json:
            question: "What is our total spending?"
EOF

# Run load test
artillery run load-test.yml
```

---

## 7. Monitoring & Maintenance

### Application Monitoring

**Vercel Analytics**
- Enable in project settings
- Monitor performance metrics
- Track error rates

**External Monitoring**
```bash
# Set up uptime monitoring
# Use services like:
# - UptimeRobot (free)
# - Pingdom
# - StatusCake
```

### Log Monitoring

**Vercel Functions Logs**
- View in Vercel dashboard
- Set up log drains for external analysis

**AI Service Logs**
```bash
# Render logs
render logs --service your-service-name --follow

# Railway logs
railway logs --follow

# Fly.io logs  
fly logs
```

### Database Monitoring

```sql
-- Monitor database performance
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE schemaname = 'public';

-- Check connection counts
SELECT count(*) FROM pg_stat_activity;

-- Monitor slow queries
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC LIMIT 5;
```

---

## 8. Security Checklist

### Environment Security
- [ ] All sensitive data in environment variables
- [ ] No hardcoded API keys or passwords
- [ ] Database credentials secured
- [ ] CORS properly configured

### API Security
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] SQL injection prevention
- [ ] HTTPS enforced

### Database Security
- [ ] Connection encryption enabled
- [ ] Firewall rules configured
- [ ] Regular backups scheduled
- [ ] User permissions restricted

---

## 9. Performance Optimization

### Frontend Optimization

```javascript
// next.config.js
module.exports = {
  compress: true,
  poweredByHeader: false,
  generateEtags: false,
  experimental: {
    optimizeCss: true,
  },
  images: {
    formats: ['image/webp'],
    deviceSizes: [640, 750, 828, 1080, 1200],
  }
}
```

### Database Optimization

```sql
-- Add indexes for performance
CREATE INDEX CONCURRENTLY idx_invoices_status_date 
ON invoices(status, "issueDate");

CREATE INDEX CONCURRENTLY idx_invoices_amount_desc 
ON invoices("totalAmount" DESC);

-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM invoices 
WHERE status = 'pending' 
AND "issueDate" > '2024-01-01';
```

### Caching Strategy

```javascript
// Add caching headers
app.use((req, res, next) => {
  if (req.path.includes('/api/analytics/')) {
    res.set('Cache-Control', 'public, max-age=300'); // 5 minutes
  }
  next();
});
```

---

## 10. Backup & Recovery

### Database Backups

```bash
# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_URL="your_database_url"

pg_dump $DB_URL > $BACKUP_DIR/flowbit_ai_$DATE.sql
gzip $BACKUP_DIR/flowbit_ai_$DATE.sql

# Keep only last 7 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

### Application Backups

- GitHub repository serves as code backup
- Environment variables backed up securely
- Database backups automated
- Monitor backup success/failure

---

## 11. Troubleshooting

### Common Deployment Issues

**CORS Errors**
```bash
# Check ALLOWED_ORIGINS in AI service
# Verify domain in environment variables
# Test with curl to isolate issue
```

**Database Connection Failures**
```bash
# Verify DATABASE_URL format
# Check network connectivity
# Validate credentials
# Test connection manually
```

**Build Failures**
```bash
# Check Node.js version compatibility
# Verify all dependencies in package.json
# Review build logs for specific errors
```

### Performance Issues

**High Response Times**
- Check database query performance
- Monitor AI service response times
- Review network latency

**Memory Usage**
- Monitor Vercel function memory usage
- Optimize database connection pooling
- Review AI service resource usage

---

## 🎯 Quick Deployment Checklist

- [ ] GitHub repository created and configured
- [ ] Database setup with seed data loaded
- [ ] AI service deployed and tested
- [ ] Frontend deployed to Vercel
- [ ] Backend API deployed to Vercel
- [ ] Environment variables configured
- [ ] CORS settings updated
- [ ] Custom domain configured (optional)
- [ ] Health checks passing
- [ ] Chat functionality tested
- [ ] Monitoring setup
- [ ] Backups configured

## 📞 Support

For deployment issues:

1. Check logs in respective platforms
2. Verify environment variables
3. Test each service independently
4. Review this documentation
5. Contact support if needed

---

**Deployment completed! Your FlowbitAI application should now be live and accessible to users.**