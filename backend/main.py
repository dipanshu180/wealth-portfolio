from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
import time
import re
from agents.mongo_agent import query_mongo
from agents.sql_agent import query_sql_database


app = FastAPI(title="Valuefy AI Portfolio Assistant", version="1.0.0")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str
    processing_time: Optional[str] = None
    visualization_data: Optional[dict] = None

@app.get("/")
async def root():
    return {"message": "Valuefy AI Portfolio Assistant API", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint to verify all components are working"""
    try:
        # Check if environment variables are set
        import os
        openai_key = os.getenv("OPENAI_API_KEY")
        mongodb_uri = os.getenv("MONGODB_URI")
        mysql_uri = os.getenv("MYSQL_URI")
        
        status = {
            "status": "healthy",
            "openai_configured": bool(openai_key),
            "mongodb_configured": bool(mongodb_uri),
            "mysql_configured": bool(mysql_uri),
            "timestamp": time.time()
        }
        
        return status
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": time.time()
        }

def determine_query_type(question: str) -> str:
    """Intelligently determine which agent to use based on the question content"""
    question_lower = question.lower()
    
    # Keywords that indicate MongoDB (client/portfolio) queries
    mongo_keywords = [
        'client', 'investor', 'portfolio', 'risk', 'manager', 'name', 'who',
        'high risk', 'low risk', 'medium risk', 'risk appetite',
        'investment preferences', 'stocks', 'real estate', 'bonds',
        'top 5', 'top 10', 'top 3', 'top 1', 'top 2', 'top 4', 'top 6', 'top 7', 'top 8', 'top 9',
        'wealth member', 'wealth members', 'relationship manager', 'rm',
        'top relationship', 'best relationship', 'top rm', 'best rm'
    ]
    
    # Keywords that indicate SQL (transaction) queries
    sql_keywords = [
        'transaction', 'amount', 'invested', 'stock', 'date', 'total',
        'sum', 'average', 'count', 'highest', 'lowest', 'between',
        'this month', 'last month', 'this year', 'last year',
        'amount invested', 'total investment', 'investment amount',
        'breakup', 'breakdown', 'group by', 'per relationship',
        'portfolio values', 'portfolio value', 'holders of', 'highest holders'
    ]
    
    # Count matches for each type
    mongo_score = sum(1 for keyword in mongo_keywords if keyword in question_lower)
    sql_score = sum(1 for keyword in sql_keywords if keyword in question_lower)
    
    # Special handling for specific query patterns
    if 'breakup' in question_lower or 'breakdown' in question_lower:
        if 'relationship manager' in question_lower or 'per relationship' in question_lower:
            return 'sql'  # Portfolio breakdown by RM should use SQL
    
    if 'holders of' in question_lower or 'highest holders' in question_lower:
        return 'sql'  # Stock holdings analysis should use SQL
    
    if 'portfolio values' in question_lower or 'portfolio value' in question_lower:
        if 'per' in question_lower or 'by' in question_lower:
            return 'sql'  # Portfolio values breakdown should use SQL
    
    # Special handling for "top N" queries
    top_match = re.search(r'top\s+(\d+)', question_lower)
    if top_match:
        # If it's about clients/investors/wealth members, use MongoDB
        if any(word in question_lower for word in ['client', 'investor', 'portfolio', 'name', 'who', 'wealth member']):
            return 'mongo'
        # If it's about transactions/amounts, use SQL
        elif any(word in question_lower for word in ['transaction', 'amount', 'invested', 'stock']):
            return 'sql'
        # Default to MongoDB for top queries about people
        else:
            return 'mongo'
    
    # If scores are equal, prefer MongoDB for people-related queries
    if mongo_score == sql_score:
        if any(word in question_lower for word in ['name', 'who', 'client', 'investor', 'wealth member']):
            return 'mongo'
        else:
            return 'sql'
    
    # Return the type with higher score
    return 'mongo' if mongo_score > sql_score else 'sql'

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    try:
        import time
        start_time = time.time()
        
        # Validate request
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Determine which agent to use based on intelligent routing
        query_type = determine_query_type(request.question)
        
        try:
            if query_type == 'mongo':
                # Use MongoDB agent for client/portfolio queries
                mongo_response = query_mongo(request.question)
                # Handle both string and dictionary responses from MongoDB agent
                if isinstance(mongo_response, dict):
                    response = mongo_response.get('answer', 'No response from MongoDB agent')
                else:
                    response = str(mongo_response)
            else:
                # Use SQL agent for transaction queries
                response = query_sql_database(request.question)
        except Exception as agent_error:
            # Log the actual error for debugging
            import logging
            logging.error(f"Agent error: {str(agent_error)}")
            import traceback
            logging.error(f"Agent traceback: {traceback.format_exc()}")
            # If agent fails, provide a fallback response
            response = f"Sorry, I encountered an error while processing your question: {str(agent_error)}. Please try rephrasing your question."
        
        processing_time = f"{(time.time() - start_time):.2f}s"
        
        # Add visualization data for certain queries
        visualization_data = None
        question_lower = request.question.lower()
        
        # Enhanced visualization detection
        if any(keyword in question_lower for keyword in ['top', 'portfolio', 'investor', 'manager', 'client', 'wealth member']):
            visualization_data = {
                "type": "portfolio_analysis",
                "query": request.question,
                "query_type": query_type
            }
        elif any(keyword in question_lower for keyword in ['transaction', 'amount', 'investment', 'trend', 'breakdown', 'breakup']):
            visualization_data = {
                "type": "transaction_analysis",
                "query": request.question,
                "query_type": query_type
            }
        elif any(keyword in question_lower for keyword in ['relationship manager', 'rm', 'holders']):
            visualization_data = {
                "type": "relationship_analysis",
                "query": request.question,
                "query_type": query_type
            }
        
        return QuestionResponse(
            answer=response,
            processing_time=processing_time,
            visualization_data=visualization_data
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the full error for debugging
        import logging
        logging.error(f"Unexpected error in ask_question: {str(e)}")
        import traceback
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
