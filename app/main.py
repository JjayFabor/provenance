from fastapi import FastAPI
from app.config import settings
from app.database import check_connection
from app.routers import auth

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    db_status = check_connection()
    return {
        "status": "ok", 
        "app": settings.app_name,
        "database": "Connected" if db_status else "Disconnected"    
    }

