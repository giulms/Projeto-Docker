from flask import Flask, jsonify
import time

app = Flask(__name__)

USERS_DATA = [
    {"id": 1, "username": "alice_dev", "status": "ativo", "since": "2023-01-15"},
    {"id": 2, "username": "bob_tester", "status": "inativo", "since": "2022-11-20"},
    {"id": 3, "username": "charlie_pm", "status": "ativo", "since": "2024-05-01"},
]

@app.route('/users', methods=['GET'])
def get_users():
    """Endpoint que retorna a lista de usuários em formato JSON."""
    print("Requisição recebida em /users.")
    return jsonify({
        "timestamp": time.time(),
        "users": USERS_DATA
    })

if __name__ == '__main__':
    print("Microsserviço A (Usuários) iniciado na porta 5000.")
    app.run(host='0.0.0.0', port=5000)