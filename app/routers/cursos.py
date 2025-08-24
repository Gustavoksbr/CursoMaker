from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Curso, CursoUpdate

router = APIRouter(prefix="/cursos", tags=["cursos"])

# Listar todos
@router.get("/", response_model=list[Curso])
async def listar_cursos():
    cursos = []
    cursor = db.cursos.find({})
    async for curso in cursor:
        cursos.append(Curso(
            codigo=curso["codigo"],
            titulo=curso["titulo"],
            descricao=curso["descricao"],
            carga_horaria=curso["carga_horaria"]
        ))
    return cursos


# Criar novo curso
@router.post("/", response_model=Curso)
async def criar_curso(curso: Curso):
    # Verifica se já existe curso com esse código
    existente = await db.cursos.find_one({"codigo": curso.codigo})
    if existente:
        raise HTTPException(status_code=400, detail="Curso com esse código já existe")
    
    await db.cursos.insert_one(curso.dict())
    return curso


# Buscar curso por código
@router.get("/{codigo}", response_model=Curso)
async def buscar_curso(codigo: str):
    curso = await db.cursos.find_one({"codigo": codigo})
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return Curso(
        codigo=curso["codigo"],
        titulo=curso["titulo"],
        descricao=curso["descricao"],
        carga_horaria=curso["carga_horaria"]
    )


# Atualizar curso por código
@router.put("/{codigo}", response_model=Curso)
async def atualizar_curso(codigo: str, dados: CursoUpdate):
    update_data = {k: v for k, v in dados.dict().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado enviado para atualização")

    result = await db.cursos.update_one(
        {"codigo": codigo},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso não encontrado")

    curso_atualizado = await db.cursos.find_one({"codigo": codigo})
    return Curso(
        codigo=curso_atualizado["codigo"],
        titulo=curso_atualizado["titulo"],
        descricao=curso_atualizado["descricao"],
        carga_horaria=curso_atualizado["carga_horaria"]
    )


# Deletar curso por código
@router.delete("/{codigo}")
async def deletar_curso(codigo: str):
    result = await db.cursos.delete_one({"codigo": codigo})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return {"detail": f"Curso {codigo} deletado com sucesso"}
