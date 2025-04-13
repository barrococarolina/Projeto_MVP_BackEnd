from pydantic import BaseModel
from typing import List
from model.turma import Turma
from model.aluno import Aluno
from sqlalchemy.orm import Session

class TurmaSchema(BaseModel):
    """ Define como uma nova turma a ser inserida deve ser representado
    """
    nome: str = "Matemática"
    ativo: bool = True

    
class TurmaDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
        Só irá deletar a turma se ela existir e se não houver aluno cadastrado.
    """
    mesage: str
    id: int = 1


class TurmaBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por Id.
        A busca será feita com base apenas no Id da turma.
    """
    id: int = 1


class ListagemTurmaSchema(BaseModel):
    """ Define como uma listagem de turmas será retornada.
    """
    turma: List[TurmaSchema]


class TurmaViewSchema(BaseModel):
    """ Define como uma turma será retornada
    """
    id: int = 1
    nome: str = "Matemática"
    ativo: bool = True


def apresenta_turma(turma: Turma):
    """ Retorna uma representação da turma seguindo o schema definido em TurmaViewSchema
    """
    return {
        "id": turma.id,
        "nome": turma.nome,
        "ativo": turma.ativo
    }


def apresenta_lista_turmas(lista_turma: List[Turma]):
    """ Retorna uma representação da lista de turmas seguindo, 
        para cada turma, o schema definido em TurmaViewSchema.
    """
    result = []
    for turma in lista_turma:
        result.append({
            "id": turma.id,
            "nome": turma.nome,
            "ativo": turma.ativo,
        })
    return {"Lista de turma": result}