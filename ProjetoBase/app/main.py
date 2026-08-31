from fastapi import FastAPI
from routes.CategoriaEquipamentoRoutes import categoria_equipamento_router
from routes.EquipamentoRoutes import equipamento_router
app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)
#inclusão de rotas para categorias de equipamentos
app.include_router(categoria_equipamento_router)
#inclusão de rotas para equipamentos
app.include_router(equipamento_router)