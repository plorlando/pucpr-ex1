from src.main import *
from unittest.mock import patch


def test_root():
    assert root() == {"message": "Hello World"}


def test_funcaoteste():
    with patch('random.randint', return_value=12345):
        result = funcaoteste()

    assert result ==  {"teste": True, "num_aleatorio": 12345}


def test_create_estudante ():
    estudante_teste = Estudante(nome="João", curso="Engenharia", ativo=True)
    assert estudante_teste == create_estudante()


def teste_update_estudante_negativo():
    assert not update_estudante(-1)


def teste_update_estudante_positivo():
    assert update_estudante(10)


def delete_estudante_negativo():
    assert not delete_estudante(-1)


def delete_estudante_positivo():
    assert delete_estudante(10)

