from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Permite acesso de qualquer origem — você pode ajustar para segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Painel de Auditoria AWS em execução!"}

@app.get("/bucket")
def get_bucket_name():
    bucket = os.getenv("S3_BUCKET")
    if not bucket:
        return {"error": "Variável S3_BUCKET não definida"}
    return {"bucket": bucket}
