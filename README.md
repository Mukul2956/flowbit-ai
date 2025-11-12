
  # FlowbitAI - Production-Ready Analytics Platform

##  Overview

FlowbitAI is a full-stack web application featuring a "Chat with Data" interface powered by Groq LLM for natural language SQL query generation. The platform provides comprehensive invoice analytics with real-time dashboard visualization.

##  Project Structure

```
/FlowbitAI
├── apps/
│   ├── web/                 # Next.js Frontend (Vercel)
│   └── api/                 # Express.js Backend API (Vercel)
├── services/
│   └── vanna/               # AI Service with Groq LLM (Render/Railway)
├── data/
│   └── Analytics_Test_Data.json  # Test dataset
├── database/
│   └── seed.sql             # PostgreSQL setup script
├── docker-compose.yml       # Local development setup
└── docs/                    # Documentation
```

##  Quick Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL 15+
- Git

### Environment Variables

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=https://flowbit-ai.vercel.app
NEXT_PUBLIC_AI_SERVER_URL=https://your-vanna-ai-service.onrender.com
```

**Backend (.env)**
```bash
DATABASE_URL=postgresql://username:password@host:5432/flowbit_ai
AI_SERVER_URL=https://your-vanna-ai-service.onrender.com
PORT=3001
```

**AI Service (.env)**
```bash
DATABASE_URL=postgresql://username:password@host:5432/flowbit_ai
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
PORT=8000
ENVIRONMENT=production
ALLOWED_ORIGINS=https://flowbit-ai.vercel.app,https://*.vercel.app
```

### Local Development Setup

1. **Clone and Install**
```bash
git clone https://github.com/yourusername/flowbit-ai.git
cd flowbit-ai
```

2. **Database Setup**
```bash
# Using Docker Compose (Recommended)
docker-compose up postgres -d

# Or manual PostgreSQL setup
createdb flowbit_ai
psql flowbit_ai < database/seed.sql
```

3. **Frontend Setup**
```bash
cd apps/web
npm install
npm run dev
# Runs on http://localhost:3000
```

4. **Backend API Setup**
```bash
cd apps/api
npm install
npm run build
npm run dev
# Runs on http://localhost:3001
```

5. **AI Service Setup**
```bash
cd services/vanna
pip install -r requirements.txt
python main.py
# Runs on http://localhost:8000
```

##  Deployment

### Frontend & Backend (Vercel)

1. **Connect GitHub Repository**
   - Link your GitHub repo to Vercel
   - Deploy frontend from `apps/web` folder
   - Deploy backend from `apps/api` folder

2. **Environment Configuration**
   - Set production environment variables in Vercel dashboard
   - Configure domain settings for CORS

### AI Service (Render/Railway/Fly.io)

1. **Dockerfile Deployment**
```bash
# Using the provided Dockerfile in services/vanna/
docker build -t flowbit-ai-service .
docker run -p 8000:8000 flowbit-ai-service
```

2. **Environment Variables**
   - Set all required environment variables
   - Ensure DATABASE_URL points to production database
   - Configure ALLOWED_ORIGINS for your Vercel domain

### Production URLs

- **Frontend**: `https://flowbit-ai.vercel.app`
- **Backend API**: `https://flowbit-ai.vercel.app/api`
- **AI Service**: `https://your-service-name.onrender.com`

##  Database Schema

### Tables Structure

```sql
-- Categories
id (SERIAL PRIMARY KEY)
name (VARCHAR)
description (TEXT)

-- Vendors  
id (SERIAL PRIMARY KEY)
name (VARCHAR)
email (VARCHAR)
phone (VARCHAR)
address (TEXT)

-- Invoices
id (SERIAL PRIMARY KEY)
invoiceId (VARCHAR)
vendorId (INTEGER FK)
categoryId (INTEGER FK)  
totalAmount (DECIMAL)
issueDate (DATE)
dueDate (DATE)
paymentDate (DATE)
status (VARCHAR)
description (TEXT)
```

##  API Documentation

### Base URL
- **Development**: `http://localhost:3001/api`
- **Production**: `https://flowbit-ai.vercel.app/api`

### Endpoints

#### Analytics Routes

**GET /api/analytics/summary**
```json
{
  "total_amount": "€115,670.38",
  "paid_invoices": 39,
  "pending_invoices": 11,
  "total_invoices": 50
}
```

**GET /api/analytics/category-spend**
```json
[
  { "name": "General", "value": 111000.50 },
  { "name": "Document", "value": 4669.88 }
]
```

**GET /api/analytics/vendor-spend**
```json
[
  { "name": "TechCorp Solutions", "value": 15250.00 },
  { "name": "Global Services GmbH", "value": 12890.00 }
]
```

#### Chat Routes

**POST /api/chat**
```json
// Request
{
  "question": "What is our total spending this year?",
  "context": {}
}

// Response
{
  "query": "SELECT SUM(totalAmount) FROM invoices WHERE EXTRACT(YEAR FROM issueDate) = 2024",
  "result": [{ "sum": "115670.38" }],
  "explanation": "Total spending for 2024 is €115,670.38"
}
```

##  "Chat with Data" Workflow

1. **User Input**: Natural language question via chat interface
2. **Frontend Processing**: Validates input and sends to backend API
3. **API Proxy**: Routes request to Vanna AI service
4. **SQL Generation**: Groq LLM converts natural language to SQL
5. **Database Query**: Executes generated SQL on PostgreSQL
6. **Result Processing**: Formats data for visualization
7. **Frontend Display**: Updates charts and displays results

##  Testing Queries

### Financial Analytics
- "What is our total spending this year?"
- "How many invoices have been paid vs pending?"
- "What is the average invoice value for paid vs pending invoices?"

### Vendor Analytics  
- "Which vendors have the highest average invoice amounts?"
- "List vendors with more than 5 invoices in the last 6 months"
- "What is the total spend per vendor for the last quarter?"

### Business Intelligence
- "Compare spending between General and Document categories"
- "What is the month-over-month growth in invoice volume?"
- "Show me the median invoice amount by vendor category"

##  Security & Performance

### Security Features
- CORS configuration for Vercel domains
- Rate limiting and input validation
- Parameterized queries to prevent SQL injection

### Performance Optimizations
- Next.js optimized builds with code splitting
- Database connection pooling
- Response caching for analytics endpoints

---

##  Quick Links

- **GitHub Repo**: https://github.com/yourusername/flowbit-ai
- **Test Queries**: See TestQueries.txt for comprehensive testing examples
  
