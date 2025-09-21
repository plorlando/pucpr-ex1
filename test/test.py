import pytest
from src.main import *
from unittest.mock import patch


@pytest.mark.asyncio
async def test_root():
    result = await root()
    assert result == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_create_estudante():
    estudante_teste = Estudante(nome="João", curso="Engenharia", ativo=True)
    result = await create_estudante(estudante_teste)
    assert result == estudante_teste


@pytest.mark.asyncio
async def test_update_estudante_negativo():
    result = await update_estudante(-1)
    assert not result


@pytest.mark.asyncio
async def test_update_estudante_positivo():
    result = await update_estudante(10)
    assert result


@pytest.mark.asyncio
async def test_delete_estudante_negativo():
    result = await delete_estudante(-1)
    assert not result


@pytest.mark.asyncio
async def test_delete_estudante_positivo():
    result = await delete_estudante(10)
    assert result
