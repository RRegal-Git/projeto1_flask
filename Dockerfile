# 1. Imagem base com Python 
FROM python:3.12-slim

# 2. Diretório de trabalho dentro do contentor
WORKDIR /app

# 3. Copiar ficheiros de dependências
COPY requirements.txt .

# 4. Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o código da aplicação
COPY app.py .

# 6. Variável de ambiente para o Flask (opcional mas boa prática)
ENV FLASK_APP=app.py

# 7. Dizer em que porta a app vai correr dentro do contentor
EXPOSE 5000

# 8. Comando para arrancar a aplicação
CMD ["python", "app.py"]
