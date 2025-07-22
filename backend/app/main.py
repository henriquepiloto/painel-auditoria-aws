from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.auth import router as auth_router
from app.audit import router as audit_router
from app.assume_role import router as assume_role_router
import os

app = FastAPI(title="Painel de Auditoria AWS")

# Inclui as rotas da API
app.include_router(auth_router)
app.include_router(audit_router)
app.include_router(assume_role_router)

# Monta o frontend na raiz
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

# Redireciona a raiz ("/") para a página HTML
#@app.get("/")
#def root():
    #return FileResponse(os.path.join("frontend", "index.html"))
from fastapi import Depends
from app.auth import get_current_user

from fastapi.responses import RedirectResponse

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/frontend/index.html")


# Cria as tabelas no banco de dados (caso ainda não existam)
Base.metadata.create_all(bind=engine)
