from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.schemas import PresencaModel, DatePresence
from app.models import Presenca
from app.database import get_db
from app.logging import AppLogger
from datetime import date

logger = AppLogger().get_logger()


router = APIRouter()

@router.post("/presenca/comentario", response_model=PresencaModel, status_code=status.HTTP_201_CREATED)
async def adicionar_comentario(presenca: PresencaModel, db: AsyncSession = Depends(get_db)):
    logger.info(f"Adicionando comentário para o usuário {presenca.usuario_id} na data {presenca.data_para_presenca}")
    try:
        query = select(Presenca).where(Presenca.usuario_id == presenca.usuario_id, Presenca.data_para_presenca == presenca.data_para_presenca)
        result = await db.execute(query)
        usuario_existente = result.scalar_one_or_none()

        if not usuario_existente:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Usuário {presenca.usuario_id} não encontrado no banco")

        usuario_existente.comentario = presenca.comentario
        await db.commit()

    except SQLAlchemyError as e:
        logger.error(f"Erro ao processar a presença: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao processar a presença {str(e)}")

    return {"mensagem": "Comentário adicionado com sucesso", "dados": presenca.dict()}


@router.put("/presenca", response_model=PresencaModel, status_code=status.HTTP_200_OK)
async def modificar_presenca(presenca: PresencaModel, db: AsyncSession = Depends(get_db)):
    logger.info(f"Modificando a presença do usuário {presenca.usuario_id} na data {presenca.data_para_presenca}")

    try:
        query = select(Presenca).where(Presenca.usuario_id == presenca.usuario_id, Presenca.data_para_presenca == presenca.data_para_presenca)
        result = await db.execute(query)
        usuario_existente = result.scalar_one_or_none()

        if not usuario_existente:
            logger.error(f"Usuário {presenca.usuario_id} não foi encontrado")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        usuario_existente.presenca = presenca.presenca
        usuario_existente.comentario = presenca.comentario
        await db.commit()

    except SQLAlchemyError as e:
        logger.error(f"Erro ao modificar a presença: {str(e)}")
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao modificar a presença {str(e)}")

    return {"mensagem": "Presença modificada com sucesso", "dados": presenca.dict()}


@router.get("/presenca/data")
async def listar_presenca_por_data(data_para_presenca: date, db: AsyncSession = Depends(get_db)):
    logger.info(f"Listando presenças para a data {data_para_presenca}")

    try:
        query = select(Presenca).where(Presenca.data_para_presenca == data_para_presenca)
        result = await db.execute(query)
        presencas = result.scalars().all()

    except SQLAlchemyError as e:
        logger.error(f"Erro ao listar presenças: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar presenças {str(e)}")

    return {"presenças": [presenca for presenca in presencas]}


@router.get("/presenca/pessoa/")
async def listar_presenca_por_pessoa(presenca_pessoa: DatePresence, db: AsyncSession = Depends(get_db)):
    logger.info(f"Listando presenças do usuário {presenca_pessoa.usuario_id} entre {presenca_pessoa.data_inicial} e {presenca_pessoa.data_final}")

    try:
        query = select(Presenca).where(
            Presenca.usuario_id == presenca_pessoa.usuario_id,
            Presenca.data_para_presenca >= presenca_pessoa.data_inicial,
            Presenca.data_para_presenca <= presenca_pessoa.data_final
        )
        result = await db.execute(query)
        presencas = result.scalars().all()

    except SQLAlchemyError as e:
        logger.error(f"Erro ao listar presenças: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar presenças {str(e)}")

    return {"presenças": [presenca for presenca in presencas]}