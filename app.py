from flask import Flask, jsonify, send_from_directory, abort, Response, request
from dotenv import load_dotenv
import os
import socket

# Carrega variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

# Obtenha o diretório de mídia do arquivo .env
MEDIA_DIR = os.getenv("PATH_MIDIA")
HOST_IP = os.getenv('HOST_IP')

# Extensões de arquivos de mídia suportados
MEDIA_EXTENSIONS = {'.mp4', '.mkv', '.mp3'}

def scan_media_files(directory):
    """Escaneia o diretório e retorna uma lista de arquivos de mídia válidos."""
    media_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in MEDIA_EXTENSIONS:
                file_path = os.path.relpath(os.path.join(root, file), directory)
                # Converte o caminho para o formato correto de URL
                file_path = file_path.replace("\\", "/")
                media_files.append(file_path)
    return media_files

def get_local_ip():
    """Obtém o IP da rede local da máquina."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # Conecta a um IP externo (não é necessário enviar dados)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    return local_ip

@app.route('/media')
def list_media():
    """Lista todos os arquivos de mídia disponíveis no diretório."""
    if not MEDIA_DIR or not os.path.exists(MEDIA_DIR):
        return jsonify({"error": "MEDIA_DIR não está configurado ou o diretório não existe."}), 500
    media_files = scan_media_files(MEDIA_DIR)
    media_urls = {file: f"/media/{file}" for file in media_files}
    return jsonify(media_urls)

@app.route('/media_playlist')
def generate_m3u():
    """Gera e serve um arquivo M3U com links para todos os arquivos de mídia."""
    if not MEDIA_DIR or not os.path.exists(MEDIA_DIR):
        return jsonify({"error": "MEDIA_DIR não está configurado ou o diretório não existe."}), 500
    
    # Escaneia os arquivos de mídia e gera links para o M3U
    media_files = scan_media_files(MEDIA_DIR)

    # Obtém o IP da rede local
    # host_ip = get_local_ip()
    host_ip = HOST_IP
    base_url = f"http://{host_ip}"  # Constrói a URL base com o IP da máquina e porta 5000
    
    m3u_content = "#EXTM3U\n"
    for file in media_files:
        media_url = f"{base_url}/media/{file}"
        m3u_content += f"#EXTINF:-1,{os.path.basename(file)}\n{media_url}\n"
    
    # Retorna o conteúdo do M3U como uma resposta
    return Response(m3u_content, mimetype="audio/x-mpegurl")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Configura o Flask para aceitar conexões externas
