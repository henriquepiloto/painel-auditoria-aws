
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Account(BaseModel):
    client: str
    account_id: str
    role: str

accounts_db = []

@app.post("/accounts/")
def add_account(account: Account):
    accounts_db.append(account)
    return {"message": "Conta adicionada com sucesso."}

@app.get("/accounts/")
def list_accounts():
    return accounts_db
