from fastapi import FastAPI
from routes import aluno_routes

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)
app.include_router(aluno_routes.aluno_rotas)

