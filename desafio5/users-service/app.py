from flask import Flask, jsonify

app = Flask(__name__)

USERS_DATA = [
    {"id": 1, "name": "Alice", "role": "Dev"},
    {"id": 2, "name": "Bob", "role": "QA"},
]

@app.route('/users', methods=['GET'])
def get_users():
    """Endpoint de usuários."""
    print("Requisição recebida em Users Service.")
    return jsonify(USERS_DATA)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)