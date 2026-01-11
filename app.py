# 1. IMPORTAR FLASK (biblioteca para criar APIs web)
from flask import Flask, jsonify, request  # Flask=framework, jsonify=converte dict→JSON

# 2. CRIAR A APLICAÇÃO (o "cérebro" da API)
app = Flask(__name__)  # __name__ = nome deste ficheiro (app.py)
app.json.ensure_ascii = False  # <--- Esta linha mágica permite UTF-8 no JSON

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

# 8. LIGAR A API (só executa se correr este ficheiro diretamente)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # debug=True: reinicia auto com erros
    # host='0.0.0.0': acessível de fora WSL
    # port=5000: "porta" padrão Flask
