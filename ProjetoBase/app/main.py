from fastapi import FastAPI
from routes.CategoriaEquipamentoRoutes import categoria_equipamento_router
from routes.RolesRoutes import roles_router
from routes.UsuarioRoutes import usuario_router
from routes.UsuarioHasRoleRoutes import usuario_has_role_router
from routes.EmprestimoRoutes import emprestimo_router
from routes.EquipamentoRoutes import equipamento_router

app = FastAPI(
    title="Minha API",
    description="API de exemplo com FastAPI",
    version="1.0.0"
)
#inclusão de rotas para categorias de equipamentos
app.include_router(categoria_equipamento_router)
app.include_router(categoria_equipamento_router)
app.include_router(roles_router)
app.include_router(usuario_router)
app.include_router(usuario_has_role_router)
app.include_router(emprestimo_router)
app.include_router(equipamento_router)


#inclusão de rotas para equipamentos
app.include_router(equipamento_router)