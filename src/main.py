import random

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My FastAPI Project", version="1.0.0")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

class Service(BaseModel):
    name: str
    description: str = None
    cost: float
    duration: int  # duration in minutes

class Estudante(BaseModel):
    nome: str
    curso: str
    ativo: bool
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.post("/services/")
async def create_item(service: Service):
    return service

@app.get("/funcaoteste")
async def funcaoteste():
    return {"teste": True, "num_aleatorio": random.randint(0, 57000)}


@app.post("/estudantes/cadastro")
async def create_estudante (estudante: Estudante):
    return estudante

@app.put("/estudantes/update/{id_estudante}")
async def update_estudante(id_estudante: int):
    return id_estudante > 0

@app.delete("/estudantes/delete/{id_estudante}")
async def delete_estudante(id_estudante: int):
    return id_estudante > 0



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
