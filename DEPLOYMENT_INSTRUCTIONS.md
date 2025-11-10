# FlowbitAI Deployment Instructions - Vercel & Render

## 🚀 Quick Deployment Guide

This guide will walk you through deploying FlowbitAI to production using:
- **Vercel** for Frontend & Backend API
- **Render** for AI Service
- **Supabase** for PostgreSQL Database (Free)

---

## 📋 Prerequisites

- [x] GitHub account
- [x] Vercel account (free)
- [x] Render account (free)
- [x] Supabase account (free)
- [x] Groq API key

---

## 1️⃣ Setup Database (Supabase)

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project"
3. Sign in with GitHub
4. Click "New Project"
5. Fill in:
   - **Name**: `flowbit-ai`
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to your users
6. Click "Create new project"

### Step 2: Setup Database Schema

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste the entire content from `/database/seed.sql`
4. Click "Run" to execute the script
5. Verify tables created in **Table Editor**

### Step 3: Get Database URL

1. Go to **Settings** → **Database**
2. Scroll down to **Connection string**
3. Select **URI** tab
4. Copy the connection string (looks like: `postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres`)
5. Replace `[PASSWORD]` with your actual password
6. Save this URL - you'll need it for deployment

---

## 2️⃣ Deploy AI Service (Render)

### Step 1: Push Code to GitHub

```bash
# Navigate to project root
cd C:\Users\ASUS\Desktop\FlowbitAI

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial deployment setup"

# Create GitHub repository and push
# Replace 'yourusername' with your actual GitHub username
git remote add origin https://github.com/Mukul2956/flowbit-ai.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your repositories

### Step 3: Deploy AI Service

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository (`flowbit-ai`)
4. Configure the service:

   **Basic Settings:**
   - **Name**: `flowbit-ai-service`
   - **Environment**: `Python 3`
   - **Region**: Choose closest region
   - **Branch**: `main`
   - **Root Directory**: `services/vanna`

   **Build & Deploy:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

5. Click **"Advanced"** and add Environment Variables:

```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
PORT=8000
ENVIRONMENT=production
ALLOWED_ORIGINS=https://*.vercel.app,https://flowbit-ai.vercel.app
```

6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Copy your service URL (e.g., `https://flowbit-ai-service.onrender.com`)

### Step 4: Test AI Service

```bash
# Test the deployed service
curl -X POST https://your-service-name.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is our total spending this year?"}'
```

---

## 3️⃣ Deploy Frontend & Backend (Vercel)

### Step 1: Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub account
3. Authorize Vercel to access repositories

### Step 2: Deploy Frontend

1. In Vercel dashboard, click **"New Project"**
2. Import `flowbit-ai` repository
3. Configure project:

   **Framework Preset:** Next.js
   **Root Directory:** `apps/web`
   **Build Settings:**
   - Build Command: `npm run build`
   - Output Directory: `.next`
   - Install Command: `npm install`

4. Add Environment Variables:
```bash
NEXT_PUBLIC_API_URL=https://flowbit-ai.vercel.app
NEXT_PUBLIC_AI_SERVER_URL=https://your-render-service-name.onrender.com
```

5. Click **"Deploy"**
6. Wait for deployment (3-5 minutes)
7. Your frontend will be available at: `https://flowbit-ai.vercel.app`

### Step 3: Deploy Backend API

1. In Vercel dashboard, click **"New Project"** again
2. Import same `flowbit-ai` repository
3. Configure project:

   **Framework Preset:** Other
   **Root Directory:** `apps/api`
   **Build Settings:**
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. Add Environment Variables:
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
AI_SERVER_URL=https://your-render-service-name.onrender.com
PORT=3001
```

5. Click **"Deploy"**
6. Your API will be available at: `https://your-api-name.vercel.app`

---

## 4️⃣ Configure Domain & CORS

### Step 1: Update Frontend Environment

1. Go to your frontend Vercel project
2. Go to **Settings** → **Environment Variables**
3. Update `NEXT_PUBLIC_API_URL` to your backend Vercel URL:
```bash
NEXT_PUBLIC_API_URL=https://your-api-name.vercel.app
```
4. Redeploy the frontend

### Step 2: Update AI Service CORS

1. Go to Render dashboard
2. Open your AI service
3. Go to **Environment**
4. Update `ALLOWED_ORIGINS`:
```bash
ALLOWED_ORIGINS=https://flowbit-ai.vercel.app,https://your-api-name.vercel.app
```
5. Service will auto-redeploy

---

## 5️⃣ Final Testing

### Test Complete Workflow

1. **Visit your frontend**: `https://flowbit-ai.vercel.app`
2. **Test API health**: `https://your-api-name.vercel.app/api/health`
3. **Test AI service**: `https://your-ai-service.onrender.com/health`

### Test Chat Functionality

1. Go to your frontend dashboard
2. Navigate to "Chat with Data" section
3. Try these test queries:

```
• "What is our total spending this year?"
• "How many invoices are pending?"
• "Which vendor has the highest spending?"
• "Show me invoices over €2000"
```

---

## 🔧 Environment Variables Summary

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-api-name.vercel.app
NEXT_PUBLIC_AI_SERVER_URL=https://your-ai-service.onrender.com
```

### Backend API (.env)
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
AI_SERVER_URL=https://your-ai-service.onrender.com
```

### AI Service (.env)
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.xxx.supabase.co:5432/postgres
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
PORT=8000
ENVIRONMENT=production
ALLOWED_ORIGINS=https://flowbit-ai.vercel.app,https://your-api-name.vercel.app
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

**1. CORS Errors**
```bash
# Check AI service ALLOWED_ORIGINS includes your Vercel domains
# Verify all URLs are HTTPS in production
```

**2. Database Connection Errors**
```bash
# Verify DATABASE_URL format is correct
# Check Supabase database is running
# Test connection from Supabase SQL Editor
```

**3. Build Failures**
```bash
# Check Node.js version in build logs
# Verify all dependencies in package.json
# Check for syntax errors in code
```

**4. AI Service Not Responding**
```bash
# Check Render service logs
# Verify GROQ_API_KEY is valid
# Test service health endpoint
```

### Getting Logs

**Vercel Logs:**
- Go to project dashboard → Functions tab
- View real-time logs for debugging

**Render Logs:**
```bash
# In Render dashboard, go to your service → Logs tab
# View real-time deployment and runtime logs
```

---

## 📝 Deployment Checklist

- [ ] Supabase database created and seeded
- [ ] Render AI service deployed and working
- [ ] Vercel frontend deployed
- [ ] Vercel backend API deployed
- [ ] All environment variables configured
- [ ] CORS settings updated
- [ ] Frontend can communicate with backend
- [ ] Backend can communicate with AI service
- [ ] AI service can query database
- [ ] Chat functionality tested end-to-end

---

## 🎉 Success URLs

After successful deployment, you should have:

- **Frontend**: `https://flowbit-ai.vercel.app`
- **Backend API**: `https://your-api-name.vercel.app/api`
- **AI Service**: `https://your-ai-service.onrender.com`
- **Database**: Supabase PostgreSQL instance

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review deployment logs in respective platforms
3. Verify all environment variables are correct
4. Test each service independently
5. Ensure all URLs use HTTPS

---

**Your FlowbitAI application is now live and ready for production use!** 🚀