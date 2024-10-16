from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import presenca_router, health_check_router, users_router
from app.exceptions import http_exception_handler, global_exception_handler
from app.logging import AppLogger
from app.database import get_db

logger = AppLogger().get_logger()

app = FastAPI(
    title="Ponto Eletrônico",
    description="Ponto Eletrônico",
    version="V0.10.0"
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(presenca_router, tags=["presenca"])
# app.include_router(auth_router, tags=["authentication"])
app.include_router(users_router, tags=["users_gen"])
app.include_router(health_check_router, tags=["health_check"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True  
    )
