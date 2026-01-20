# 🚀 Projeto 1 - API REST com Flask + PostgreSQL

API RESTful para gestão de tarefas (CRUD completo) com Flask, PostgreSQL e Docker.

## 🛠️ Tecnologias

- **Python 3.12** - Linguagem principal
- **Flask** - Framework web
- **PostgreSQL 15** - Base de dados relacional
- **SQLAlchemy** - ORM
- **Docker + Docker Compose** - Containerização

## 📋 Funcionalidades

- ✅ CRUD completo de tarefas (Create, Read, Update, Delete)
- ✅ Persistência em PostgreSQL com volumes
- ✅ API RESTful com respostas JSON
- ✅ Tratamento de erros personalizado
- ✅ Health check endpoint
- ✅ Dockerizado (ambiente reproduzível)

## 📡 Endpoints

### Gerais
- `GET /` → Informação da API e endpoints disponíveis
- `GET /hello/<nome>` → Mensagem personalizada
- `GET /health` → Health check (verifica se a API está viva)
- `POST /echo` → Recebe e processa JSON

### CRUD Tarefas
- `GET /tarefas` → Listar todas as tarefas
- `POST /tarefas` → Criar nova tarefa
- `GET /tarefas/<id>` → Obter tarefa específica
- `PUT /tarefas/<id>` → Atualizar tarefa
- `DELETE /tarefas/<id>` → Apagar tarefa

**Erros:** Rotas inexistentes devolvem 404 em JSON.

## 🚀 Como Executar

### Opção 1: Docker Compose (Recomendado)

1. **Clonar repositório**
```bash
git clone https://github.com/RRegal-Git/projeto1_flask.git
cd projeto1_flask
Iniciar containers

bash
docker compose up --build
Aceder à API

API: http://localhost:5000

PostgreSQL: localhost:5432

Parar containers

bash
docker compose down  # Mantém dados
docker compose down -v  # Apaga dados da BD (cuidado!)
Opção 2: Ambiente Virtual (Desenvolvimento)
Entrar na pasta do projeto

bash
cd ~/projetos/projeto1_flask
Criar e ativar ambiente virtual

bash
python3 -m venv venv
source venv/bin/activate
Instalar dependências

bash
pip install -r requirements.txt
Correr a API

bash
python app.py
A API fica disponível em: http://127.0.0.1:5000

🧪 Testar com curl
Endpoints gerais
bash
curl -i http://localhost:5000/
curl -i http://localhost:5000/hello/Ricardo
curl -i http://localhost:5000/health
CRUD Tarefas
bash
# Criar tarefa
curl -X POST http://localhost:5000/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Aprender Docker", "concluida": false}'

# Listar tarefas
curl http://localhost:5000/tarefas

# Obter tarefa por ID
curl http://localhost:5000/tarefas/1

# Atualizar tarefa
curl -X PUT http://localhost:5000/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"concluida": true}'

# Apagar tarefa
curl -X DELETE http://localhost:5000/tarefas/1
🗄️ Modelo de Dados
Tabela: tarefas
Campo	Tipo	Descrição
id	Integer	Chave primária (auto-incremento)
titulo	String(200)	Título da tarefa (obrigatório)
concluida	Boolean	Estado da tarefa (default: false)
🏗️ Estrutura do Projeto
text
projeto1_flask/
├── app.py                 # Aplicação Flask principal
├── requirements.txt       # Dependências Python
├── Dockerfile            # Imagem Docker
├── docker-compose.yml    # Orquestração
├── .dockerignore         # Excluir do build
├── .gitignore            # Excluir do Git
└── README.md             # Documentação
🐛 Troubleshooting
Problema	Solução
"port already in use"	Parar outros serviços na porta 5000
"database does not exist"	Verificar POSTGRES_DB no docker-compose.yml
Mudanças não aplicadas	docker compose up --build
Dados desapareceram	Não usar down -v (apaga volumes)
🎯 Próximos Passos
 Autenticação JWT

 Paginação no GET /tarefas

 Testes automatizados (pytest)

 Deploy (Render/Railway)

👨‍💻 Autor
Ricardo Regal
GitHub: @RRegal-Git

📝 Notas
A pasta venv/ é local e não vai para o GitHub (recriada via requirements.txt)

Docker Compose cria volumes para persistir dados entre restarts

Usar localhost no Windows/Mac e 127.0.0.1 no Linux
