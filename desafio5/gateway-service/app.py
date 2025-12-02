from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL', 'http://users-service:5000')
ORDERS_SERVICE_URL = os.environ.get('ORDERS_SERVICE_URL', 'http://orders-service:5001')

def fetch_data(url, endpoint):
    """Função auxiliar para fazer requisição HTTP para um serviço interno."""
    full_url = f"{url}{endpoint}"
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Não foi possível conectar a {url}. Detalhes: {e}"}), 503

@app.route('/users', methods=['GET'])
def get_users():
    """Endpoint público /users. Roteia para users-service/users."""
    return fetch_data(USERS_SERVICE_URL, '/users')

@app.route('/orders', methods=['GET'])
def get_orders():
    """Endpoint público /orders. Roteia para orders-service/orders."""
    return fetch_data(ORDERS_SERVICE_URL, '/orders')

@app.route('/')
def home():
    return "API Gateway rodando. Use /users ou /orders."

if __name__ == '__main__':
    print("API Gateway iniciado.")
    app.run(host='0.0.0.0', port=8000)