from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from model.base import Base

class Aluno(Base):
    __tablename__ = 'aluno'

    id = Column("pk_aluno", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    email = Column(String)
    faltas = Column(Integer)
    turmaId = Column(Integer, ForeignKey('turma.pk_turma'))

    turma = relationship("Turma", back_populates="alunos")  # Referência à turma

    def __init__(self, nome: str, email: str, faltas: int, turmaId: int):
        """
        Cria um Aluno com os seguintes argumentos:
            nome: nome do Aluno
            email: e-mail do Aluno adicionado
            faltas: faltas registradas de cada aluno
            turmaId: id da turma em que ele será cadastrado
        """
        self.nome = nome
        self.email = email
        self.faltas = faltas
        self.turmaId = turmaId
