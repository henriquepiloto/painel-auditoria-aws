from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Painel de Auditoria AWS em execução!"}

@app.get("/bucket")
def get_bucket_name():
    return {"bucket": os.getenv("S3_BUCKET", "Bucket não definido")}
