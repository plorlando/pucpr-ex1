import pytest
from src.main import *
from datetime import datetime


@pytest.mark.asyncio
async def test_create_curso():
    curso_teste = Curso(nome="Python Avançado", codigo="PY101", creditos=4)
    result = await create_curso(curso_teste)
    assert result.nome == "Python Avançado"
    assert result.codigo == "PY101"
    assert result.creditos == 4
    assert result.ativo == True
    assert result.id is not None


@pytest.mark.asyncio
async def test_get_curso_existente():
    curso = Curso(nome="Java Básico", codigo="JV100", creditos=3)
    created = await create_curso(curso)

    result = await get_curso(created.id)
    assert result.nome == "Java Básico"
    assert result.codigo == "JV100"


@pytest.mark.asyncio
async def test_get_curso_inexistente():
    result = await get_curso(9999)
    assert result == {"error": "Curso não encontrado"}


@pytest.mark.asyncio
async def test_list_cursos():
    result = await list_cursos()
    assert "cursos" in result
    assert "total" in result
    assert isinstance(result["total"], int)


@pytest.mark.asyncio
async def test_create_matricula():
    matricula_teste = Matricula(estudante_id=1, curso_id=1)
    result = await create_matricula(matricula_teste)
    assert result.estudante_id == 1
    assert result.curso_id == 1
    assert result.status == "ativa"
    assert result.id is not None


@pytest.mark.asyncio
async def test_create_matricula_duplicada():
    # Primeira matrícula
    matricula1 = Matricula(estudante_id=2, curso_id=2)
    await create_matricula(matricula1)

    matricula2 = Matricula(estudante_id=2, curso_id=2)
    result = await create_matricula(matricula2)
    assert result == {"error": "Estudante já matriculado neste curso"}


@pytest.mark.asyncio
async def test_get_matriculas_estudante():
    result = await get_matriculas_estudante(1)
    assert "matriculas" in result
    assert "total" in result


@pytest.mark.asyncio
async def test_get_matriculas_curso():
    result = await get_matriculas_curso(1)
    assert "matriculas" in result
    assert "total" in result


@pytest.mark.asyncio
async def test_update_status_matricula_valido():
    matricula = Matricula(estudante_id=3, curso_id=3)
    created = await create_matricula(matricula)

    result = await update_status_matricula(created.id, "cancelada")
    assert result.status == "cancelada"


@pytest.mark.asyncio
async def test_update_status_matricula_invalido():
    matricula = Matricula(estudante_id=4, curso_id=4)
    created = await create_matricula(matricula)

    result = await update_status_matricula(created.id, "status_inexistente")
    assert "error" in result


@pytest.mark.asyncio
async def test_update_nota_matricula_valida():
    matricula = Matricula(estudante_id=5, curso_id=5)
    created = await create_matricula(matricula)

    result = await update_nota_matricula(created.id, 8.5)
    assert result.nota_final == 8.5
    assert result.status == "concluida"  # Nota >= 6.0


@pytest.mark.asyncio
async def test_update_nota_matricula_invalida():
    matricula = Matricula(estudante_id=6, curso_id=6)
    created = await create_matricula(matricula)

    result = await update_nota_matricula(created.id, 11.0)
    assert result == {"error": "Nota deve estar entre 0 e 10"}


@pytest.mark.asyncio
async def test_delete_matricula():
    matricula = Matricula(estudante_id=7, curso_id=7)
    created = await create_matricula(matricula)

    result = await delete_matricula(created.id)
    assert result == {"message": "Matrícula deletada com sucesso"}


@pytest.mark.asyncio
async def test_delete_curso():
    curso = Curso(nome="Teste Delete", codigo="TD001", creditos=2)
    created = await create_curso(curso)

    result = await delete_curso(created.id)
    assert result == {"message": "Curso deletado com sucesso"}
