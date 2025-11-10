# Vanna AI Setup Guide

This guide explains how to set up Vanna AI for the FlowbitAI Analytics Dashboard project.

## What is Vanna AI?

Vanna AI is a framework that allows you to chat with your SQL database using natural language. It generates SQL queries from natural language questions and can learn from your database schema and example queries.

## Why We Use Vanna AI

According to the project requirements, we must use:
- **Self-hosted Vanna AI (Python FastAPI/Flask server)**
- **Vanna AI must connect to PostgreSQL database**
- **Use Groq for SQL generation**

## Setup Instructions

### 1. Create Vanna AI Account

1. Go to [https://vanna.ai](https://vanna.ai)
2. Sign up for a free account
3. Verify your email address

### 2. Get API Credentials

1. Log into your Vanna AI account
2. Go to [https://vanna.ai/account/profile](https://vanna.ai/account/profile)
3. Copy your **API Key**
4. Create a new model or use existing model name

### 3. Configure Environment Variables

Update your `ai-server/.env` file:

```env
# Vanna AI Configuration
VANNA_API_KEY="your_actual_api_key_here"
VANNA_MODEL="your_model_name_here"
```

### 4. Model Training

Once you have valid credentials, Vanna AI will automatically train on:

- **Database Schema (DDL)**: Table structures, relationships, and constraints
- **Sample Questions**: Common business queries with their SQL equivalents

Example training data includes:
- "What is the total spend this year?"
- "Who are the top 5 vendors by spend?"
- "Show overdue invoices"

## Current Implementation

### Without Vanna Credentials
- Server starts successfully
- Shows warning messages about missing credentials
- Falls back to basic database connection
- Training is skipped to avoid authentication errors

### With Valid Vanna Credentials
- Full Vanna AI functionality
- Automatic training on database schema
- Natural language to SQL conversion
- Query explanation generation

## API Endpoints

### `/chat` - Natural Language Querying
```json
POST /chat
{
  "question": "What is the total spend this year?"
}
```

Response:
```json
{
  "question": "What is the total spend this year?",
  "sql": "SELECT SUM(total_amount) as total_spend FROM invoices WHERE status = 'PAID' AND issue_date >= DATE_TRUNC('year', CURRENT_DATE)",
  "data": [{"total_spend": 22178.50}],
  "explanation": "This query calculates the total spend for the current year...",
  "chart_config": {"type": "metric", "value": 22178.50}
}
```

### `/train` - Add Training Data
```json
POST /train
{
  "question": "Show monthly revenue",
  "sql": "SELECT EXTRACT(MONTH FROM issue_date) as month, SUM(total_amount) FROM invoices GROUP BY month"
}
```

### `/health` - System Status
```json
GET /health
```

Returns Vanna AI connection status, database connectivity, and system health.

## Troubleshooting

### "Error adding DDL: No email" 
- This means you need valid Vanna AI credentials
- Sign up at vanna.ai and get your API key
- Update the .env file with real credentials

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in .env file
- Verify the database name exists

### Vanna AI Training Errors
- Ensure you have a valid Vanna AI account
- Check API key is correct
- Verify model name exists in your Vanna dashboard

## Benefits of Vanna AI

1. **Learns from your data**: Improves over time with more training
2. **Natural language interface**: Users can ask questions in plain English
3. **SQL generation**: Automatically creates optimized SQL queries
4. **Explanations**: Provides human-readable explanations of what queries do
5. **Schema awareness**: Understands your database structure and relationships

## Production Deployment

For production deployment:
1. Use environment variables for all credentials
2. Set up proper logging and monitoring
3. Implement rate limiting for API endpoints
4. Use HTTPS for all external communications
5. Regular backup of training data

## Example Queries

Once properly configured, you can ask:

- "What's our total revenue this quarter?"
- "Show me the top 10 customers by spending"
- "Which invoices are overdue?"
- "What's the average invoice amount?"
- "Show spending trends by month"

Vanna AI will convert these to appropriate SQL queries and return results.