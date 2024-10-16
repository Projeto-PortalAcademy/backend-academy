from fastapi import FastAPI, HTTPException, Request
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from fastapi.responses import JSONResponse
import logging as logger

logger.basicConfig(level=logger.ERROR)
logger = logger.getLogger(__name__)

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"Erro http: {exc.detail} - URL: {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "type": "HTTPException"}
    )
    
    
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error inesperado: {exc} - URL: {request.url}")
    return JSONResponse(
        
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "ocorreu um erro interno", "type": "Exception"}
    )
