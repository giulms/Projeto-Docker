import time, requests

SERVER_URL = "http://servidor:5000"

while True:
    try:
        response = requests.get(SERVER_URL)
        print("Resposta:", response.text, flush= True)
        
    except Exception as e:
        print("Erro ao conectar:", e, flush= True)
    time.sleep(5)