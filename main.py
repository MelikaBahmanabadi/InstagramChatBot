from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pydantic import BaseModel, Field, validator
import uvicorn
from datetime import datetime

from services.rag_service import RAGService
from services.llm_service import LLMService
from database.db_manager import DatabaseManager
from utils.logger import logger
import config

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="Instagram DM Bot Simulator")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

allowed_origins = config.ALLOWED_ORIGINS if config.ALLOWED_ORIGINS else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

db_manager = DatabaseManager()
rag_service = RAGService(db_manager)
llm_service = LLMService()

request_count = 0
start_time = datetime.now()


class DMRequest(BaseModel):
    sender_id: str = Field(..., min_length=1, max_length=100)
    message_id: str = Field(..., min_length=1, max_length=100)
    text: str = Field(..., min_length=1, max_length=500)

    @validator('sender_id', 'message_id', 'text')
    def validate_input(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty or whitespace')
        return v.strip()


class DMResponse(BaseModel):
    reply: str


@app.post("/simulate_dm", response_model=DMResponse)
@limiter.limit(config.RATE_LIMIT)
async def simulate_dm(request: Request, dm_request: DMRequest):
    global request_count
    request_count += 1
    
    logger.info(f"Processing DM from {dm_request.sender_id}: {dm_request.text[:50]}...")
    
    try:
        retrieved_products = rag_service.retrieve_relevant_products(dm_request.text)
        logger.info(f"Retrieved {len(retrieved_products)} products for query")
        
        llm_response = await llm_service.generate_response(
            user_message=dm_request.text,
            context_products=retrieved_products
        )
        
        logger.info(f"Successfully generated response for {dm_request.sender_id}")
        return DMResponse(reply=llm_response)
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="خطا در پردازش درخواست")


@app.get("/health")
async def health_check():
    try:
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM products")
        product_count = cursor.fetchone()['count']
        conn.close()
        
        uptime = (datetime.now() - start_time).total_seconds()
        
        return {
            "status": "healthy",
            "database": "connected",
            "products_count": product_count,
            "uptime_seconds": uptime,
            "requests_processed": request_count
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.get("/metrics")
async def get_metrics():
    uptime = (datetime.now() - start_time).total_seconds()
    
    return {
        "uptime_seconds": uptime,
        "total_requests": request_count,
        "requests_per_minute": (request_count / uptime * 60) if uptime > 0 else 0,
        "start_time": start_time.isoformat()
    }


if __name__ == "__main__":
    db_manager.initialize_database()
    uvicorn.run(app, host="0.0.0.0", port=8000)

