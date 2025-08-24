from fastapi import FastAPI
from app.routers import cursos

app = FastAPI(title="API de Cursos com FastAPI + MongoDB")

# Inclui as rotas
app.include_router(cursos.router)
