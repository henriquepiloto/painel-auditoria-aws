from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models import User, fake_users_db
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "secretkeyjwt"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict or user_dict["password"] != form_data.password:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    access_token = jwt.encode({
        "sub": form_data.username,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": access_token, "token_type": "bearer"}