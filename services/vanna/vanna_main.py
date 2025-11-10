"""
FlowbitAI - Vanna AI Analytics Server
Production-grade FastAPI server using Vanna AI framework with Groq LLM integration
"""

import os
import logging
import traceback
from typing import Dict, List, Optional
from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Vanna AI import
from vanna.remote import VannaDefault

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="FlowbitAI - Vanna AI Analytics Server",
    description="Natural language to SQL conversion using Vanna AI framework with Groq LLM",
    version="2.0.0"
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

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
VANNA_API_KEY = os.getenv("VANNA_API_KEY")  # Vanna AI API key
VANNA_MODEL = os.getenv("VANNA_MODEL", "flowbitai_analytics")  # Vanna model name
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Keep for reference but Vanna handles LLM
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Initialize Vanna AI
vn = None
vanna_initialized = False
try:
    # Initialize VannaDefault with API key and optional model
    if VANNA_API_KEY:
        if VANNA_MODEL and VANNA_MODEL.strip():
            # Use specified model
            vn = VannaDefault(model=VANNA_MODEL, api_key=VANNA_API_KEY)
        else:
            # Use just API key, let Vanna create default model
            vn = VannaDefault(api_key=VANNA_API_KEY)
        
        # Connect to PostgreSQL database
        vn.connect_to_postgres(
            host='localhost',
            dbname='flowbitai_analytics',
            user='postgres',
            password='mukul@237lassi',
            port=5432
        )
        
        vanna_initialized = True
        logger.info("Vanna AI initialized successfully with VannaDefault")
    else:
        logger.warning("VANNA_API_KEY or VANNA_MODEL not provided. Get them from https://vanna.ai/account/profile")
        vanna_initialized = False
except Exception as e:
    logger.error(f"Failed to initialize Vanna AI: {e}")
    vanna_initialized = False

# Pydantic models
class ChatRequest(BaseModel):
    question: str
    context: Optional[Dict] = {}

class ChatResponse(BaseModel):
    question: str
    sql: Optional[str] = None
    data: Optional[List[Dict]] = None
    chart_config: Optional[Dict] = None
    error: Optional[str] = None
    explanation: Optional[str] = None

class TrainingData(BaseModel):
    question: Optional[str] = None
    sql: Optional[str] = None
    ddl: Optional[str] = None

def setup_vanna_training():
    """Train Vanna AI with database schema and sample queries"""
    if not vanna_initialized or not vn:
        logger.warning("Vanna AI not initialized, skipping training")
        return
    
    # Check if we have proper API credentials before attempting training
    if not VANNA_API_KEY or VANNA_API_KEY == "your_vanna_api_key_here":
        logger.warning("No valid Vanna API key provided. Training requires Vanna AI account. Get API key from https://vanna.ai/account/profile")
        return
    
    try:
        logger.info("Starting Vanna AI training with database schema...")
        
        # First, let's try to remove any conflicting old training data
        try:
            logger.info("Checking for existing training data...")
            existing_data = vn.get_training_data()
            if existing_data and len(existing_data) > 0:
                logger.info(f"Found {len(existing_data)} existing training items")
                # Remove old DDL statements that might have wrong column names
                for item in existing_data:
                    if 'content' in item and ('total_amount' in item.get('content', '') or 'issue_date' in item.get('content', '')):
                        try:
                            if 'id' in item:
                                vn.remove_training_data(item['id'])
                                logger.info("Removed old training data with incorrect column names")
                        except Exception as e:
                            logger.warning(f"Failed to remove old training item: {e}")
        except Exception as e:
            logger.warning(f"Could not check/clear existing training data: {e}")
        
        # Train with DDL (Data Definition Language) - database schema
        ddl_statements = [
            """
            CREATE TABLE vendors (
                id VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                email VARCHAR,
                phone VARCHAR,
                address VARCHAR,
                city VARCHAR,
                country VARCHAR,
                category VARCHAR,
                "taxId" VARCHAR,
                "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE customers (
                id VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL,
                email VARCHAR,
                phone VARCHAR,
                address VARCHAR,
                city VARCHAR,
                country VARCHAR,
                "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE invoices (
                id VARCHAR PRIMARY KEY,
                "invoiceNumber" VARCHAR UNIQUE NOT NULL,
                "vendorId" VARCHAR REFERENCES vendors(id),
                "customerId" VARCHAR REFERENCES customers(id),
                "issueDate" TIMESTAMP NOT NULL,
                "dueDate" TIMESTAMP,
                "paidDate" TIMESTAMP,
                subtotal DECIMAL(15,2) NOT NULL,
                "taxAmount" DECIMAL(15,2) NOT NULL DEFAULT 0,
                "totalAmount" DECIMAL(15,2) NOT NULL,
                currency VARCHAR DEFAULT 'EUR',
                status VARCHAR DEFAULT 'PENDING',
                description TEXT,
                category VARCHAR,
                "paymentTerms" VARCHAR,
                "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE line_items (
                id VARCHAR PRIMARY KEY,
                "invoiceId" VARCHAR REFERENCES invoices(id),
                description TEXT,
                quantity DECIMAL(10,2),
                "unitPrice" DECIMAL(15,2),
                "totalPrice" DECIMAL(15,2),
                category VARCHAR,
                "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            """
            CREATE TABLE payments (
                id VARCHAR PRIMARY KEY,
                "invoiceId" VARCHAR REFERENCES invoices(id),
                amount DECIMAL(15,2) NOT NULL,
                currency VARCHAR DEFAULT 'EUR',
                method VARCHAR DEFAULT 'BANK_TRANSFER',
                reference VARCHAR,
                "paidDate" TIMESTAMP NOT NULL,
                notes TEXT,
                "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        ]
        
        for ddl in ddl_statements:
            vn.train(ddl=ddl)
        
        # Train with sample question-SQL pairs using correct column names
        training_pairs = [
            {
                "question": "What is the total spend this year?",
                "sql": "SELECT SUM(\"totalAmount\") as total_spend FROM invoices WHERE status = 'PAID' AND \"issueDate\" >= DATE_TRUNC('year', CURRENT_DATE)"
            },
            {
                "question": "Who are the top 5 vendors by spend?",
                "sql": "SELECT v.name, SUM(i.\"totalAmount\") as total_spend FROM vendors v JOIN invoices i ON v.id = i.\"vendorId\" WHERE i.status = 'PAID' GROUP BY v.id, v.name ORDER BY total_spend DESC LIMIT 5"
            },
            {
                "question": "Show overdue invoices",
                "sql": "SELECT i.\"invoiceNumber\", v.name as vendor, i.\"totalAmount\", i.\"dueDate\" FROM invoices i JOIN vendors v ON i.\"vendorId\" = v.id WHERE i.status = 'PENDING' AND i.\"dueDate\" < CURRENT_DATE"
            },
            {
                "question": "What is the monthly invoice trend?",
                "sql": "SELECT EXTRACT(YEAR FROM \"issueDate\") as year, EXTRACT(MONTH FROM \"issueDate\") as month, COUNT(*) as invoice_count, SUM(\"totalAmount\") as total_spend FROM invoices WHERE status = 'PAID' GROUP BY year, month ORDER BY year DESC, month DESC LIMIT 12"
            },
            {
                "question": "Show spending by category",
                "sql": "SELECT category, SUM(\"totalAmount\") as total_spend FROM invoices WHERE status = 'PAID' GROUP BY category ORDER BY total_spend DESC"
            },
            {
                "question": "What is the total spend?",
                "sql": "SELECT SUM(\"totalAmount\") as total_spend FROM invoices WHERE status = 'PAID'"
            },
            {
                "question": "How many invoices do we have?",
                "sql": "SELECT COUNT(*) as total_invoices FROM invoices"
            },
            {
                "question": "What is the average invoice amount?",
                "sql": "SELECT AVG(\"totalAmount\") as average_amount FROM invoices WHERE status = 'PAID'"
            }
        ]
        
        for pair in training_pairs:
            vn.train(question=pair["question"], sql=pair["sql"])
        
        logger.info("Vanna AI training completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to train Vanna AI: {e}")

def generate_chart_config(question: str, data: List[Dict]) -> Dict:
    """Generate chart configuration based on question and data"""
    if not data:
        return {"type": "table", "data": data, "title": question}
    
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

@app.on_event("startup")
async def startup_event():
    """Initialize Vanna AI training on startup"""
    if vanna_initialized:
        setup_vanna_training()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "FlowbitAI - Vanna AI Analytics Server",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "vanna_configured": vanna_initialized,
        "vanna_api_key_set": VANNA_API_KEY is not None and VANNA_API_KEY != "your_vanna_api_key_here",
        "vanna_model": VANNA_MODEL,
        "groq_configured": GROQ_API_KEY is not None,
        "database_configured": DATABASE_URL is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_with_data(request: ChatRequest) -> ChatResponse:
    """Process natural language questions using Vanna AI"""
    try:
        if not vanna_initialized:
            raise HTTPException(status_code=500, detail="Vanna AI not initialized")
        
        question = request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        logger.info(f"Processing question with Vanna AI: {question}")
        
        # Use Vanna AI to generate SQL
        sql = vn.generate_sql(question)
        logger.info(f"Vanna AI generated SQL: {sql}")
        
        # Execute the SQL query using Vanna AI
        data = vn.run_sql(sql)
        
        # Convert pandas DataFrame to list of dictionaries if needed
        if hasattr(data, 'to_dict'):
            data = data.to_dict('records')
        elif not isinstance(data, list):
            data = []
        
        logger.info(f"Query returned {len(data)} rows")
        
        # Generate chart configuration
        chart_config = generate_chart_config(question, data)
        
        # Generate explanation using Vanna AI (if available)
        explanation = ""
        try:
            if hasattr(vn, 'generate_explanation'):
                explanation = vn.generate_explanation(question, sql)
            else:
                explanation = f"Generated SQL query to answer: {question}. Found {len(data)} result(s)."
        except Exception as e:
            logger.warning(f"Could not generate explanation: {e}")
            explanation = f"Query executed successfully. Found {len(data)} result(s)."
        
        return ChatResponse(
            question=question,
            sql=sql,
            data=data,
            chart_config=chart_config,
            explanation=explanation
        )
        
    except Exception as e:
        logger.error(f"Chat processing error: {traceback.format_exc()}")
        return ChatResponse(
            question=request.question,
            error=str(e)
        )

@app.post("/clear-training")
async def clear_training():
    """Clear all training data and retrain with fresh schema"""
    try:
        if not vanna_initialized or not vn:
            raise HTTPException(status_code=500, detail="Vanna AI not initialized")
        
        if not VANNA_API_KEY or VANNA_API_KEY == "your_vanna_api_key_here":
            raise HTTPException(status_code=400, detail="Valid Vanna API key required for training operations")
        
        logger.info("Clearing existing training data...")
        
        # Get current training data
        training_data = vn.get_training_data()
        
        # Remove old training data
        if training_data and len(training_data) > 0:
            for item in training_data:
                if 'id' in item:
                    try:
                        vn.remove_training_data(item['id'])
                    except Exception as e:
                        logger.warning(f"Failed to remove training data item {item.get('id')}: {e}")
        
        logger.info("Retraining with correct schema...")
        setup_vanna_training()
        
        return {
            "message": "Training data cleared and retrained successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Clear training error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear training: {str(e)}")

@app.post("/train")
async def train_vanna(training_data: TrainingData):
    """Train Vanna AI with new question-SQL pairs or DDL"""
    try:
        if not vanna_initialized:
            raise HTTPException(status_code=500, detail="Vanna AI not initialized")
        
        # Train with DDL if provided
        if training_data.ddl:
            vn.train(ddl=training_data.ddl)
            return {
                "message": "DDL training completed successfully",
                "ddl": training_data.ddl[:100] + "..." if len(training_data.ddl) > 100 else training_data.ddl
            }
        
        # Train with question-SQL pair if provided
        elif training_data.question and training_data.sql:
            vn.train(question=training_data.question, sql=training_data.sql)
            return {
                "message": "Training completed successfully",
                "question": training_data.question
            }
        else:
            raise HTTPException(status_code=400, detail="Either provide question+sql or ddl")
        
    except Exception as e:
        logger.error(f"Training error: {e}")
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@app.get("/training-data")
async def get_training_data():
    """Get current training data from Vanna AI"""
    try:
        if not vanna_initialized:
            raise HTTPException(status_code=500, detail="Vanna AI not initialized")
        
        training_data = vn.get_training_data()
        return {"training_data": training_data}
        
    except Exception as e:
        logger.error(f"Error retrieving training data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve training data: {str(e)}")

@app.get("/health")
async def health_check():
    """Detailed health check"""
    health_status = {
        "service": "FlowbitAI - Vanna AI Analytics Server",
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "vanna_ai": vanna_initialized,
            "vanna_api_key": VANNA_API_KEY is not None and VANNA_API_KEY != "your_vanna_api_key_here",
            "database": False
        }
    }
    
    # Test database connection through Vanna AI
    try:
        if vanna_initialized and vn:
            vn.run_sql("SELECT 1 as test")
            health_status["checks"]["database"] = True
    except Exception as e:
        health_status["checks"]["database"] = False
        health_status["errors"] = {"database": str(e)}
    
    return health_status

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting FlowbitAI Vanna AI Analytics Server on {host}:{port}")
    
    uvicorn.run(
        "vanna_main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )