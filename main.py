from enum import Enum
from fastapi import FastAPI

app = FastAPI()

db = [
    {"username": "Cesar",},
    {"username": "Bruno"},
    {"username": "Rodrigo"},
    {"username": "Tércio"},
]


class UserModel(str, Enum):
    profile = "profile"
    hello = "hello"
    content = "content"


@app.get("/")
async def hello_world():
    return {"msg": "Hello world"}


@app.get("/users/profile")
async def get_user_profile():
    return {
        "id": 1,
        "info": db[1],
    }


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    return {
        "id": user_id,
        "info": db[user_id],
    }


@app.get("/models/{model_name}")
async def get_model(model_name: UserModel):
    if model_name == UserModel.profile:
        return {
            "model_name": model_name,
            "msg": "Acesso ao perfil",
        }
    
    if model_name == UserModel.hello:
        return {
            "model_name": model_name,
            "msg": "Olá mundo",
        }
    
    return {
        "model_name": model_name,
        "msg": "Conteúdo",
    }


# Usando caminhos como parâmetro
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    return {"file_path": file_path}

# Parei em https://fastapi.tiangolo.com/tutorial/path-params/#path-convertor
