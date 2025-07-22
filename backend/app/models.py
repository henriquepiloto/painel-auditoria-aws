from pydantic import BaseModel

# Classe para representar um usuário
class User(BaseModel):
    username: str
    password: str
    role: str

# Banco de dados falso
fake_users_db = {
    "piloto": {
        "username": "piloto",
        "password": "Select09*@!",
        "role": "admin"
    }
}
