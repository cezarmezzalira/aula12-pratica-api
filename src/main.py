import json
from typing import Optional, List
from uuid import uuid4
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}

# Métodos HTTP

# GET - Obter informações da API
# POST - Persistir ou gravar uma informação na API
# PUT - Serve para atualizar as informações completas de um registro
# PATCH - Serve para atualizar apenas o que foi mudado
# DELETE - Serve para excluir um registro

# CRUD - Create, Retrieve, Update e Delete

# Cadastro de usuários
# nome, email, cpf, data nascimento, telefone


class Usuario(BaseModel):
    id: Optional[str | None] = None
    nome: str
    email: str
    cpf: str
    data_nascimento: str
    telefone: str


class UsuarioPatch(BaseModel):
    id: Optional[str | None] = None
    nome: Optional[str | None] = None
    email: Optional[str | None] = None
    cpf: Optional[str | None] = None
    data_nascimento: Optional[str | None] = None
    telefone: Optional[str | None] = None


usuarios: List[Usuario] = []

# Criar um novo usuário


@app.post("/usuarios")
async def criar_usuario(request: Request):
    body = await request.body()
    print(type(body), body)
    # Converte para um dictionary
    body = json.loads(body)
    print(type(body), body)

    # Cria um identificador único para o usuário
    id = str(uuid4())

    # Crio o objeto com os dados do usuário
    usuario = Usuario(
        id=id,
        nome=body.get("nome"),
        cpf=body.get("cpf"),
        email=body.get("email"),
        data_nascimento=body.get("data_nascimento"),
        telefone=body.get("telefone"),
    )

    # Adicionar o usuário a lista de usuários
    usuarios.append(usuario)

    return {"message": "ok",
            "usuario": usuario}

# Obter todos os usuários


@app.get("/usuarios")
def obter_usuarios():
    return {"message": "ok",
            "usuarios": usuarios}


# Update completo
@app.put("/usuarios/{id}")
def atualizar_usuario_completo(id: str,
                               usuario: Usuario):
    # verificar se o usuario existe na lista
    usuario_existente = None
    for u in usuarios:
        if u.id == id:
            usuario_existente = u
            break

    # se ele existir, vamos atualizar ele completamente
    # Truthy -> valor = None, "", 0
    if (not usuario_existente):
        return JSONResponse(content={"status": "error",
                                     "message": "Usuário não encontrado",
                                     "usuario": {}},
                            status_code=404)

    index = usuarios.index(usuario_existente)
    usuarios[index].nome = usuario.nome
    usuarios[index].cpf = usuario.cpf
    usuarios[index].email = usuario.email
    usuarios[index].data_nascimento = usuario.data_nascimento
    usuarios[index].telefone = usuario.telefone

    return {"message": "ok",
            "id": id,
            "usuario": usuarios[index].model_dump()}


# Update parcial
@app.patch("/usuarios/{id}")
def atualizar_usuario_parcial(id: str,
                              usuario: UsuarioPatch):
    # verificar se o usuario existe na lista
    usuario_existente = None
    for u in usuarios:
        if u.id == id:
            usuario_existente = u
            break

    # se ele existir, vamos atualizar ele completamente
    # Truthy -> valor = None, "", 0
    if (not usuario_existente):
        return JSONResponse(content={"status": "error",
                                     "message": "Usuário não encontrado",
                                     "usuario": {}},
                            status_code=404)

    index = usuarios.index(usuario_existente)

    if (usuario.nome):
        usuarios[index].nome = usuario.nome

    if (usuario.cpf):
        usuarios[index].cpf = usuario.cpf

    if (usuario.email):
        usuarios[index].email = usuario.email

    if (usuario.data_nascimento):
        usuarios[index].data_nascimento = usuario.data_nascimento

    if (usuario.telefone):
        usuarios[index].telefone = usuario.telefone

    return {"message": "ok",
            "id": id,
            "usuario": usuarios[index].model_dump()}

# Delete


@app.delete("/usuarios/{id}")
def atualizar_usuario_parcial(id: str):
    # verificar se o usuario existe na lista
    usuario_existente = None
    for u in usuarios:
        if u.id == id:
            usuario_existente = u
            break

    # se ele existir, vamos atualizar ele completamente
    # Truthy -> valor = None, "", 0
    if (not usuario_existente):
        return JSONResponse(content={"status": "error",
                                     "message": "Usuário não encontrado",
                                     "usuario": {}},
                            status_code=404)

    usuarios.remove(usuario_existente)

    return {"message": "ok",
            "id": id,
            "usuario": {}}
