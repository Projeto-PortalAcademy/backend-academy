from pydantic import BaseModel, Field
from pydantic.types import Annotated
from typing import Union, Optional
from datetime import date

class PresencaModel(BaseModel):
    usuario_id: int  # Mudança para manter consistência com o modelo SQLAlchemy
    data_para_presenca: Annotated[date, Field(description="Data da presença no formato AAAA-MM-DD")]  # Mudança para manter consistência
    presenca: Optional[bool] = None
    comentario: Annotated[str, Field(min_length=10, max_length=100, description="Comentário sobre a presença")]

    class Config:
        schema_extra = {
            "example": {
                "usuario_id": 123,
                "data_para_presenca": "2024-10-10",
                "presenca": True,
                "comentario": "Usuário presente na reunião"
            }
        }

class TokenModel(BaseModel):
    token: Annotated[str, Field(min_length=10, max_length=100, description="Token de autenticação")]  

    class Config:
        schema_extra = {
            "example": {
                "token": "abc123xyz987token"
            }
        }

class WordModel(BaseModel):
    word: Annotated[str, Field(min_length=10, max_length=100, description="Palavra a ser codificada")]

    class Config:
        schema_extra = {
            "example": {
                "word": "palavraexemplo"
            }
        }

class DatePresence(BaseModel):
    usuario_id: int  # Mudança para manter consistência com o modelo SQLAlchemy
    data_inicial: date
    data_final: date
