from flask import Flask, jsonify
import requests
import os
import time

app = Flask(__name__)

SERVICE_A_URL = os.environ.get('SERVICE_A_URL', 'http://service-a:5000/users')

@app.route('/')
def home():
    return "Microsserviço B (Consumidor) rodando. Acesse /combined-data para ver os usuários."

@app.route('/combined-data', methods=['GET'])
def get_combined_data():
    """Endpoint que consome o Serviço A e formata a resposta."""
    print(f"Tentando consumir o Serviço A em: {SERVICE_A_URL}")
    
    try:
        response = requests.get(SERVICE_A_URL)
        response.raise_for_status()
        
        data = response.json()

        output_lines = ["--- Lista de Usuários Combinada ---"]
        
        for user in data.get('users', []):
            line = f"Usuário {user['username']} | Status: {user['status']} | Membro desde: {user['since']}"
            output_lines.append(line)
        
        return jsonify({
            "status": "SUCCESS",
            "source": SERVICE_A_URL,
            "processed_at": time.time(),
            "report": output_lines
        })
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO ao conectar com o Serviço A: {e}")
        return jsonify({
            "status": "ERROR",
            "message": f"Não foi possível conectar ao Serviço A. Detalhes: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("Aguardando 5 segundos antes de iniciar o Serviço B...")
    time.sleep(5)
    print("Microsserviço B (Consumidor) iniciado na porta 5001.")
    app.run(host='0.0.0.0', port=5001)