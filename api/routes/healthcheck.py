from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.logging import AppLogger
from app.database import get_db

logger = AppLogger().get_logger()
router = APIRouter()

@router.get("/healthcheck", tags=["health_check"])
async def health_check(db: AsyncSession = Depends(get_db)) -> dict:
    logger.info("Executando health check do banco de dados PostgreSQL")
    try:
        # Executa uma consulta simples para verificar a conexão
        await db.execute("SELECT 1")
    except SQLAlchemyError as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro ao conectar ao banco de dados.")
    
    return {"message": "Conexão com o banco de dados está funcionando corretamente."}