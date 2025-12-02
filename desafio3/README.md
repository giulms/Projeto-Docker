# Desafio 3 - Sistema Multi-Container 🚀

## 📖 Descrição da Solução

Este desafio implementa um sistema completo de gerenciamento de tarefas com arquitetura de **microserviços**. O sistema é composto por dois serviços independentes:

- **Frontend:** Servidor Flask que serve uma interface de documentação da API
- **Backend:** Servidor Flask que implementa uma API REST completa com operações CRUD

Ambos os serviços são orquestrados usando **Docker Compose**, comunicando-se através de uma rede Docker customizada.

---

## 🏗️ Arquitetura e Decisões Técnicas

### Diagrama de Arquitetura Completo

```
┌────────────────────────────────────────────────────────────────┐
│                        Host Machine                            │
│                                                                │
│  Browser                          API Client (curl/Postman)   │
│     │                                      │                   │
│     │ http://localhost:5000               │ http://localhost:5001
│     │                                      │                   │
└─────┼──────────────────────────────────────┼───────────────────┘
      │                                      │
      │ Port 5000:5000                      │ Port 5001:5001
      │                                      │
┌─────▼──────────────────────────────────────▼───────────────────┐
│                     Docker Network (app-network)               │
│                           Bridge Driver                        │
│                                                                │
│  ┌──────────────────────────┐    ┌─────────────────────────┐  │
│  │  Frontend Container      │    │  Backend Container      │  │
│  │  (desafio3-frontend)     │    │  (desafio3-backend)     │  │
│  │                          │    │                         │  │
│  │  ┌────────────────────┐  │    │  ┌───────────────────┐ │  │
│  │  │  Flask Server      │  │    │  │  Flask API        │ │  │
│  │  │  - Porta 5000      │  │    │  │  - Porta 5001     │ │  │
│  │  │  - UI Docs         │  │    │  │  - REST CRUD      │ │  │
│  │  │  - Health Check    │  │    │  │  - Health Check   │ │  │
│  │  └────────────────────┘  │    │  │  - In-memory DB   │ │  │
│  │                          │    │  └───────────────────┘ │  │
│  │  Imagem:                 │    │  Imagem:              │  │
│  │  python:3.11-slim        │    │  python:3.11-slim     │  │
│  └──────────────────────────┘    └─────────────────────────┘  │
│              │                              │                  │
│              └──────── depends_on ──────────┘                  │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| **Separação Frontend/Backend** | Seguir princípio SoC (Separation of Concerns) |
| **Bridge Network Customizada** | Comunicação segura entre containers |
| **Docker Compose** | Simplifica gerenciamento de múltiplos containers |
| **depends_on** | Garante ordem de inicialização (backend primeiro) |
| **restart: unless-stopped** | Alta disponibilidade - containers reiniciam após falhas |
| **Dados em Memória** | Simplifica demonstração (fácil migrar para PostgreSQL) |
| **Health Checks** | Monitoramento de saúde dos serviços |

---

## 🔍 Explicação Detalhada do Funcionamento

### Containers Envolvidos

| Container | Imagem | Porta | Função | Estado |
|-----------|--------|-------|--------|--------|
| `desafio3-frontend` | python:3.11-slim | 5000 | Interface de documentação | Stateless |
| `desafio3-backend` | python:3.11-slim | 5001 | API REST com CRUD | Stateful (memória) |

### Rede Docker

- **Nome:** `app-network`
- **Driver:** Bridge
- **Comunicação:** Containers se comunicam via nome do serviço (DNS interno)
- **Isolamento:** Rede separada da rede host

**Port Mapping:**
- Frontend: `5000:5000` (Host:Container)
- Backend: `5001:5001` (Host:Container)

### Microserviços

#### Frontend Service

```
Responsabilidades:
├── Servir interface HTML com documentação da API
├── Exibir endpoints disponíveis
├── Listar métodos HTTP e descrições
└── Health check endpoint (/health)

Características:
├── Stateless (não mantém dados)
├── Depende do backend
└── Pode ser escalado horizontalmente
```

#### Backend Service

```
Responsabilidades:
├── Implementar API REST completa
├── Gerenciar tarefas (CRUD)
├── Validar dados de entrada
├── Retornar respostas padronizadas em JSON
└── Health check endpoint (/health)

Características:
├── Stateful (mantém dados em memória)
├── Independente do frontend
├── Banco de dados in-memory (lista Python)
└── IDs únicos auto-incrementais
```

### Fluxos de Dados Detalhados

#### 1. Acesso à Documentação

```
Usuário
  ↓
Browser → localhost:5000
  ↓
Docker Bridge Network
  ↓
Frontend Container (Flask)
  ↓
Renderiza HTML com CSS
  ↓
Docker Bridge Network
  ↓
Browser ← HTML estilizado
```

#### 2. Criar Tarefa (POST)

```
Cliente (curl/Postman)
  ↓
POST /api/tarefas
Body: {"titulo": "...", "descricao": "..."}
  ↓
localhost:5001
  ↓
Docker Bridge Network
  ↓
Backend Container
  ↓
Validação: titulo é obrigatório?
  ├── ❌ Não → Retorna 400 (Bad Request)
  └── ✅ Sim → Continua
       ↓
Cria tarefa com ID único
  ↓
Adiciona à lista em memória
  ↓
Prepara resposta JSON
  ↓
Docker Bridge Network
  ↓
Cliente ← 201 Created + JSON da tarefa
```

#### 3. Listar Tarefas (GET)

```
Cliente
  ↓
GET /api/tarefas
  ↓
localhost:5001
  ↓
Docker Bridge Network
  ↓
Backend Container
  ↓
Busca todas as tarefas da lista
  ↓
Monta resposta com:
  - sucesso: true
  - quantidade: N
  - tarefas: [...]
  ↓
Docker Bridge Network
  ↓
Cliente ← 200 OK + JSON
```

#### 4. Atualizar Tarefa (PUT)

```
Cliente
  ↓
PUT /api/tarefas/:id
Body: {"concluida": true}
  ↓
localhost:5001
  ↓
Docker Bridge Network
  ↓
Backend Container
  ↓
Busca tarefa por ID
  ├── ❌ Não encontrada → Retorna 404
  └── ✅ Encontrada → Continua
       ↓
Atualiza campos fornecidos
  ↓
Mantém campos não fornecidos
  ↓
Docker Bridge Network
  ↓
Cliente ← 200 OK + Tarefa atualizada
```

#### 5. Deletar Tarefa (DELETE)

```
Cliente
  ↓
DELETE /api/tarefas/:id
  ↓
localhost:5001
  ↓
Docker Bridge Network
  ↓
Backend Container
  ↓
Busca tarefa por ID
  ├── ❌ Não encontrada → Retorna 404
  └── ✅ Encontrada → Continua
       ↓
Remove tarefa da lista
  ↓
Docker Bridge Network
  ↓
Cliente ← 200 OK + Mensagem de confirmação
```

### Estrutura do docker-compose.yml

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

---

## 🚀 Instruções de Execução

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose instalado (já vem com Docker Desktop)

### Subir os Containers

```bash
# 1. Navegar até a pasta do desafio
cd desafio3

# 2. Construir e iniciar todos os serviços
docker-compose up --build

# OU em modo detached (background)
docker-compose up -d --build
```

### Verificar Status dos Serviços

```bash
# Ver containers em execução
docker-compose ps

# Ver logs de todos os serviços
docker-compose logs

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

### Gerenciamento dos Containers

```bash
# Parar todos os serviços (mantém containers)
docker-compose stop

# Iniciar serviços parados
docker-compose start

# Reiniciar todos os serviços
docker-compose restart

# Reiniciar um serviço específico
docker-compose restart backend

# Parar e remover containers
docker-compose down

# Parar, remover containers E volumes
docker-compose down -v

# Reconstruir sem cache
docker-compose build --no-cache
docker-compose up --build
```

### Escalar Serviços

```bash
# Criar 3 instâncias do backend
docker-compose up --scale backend=3

# Nota: Requer configuração adicional de load balancer
```

---

## 🧪 Testando a Aplicação

### Via Navegador

1. **Frontend (Documentação):**
   - Acesse: http://localhost:5000
   - Interface moderna listando todos os endpoints

2. **Backend (Dados):**
   - Acesse: http://localhost:5001/api/tarefas
   - Retorna JSON com tarefas

### Via cURL (Recomendado)

#### Health Checks

```bash
# Frontend
curl http://localhost:5000/health

# Backend
curl http://localhost:5001/health
```

#### Listar Tarefas

```bash
curl http://localhost:5001/api/tarefas
```

#### Buscar Tarefa por ID

```bash
curl http://localhost:5001/api/tarefas/1
```

#### Criar Nova Tarefa

```bash
curl -X POST http://localhost:5001/api/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Estudar Docker Compose", "descricao": "Completar desafio 3"}'
```

#### Atualizar Tarefa

```bash
# Marcar tarefa 1 como concluída
curl -X PUT http://localhost:5001/api/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"concluida": true}'
```

#### Deletar Tarefa

```bash
curl -X DELETE http://localhost:5001/api/tarefas/1
```

### Via PowerShell

```powershell
# Listar tarefas
Invoke-RestMethod -Uri http://localhost:5001/api/tarefas

# Criar tarefa
$body = @{
    titulo = "Nova Tarefa"
    descricao = "Descrição da tarefa"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://localhost:5001/api/tarefas `
    -ContentType "application/json" -Body $body

# Atualizar tarefa
$body = @{ concluida = $true } | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri http://localhost:5001/api/tarefas/1 `
    -ContentType "application/json" -Body $body

# Deletar tarefa
Invoke-RestMethod -Method Delete -Uri http://localhost:5001/api/tarefas/1
```

### Script de Teste Automatizado

```bash
# Testa todos os endpoints automaticamente
python testar.py
```

---

## 📡 API REST Completa

### Modelo de Dados - Tarefa

```json
{
  "id": 1,
  "titulo": "Aprender Docker",
  "descricao": "Estudar conceitos de containers",
  "concluida": false,
  "criada_em": "2025-12-02T10:30:00"
}
```

### Endpoints da API

#### 1. GET /api/tarefas

**Descrição:** Lista todas as tarefas

**Resposta:**
```json
{
  "sucesso": true,
  "quantidade": 2,
  "tarefas": [
    {
      "id": 1,
      "titulo": "Aprender Docker",
      "descricao": "Estudar conceitos",
      "concluida": false,
      "criada_em": "2025-12-01T10:00:00"
    },
    {
      "id": 2,
      "titulo": "Implementar API",
      "descricao": "Criar API REST",
      "concluida": true,
      "criada_em": "2025-12-01T11:00:00"
    }
  ]
}
```

#### 2. GET /api/tarefas/:id

**Descrição:** Busca uma tarefa específica

**Sucesso (200):**
```json
{
  "sucesso": true,
  "tarefa": {
    "id": 1,
    "titulo": "Aprender Docker",
    "descricao": "Estudar conceitos",
    "concluida": false,
    "criada_em": "2025-12-01T10:00:00"
  }
}
```

**Erro (404):**
```json
{
  "sucesso": false,
  "mensagem": "Tarefa não encontrada"
}
```

#### 3. POST /api/tarefas

**Descrição:** Cria uma nova tarefa

**Corpo da Requisição:**
```json
{
  "titulo": "Estudar Docker",          // Obrigatório
  "descricao": "Completar desafios",   // Opcional
  "concluida": false                    // Opcional (default: false)
}
```

**Sucesso (201):**
```json
{
  "sucesso": true,
  "mensagem": "Tarefa criada com sucesso",
  "tarefa": {
    "id": 3,
    "titulo": "Estudar Docker",
    "descricao": "Completar desafios",
    "concluida": false,
    "criada_em": "2025-12-02T10:30:00"
  }
}
```

**Erro (400):**
```json
{
  "sucesso": false,
  "mensagem": "Título da tarefa é obrigatório"
}
```

#### 4. PUT /api/tarefas/:id

**Descrição:** Atualiza uma tarefa existente

**Corpo da Requisição (todos opcionais):**
```json
{
  "titulo": "Novo título",
  "descricao": "Nova descrição",
  "concluida": true
}
```

**Sucesso (200):**
```json
{
  "sucesso": true,
  "mensagem": "Tarefa atualizada com sucesso",
  "tarefa": {
    "id": 1,
    "titulo": "Novo título",
    "descricao": "Nova descrição",
    "concluida": true,
    "criada_em": "2025-12-01T10:00:00"
  }
}
```

#### 5. DELETE /api/tarefas/:id

**Descrição:** Remove uma tarefa

**Sucesso (200):**
```json
{
  "sucesso": true,
  "mensagem": "Tarefa removida com sucesso"
}
```

---

## 🐛 Problemas Comuns

### 1. Docker Compose

Ferramenta para definir e executar aplicações Docker multi-container usando arquivo YAML.

**Vantagens:**
- ✅ Configuração declarativa
- ✅ Múltiplos containers com um comando
- ✅ Redes e volumes automáticos
- ✅ Fácil compartilhamento

### 2. Redes Docker

```yaml
networks:
  app-network:
    driver: bridge
```

- Containers na mesma rede se comunicam por nome
- Isolamento de outras redes
- DNS interno automático

### 3. Dependências entre Serviços

```yaml
depends_on:
  - backend
```

- Define ordem de inicialização
- Garante que backend suba primeiro
- Não espera pelo "ready" (apenas "started")

### 4. Restart Policies

```yaml
restart: unless-stopped
```

| Policy | Comportamento |
|--------|---------------|
| `no` | Nunca reinicia (padrão) |
| `always` | Sempre reinicia |
| `on-failure` | Reinicia apenas em caso de erro |
| `unless-stopped` | Reinicia exceto se parado manualmente |

### 5. Arquitetura de Microserviços

**Princípios aplicados:**
- **Single Responsibility:** Cada serviço tem uma responsabilidade
- **Independência:** Serviços podem ser desenvolvidos independentemente
- **Escalabilidade:** Cada serviço pode escalar separadamente
- **Resiliência:** Falha de um não derruba o outro

### 6. API RESTful

**Padrões seguidos:**
- Verbos HTTP apropriados (GET, POST, PUT, DELETE)
- Códigos de status corretos (200, 201, 400, 404)
- Respostas em JSON padronizadas
- URIs significativas (`/api/tarefas`)

---

## 🎯 Comparação: Compose vs Manual

| Aspecto | Docker Manual | Docker Compose |
|---------|---------------|----------------|
| **Comando** | Múltiplos `docker run` | Um `docker-compose up` |
| **Rede** | Criar manualmente | Automática |
| **Gerenciamento** | Individual por container | Todos juntos |
| **Configuração** | Linha de comando | Arquivo YAML |
| **Reprodutibilidade** | Difícil | Fácil (compartilhar arquivo) |

---

## 💡 Dicas e Boas Práticas

### 1. Estrutura de Projeto

```
desafio3/
├── docker-compose.yml       # Raiz do projeto
├── frontend/
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── backend/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

### 2. Build Context

```yaml
build:
  context: ./frontend
  dockerfile: Dockerfile
```

### 3. Variáveis de Ambiente

```yaml
environment:
  - DEBUG=True
  - DATABASE_URL=postgresql://...
```

### 4. Volumes para Desenvolvimento

```yaml
volumes:
  - ./backend:/app  # Hot reload durante desenvolvimento
```

### 5. Health Checks no Compose

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5001/health"]
  interval: 30s
  timeout: 3s
  retries: 3
```

---

## 🆘 Problemas Comuns

### Erro: "network not found"

**Solução:**
```bash
docker-compose down
docker-compose up --build
```

### Erro: "address already in use"

**Solução:**
```bash
# Parar serviços conflitantes
docker-compose down

# Ou mudar porta no docker-compose.yml
ports:
  - "5002:5000"  # Usa 5002 no host
```

### Containers não se comunicam

**Causas possíveis:**
- Não estão na mesma rede
- Nome do serviço errado
- Firewall bloqueando

**Solução:**
```bash
# Verificar rede
docker network ls
docker network inspect desafio3_app-network

# Testar conectividade
docker-compose exec frontend ping backend
```

### Backend inicia antes do tempo

**Solução:** Use `wait-for-it` script:
```yaml
command: ["./wait-for-it.sh", "backend:5001", "--", "python", "app.py"]
```

---

## 📖 Documentação Adicional

Após completar este desafio, você pode:

1. **Adicionar Banco de Dados:**
   - PostgreSQL ou MySQL
   - Persistência real de dados

2. **Adicionar Redis:**
   - Cache de requisições
   - Sessões distribuídas

3. **Adicionar Nginx:**
   - Load balancer
   - Proxy reverso

4. **Monitoramento:**
   - Prometheus + Grafana
   - Logs centralizados

---

## 📖 Documentação Adicional

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Networking](https://docs.docker.com/network/)
- [RESTful API Best Practices](https://restfulapi.net/)

---

<div align="center">

**[⬅️ Desafio Anterior](../desafio2/README.md)** | **[Voltar ao Índice](../README.md)**

### 🎉 Parabéns por completar todos os desafios! 🎉

</div>
