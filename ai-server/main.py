import os
import logging
import traceback
from typing import Dict, List, Any
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg
from dotenv import load_dotenv

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Groq package not available. Install with: pip install groq")

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FlowbitAI - Vanna Analytics Server",
    description="Natural language to SQL conversion using Vanna AI and Groq LLM",
    version="1.0.0"
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

# Initialize Groq client
groq_client = None
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)

# Type definitions for request/response (no Pydantic needed)
def validate_chat_request(data: dict) -> dict:
    """Validate chat request data"""
    if not isinstance(data, dict):
        raise ValueError("Request must be a JSON object")
    if "question" not in data or not isinstance(data["question"], str):
        raise ValueError("Missing or invalid 'question' field")
    return {
        "question": data["question"].strip(),
        "context": data.get("context", {})
    }

def create_chat_response(question: str, sql: str = None, data: List[Dict] = None, 
                        chart_config: Dict = None, error: str = None, explanation: str = None) -> dict:
    """Create chat response dictionary"""
    return {
        "question": question,
        "sql": sql,
        "data": data,
        "chart_config": chart_config,
        "error": error,
        "explanation": explanation
    }

class DatabaseSchema:
    """Database schema information for context"""
    
    @staticmethod
    def get_schema_info() -> str:
        return """
        Database Schema for FlowbitAI Analytics:
        
        1. vendors table:
        - id: string (primary key)
        - name: string (vendor name)
        - email: string (optional)
        - category: string (vendor category like 'Technology', 'Marketing', etc.)
        - city: string, country: string
        
        2. customers table:
        - id: string (primary key) 
        - name: string (customer name)
        - email: string (optional)
        - city: string, country: string
        
        3. invoices table:
        - id: string (primary key)
        - "invoiceNumber": string (unique invoice number) 
        - "vendorId": string (foreign key to vendors)
        - "customerId": string (foreign key to customers, optional)
        - "issueDate": timestamp (when invoice was issued)
        - "dueDate": timestamp (when payment is due)
        - "paidDate": timestamp (when invoice was paid, null if unpaid)
        - subtotal: decimal (invoice subtotal)
        - "taxAmount": decimal (tax amount)
        - "totalAmount": decimal (total invoice amount)
        - currency: string (default EUR)
        - status: enum (PENDING, PAID, OVERDUE, CANCELLED, DRAFT)
        - category: string (invoice category)
        
        4. line_items table:
        - id: string (primary key)
        - "invoiceId": string (foreign key to invoices)
        - description: string (item description)
        - quantity: decimal
        - "unitPrice": decimal
        - "totalPrice": decimal
        - category: string
        
        5. payments table:
        - id: string (primary key)
        - "invoiceId": string (foreign key to invoices)
        - amount: decimal (payment amount)
        - method: enum (BANK_TRANSFER, CREDIT_CARD, PAYPAL, CASH, CHECK, OTHER)
        - "paidDate": timestamp
        
        IMPORTANT: Use double quotes around camelCase column names in SQL queries!
        Examples:
        - SELECT SUM("totalAmount") FROM invoices WHERE status = 'PAID'
        - SELECT v.name, SUM(i."totalAmount") FROM vendors v JOIN invoices i ON v.id = i."vendorId"
        
        Common queries:
        - Total spend: SUM(total_amount) FROM invoices WHERE status = 'PAID'
        - Top vendors: JOIN invoices with vendors, GROUP BY vendor, ORDER BY total spend
        - Overdue invoices: WHERE status = 'OVERDUE' OR (status = 'PENDING' AND due_date < CURRENT_DATE)
        - Monthly trends: GROUP BY EXTRACT(YEAR FROM issue_date), EXTRACT(MONTH FROM issue_date)
        """

def get_db_connection():
    """Create database connection using psycopg3"""
    try:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL not configured")
        
        # Convert from postgres:// to postgresql:// if needed
        db_url = DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")
        
        conn = psycopg.connect(db_url)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

def execute_sql_query(sql: str) -> List[Dict[str, Any]]:
    """Execute SQL query and return results"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Execute query
        if sql.strip().upper().startswith('SELECT'):
            cursor.execute(sql)
            results = cursor.fetchall()
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            # Convert to list of dictionaries
            return [dict(zip(columns, row)) for row in results]
        else:
            cursor.execute(sql)
            conn.commit()
            return [{"message": "Query executed successfully"}]
            
    except Exception as e:
        logger.error(f"SQL execution error: {e}")
        raise Exception(f"SQL execution failed: {str(e)}")
    finally:
        if conn:
            conn.close()

def generate_sql_with_groq(question: str) -> str:
    """Generate SQL using Groq LLM"""
    try:
        if not groq_client:
            raise Exception("Groq API not configured")
        
        schema_info = DatabaseSchema.get_schema_info()
        
        system_prompt = f"""
        You are an expert SQL analyst for a financial analytics database. 
        Generate ONLY valid PostgreSQL SQL queries based on the user's question.
        
        {schema_info}
        
        CRITICAL RULES:
        1. Return ONLY the SQL query, no explanations or markdown
        2. Use proper PostgreSQL syntax
        3. Always use table aliases for clarity
        4. ALWAYS use double quotes around camelCase column names
        5. For aggregations, include proper GROUP BY clauses
        6. Use LIMIT clauses for large result sets (default LIMIT 100)
        
        CORRECT COLUMN EXAMPLES:
        - "totalAmount" NOT total_amount
        - "vendorId" NOT vendor_id  
        - "issueDate" NOT issue_date
        
        CORRECT SQL EXAMPLES:
        - "total spend" → SELECT SUM("totalAmount") FROM invoices WHERE status = 'PAID'
        - "spending by category" → SELECT category, SUM("totalAmount") as total_spend FROM invoices WHERE status = 'PAID' GROUP BY category ORDER BY total_spend DESC
        - "top vendors" → SELECT v.name, SUM(i."totalAmount") as total_spend FROM vendors v JOIN invoices i ON v.id = i."vendorId" WHERE i.status = 'PAID' GROUP BY v.id, v.name ORDER BY total_spend DESC LIMIT 5
        """
        
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        sql = response.choices[0].message.content.strip()
        
        # Clean up the SQL (remove markdown if present)
        if sql.startswith("```sql"):
            sql = sql.replace("```sql", "").replace("```", "").strip()
        elif sql.startswith("```"):
            sql = sql.replace("```", "").strip()
        
        return sql
        
    except Exception as e:
        logger.error(f"Groq SQL generation error: {e}")
        raise Exception(f"Failed to generate SQL: {str(e)}")

def generate_chart_config(question: str, data: List[Dict]) -> Dict:
    """Generate chart configuration based on question and data"""
    if not data:
        return {}
    
    # Determine chart type based on question keywords and data structure
    question_lower = question.lower()
    columns = list(data[0].keys()) if data else []
    
    chart_config = {
        "type": "table",  # default
        "data": data,
        "title": question
    }
    
    # Detect chart types based on keywords and data structure
    if any(word in question_lower for word in ['trend', 'over time', 'monthly', 'yearly']):
        chart_config["type"] = "line"
    elif any(word in question_lower for word in ['top', 'best', 'highest', 'vendors', 'categories']):
        chart_config["type"] = "bar"
    elif any(word in question_lower for word in ['distribution', 'breakdown', 'percentage']):
        chart_config["type"] = "pie"
    
    # Set axes based on column names
    if len(columns) >= 2:
        chart_config["x_axis"] = columns[0]
        chart_config["y_axis"] = columns[1]
    
    return chart_config

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "FlowbitAI Vanna Analytics Server",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "groq_configured": groq_client is not None,
        "database_configured": DATABASE_URL is not None
    }

@app.post("/chat")
async def chat_with_data(request: dict) -> dict:
    """Process natural language questions and return SQL + data"""
    try:
        # Validate request
        validated_request = validate_chat_request(request)
        question = validated_request["question"]
        
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing question: {question}")
        
        # Generate SQL query
        sql = generate_sql_with_groq(question)
        logger.info(f"Generated SQL: {sql}")
        
        # Execute SQL query
        data = execute_sql_query(sql)
        logger.info(f"Query returned {len(data)} rows")
        
        # Generate chart configuration
        chart_config = generate_chart_config(question, data)
        
        # Generate explanation
        explanation = f"Generated SQL query based on your question about {question.lower()}. Found {len(data)} result(s)."
        
        return create_chat_response(
            question=question,
            sql=sql,
            data=data,
            chart_config=chart_config,
            explanation=explanation
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Chat processing error: {traceback.format_exc()}")
        return create_chat_response(
            question=request.get("question", "") if isinstance(request, dict) else "",
            error=str(e)
        )

@app.get("/schema")
async def get_schema():
    """Get database schema information"""
    return {
        "schema": DatabaseSchema.get_schema_info(),
        "tables": ["vendors", "customers", "invoices", "line_items", "payments", "documents", "analytics"]
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    health_status = {
        "service": "FlowbitAI Vanna Analytics Server",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "groq_api": groq_client is not None,
            "database": False
        }
    }
    
    # Test database connection
    try:
        conn = get_db_connection()
        conn.close()
        health_status["checks"]["database"] = True
    except Exception as e:
        health_status["checks"]["database"] = False
        health_status["errors"] = {"database": str(e)}
    
    return health_status

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting FlowbitAI Vanna Analytics Server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )