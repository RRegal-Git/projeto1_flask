# 1. IMPORTAR FLASK (biblioteca para criar APIs web)
from flask import Flask, jsonify  # Flask=framework, jsonify=converte dict→JSON

# 2. CRIAR A APLICAÇÃO (o "cérebro" da API)
app = Flask(__name__)  # __name__ = nome deste ficheiro (app.py)

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

# 6. LIGAR A API (só executa se correr este ficheiro diretamente)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # debug=True: reinicia auto com erros
    # host='0.0.0.0': acessível de fora WSL
    # port=5000: "porta" padrão Flask
