# 🐳 Projeto Docker - Desafios de Containers

## 🛠️ Tecnologias Utilizadas

<div align="left">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose"/>
</div>

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| Python | 3.11 | Linguagem de programação |
| Flask | 3.0.0 | Framework web minimalista |
| Docker | Latest | Plataforma de containerização |
| Docker Compose | Latest | Orquestração de containers |

---

## 📁 Estrutura do Projeto

```
Projeto-Docker/
│
├── 📄 README.md                          # Este arquivo
│
├── 📂 desafio1/                          # Desafio 1: Container básico
│   ├── app.py                            # Aplicação Python simples
│   ├── requirements.txt                  # Dependências (vazio)
│   ├── Dockerfile                        # Instruções de build da imagem
│   ├── README.md                         # Documentação do desafio
│   ├── INSTRUCOES_DOCKER.md             # Guia passo a passo
│   └── testar.py                         # Script de teste automatizado
│
├── 📂 desafio2/                          # Desafio 2: Aplicação web
│   ├── app.py                            # Servidor Flask
│   ├── requirements.txt                  # Flask + Werkzeug
│   ├── Dockerfile                        # Instruções de build
│   ├── .dockerignore                     # Arquivos a ignorar no build
│   ├── README.md                         # Documentação do desafio
│   ├── INSTRUCOES_DOCKER.md             # Guia passo a passo
│   └── testar.py                         # Script de teste automatizado
│
└── 📂 desafio3/                          # Desafio 3: Multi-container
    ├── docker-compose.yml                # Orquestração dos serviços
    ├── README.md                         # Documentação do desafio
    ├── INSTRUCOES_DOCKER.md             # Guia passo a passo
    ├── testar.py                         # Script de teste automatizado
    │
    ├── 📂 frontend/                      # Serviço Frontend
    │   ├── app.py                        # Interface de documentação
    │   ├── requirements.txt              # Dependências
    │   ├── Dockerfile                    # Build do frontend
    │   └── .dockerignore                 # Arquivos a ignorar
    │
    └── 📂 backend/                       # Serviço Backend
        ├── app.py                        # API REST (CRUD)
        ├── requirements.txt              # Dependências
        ├── Dockerfile                    # Build do backend
        └── .dockerignore                 # Arquivos a ignorar
```

---

## 🎯 Desafios

### Desafio 1 - Container Python Simples

**🎓 Nível:** Iniciante  
**📁 Pasta:** `desafio1/`

#### Descrição da Solução

Container básico que executa uma aplicação Python simples, exibindo mensagens de boas-vindas no terminal.

#### Arquitetura e Decisões Técnicas

```
┌─────────────────────────────┐
│     Imagem Base             │
│   python:3.11-slim          │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   Aplicação Python          │
│   - app.py                  │
│   - Sem dependências ext.   │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   Container em Execução     │
│   - Exibe mensagens         │
│   - Finaliza após execução  │
└─────────────────────────────┘
```

**Decisões Técnicas:**
- ✅ Uso de imagem `python:3.11-slim` para reduzir tamanho
- ✅ Sem dependências externas para simplicidade
- ✅ Container efêmero (executa e finaliza)

#### Explicação Detalhada do Funcionamento

**Containers envolvidos:**
- 1 container Python executando `app.py`

**Rede:**
- Não requer rede (execução local)

**Microserviços:**
- Aplicação standalone sem comunicação externa

**Fluxos de dados:**
```
Usuário → docker run → Container inicia → app.py executa → Saída no terminal → Container finaliza
```

#### Instruções de Execução

```bash
# 1. Navegar até a pasta
cd desafio1

# 2. Construir a imagem Docker
docker build -t desafio1-python .

# 3. Executar o container
docker run desafio1-python

# 4. (Opcional) Testar localmente sem Docker
python testar.py
```

**📖 Documentação completa:** [desafio1/INSTRUCOES_DOCKER.md](desafio1/INSTRUCOES_DOCKER.md)

---

### Desafio 2 - Aplicação Web Flask

**🎓 Nível:** Intermediário  
**📁 Pasta:** `desafio2/`

#### Descrição da Solução

Servidor web Flask containerizado com interface visual moderna e API REST para consulta de status.

#### Arquitetura e Decisões Técnicas

```
┌─────────────────────────────────────┐
│        Host Machine                 │
│                                     │
│  Browser → http://localhost:5000   │
└───────────────┬─────────────────────┘
                │ Port Mapping (-p 5000:5000)
                ▼
┌─────────────────────────────────────┐
│        Docker Container             │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Flask Web Server          │   │
│  │   - app.py                  │   │
│  │   - Porta 5000              │   │
│  │                             │   │
│  │   Endpoints:                │   │
│  │   GET /                     │   │
│  │   GET /api/status           │   │
│  └─────────────────────────────┘   │
│                                     │
│  Imagem: python:3.11-slim          │
└─────────────────────────────────────┘
```

**Decisões Técnicas:**
- ✅ Flask para simplicidade e leveza
- ✅ Porta 5000 (padrão do Flask)
- ✅ `.dockerignore` para otimizar build
- ✅ HTML/CSS inline para evitar arquivos estáticos
- ✅ Debug mode para desenvolvimento

#### Explicação Detalhada do Funcionamento

**Containers envolvidos:**
- 1 container Flask na porta 5000

**Rede:**
- Bridge network (padrão do Docker)
- Port mapping: Host:5000 → Container:5000

**Microserviços:**
- Serviço web standalone

**Fluxos de dados:**
```
Cliente HTTP → localhost:5000 → Docker Bridge → Container Flask
                                                      ↓
Cliente HTTP ← Resposta HTML/JSON ← Docker Bridge ← Flask processa
```

**Endpoints disponíveis:**
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/` | Página principal com UI |
| GET | `/api/status` | Status do servidor (JSON) |

#### Instruções de Execução

```bash
# 1. Navegar até a pasta
cd desafio2

# 2. Construir a imagem
docker build -t desafio2-flask .

# 3. Executar o container
docker run -p 5000:5000 desafio2-flask

# 4. Executar em background (opcional)
docker run -d -p 5000:5000 --name flask-server desafio2-flask

# 5. Acessar no navegador
# - Página principal: http://localhost:5000
# - API de status: http://localhost:5000/api/status

# 6. (Opcional) Testar localmente sem Docker
pip install -r requirements.txt
python testar.py
```

**📖 Documentação completa:** [desafio2/INSTRUCOES_DOCKER.md](desafio2/INSTRUCOES_DOCKER.md)

---

### Desafio 3 - Sistema Multi-Container

**🎓 Nível:** Avançado  
**📁 Pasta:** `desafio3/`

#### Descrição da Solução

Sistema completo de gerenciamento de tarefas com arquitetura de microserviços, separando frontend (documentação) e backend (API REST) em containers independentes, orquestrados via Docker Compose.

#### Arquitetura e Decisões Técnicas

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

**Decisões Técnicas:**

**1. Separação de Serviços:**
- ✅ Frontend e Backend em containers separados
- ✅ Responsabilidades bem definidas (SoC - Separation of Concerns)
- ✅ Escalabilidade independente de cada serviço

**2. Rede Docker:**
- ✅ Bridge network customizada (`app-network`)
- ✅ Comunicação inter-container via nome do serviço
- ✅ Isolamento da rede host

**3. Orquestração:**
- ✅ Docker Compose para gerenciamento simplificado
- ✅ `depends_on` para garantir ordem de inicialização
- ✅ `restart: unless-stopped` para alta disponibilidade

**4. Persistência:**
- ✅ Dados em memória (para demonstração)
- ✅ Pode ser facilmente migrado para PostgreSQL/MySQL

**5. API Design:**
- ✅ RESTful API seguindo padrões HTTP
- ✅ CRUD completo (Create, Read, Update, Delete)
- ✅ Respostas em JSON padronizadas

#### Explicação Detalhada do Funcionamento

**Containers envolvidos:**

| Container | Imagem | Porta | Função |
|-----------|--------|-------|--------|
| `desafio3-frontend` | python:3.11-slim | 5000 | Interface de documentação |
| `desafio3-backend` | python:3.11-slim | 5001 | API REST com CRUD |

**Rede:**
- **Nome:** `app-network`
- **Driver:** Bridge
- **Comunicação:** Containers se comunicam via nome do serviço
- **Port Mapping:**
  - Frontend: `5000:5000` (Host:Container)
  - Backend: `5001:5001` (Host:Container)

**Microserviços:**

**Frontend Service:**
- Serve interface HTML com documentação da API
- Health check endpoint: `/health`
- Não mantém estado
- Depende do backend para funcionar

**Backend Service:**
- API REST completa
- Banco de dados em memória (lista Python)
- 5 endpoints CRUD
- Health check endpoint: `/health`
- Retorna JSON padronizado

**Fluxos de Dados:**

**1. Acesso à Documentação:**
```
Usuário → Browser → localhost:5000 → Docker Bridge
                                          ↓
Browser ← HTML estilizado ← Docker Bridge ← Frontend Container
```

**2. Criar Tarefa (POST):**
```
Cliente → POST /api/tarefas → localhost:5001 → Docker Bridge
                                                     ↓
                                              Backend Container
                                                     ↓
                                        Valida dados (titulo obrigatório)
                                                     ↓
                                        Cria tarefa com ID único
                                                     ↓
                                        Adiciona à lista em memória
                                                     ↓
Cliente ← JSON (201 Created) ← Docker Bridge ← Retorna tarefa criada
```

**3. Listar Tarefas (GET):**
```
Cliente → GET /api/tarefas → localhost:5001 → Docker Bridge
                                                    ↓
                                             Backend Container
                                                    ↓
                                        Busca todas as tarefas
                                                    ↓
Cliente ← JSON (200 OK) ← Docker Bridge ← Retorna lista completa
```

**4. Atualizar Tarefa (PUT):**
```
Cliente → PUT /api/tarefas/:id → localhost:5001 → Docker Bridge
                                                        ↓
                                                 Backend Container
                                                        ↓
                                            Busca tarefa por ID
                                                        ↓
                                    Atualiza campos fornecidos
                                                        ↓
Cliente ← JSON (200 OK) ← Docker Bridge ← Retorna tarefa atualizada
```

**5. Deletar Tarefa (DELETE):**
```
Cliente → DELETE /api/tarefas/:id → localhost:5001 → Docker Bridge
                                                          ↓
                                                   Backend Container
                                                          ↓
                                                Remove da lista
                                                          ↓
Cliente ← JSON (200 OK) ← Docker Bridge ← Confirma remoção
```

#### Instruções de Execução

**Passo a Passo para Subir os Containers:**

```bash
# 1. Navegar até a pasta do desafio
cd desafio3

# 2. Construir e iniciar todos os serviços
docker-compose up --build

# Ou em modo detached (background)
docker-compose up -d --build

# 3. Verificar se os containers estão rodando
docker-compose ps

# 4. Ver logs de todos os serviços
docker-compose logs -f

# 5. Ver logs de um serviço específico
docker-compose logs -f frontend
docker-compose logs -f backend
```

**Testando a Aplicação:**

```bash
# 1. Acessar no navegador
# Frontend: http://localhost:5000
# Backend: http://localhost:5001/api/tarefas

# 2. Testar Health Checks
curl http://localhost:5000/health
curl http://localhost:5001/health

# 3. Listar todas as tarefas
curl http://localhost:5001/api/tarefas

# 4. Buscar tarefa por ID
curl http://localhost:5001/api/tarefas/1

# 5. Criar nova tarefa
curl -X POST http://localhost:5001/api/tarefas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Estudar Docker", "descricao": "Completar os 3 desafios"}'

# 6. Atualizar tarefa (marcar como concluída)
curl -X PUT http://localhost:5001/api/tarefas/1 \
  -H "Content-Type: application/json" \
  -d '{"concluida": true}'

# 7. Deletar tarefa
curl -X DELETE http://localhost:5001/api/tarefas/1

# 8. (Opcional) Testar localmente sem Docker
python testar.py
```

**Gerenciamento dos Containers:**

```bash
# Parar todos os serviços
docker-compose stop

# Iniciar serviços parados
docker-compose start

# Reiniciar todos os serviços
docker-compose restart

# Parar e remover containers
docker-compose down

# Parar, remover containers e volumes
docker-compose down -v

# Reconstruir sem cache
docker-compose build --no-cache

# Escalar um serviço (exemplo: 3 instâncias do backend)
docker-compose up --scale backend=3
```

**📖 Documentação completa:** [desafio3/INSTRUCOES_DOCKER.md](desafio3/INSTRUCOES_DOCKER.md)

---

## 🔧 Pré-requisitos

### Software Necessário

1. **Docker Desktop**
   - [Windows](https://docs.docker.com/desktop/install/windows-install/)
   - [Mac](https://docs.docker.com/desktop/install/mac-install/)
   - [Linux](https://docs.docker.com/engine/install/)

2. **Python 3.11+** (para testes locais)
   - [Download Python](https://www.python.org/downloads/)

3. **Git** (opcional)
   - [Download Git](https://git-scm.com/downloads)

### Verificar Instalação

```bash
# Verificar Docker
docker --version
docker-compose --version

# Verificar Python
python --version

# Verificar se Docker está rodando
docker ps
```

---

## 🚀 Como Executar

### Opção 1: Executar com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/giulms/Projeto-Docker.git
cd Projeto-Docker

# Escolha um desafio
cd desafio1  # ou desafio2, ou desafio3

# Siga as instruções no INSTRUCOES_DOCKER.md de cada desafio
```

### Opção 2: Executar Localmente (Sem Docker)

```bash
# Navegue até um desafio
cd desafio1  # ou desafio2, ou desafio3

# Instale dependências (se necessário)
pip install -r requirements.txt

# Execute o script de teste
python testar.py
```

---

## 🐛 Troubleshooting

### Porta já em uso

**Windows PowerShell:**
```powershell
# Verificar processo usando a porta
Get-NetTCPConnection -LocalPort 5000

# Parar o processo
Stop-Process -Id <PID>
```

**Linux/Mac:**
```bash
# Verificar processo
lsof -i :5000

# Parar o processo
kill -9 <PID>
```

### Container não inicia

```bash
# Ver logs do container
docker logs <container_name>

# Ver logs em tempo real
docker logs -f <container_name>

# Inspecionar container
docker inspect <container_name>
```

### Imagem não atualiza

```bash
# Reconstruir sem cache
docker build --no-cache -t nome-da-imagem .

# Com Docker Compose
docker-compose build --no-cache
```

### Problemas de permissão (Linux)

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Relogar ou executar
newgrp docker
```

### Limpar recursos Docker

```bash
# Remover containers parados
docker container prune

# Remover imagens não utilizadas
docker image prune

# Remover volumes não utilizados
docker volume prune

# Limpar tudo
docker system prune -a --volumes
```

---

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

---

## 👨‍💻 Autor

**Giulliano Muniz**

- GitHub: [@giulms](https://github.com/giulms)
- Projeto: [Projeto-Docker](https://github.com/giulms/Projeto-Docker)

---

<div align="center">

### ⭐ Se este projeto foi útil para você, considere dar uma estrela!

**Desenvolvido com ❤️ e 🐳 Docker**

</div>
