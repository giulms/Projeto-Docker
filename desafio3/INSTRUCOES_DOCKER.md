# 📝 Instruções para Criar os Arquivos Docker - Desafio 3

## Objetivo
Criar uma aplicação multi-container usando Docker Compose com frontend e backend separados.

## Estrutura do Projeto

```
desafio3/
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
└── docker-compose.yml
```

## Passo a Passo

### 1. Criar o Dockerfile do Frontend

Na pasta `desafio3/frontend/`, crie um arquivo **`Dockerfile`**:

```dockerfile
# Frontend Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 2. Criar o Dockerfile do Backend

Na pasta `desafio3/backend/`, crie um arquivo **`Dockerfile`**:

```dockerfile
# Backend API Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5001

CMD ["python", "app.py"]
```

### 3. Criar o docker-compose.yml

Na pasta `desafio3/`, crie um arquivo **`docker-compose.yml`**:

```yaml
version: '3.8'

services:
  frontend:
    build: ./frontend
    container_name: desafio3-frontend
    ports:
      - "5000:5000"
    networks:
      - app-network
    depends_on:
      - backend
    restart: unless-stopped

  backend:
    build: ./backend
    container_name: desafio3-backend
    ports:
      - "5001:5001"
    networks:
      - app-network
    restart: unless-stopped

networks:
  app-network:
    driver: bridge
```

## Executando o Projeto

### 1. Construir e Iniciar os Containers

No terminal, na pasta `desafio3`, execute:

```bash
docker-compose up --build
```

**Explicação:**
- `docker-compose up`: inicia os serviços definidos no docker-compose.yml
- `--build`: reconstrói as imagens antes de iniciar

### 2. Executar em Background

Para executar em segundo plano:

```bash
docker-compose up -d
```

### 3. Acessar a Aplicação

- **Frontend (Documentação):** http://localhost:5000
- **Backend API:** http://localhost:5001
- **Health Check Frontend:** http://localhost:5000/health
- **Health Check Backend:** http://localhost:5001/health

### 4. Testar a API

**Listar todas as tarefas:**
```bash
curl http://localhost:5001/api/tarefas
```

**Criar uma nova tarefa:**
```bash
curl -X POST http://localhost:5001/api/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Nova Tarefa", "descricao": "Descrição da tarefa"}'
```

**Buscar tarefa por ID:**
```bash
curl http://localhost:5001/api/tarefas/1
```

**Atualizar uma tarefa:**
```bash
curl -X PUT http://localhost:5001/api/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"concluida": true}'
```

**Deletar uma tarefa:**
```bash
curl -X DELETE http://localhost:5001/api/tarefas/1
```

## Comandos Úteis do Docker Compose

**Ver logs de todos os serviços:**
```bash
docker-compose logs
```

**Ver logs de um serviço específico:**
```bash
docker-compose logs frontend
docker-compose logs backend
```

**Ver logs em tempo real:**
```bash
docker-compose logs -f
```

**Parar os containers:**
```bash
docker-compose stop
```

**Parar e remover os containers:**
```bash
docker-compose down
```

**Parar, remover containers e volumes:**
```bash
docker-compose down -v
```

**Listar containers em execução:**
```bash
docker-compose ps
```

**Reiniciar um serviço específico:**
```bash
docker-compose restart frontend
```

**Executar comando em um container:**
```bash
docker-compose exec frontend bash
docker-compose exec backend bash
```

## 🎯 Resultado Esperado

Ao acessar http://localhost:5000, você verá a interface de documentação da API. O backend estará rodando em http://localhost:5001 e responderá às requisições da API.

## 📚 Conceitos Aprendidos

- ✅ Docker Compose para orquestração de containers
- ✅ Comunicação entre containers via redes Docker
- ✅ Construção de múltiplas imagens simultaneamente
- ✅ Gerenciamento de dependências entre serviços
- ✅ Mapeamento de portas para múltiplos serviços
- ✅ Health checks para monitoramento
- ✅ API REST completa com CRUD
- ✅ Separação de frontend e backend

## 💡 Dicas

1. Use `docker-compose logs -f` para debugar problemas
2. O `depends_on` garante que o backend inicie antes do frontend
3. A rede `app-network` permite comunicação entre os containers
4. Use `restart: unless-stopped` para manter os containers rodando após reinicializações

## 🔧 Troubleshooting

**Porta já em uso:**
```bash
# No Windows PowerShell, verificar processos usando a porta
Get-NetTCPConnection -LocalPort 5000
Get-NetTCPConnection -LocalPort 5001
```

**Reconstruir tudo do zero:**
```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```
