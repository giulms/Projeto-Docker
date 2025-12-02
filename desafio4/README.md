# Desafio 4 - Comunicação Entre Microserviços 🔄

## 📖 Descrição da Solução

Este desafio implementa dois microserviços que se comunicam entre si:

- **Service A (Microservice1):** Servidor Flask que gerencia dados de usuários
- **Service B (Microservice2):** Servidor Flask que consome dados do Service A e os processa

Demonstra **comunicação inter-container**, onde um serviço faz requisições HTTP para outro serviço dentro da mesma rede Docker.

---

## 🏗️ Arquitetura e Decisões Técnicas

### Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────┐
│                     Host Machine                           │
│                                                            │
│  Browser/Client                    Browser/Client         │
│       │                                  │                 │
│       │ http://localhost:8080           │ http://localhost:8081
│       │                                  │                 │
└───────┼──────────────────────────────────┼─────────────────┘
        │                                  │
        │ Port 8080:5000                  │ Port 8081:5001
        │                                  │
┌───────▼──────────────────────────────────▼─────────────────┐
│              Docker Network (microservice-network)         │
│                                                            │
│   ┌──────────────────────┐      ┌────────────────────────┐│
│   │   Service A          │      │   Service B            ││
│   │  (microservice1)     │◄─────│  (microservice2)       ││
│   │                      │      │                        ││
│   │  Flask Server        │      │  Flask Server          ││
│   │  Porta 5000          │      │  Porta 5001            ││
│   │                      │      │                        ││
│   │  GET /users          │      │  GET /                 ││
│   │  Retorna lista de    │      │  GET /combined-data    ││
│   │  usuários            │      │  Consome Service A     ││
│   │                      │      │  Formata resposta      ││
│   └──────────────────────┘      └────────────────────────┘│
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| **Comunicação HTTP** | Protocolo universal, fácil de debugar e monitorar |
| **DNS Interno Docker** | Containers se comunicam pelo nome do serviço |
| **depends_on** | Garante que Service A esteja rodando antes do Service B |
| **Variável de ambiente** | SERVICE_A_URL configurável, facilita testes |
| **requests library** | Biblioteca Python padrão para HTTP |
| **restart: always** | Alta disponibilidade - containers reiniciam automaticamente |

---

## 🔍 Explicação Detalhada do Funcionamento

### Containers Envolvidos

| Container | Imagem | Porta | Função |
|-----------|--------|-------|--------|
| `microservice1` | python:3.13 + Flask | 5000 (8080 no host) | Fornece dados de usuários |
| `microservice2` | python:3.13 + Flask | 5001 (8081 no host) | Consome e processa dados |

### Rede

- **Nome:** `microservice-network`
- **Driver:** Bridge
- **DNS:** Service A acessível via `http://service-a:5000`
- **Port Mapping:**
  - Service A: `8080:5000` (Host:Container)
  - Service B: `8081:5001` (Host:Container)

### Microserviços

#### Service A - Provedor de Dados

```
Responsabilidades:
├── Manter lista de usuários em memória
├── Endpoint GET /users retorna JSON
└── Responder requisições do Service B

Dados fornecidos:
├── ID do usuário
├── Username
├── Status (ativo/inativo)
└── Data de registro
```

#### Service B - Consumidor de Dados

```
Responsabilidades:
├── Fazer requisição HTTP para Service A
├── Processar dados recebidos
├── Formatar resposta de forma legível
└── Tratar erros de conexão

Features:
├── Aguarda 5 segundos antes de iniciar
├── Usa variável de ambiente para URL
└── Retorna relatório formatado
```

### Fluxos de Dados Detalhados

#### 1. Acesso Direto ao Service A

```
Cliente
  ↓
GET http://localhost:8080/users
  ↓
Docker Port Mapping (8080→5000)
  ↓
Service A (microservice1)
  ↓
Retorna lista de usuários em JSON
  ↓
Cliente recebe dados brutos
```

**Resposta do Service A:**
```json
{
  "timestamp": 1733158800.123,
  "users": [
    {
      "id": 1,
      "username": "alice_dev",
      "status": "ativo",
      "since": "2023-01-15"
    },
    ...
  ]
}
```

#### 2. Acesso ao Service B (Processado)

```
Cliente
  ↓
GET http://localhost:8081/combined-data
  ↓
Docker Port Mapping (8081→5001)
  ↓
Service B (microservice2)
  ↓
Faz requisição interna: http://service-a:5000/users
  ↓
Docker Network (microservice-network)
  ↓
Service A processa requisição
  ↓
Retorna dados para Service B
  ↓
Service B formata os dados
  ↓
Retorna relatório processado
  ↓
Cliente recebe dados formatados
```

**Resposta do Service B:**
```json
{
  "status": "SUCCESS",
  "source": "http://service-a:5000/users",
  "processed_at": 1733158805.456,
  "report": [
    "--- Lista de Usuários Combinada ---",
    "Usuário alice_dev | Status: ativo | Membro desde: 2023-01-15",
    "Usuário bob_tester | Status: inativo | Membro desde: 2022-11-20",
    "Usuário charlie_pm | Status: ativo | Membro desde: 2024-05-01"
  ]
}
```

#### 3. Tratamento de Erro

```
Service B tenta conectar ao Service A
  ↓
Service A está offline/indisponível
  ↓
requests.exceptions.RequestException
  ↓
Service B captura exceção
  ↓
Retorna erro 500 com mensagem descritiva
```

---

## 🚀 Instruções de Execução

### Pré-requisitos

- Docker Desktop instalado e rodando
- Docker Compose instalado

### Subir os Containers

```bash
# 1. Navegar até a pasta do desafio
cd desafio4

# 2. Construir e iniciar os serviços
docker-compose -f composezada.yml up --build

# OU em background
docker-compose -f composezada.yml up -d --build
```

### Verificar Status

```bash
# Ver containers rodando
docker-compose -f composezada.yml ps

# Ver logs de ambos os serviços
docker-compose -f composezada.yml logs -f

# Ver logs de um serviço específico
docker-compose -f composezada.yml logs -f service-a
docker-compose -f composezada.yml logs -f service-b
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

### 1. Testar Service A (Dados Brutos)

**Via Navegador:**
- Acesse: http://localhost:8080/users

**Via cURL:**
```bash
curl http://localhost:8080/users
```

**Via PowerShell:**
```powershell
Invoke-RestMethod -Uri http://localhost:8080/users
```

### 2. Testar Service B (Dados Processados)

**Via Navegador:**
- Página inicial: http://localhost:8081/
- Dados combinados: http://localhost:8081/combined-data

**Via cURL:**
```bash
# Página inicial
curl http://localhost:8081/

# Dados processados
curl http://localhost:8081/combined-data
```

**Via PowerShell:**
```powershell
# Dados processados
Invoke-RestMethod -Uri http://localhost:8081/combined-data
```

### 3. Verificar Comunicação Inter-Container

```bash
# Entrar no container do Service B
docker exec -it microservice2 bash

# Dentro do container, testar conexão com Service A
curl http://service-a:5000/users

# Sair do container
exit
```

### 4. Simular Falha do Service A

```bash
# Parar apenas o Service A
docker stop microservice1

# Testar Service B (deve retornar erro)
curl http://localhost:8081/combined-data

# Reiniciar Service A
docker start microservice1

# Testar novamente (deve funcionar)
curl http://localhost:8081/combined-data
```

---

## 💡 Dicas e Boas Práticas

### 1. Comunicação Entre Containers

**DNS Interno do Docker:**
- Containers na mesma rede se comunicam pelo nome do serviço
- `http://service-a:5000` resolve automaticamente para o IP do container

**Alternativas de URL:**
```python
# ✅ CORRETO: Usa nome do serviço
SERVICE_A_URL = 'http://service-a:5000/users'

# ❌ ERRADO: Usa localhost (não funciona entre containers)
SERVICE_A_URL = 'http://localhost:5000/users'

# ❌ ERRADO: Usa IP do host
SERVICE_A_URL = 'http://192.168.1.100:5000/users'
```

### 2. Dependências entre Serviços

```yaml
depends_on:
  service-a:
    condition: service_started
```

**O que faz:**
- Service B só inicia após Service A estar "started"
- Não garante que Service A esteja "ready" (pronto para receber requisições)

**Solução para "ready":**
```python
# Service B espera 5 segundos antes de iniciar
time.sleep(5)
```

### 3. Variáveis de Ambiente

```yaml
environment:
  SERVICE_A_URL: http://service-a:5000/users
```

**No código Python:**
```python
SERVICE_A_URL = os.environ.get('SERVICE_A_URL', 'http://service-a:5000/users')
```

**Vantagens:**
- Configuração flexível
- Fácil mudança sem recompilar
- Suporta diferentes ambientes (dev, staging, prod)

### 4. Tratamento de Erros em Microserviços

```python
try:
    response = requests.get(SERVICE_A_URL)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    return jsonify({"error": str(e)}), 503
```

**Códigos de Status:**
- `200 OK` - Sucesso
- `503 Service Unavailable` - Serviço dependente indisponível

### 5. Padrões de Microserviços

**Service Mesh Básico:**
```
Service B → Service A → Dados
         (HTTP)
```

**Resiliência:**
- Timeouts
- Retry logic
- Circuit breakers (avançado)

---

## 💡 Dicas e Boas Práticas

### 1. Health Checks

Adicione endpoints de saúde:
```python
@app.route('/health')
def health():
    return jsonify({"status": "healthy"})
```

### 2. Timeouts

Configure timeouts para evitar travamentos:
```python
response = requests.get(SERVICE_A_URL, timeout=5)
```

### 3. Retry Logic

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
```

### 4. Logging

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"Conectando ao Service A: {SERVICE_A_URL}")
```

---

## 🆘 Problemas Comuns

### Service B não consegue conectar ao Service A

**Causa:** Não estão na mesma rede

**Solução:**
```bash
# Verificar redes
docker network ls

# Inspecionar rede
docker network inspect microservice-network
```

### Erro "Name or service not known"

**Causa:** Nome do serviço errado no código

**Solução:** Verificar `docker-compose.yml`:
```yaml
services:
  service-a:  # ← Este é o nome usado no DNS
```

### Service B inicia antes do Service A estar pronto

**Solução:** Adicionar delay ou health check:
```python
time.sleep(5)  # Espera 5 segundos
```

---

## 📖 Documentação Adicional

- [Docker Networking](https://docs.docker.com/network/)
- [Python Requests Library](https://requests.readthedocs.io/)
- [Microservices Patterns](https://microservices.io/patterns/)

---

<div align="center">

**[⬅️ Desafio Anterior](../desafio3/README.md)** | **[Voltar ao Índice](../README.md)** | **[Próximo Desafio ➡️](../desafio5/README.md)**

</div>
