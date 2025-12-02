from flask import Flask, jsonify

app = Flask(__name__)

ORDERS_DATA = [
    {"order_id": "O1001", "user_id": 1, "product": "Laptop"},
    {"order_id": "O1002", "user_id": 2, "product": "Mouse"},
    {"order_id": "O1003", "user_id": 1, "product": "Monitor"},
]

@app.route('/orders', methods=['GET'])
def get_orders():
    """Endpoint de pedidos."""
    print("Requisição recebida em Orders Service.")
    return jsonify(ORDERS_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)