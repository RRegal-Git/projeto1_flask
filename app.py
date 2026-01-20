
# ============================================================================
# PROJETO 1: API REST COM FLASK + POSTGRESQL
# ============================================================================
# Descrição: API para gestão de tarefas (CRUD completo)
# Autor: Ricardo Regal
# Data: Janeiro 2026
# ============================================================================


# ----------------------------------------------------------------------------
# 1. IMPORTAÇÕES
# ----------------------------------------------------------------------------
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os


# ----------------------------------------------------------------------------
# 2. INICIALIZAÇÃO DA APLICAÇÃO
# ----------------------------------------------------------------------------
app = Flask(__name__)
app.json.ensure_ascii = False  # Permite caracteres UTF-8 em respostas JSON


# ----------------------------------------------------------------------------
# 3. CONFIGURAÇÃO DA BASE DE DADOS
# ----------------------------------------------------------------------------
# Usa variável de ambiente DATABASE_URL (Docker) ou SQLite local como fallback
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'sqlite:///tarefas.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa warnings

db = SQLAlchemy(app)


# ----------------------------------------------------------------------------
# 4. MODELO DE DADOS
# ----------------------------------------------------------------------------
class Tarefa(db.Model):
    """Modelo da tabela 'tarefas' na base de dados"""
    __tablename__ = 'tarefas'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """Converte o objeto para dicionário JSON"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'concluida': self.concluida
        }


# ----------------------------------------------------------------------------
# 5. ROTAS GERAIS
# ----------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def home():
    """Página inicial: informação sobre a API"""
    return jsonify({
        "api": "projeto1_flask",
        "version": "1.0",
        "endpoints": {
            "geral": ["/", "/health", "/hello/<nome>", "/echo"],
            "tarefas": ["/tarefas", "/tarefas/<id>"]
        },
        "author": "Ricardo Regal"
    })


@app.route('/hello/<nome>', methods=['GET'])
def hello_person(nome):
    """Rota dinâmica: mensagem personalizada"""
    return jsonify({
        "message": f"Olá {nome}! 🌟",
        "status": "Personalizado"
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check: verifica se a API está operacional"""
    return jsonify({
        "status": "ok",
        "service": "projeto1_flask"
    }), 200


@app.route('/echo', methods=['POST'])
def echo():
    """Recebe dados JSON e devolve processados"""
    dados_recebidos = request.get_json()
    
    if not dados_recebidos:
        return jsonify({"erro": "Nenhum dado enviado"}), 400
    
    # Processa o campo 'nome' se existir
    nome_original = dados_recebidos.get('nome', 'Visitante')
    nome_gritado = nome_original.upper()
    
    return jsonify({
        "mensagem": "Recebi os teus dados!",
        "input_original": dados_recebidos,
        "resposta_backend": f"OLÁ {nome_gritado}!!",
        "status": "Processado"
    }), 201


# ----------------------------------------------------------------------------
# 6. ROTAS CRUD - TAREFAS
# ----------------------------------------------------------------------------

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    """GET: Lista todas as tarefas"""
    todas = Tarefa.query.all()
    return jsonify([t.to_dict() for t in todas]), 200


@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    """POST: Cria uma nova tarefa"""
    dados = request.get_json()
    
    if not dados or not dados.get('titulo'):
        return jsonify({"erro": "Campo 'titulo' obrigatório"}), 400
    
    nova = Tarefa(
        titulo=dados.get("titulo"),
        concluida=dados.get("concluida", False)
    )
    db.session.add(nova)
    db.session.commit()
    
    return jsonify(nova.to_dict()), 201


@app.route('/tarefas/<int:id>', methods=['GET'])
def obter_tarefa(id):
    """GET: Obtém uma tarefa específica por ID"""
    tarefa = Tarefa.query.get(id)
    
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    
    return jsonify(tarefa.to_dict()), 200


@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    """PUT: Atualiza uma tarefa existente"""
    tarefa = Tarefa.query.get(id)
    
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.concluida = dados.get('concluida', tarefa.concluida)
    
    db.session.commit()
    return jsonify(tarefa.to_dict()), 200


@app.route('/tarefas/<int:id>', methods=['DELETE'])
def apagar_tarefa(id):
    """DELETE: Remove uma tarefa"""
    tarefa = Tarefa.query.get(id)
    
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    
    db.session.delete(tarefa)
    db.session.commit()
    
    return jsonify({"mensagem": "Tarefa apagada com sucesso"}), 200


# ----------------------------------------------------------------------------
# 7. TRATAMENTO DE ERROS
# ----------------------------------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    """Resposta JSON para rotas inexistentes"""
    return jsonify({
        "error": "not found",
        "message": "Rota não existe"
    }), 404


# ----------------------------------------------------------------------------
# 8. INICIALIZAÇÃO DO SERVIDOR
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    # Criar tabelas antes de iniciar (apenas em modo desenvolvimento)
    with app.app_context():
        db.create_all()
        print("✅ Base de dados inicializada")
    
    # Iniciar servidor Flask
    app.run(
        debug=True,        # Reinicia automaticamente ao detetar alterações
        host='0.0.0.0',    # Acessível externamente (WSL/Docker)
        port=5000          # Porta padrão Flask
    )