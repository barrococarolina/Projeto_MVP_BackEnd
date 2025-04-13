# MVP Full Stack - Back-End (API)
## 1. Introdução

Este projeto é parte do MVP - _Minimum Viable Product_ - da _Sprint_ **Desenvolvimento _Full Stack_ Básico** do Curso de Engenharia de Software da PUC-Rio. O MVP é composto de um Back-End, com banco de dados, e de um Front-End. Neste repositório encontra-se a parte do Back-end da aplicação. A parte do front-end pode ser acessada em [Projeto_MVP_FrontEnd](https://github.com/barrococarolina/Projeto_MVP_FrontEnd).

>O projeto desenvolvido objetiva o *Gerenciamento de uma Escola*.

>Este projeto visa, de forma bastante simplificada, implementar um banco de dados no qual seja possível criar turmas escolares para que os alunos possam ser matriculados nessas turmas. Além da criação, pode-se consultar as turmas existentes e deletá-las. Os alunos podem ser cadastrados no sistema sendo incluídos em turmas, deletados do sistema e também pode-se fazer uma consulta com todos os alunos cadastrados e uma consulta por seu id.
  
  
## 2. Back-end
O back-end da aplicação é responsável pela criação e manutenção do banco de dados da aplicação, bem como pelas rotas de requisição ao servidor. As rotas implementadas foram do tipo GET, POST e DELETE, e sua documentação pode ser acessada em Swagger, conforme instruções do item 4 do presente documento.

O back-end está organizado da seguinte forma:

- app.py *(onde estão definidas as rotas de requisição)*
- model:
    - __ init __.py *(encontra-se vazia pois seu conteúdo foi movido para a session.py)*
    - base.py *(responsável pela criação de uma super classe com modelo em SQLAlchemy)*
    - session.py *(responsável pela criação do banco de dados)*
    - aluno.py *(responsável por criar a classe aluno)*
    - turma.py *(responsável por criar a classe turma)*
- schemas:
    - __ init __.py *(responsável por importar os schemas criados nos arquivos error.py, aluno.py e turma.py)*
    - error.py *(define como uma mensagem de erro será representada)*
    - aluno.py *(define os schemas que serão utilizados nas rotas de requisição)*
    - turma.py *(define os schemas que serão utilizados nas rotas de requisição)*
- requirements.txt *(contém as bibliotecas a serem instaladas, conforme instruções do item 4 do presente documento)*


## 3. Pré-Requisitos
- Recomenda-se o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

- Faz-se necessária a instalação de todas as dependências/bibliotecas listadas no arquivo requirements.txt:
```
    (env)$ pip install -r requirements.txt
```
- Se receber o erro Failed to build greenlet, rodar:
pip install --only-binary :all: greenlet
pip install --only-binary :all: Flask-SQLAlchemy

## 4. Como executar
- Para processar a API e consultar sua documentação em Swagger, executar:
```
(env)$ flask run --host 0.0.0.0 --port 5000
```
- Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.


## 5. Considerações
Por se tratar de um MVP, diversas funcionalidades da API não foram priorizadas neste momento, ficando sua implementação para as versões futuras da aplicação. Dentre as já mapeadas, destaca-se a listada a seguir:

- Rota PUT para a edição de produtos exitentes no banco (alunos e/ou turmas).