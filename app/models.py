from pydantic import BaseModel
from typing import Optional

class Curso(BaseModel):
    codigo: str  # identificador único do curso
    titulo: str
    descricao: str
    carga_horaria: int

class CursoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    carga_horaria: Optional[int] = None
