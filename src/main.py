from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI(title="My FastAPI Project", version="1.0.0")

class Estudante(BaseModel):
    nome: str
    curso: str
    ativo: bool

class Curso(BaseModel):
    id: Optional[int] = None
    nome: str
    codigo: str
    creditos: int
    ativo: bool = True

class Matricula(BaseModel):
    id: Optional[int] = None
    estudante_id: int
    curso_id: int
    data_matricula: datetime = datetime.now()
    status: str = "ativa"  # ativa, cancelada, concluida
    nota_final: Optional[float] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/estudantes/cadastro")
async def create_estudante (estudante: Estudante):
    return estudante

@app.put("/estudantes/update/{id_estudante}")
async def update_estudante(id_estudante: int):
    return id_estudante > 0

@app.delete("/estudantes/delete/{id_estudante}")
async def delete_estudante(id_estudante: int):
    return id_estudante > 0


# Simulação de banco de dados em memória
cursos_db = []
matriculas_db = []
curso_id_counter = 1
matricula_id_counter = 1


# Endpoints para Cursos
@app.post("/cursos/cadastro")
async def create_curso(curso: Curso):
    global curso_id_counter
    curso.id = curso_id_counter
    curso_id_counter += 1
    cursos_db.append(curso)
    return curso


@app.get("/cursos/{curso_id}")
async def get_curso(curso_id: int):
    for curso in cursos_db:
        if curso.id == curso_id:
            return curso
    return {"error": "Curso não encontrado"}


@app.get("/cursos")
async def list_cursos():
    return {"cursos": cursos_db, "total": len(cursos_db)}


@app.put("/cursos/{curso_id}")
async def update_curso(curso_id: int, curso_atualizado: Curso):
    for i, curso in enumerate(cursos_db):
        if curso.id == curso_id:
            curso_atualizado.id = curso_id
            cursos_db[i] = curso_atualizado
            return curso_atualizado
    return {"error": "Curso não encontrado"}


@app.delete("/cursos/{curso_id}")
async def delete_curso(curso_id: int):
    for i, curso in enumerate(cursos_db):
        if curso.id == curso_id:
            cursos_db.pop(i)
            return {"message": "Curso deletado com sucesso"}
    return {"error": "Curso não encontrado"}


# Endpoints para Matrículas
@app.post("/matriculas/cadastro")
async def create_matricula(matricula: Matricula):
    global matricula_id_counter

    # Verificar se já existe matrícula ativa para este estudante neste curso
    for mat in matriculas_db:
        if (mat.estudante_id == matricula.estudante_id and
                mat.curso_id == matricula.curso_id and
                mat.status == "ativa"):
            return {"error": "Estudante já matriculado neste curso"}

    matricula.id = matricula_id_counter
    matricula_id_counter += 1
    matriculas_db.append(matricula)
    return matricula


@app.get("/matriculas/{matricula_id}")
async def get_matricula(matricula_id: int):
    for matricula in matriculas_db:
        if matricula.id == matricula_id:
            return matricula
    return {"error": "Matrícula não encontrada"}


@app.get("/matriculas/estudante/{estudante_id}")
async def get_matriculas_estudante(estudante_id: int):
    matriculas_estudante = [m for m in matriculas_db if m.estudante_id == estudante_id]
    return {"matriculas": matriculas_estudante, "total": len(matriculas_estudante)}


@app.get("/matriculas/curso/{curso_id}")
async def get_matriculas_curso(curso_id: int):
    matriculas_curso = [m for m in matriculas_db if m.curso_id == curso_id]
    return {"matriculas": matriculas_curso, "total": len(matriculas_curso)}


@app.put("/matriculas/{matricula_id}/status")
async def update_status_matricula(matricula_id: int, status: str):
    valid_status = ["ativa", "cancelada", "concluida"]
    if status not in valid_status:
        return {"error": f"Status inválido. Use: {valid_status}"}

    for matricula in matriculas_db:
        if matricula.id == matricula_id:
            matricula.status = status
            return matricula
    return {"error": "Matrícula não encontrada"}


@app.put("/matriculas/{matricula_id}/nota")
async def update_nota_matricula(matricula_id: int, nota: float):
    if nota < 0 or nota > 10:
        return {"error": "Nota deve estar entre 0 e 10"}

    for matricula in matriculas_db:
        if matricula.id == matricula_id:
            matricula.nota_final = nota
            if nota >= 6.0:
                matricula.status = "concluida"
            return matricula
    return {"error": "Matrícula não encontrada"}


@app.delete("/matriculas/{matricula_id}")
async def delete_matricula(matricula_id: int):
    for i, matricula in enumerate(matriculas_db):
        if matricula.id == matricula_id:
            matriculas_db.pop(i)
            return {"message": "Matrícula deletada com sucesso"}
    return {"error": "Matrícula não encontrada"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
