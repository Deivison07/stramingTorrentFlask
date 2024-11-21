# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR .

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do projeto para o contêiner
COPY . .

# Expõe a porta do Flask
EXPOSE 5000

# Define o comando de execução do aplicativo
CMD ["python", "app.py"]
