from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model.session import Session
from model.aluno import Aluno
from model.turma import Turma
from logger import logger
from flask_cors import CORS

from schemas.aluno import AlunoBuscaIdSchema, AlunoDeleteSchema, AlunoSchema, AlunoViewSchema, ListagemAlunosSchema, apresenta_aluno, apresenta_lista_alunos
from schemas.error import ErrorSchema
from schemas.turma import ListagemTurmaSchema, TurmaBuscaIdSchema, TurmaDeleteSchema, TurmaSchema, TurmaViewSchema, apresenta_lista_turmas, apresenta_turma

# Configuração da aplicação
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app, supports_credentials=True)

# Definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Aluno", description="Adição, visualização e remoção de alunos à base de dados")
turma_tag = Tag(name="Turma", description="Adição,visualização e remoção de turmas à base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/aluno', tags=[aluno_tag],
          responses={"200": AlunoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_aluno(form: AlunoSchema):
    """Adiciona um novo Aluno à base de dados.

    Só permite o cadastro se a turma informada existir.

    Retorna uma representação dos alunos e turmas associados.
    """
    logger.debug(f"Tentando adicionar aluno com nome: '{form.nome}' e turmaId: {form.turmaId}")

    try:
        # Criando conexão com a base
        session = Session()

        # Verifica se a turma existe primeiro
        turma = session.query(Turma).filter(Turma.id == form.turmaId).first()
        if not turma:
            error_msg = f"Turma com id {form.turmaId} não encontrada. Por favor, adicione uma turma com id {form.turmaId}"
            logger.warning(error_msg)
            return {"message": error_msg}, 400

        # Criando o aluno somente com a validação da turma
        aluno = Aluno(
            nome=form.nome,
            email=form.email,
            faltas=form.faltas,
            turmaId=form.turmaId)
        session.add(aluno)
        session.commit()

        logger.debug(f"Adicionando aluno de nome: '{aluno.nome}'")
        return apresenta_aluno(aluno), 200
    
    except IntegrityError:
        error_msg = "Aluno de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar aluno '{form.nome}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        error_msg = f"Não foi possível salvar novo aluno :/ - {str(e)}"
        logger.error(f"Erro inesperado: {error_msg}")
        return {"message": error_msg}, 400


@app.get('/aluno', tags=[aluno_tag],
         responses={"200": ListagemAlunosSchema, "404": ErrorSchema})
def get_aluno():
    """Faz a busca por todos os alunos cadastrados

    Retorna uma representação da listagem de alunos.
    """
    logger.debug(f"Coletando alunos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    aluno = session.query(Aluno).all()

    if not aluno:
        # se não há aluno cadastrados
        return {"alunos": []}, 200
    else:
        logger.debug(f"%d alunos econtrados" % len(aluno))
        # retorna a representação de aluno
        print(aluno)
        return apresenta_lista_alunos(aluno), 200


@app.get('/alunoId', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema})
def get_alunoId(query: AlunoBuscaIdSchema):
    """Faz a busca por um Aluno a partir do id do aluno.

    Retorna uma representação do aluno selecionado.
    """
    aluno_id = query.id
    logger.debug(f"Coletando dados sobre aluno #{aluno_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    aluno = session.query(Aluno).filter(Aluno.id == aluno_id).first()

    if not aluno:
        # se o aluno não foi encontrado
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(f"Erro ao buscar aluno '{aluno_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Aluno econtrado: '{aluno.id}'")
        # retorna a representação de aluno
        return apresenta_aluno(aluno), 200


@app.delete('/aluno', tags=[aluno_tag],
            responses={"200": AlunoDeleteSchema, "404": ErrorSchema})
def del_aluno(query: AlunoBuscaIdSchema):
    """Deleta um aluno a partir do id de aluno informado

    Retorna uma mensagem de confirmação da remoção.
    """
    aluno_id = query.id
    print(aluno_id)
    logger.debug(f"Deletando dados sobre aluno #{aluno_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    aluno = session.query(Aluno).filter(Aluno.id == aluno_id).first()
    nome_aluno = aluno.nome

    if aluno:
        # deleta o aluno e retorna a representação da mensagem de confirmação
        session.delete(aluno)
        session.commit()
        logger.debug(f"Deletado aluno #{aluno_id} ({nome_aluno})")
        return {"mesage": f"Aluno '{nome_aluno}' removido", "id": aluno_id}
    else:
        # se o aluno não foi encontrado
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(f"Erro ao deletar aluno #'{aluno_id}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/turma', tags=[turma_tag],
          responses={"200": TurmaViewSchema, "400": ErrorSchema})
def add_turma(form: TurmaSchema):
    """Adiciona uma nova turma à base de dados

    Retorna uma representação das turmas.
    """
    try:
        turma  = Turma(
            nome=form.nome,
            ativo=form.ativo)

        logger.debug(f"Adicionando turma #{turma}")
        # criando conexão com a base
        session = Session()
        session.add(turma)
        session.commit()

        logger.debug(f"Turma adicionada: '{turma.nome}'")

        return apresenta_turma(turma), 200
    
    except IntegrityError:
        error_msg = "Turma de mesmo nome já salva na base :/"
        logger.warning(f"Erro ao adicionar turma '{form.nome}': {error_msg}")
        return {"message": error_msg}, 409


    except Exception as e:
        logger.error(f"Erro ao adicionar turma: {str(e)}")
        return {"message": "Não foi possível salvar nova turma."}, 400

@app.get('/turma', tags=[turma_tag],
         responses={"200": ListagemTurmaSchema, "404": ErrorSchema})
def get_turma():
    """Faz a busca por todas as turmas cadastradas

    Retorna uma representação da listagem de turmas.
    """
    logger.debug(f"Coletando turmas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    turma = session.query(Turma).all()

    if not turma:
        # se não há turma cadastradas
        return {"turmas": []}, 200
    else:
        logger.debug(f"%d turmas econtradas" % len(turma))
        # retorna a representação de turma
        print(turma)
        return apresenta_lista_turmas(turma), 200

@app.delete('/turma', tags=[turma_tag],
            responses={"200": TurmaDeleteSchema, "404": ErrorSchema})
def del_turma(query: TurmaBuscaIdSchema):
    """Deleta uma turma a partir do id de turma informado

    Só permite a deleção se não houver alunos cadastrados na turma.

    Retorna uma mensagem de confirmação da remoção se tudo correr certo.
    """
    turma_id = query.id
    print(turma_id)
    logger.debug(f"Tentando deletar a turma com id: {turma_id}")
    # criando conexão com a base
    session = Session()

    turma = session.query(Turma).filter(Turma.id == turma_id).first()

    if not turma:
        error_msg = f"Turma com id {turma_id} não encontrada."
        logger.warning(error_msg)
        return {"message": error_msg}, 404

    # Verifica se existem alunos associados a essa turma
    alunos_vinculados = session.query(Aluno).filter(Aluno.turmaId == turma_id).count()

    if alunos_vinculados > 0:
        error_msg = f"Não é possível deletar a turma. Existem {alunos_vinculados} aluno(s) vinculados."
        logger.warning(error_msg)
        return {"message": error_msg}, 400
    
    # Deleta a turma
    session.delete(turma)
    session.commit()
    logger.debug(f"Turma com id {turma_id} deletada com sucesso.")
    return {"message": "Turma deletada com sucesso.", "id": turma_id}, 200

