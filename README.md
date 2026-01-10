# Projeto 1: Primeira API Flask

API web simples em Python + Flask que devolve respostas em JSON.

## API endpoints
- `GET /` → informação da API e endpoints disponíveis.
- `GET /hello` → mensagem de teste.
- `GET /hello/<nome>` → mensagem personalizada.
- `GET /health` → health check (verifica se a API está viva).
- Erros: rotas inexistentes devolvem 404 em JSON.

## Como correr (WSL / Linux)

1) Entrar na pasta do projeto:
```bash
cd ~/projetos/projeto1_flask
```

2) Criar e ativar o ambiente virtual (venv):
```bash
python3 -m venv venv
source venv/bin/activate
```

3) Instalar dependências:
```bash
python -m pip install -r requirements.txt
```

4) Correr a API:
```bash
python app.py
```

A API fica disponível em:
- http://127.0.0.1:5000/

## Testar rapidamente (curl)
```bash
curl -i http://127.0.0.1:5000/
curl -i http://127.0.0.1:5000/hello
curl -i http://127.0.0.1:5000/hello/Ricardo
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/rota_inventada
```

## Notas
- A pasta `venv/` é local e não deve ir para o GitHub (é recriada a partir do `requirements.txt`).
