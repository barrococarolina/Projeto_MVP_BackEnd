from pydantic import BaseModel
from typing import List
from model.aluno import Aluno

class AlunoSchema(BaseModel):
    """ Define como um novo aluno a ser inserido deve ser representado.
    """
    nome: str = "Rafael Fonte"
    email: str = "rafa.fonte@gmail.com"
    faltas: int = 2
    turmaId: int = 1

    
class AlunoDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    mesage: str
    id: int = 1
    nome: str = "Rafael Fonte"


class AlunoBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por Id.
        A busca será feita com base apenas no Id do aluno.
    """
    id: int = 1


class ListagemAlunosSchema(BaseModel):
    """ Define como uma listagem de alunos será retornada.
    """
    aluno: List[AlunoSchema]


class AlunoViewSchema(BaseModel):
    """ Define como um aluno será retornado
    """
    id: int = 1
    nome: str = "Rafael Fonte"
    email: str = "rafa.fonte@gmail.com"
    faltas: int = 2
    turmaId: int = 1


def apresenta_aluno(aluno: Aluno):
    """ Retorna uma representação de somente um aluno seguindo o schema definido em AlunoViewSchema
    """
    return {
        "id": aluno.id,
        "nome": aluno.nome,
        "email": aluno.email,
        "faltas": aluno.faltas,
        "turmaId": aluno.turmaId
    }


def apresenta_lista_alunos(lista_alunos: List[Aluno]):
    """ Retorna uma representação da lista de alunos cadastrados seguindo, 
        para cada aluno, o schema definido em AlunoViewSchema.
    """
    result = []
    for aluno in lista_alunos:
        result.append({
            "id": aluno.id,
            "nome": aluno.nome,
            "email": aluno.email,
            "faltas": aluno.faltas,
            "turmaId": aluno.turmaId
        })
    return {"Lista de aluno": result}