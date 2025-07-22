# Etapa 1: imagem base com Python
FROM python:3.11-slim

# Etapa 2: define diretório de trabalho
WORKDIR /app

# Etapa 3: copia os arquivos
COPY ./requirements.txt /app/
COPY ./app /app/app
COPY ./frontend /app/frontend

# Etapa 4: instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: expõe a porta
EXPOSE 8000

# Etapa 6: comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
