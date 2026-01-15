# 1. IMPORTAR FLASK (biblioteca para criar APIs web)
from flask import Flask, jsonify, request  # Flask=framework, jsonify=converte dict→JSON

# 2. CRIAR A APLICAÇÃO (o "cérebro" da API)
app = Flask(__name__)  # __name__ = nome deste ficheiro (app.py)
app.json.ensure_ascii = False  # <--- Esta linha mágica permite UTF-8 no JSON

# --- A NOSSA BASE DE DADOS (Simples e em Memória) ---
tarefas = [] 
# ----------------------------------------------------

# 3. PRIMEIRA ROTA: http://localhost:5000/hello
@app.route('/hello', methods=['GET'])  # @ = decorador, GET = pedido "ler"
def hello():  # Função que executa quando alguém visita /hello
    # 4. RETORNAR JSON (formato universal para APIs)
    return jsonify({
        "message": "Olá do Backend Ricardo! 🌟",  # Mensagem principal
        "status": "API funcionando 100%",         # Estado da API
        "timestamp": "2026-01-09"                 # Data criação
    })

# 5. SEGUNDA ROTA: http://localhost:5000/ (página inicial)
@app.route('/', methods=['GET'])  # "/" = raiz da API
def home():
    return jsonify({
        "api": "projeto1_flask",           # Nome do projeto
        "endpoints": ["/hello"],           # Lista rotas disponíveis
        "author": "Ricardo Regal"          # Teu nome (CV!)
    })

# 6. Rota dinâmica: aceita qualquer nome
@app.route('/hello/<nome>', methods=['GET'])
def hello_person(nome):
    return jsonify({
        "message": f"Olá {nome}! 🌟",
        "status": "Personalizado",
        "timestamp": "2026-01-09"
    })

# 7. ROTA DE SAÚDE: http://localhost:5000/health
# Ideia: é o "teste rápido" para confirmar que a API está viva.
# Muito usado por Docker/servidores/monitorização para ver se está tudo ok.
@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",                 # A API está online
        "service": "projeto1_flask"     # Nome do serviço (ajuda em logs)
    }), 200  # 200 = "OK"

# 7.1. Rota inexistente : ERRO 404 EM JSON (rota não encontrada)
# Por defeito o Flask devolve uma página HTML quando falhas uma rota.
# Como isto é uma API, queremos responder em JSON (mais consistente para quem consome).
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "error": "not found",           # Tipo de erro
        "message": "Rota não existe"    # Explicação simples para humanos
    }), 404  # 404 = "não encontrado"

# 7.2. ROTA POST: RECEBER DADOS
# Aqui usamos o método POST. O 'request.get_json()' vai ler
# o que enviarmos no corpo do pedido.
@app.route('/echo', methods=['POST'])
def echo():
    dados_recebidos = request.get_json()
    
    if not dados_recebidos:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    # --- NOVO: Lógica de processamento ---
    # Vamos verificar se existe 'nome' e passá-lo para MAIÚSCULAS
    nome_original = dados_recebidos.get('nome', 'Visitante') # Se não houver nome, usa 'Visitante'
    nome_gritado = nome_original.upper() # A função mágica do Python
    # -------------------------------------

    return jsonify({
        "mensagem": "Recebi os teus dados!",
        "input_original": dados_recebidos,
        "resposta_backend": f"OLÁ {nome_gritado}!!", # Usamos aqui a variável nova
        "status": "Processado com lógica"
    }), 201  # 201 = "Criado"

# 7.3. ROTA GET: LISTAR TAREFAS
# Aqui usamos o método GET para devolver a lista de tarefas
# que está na "base de dados" em memória.
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    # Devolve a lista completa em formato JSON
    return jsonify(tarefas)

# 7.4. ROTA POST: CRIAR TAREFA
# Aqui usamos o método POST para criar uma nova tarefa
# e adicioná-la à lista em memória.
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    # 1. Receber o JSON enviado pelo Postman
    nova_tarefa = request.get_json()
    
    # 2. Adicionar à nossa lista "tarefas"
    tarefas.append(nova_tarefa)
    
    # 3. Responder que correu tudo bem
    return jsonify({"mensagem": "Tarefa criada com sucesso!", "tarefa": nova_tarefa}), 201

# 7.5. ROTA GET: OBTER TAREFA POR ID
# Aqui usamos o método GET para obter uma tarefa específica
# pelo seu ID.
@app.route('/tarefas/<int:id>', methods=['GET'])
def obter_tarefa(id):
    print(f"--> ID SOLICITADO: {id} (Tipo: {type(id)})")
    print(f"--> LISTA COMPLETA: {tarefas}")
    
    for tarefa in tarefas:
        print(f"Comparando com tarefa ID: {tarefa.get('id')} (Tipo: {type(tarefa.get('id'))})")
        if tarefa['id'] == id:
            print("--> ENCONTREI!")
            return jsonify(tarefa)
            
    print("--> NÃO ENCONTREI NADA")
    return jsonify({"erro": "Tarefa não encontrada"}), 404

# 7.6. ROTA PUT:
# ATUALIZAR uma tarefa (PUT), dado o seu ID.
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    # 1. Procurar a tarefa
    tarefa_encontrada = None
    for t in tarefas:
        if t['id'] == id:
            tarefa_encontrada = t
            break
            
    if not tarefa_encontrada:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
        
    # 2. Receber os dados novos
    dados_novos = request.get_json()
    
    # 3. Atualizar os campos (mantemos o ID original por segurança)
    tarefa_encontrada['titulo'] = dados_novos.get('titulo', tarefa_encontrada['titulo'])
    tarefa_encontrada['concluido'] = dados_novos.get('concluido', tarefa_encontrada['concluido'])
    
    return jsonify(tarefa_encontrada)

# 7.7. ROTA DELETE:
# REMOVER uma tarefa (DELETE), dado o seu ID.

# APAGAR uma tarefa (DELETE)
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def apagar_tarefa(id):
    # Vamos usar uma técnica diferente para remover:
    # Recriar a lista mantendo APENAS o que NÃO for o ID que queremos apagar.
    # (É mais seguro do que remover itens enquanto percorremos a lista)
    
    global tarefas # Precisamos de dizer que vamos mexer na variável global
    
    lista_filtrada = [t for t in tarefas if t['id'] != id]
    
    # Se o tamanho for igual, é porque não apagou nada (ID não existia)
    if len(lista_filtrada) == len(tarefas):
        return jsonify({"erro": "Tarefa não encontrada"}), 404
        
    tarefas = lista_filtrada
    return jsonify({"mensagem": "Tarefa apagada com sucesso"}), 200

# 8. LIGAR A API (só executa se correr este ficheiro diretamente)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # debug=True: reinicia auto com erros
    # host='0.0.0.0': acessível de fora WSL
    # port=5000: "porta" padrão Flask
