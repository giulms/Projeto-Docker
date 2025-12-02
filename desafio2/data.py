import sqlite3
import datetime
import os
import time

DB_FOLDER = "/app/data"
DB_FILE = os.path.join(DB_FOLDER, "app_data.db")

def setup_database():
    """Conecta/cria o banco de dados e garante que a tabela de logs exista."""
    os.makedirs(DB_FOLDER, exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            message TEXT
        );
    """)
    conn.commit()
    return conn

def write_and_read_data(conn):
    """Insere um novo registro e lê todos os registros existentes."""
    cursor = conn.cursor()
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"Container acessado em {current_time}"
    
    cursor.execute("INSERT INTO access_logs (timestamp, message) VALUES (?, ?)", 
                   (current_time, log_message))
    conn.commit()
    
    print("-" * 50)
    print("✅ Novo registro inserido com sucesso!")
    print(f"   Mensagem: {log_message}")
    print("-" * 50)
    
    cursor.execute("SELECT id, timestamp, message FROM access_logs ORDER BY id")
    logs = cursor.fetchall()
    
    print(f"\n📑 Histórico de Logs (Total: {len(logs)} registros):")
    
    for log in logs:
        print(f"   [ID: {log[0]}] {log[2]}")
        
    print("-" * 50)


if __name__ == "__main__":
    print(f"Tentando conectar ao banco de dados: {DB_FILE}")
    
    try:
        db_connection = setup_database()
        print("Conexão com o banco de dados SQLite estabelecida.")

        write_and_read_data(db_connection)
        
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")
        
    finally:
        if 'db_connection' in locals() and db_connection:
            db_connection.close()
            print("Conexão com o banco de dados fechada.")