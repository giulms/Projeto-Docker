# app.py
from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST') 
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')

@app.route('/')
def home():
    return "Serviço WEB rodando. Acesse /status para verificar a conexão com o DB."

@app.route('/status')
def status():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        conn.close()
        return jsonify({
            "status": "OK",
            "db_host": DB_HOST,
            "message": "Conexão bem-sucedida com o Banco de Dados (PostgreSQL)."
        })
    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "db_host": DB_HOST,
            "error": str(e),
            "message": "Falha ao conectar ao Banco de Dados. Verifique o serviço 'db'."
        }), 500

if __name__ == '__main__':
    print("Aguardando o serviço DB...")
    time.sleep(10)
    print("Iniciando o Serviço WEB...")
    app.run(host='0.0.0.0', port=5000)