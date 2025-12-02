# Desafio 5 - API Gateway com Microserviços 🌐

## 📖 Descrição da Solução

Este desafio implementa um **API Gateway** que centraliza o acesso a múltiplos microserviços:

- **Gateway Service:** Porta de entrada única (porta 80), roteia requisições para os serviços apropriados
- **Users Service:** Gerencia dados de usuários
- **Orders Service:** Gerencia pedidos

Demonstra o **padrão API Gateway**, onde um ponto de entrada único simplifica o acesso a uma arquitetura de microserviços complexa.

---

## 🏗️ Arquitetura e Decisões Técnicas

### Diagrama de Arquitetura

```
┌───────────────────────────────────────────────────────────────┐
│                        Host Machine                           │
│                                                               │
│                     Browser/Client                            │
│                            │                                  │
│                            │ http://localhost                 │
│                            │                                  │
└────────────────────────────┼──────────────────────────────────┘
                             │
                             │ Port 80:8000
                             │
┌────────────────────────────▼──────────────────────────────────┐
│                    Docker Network (gateway-network)           │
│                                                               │
│                   ┌─────────────────────┐                    │
│                   │   Gateway Service   │                    │
│                   │   (API Gateway)     │                    │
│                   │                     │                    │
│                   │   Flask Server      │                    │
│                   │   Porta 8000        │                    │
│                   │                     │                    │
│                   │   Rotas:            │                    │
│                   │   /                 │                    │
│                   │   /health           │                    │
│                   │   /users/*          │───┐                │
│                   │   /orders/*         │   │                │
│                   └─────────────────────┘   │                │
│                            │                │                │
│          ┌─────────────────┼────────────────┘                │
│          │                 │                                 │
│          ▼                 ▼                                 │
│   ┌──────────────┐  ┌──────────────┐                        │
│   │Users Service │  │Orders Service│                        │
│   │              │  │              │                        │
│   │Flask Server  │  │Flask Server  │                        │
│   │Porta 5000    │  │Porta 5001    │                        │
│   │              │  │              │                        │
│   │GET /         │  │GET /         │                        │
│   │GET /users    │  │GET /orders   │                        │
│   │POST /users   │  │POST /orders  │                        │
│   │GET /users/:id│  │GET /orders/:id                        │
│   └──────────────┘  └──────────────┘                        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

### Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| **API Gateway Pattern** | Ponto único de entrada, simplifica acesso do cliente |
| **requests library** | Proxy HTTP simples e eficiente |
| **Path-based routing** | `/users/*` → Users Service, `/orders/*` → Orders Service |
| **depends_on** | Gateway só inicia após backends estarem rodando |
| **Porta 80** | Porta padrão HTTP, não precisa especificar na URL |
| **Health checks** | Permite monitorar status de todos os serviços |
| **JSON responses** | Formato padrão para APIs RESTful |

### Comparação: Sem Gateway vs Com Gateway

#### Sem Gateway (Acesso Direto)
```
Cliente → [Porta 5000] → Users Service
Cliente → [Porta 5001] → Orders Service
Cliente → [Porta 5002] → Payments Service
Cliente → [Porta 5003] → Notifications Service
```
**Problemas:**
- Cliente precisa saber múltiplas portas
- CORS complexo para cada serviço
- Difícil adicionar autenticação centralizada
- Logging e monitoramento distribuídos

#### Com Gateway (Este Desafio)
```
Cliente → [Porta 80] → Gateway → Users Service
                              → Orders Service
                              → Payments Service
                              → Notifications Service
```
**Vantagens:**
- ✅ Porta única (80)
- ✅ CORS configurado em um lugar
- ✅ Autenticação centralizada
- ✅ Logging centralizado
- ✅ Rate limiting centralizado

---

## 🔍 Explicação Detalhada do Funcionamento

### Containers Envolvidos

| Container | Imagem | Porta | Função |
|-----------|--------|-------|--------|
| `gateway-service` | python:3.11-slim + Flask | 8000 (80 no host) | Roteador de requisições |
| `users-service` | python:3.11-slim + Flask | 5000 | Gerencia usuários |
| `orders-service` | python:3.11-slim + Flask | 5001 | Gerencia pedidos |

### Rede

- **Nome:** `gateway-network`
- **Driver:** Bridge
- **DNS Interno:**
  - Users Service: `http://users-service:5000`
  - Orders Service: `http://orders-service:5001`
- **Port Mapping:**
  - Gateway: `80:8000` (Host:Container)
  - Users: Apenas interno (não exposto ao host)
  - Orders: Apenas interno (não exposto ao host)

### Serviços Detalhados

#### 1. Gateway Service - Roteador Central

```
Responsabilidades:
├── Receber todas as requisições HTTP do cliente
├── Analisar o path da URL (ex: /users, /orders)
├── Rotear para o microserviço apropriado
├── Repassar resposta para o cliente
└── Tratar erros de conexão

Rotas implementadas:
├── GET  /              → Página de boas-vindas
├── GET  /health        → Status de todos os serviços
├── ANY  /users         → Proxy para Users Service
├── ANY  /users/:id     → Proxy para Users Service
├── ANY  /orders        → Proxy para Orders Service
└── ANY  /orders/:id    → Proxy para Orders Service

Lógica de roteamento:
├── path.startswith('/users') → http://users-service:5000
└── path.startswith('/orders') → http://orders-service:5001
```

#### 2. Users Service - Backend de Usuários

```
Responsabilidades:
├── Armazenar lista de usuários em memória
├── CRUD de usuários (Create, Read)
└── Validar dados de entrada

Endpoints:
├── GET  /              → Informações do serviço
├── GET  /users         → Lista todos os usuários
├── GET  /users/:id     → Retorna usuário específico
└── POST /users         → Cria novo usuário

Estrutura de dados:
{
  "id": 1,
  "name": "João Silva",
  "email": "joao@example.com",
  "role": "admin"
}
```

#### 3. Orders Service - Backend de Pedidos

```
Responsabilidades:
├── Armazenar lista de pedidos em memória
├── CRUD de pedidos (Create, Read)
└── Calcular total de pedidos

Endpoints:
├── GET  /              → Informações do serviço
├── GET  /orders        → Lista todos os pedidos
├── GET  /orders/:id    → Retorna pedido específico
└── POST /orders        → Cria novo pedido

Estrutura de dados:
{
  "id": 1,
  "user_id": 1,
  "product": "Laptop Dell",
  "quantity": 2,
  "total": 5000.00,
  "status": "pending"
}
```

### Fluxos de Requisição Detalhados

#### 1. Listar Usuários (GET /users)

```
1. Cliente
   ↓
   GET http://localhost/users
   
2. Docker Port Mapping (80→8000)
   ↓
   Gateway Service recebe requisição
   
3. Gateway analisa o path
   ↓
   path = "/users"
   path.startswith('/users') → TRUE
   
4. Gateway faz proxy
   ↓
   requests.get('http://users-service:5000/users')
   
5. Docker DNS resolve users-service
   ↓
   Requisição chega ao Users Service
   
6. Users Service processa
   ↓
   Retorna lista de usuários em JSON
   
7. Gateway repassa resposta
   ↓
   Cliente recebe:
   {
     "users": [
       {"id": 1, "name": "João Silva", ...},
       {"id": 2, "name": "Maria Santos", ...}
     ]
   }
```

#### 2. Criar Pedido (POST /orders)

```
1. Cliente envia dados
   ↓
   POST http://localhost/orders
   Body: {
     "user_id": 1,
     "product": "Mouse Gamer",
     "quantity": 1
   }
   
2. Gateway recebe e analisa
   ↓
   path = "/orders"
   method = "POST"
   
3. Gateway faz proxy POST
   ↓
   requests.post(
     'http://orders-service:5001/orders',
     json=request_data
   )
   
4. Orders Service processa
   ↓
   ├── Valida dados
   ├── Gera ID único
   ├── Calcula total
   └── Salva em memória
   
5. Orders Service responde
   ↓
   {
     "id": 3,
     "user_id": 1,
     "product": "Mouse Gamer",
     "quantity": 1,
     "total": 150.00,
     "status": "pending",
     "created_at": "2024-12-02T15:30:00"
   }
   
6. Gateway repassa resposta
   ↓
   Cliente recebe confirmação
```

#### 3. Health Check (GET /health)

```
1. Cliente
   ↓
   GET http://localhost/health
   
2. Gateway verifica todos os serviços
   ↓
   ├── Tenta conectar users-service:5000
   └── Tenta conectar orders-service:5001
   
3. Gateway compila status
   ↓
   {
     "gateway": "healthy",
     "services": {
       "users": "healthy",    // OU "unhealthy"
       "orders": "healthy"    // OU "unhealthy"
     },
     "timestamp": 1733165432.123
   }
   
4. Cliente recebe relatório completo
```

#### 4. Erro de Serviço Indisponível

```
1. Cliente faz requisição
   ↓
   GET http://localhost/users
   
2. Gateway tenta proxy
   ↓
   requests.get('http://users-service:5000/users', timeout=5)
   
3. Users Service está offline
   ↓
   requests.exceptions.RequestException
   
4. Gateway captura erro
   ↓
   {
     "error": "Service unavailable",
     "message": "Failed to connect to users-service"
   }
   Status: 503 Service Unavailable
   
5. Cliente recebe erro tratado
```

---

## 🚀 Instruções de Execução

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose instalado

### Subir os Containers

```bash
# 1. Navegar até a pasta do desafio
cd desafio5

# 2. Construir e iniciar todos os serviços
docker-compose -f composezada.yml up --build

# OU em background
docker-compose -f composezada.yml up -d --build
```

### Verificar Status

```bash
# Ver todos os containers
docker-compose -f composezada.yml ps

# Ver logs de todos os serviços
docker-compose -f composezada.yml logs -f

# Ver logs de um serviço específico
docker-compose -f composezada.yml logs -f gateway-service
docker-compose -f composezada.yml logs -f users-service
docker-compose -f composezada.yml logs -f orders-service
```

### Parar os Serviços

```bash
# Parar containers
docker-compose -f composezada.yml stop

# Parar e remover
docker-compose -f composezada.yml down
```

---

## 🧪 Testando a Aplicação

### 1. Testar Gateway (Página Inicial)

**Via Navegador:**
- Acesse: http://localhost/

**Via cURL:**
```bash
curl http://localhost/
```

**Via PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost/
```

### 2. Testar Users Service (via Gateway)

**Listar usuários:**
```bash
# cURL
curl http://localhost/users

# PowerShell
Invoke-RestMethod -Uri http://localhost/users
```

**Buscar usuário específico:**
```bash
# cURL
curl http://localhost/users/1

# PowerShell
Invoke-RestMethod -Uri http://localhost/users/1
```

**Criar novo usuário:**
```bash
# cURL
curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Carlos Souza", "email": "carlos@example.com", "role": "user"}'

# PowerShell
$body = @{
    name = "Carlos Souza"
    email = "carlos@example.com"
    role = "user"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost/users -Method Post -Body $body -ContentType "application/json"
```

### 3. Testar Orders Service (via Gateway)

**Listar pedidos:**
```bash
# cURL
curl http://localhost/orders

# PowerShell
Invoke-RestMethod -Uri http://localhost/orders
```

**Buscar pedido específico:**
```bash
# cURL
curl http://localhost/orders/1

# PowerShell
Invoke-RestMethod -Uri http://localhost/orders/1
```

**Criar novo pedido:**
```bash
# cURL
curl -X POST http://localhost/orders \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product": "Teclado Mecânico", "quantity": 1}'

# PowerShell
$body = @{
    user_id = 1
    product = "Teclado Mecânico"
    quantity = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost/orders -Method Post -Body $body -ContentType "application/json"
```

### 4. Verificar Health Check

```bash
# cURL
curl http://localhost/health

# PowerShell
Invoke-RestMethod -Uri http://localhost/health
```

### 5. Teste de Resiliência - Simular Falha

```bash
# Parar o Users Service
docker stop users-service

# Tentar acessar usuários (deve falhar gracefully)
curl http://localhost/users

# Verificar health check (users deve estar unhealthy)
curl http://localhost/health

# Reiniciar Users Service
docker start users-service

# Tentar novamente (deve funcionar)
curl http://localhost/users
```

### 6. Teste de Isolamento - Acesso Direto Bloqueado

```bash
# Tentar acessar Users Service diretamente (deve falhar - porta não exposta)
curl http://localhost:5000/users
# Erro: Connection refused

# Acessar via Gateway (deve funcionar)
curl http://localhost/users
# Sucesso!
```

---

## 📚 Conceitos Aprendidos

### 1. API Gateway Pattern

**O que é:**
Um componente que atua como ponto de entrada único para múltiplos microserviços.

**Benefícios:**
```
┌─────────────────────────────────────────┐
│         Vantagens do Gateway            │
├─────────────────────────────────────────┤
│ ✅ Simplifica acesso do cliente         │
│ ✅ Centraliza autenticação              │
│ ✅ Permite rate limiting                │
│ ✅ Facilita versionamento de API        │
│ ✅ Reduz número de chamadas do cliente  │
│ ✅ Centraliza logging e monitoramento   │
│ ✅ Permite transformação de respostas   │
└─────────────────────────────────────────┘
```

**Implementação:**
```python
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gateway(path):
    # Determina serviço baseado no path
    if path.startswith('users'):
        target = 'http://users-service:5000'
    elif path.startswith('orders'):
        target = 'http://orders-service:5001'
    
    # Faz proxy da requisição
    response = requests.request(
        method=request.method,
        url=f'{target}/{path}',
        json=request.json
    )
    return response.json(), response.status_code
```

### 2. Service Discovery

**DNS Interno do Docker:**
```yaml
services:
  gateway-service:
    networks:
      - gateway-network
  
  users-service:
    networks:
      - gateway-network  # Mesma rede = DNS funciona
```

**No código:**
```python
# ✅ Usa nome do serviço (DNS automático)
USERS_SERVICE_URL = 'http://users-service:5000'

# ❌ Usa IP (quebra se IP mudar)
USERS_SERVICE_URL = 'http://172.18.0.3:5000'
```

### 3. Port Mapping Estratégico

```yaml
# Gateway - Exposto ao host
gateway-service:
  ports:
    - "80:8000"

# Backend - NÃO exposto (apenas interno)
users-service:
  # SEM ports: - cliente não acessa diretamente
```

**Segurança:**
- Clientes só acessam via Gateway
- Serviços backend protegidos
- Controle centralizado de acesso

### 4. Proxy HTTP com Python Requests

```python
# Repassa método, headers e body
response = requests.request(
    method=request.method,        # GET, POST, etc
    url=target_url,
    headers=request.headers,      # Repassa headers
    json=request.json,            # Repassa body
    timeout=5                     # Previne travamento
)

# Retorna resposta do backend
return response.json(), response.status_code
```

### 5. Health Checks Distribuídos

```python
def check_service(url):
    try:
        response = requests.get(url, timeout=2)
        return "healthy" if response.ok else "unhealthy"
    except:
        return "unhealthy"

@app.route('/health')
def health():
    return {
        "gateway": "healthy",
        "services": {
            "users": check_service('http://users-service:5000'),
            "orders": check_service('http://orders-service:5001')
        }
    }
```

### 6. Dependências entre Serviços

```yaml
gateway-service:
  depends_on:
    - users-service
    - orders-service
```

**Garante:**
- Gateway inicia por último
- Backends já estão rodando
- Reduz erros de conexão iniciais

---

## 💡 Padrões Avançados de API Gateway

### 1. Authentication & Authorization

```python
@app.before_request
def authenticate():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Unauthorized"}), 401
    
    # Validar token (JWT, OAuth, etc)
    if not validate_token(token):
        return jsonify({"error": "Invalid token"}), 403
```

### 2. Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/users')
@limiter.limit("100 per hour")
def users():
    # Máximo 100 requisições por hora por IP
    pass
```

### 3. Request/Response Transformation

```python
@app.route('/users')
def users():
    response = requests.get('http://users-service:5000/users')
    data = response.json()
    
    # Transforma resposta (ex: adiciona metadata)
    return {
        "data": data,
        "metadata": {
            "source": "users-service",
            "timestamp": time.time()
        }
    }
```

### 4. Circuit Breaker

```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_users_service():
    return requests.get('http://users-service:5000/users')
```

### 5. Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/users')
@cache.cached(timeout=300)  # Cache por 5 minutos
def users():
    return requests.get('http://users-service:5000/users').json()
```

---

## 🆘 Problemas Comuns

### Gateway não consegue conectar aos backends

**Causa:** Serviços não estão na mesma rede

**Solução:**
```bash
# Verificar rede
docker network inspect gateway-network

# Verificar se todos os serviços estão listados
```

### Erro "Service Unavailable" constante

**Causa:** Backends demorando para iniciar

**Solução:** Adicionar healthcheck no docker-compose:
```yaml
users-service:
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:5000"]
    interval: 10s
    timeout: 5s
    retries: 3
```

### Requisições POST não funcionam

**Causa:** Body não está sendo repassado

**Solução:**
```python
# Garantir que json/data seja repassado
response = requests.request(
    method=request.method,
    url=target_url,
    json=request.get_json(),  # ← Importante!
    headers=request.headers
)
```

### Timeout em requisições lentas

**Causa:** Timeout muito baixo

**Solução:**
```python
# Aumentar timeout
response = requests.get(url, timeout=30)  # 30 segundos
```

---

## 🎯 Próximos Passos e Melhorias

### Nível Intermediário
- [ ] Adicionar autenticação JWT no Gateway
- [ ] Implementar rate limiting por endpoint
- [ ] Adicionar logging estruturado (JSON logs)
- [ ] Implementar CORS adequadamente

### Nível Avançado
- [ ] Circuit breaker para resiliência
- [ ] Service mesh com Istio
- [ ] Tracing distribuído com Jaeger
- [ ] Métricas com Prometheus + Grafana
- [ ] Load balancing entre réplicas

### Nível Especialista
- [ ] API versioning (v1, v2)
- [ ] GraphQL Gateway
- [ ] WebSocket support
- [ ] gRPC backend communication

---

## 📖 Documentação Adicional

- [Microservices Patterns - API Gateway](https://microservices.io/patterns/apigateway.html)
- [Kong API Gateway](https://docs.konghq.com/)
- [AWS API Gateway](https://aws.amazon.com/api-gateway/)
- [Python Requests](https://requests.readthedocs.io/)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

<div align="center">

**[⬅️ Desafio Anterior](../desafio4/README.md)** | **[Voltar ao Índice](../README.md)**

---

### 🎉 Parabéns! Você completou todos os desafios! 🎉

</div>
