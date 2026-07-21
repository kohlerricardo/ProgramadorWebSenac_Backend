from fastapi import FastAPI
from router import aluno

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)
app.include_router(aluno.routes)

