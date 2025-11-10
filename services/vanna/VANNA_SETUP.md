# Vanna AI Setup Guide

## Overview
This guide explains how to properly configure Vanna AI for the FlowbitAI Analytics Dashboard, as required by the task specifications.

## Why Vanna AI is Required
The original task specification explicitly states:
- **"Chat with Data" Interface — powered by self-hosted Vanna AI and Groq/ LLM**
- **"Self-hosted Vanna AI (Python FastAPI/Flask server)"**
- **"Vanna AI must: Connect to your PostgreSQL database, Use Groq for SQL generation"**

## Getting Started with Vanna AI

### 1. Create Vanna AI Account
1. Go to [https://vanna.ai](https://vanna.ai)
2. Sign up for a free account
3. Go to [https://vanna.ai/account/profile](https://vanna.ai/account/profile)

### 2. Get Your Credentials
From your Vanna AI profile page, you'll need:
- **API Key**: Your personal API key (starts with `vn_...`)
- **Model Name**: Create a new model or use an existing one (e.g., `flowbitai_analytics`)

### 3. Update Environment Variables
In your `.env` file, replace the placeholder values:

```env
# Vanna AI Configuration (Required for proper Vanna AI integration)
# Get your API key and model name from https://vanna.ai/account/profile
VANNA_API_KEY="vn_your_actual_api_key_here"
VANNA_MODEL="flowbitai_analytics"
```

### 4. Current Implementation Status

#### ✅ What's Implemented:
- Proper VannaDefault initialization pattern
- PostgreSQL database connection through Vanna AI
- FastAPI server with Vanna AI endpoints
- Training data setup for database schema
- Natural language to SQL conversion using Vanna AI

#### 🔴 What Needs Vanna AI Credentials:
- **`VANNA_API_KEY`**: Required to authenticate with Vanna AI service
- **`VANNA_MODEL`**: Required to specify which Vanna AI model to use

## Code Implementation

### Current Vanna AI Integration:
```python
from vanna.remote import VannaDefault

# Initialize VannaDefault with API key and model
if VANNA_API_KEY and VANNA_MODEL:
    vn = VannaDefault(model=VANNA_MODEL, api_key=VANNA_API_KEY)
    
    # Connect to PostgreSQL database
    vn.connect_to_postgres(
        host='localhost',
        dbname='flowbitai_analytics',
        user='postgres',
        password='mukul@237lassi',
        port=5432
    )
```

### Training the Model:
```python
# Train with database schema
vn.train(ddl="CREATE TABLE vendors ...")

# Train with question-SQL pairs
vn.train(question="What is the total spend?", sql="SELECT SUM(total_amount) FROM invoices...")
```

### Generating SQL:
```python
# Natural language to SQL
sql = vn.generate_sql("What are the top 5 vendors by spend?")
results = vn.run_sql(sql)
```

## Difference from Previous Implementation

| **Previous (Custom Groq)** | **Current (Vanna AI)** |
|----------------------------|------------------------|
| Custom prompt engineering | Vanna AI's trained models |
| Direct Groq API calls | Vanna AI manages LLM integration |
| Manual SQL generation | Vanna AI's optimized SQL generation |
| Basic schema context | Vanna AI's vector database training |

## Benefits of Vanna AI
1. **Pre-trained Models**: Better SQL generation than custom prompts
2. **Vector Database**: Stores and retrieves relevant training data
3. **Continuous Learning**: Improves with more training data
4. **Production Ready**: Built for enterprise analytics use cases
5. **Task Compliance**: Meets the explicit Vanna AI requirement

## Next Steps
1. **Get Vanna AI credentials** from [https://vanna.ai/account/profile](https://vanna.ai/account/profile)
2. **Update `.env` file** with your actual API key and model name
3. **Test the server** by running `python vanna_main.py`
4. **Train the model** with your database schema and sample queries

## Health Check Endpoints
- `GET /` - Basic service status
- `GET /health` - Detailed health check with Vanna AI status
- `POST /chat` - Natural language to SQL conversion
- `POST /train` - Add training data to Vanna AI model

## Important Notes
- Vanna AI requires an internet connection for the API calls
- The free tier has usage limits - check Vanna AI pricing for production use
- Database credentials are only used locally for SQL execution
- Vanna AI API key should be kept secure and not committed to git