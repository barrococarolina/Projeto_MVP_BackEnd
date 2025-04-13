from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship
from model.base import Base

class Turma (Base):
    __tablename__ = 'turma'

    id = Column("pk_turma", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    ativo = Column(Boolean)

    # Definição de relacionamento entre turma e aluno.
    alunos = relationship("Aluno", back_populates="turma", cascade="all, delete-orphan")
    
    def __init__(self, nome: str, ativo: bool):
        """
        Cria uma turma com os argumentos:
        nome: nome da turma
        ativo: se a turma está ativa
        """
        self.nome = nome
        self.ativo = ativo