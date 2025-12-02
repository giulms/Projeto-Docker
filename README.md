# 🐳 Projeto Docker - Desafios de Containers

> Projeto da disciplina de **Fundamentos de Computação Concorrente, Paralela e Distribuída**

<div align="left">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose"/>
</div>

---

## 📖 Sobre o Projeto

Este projeto contém **5 desafios progressivos** para aprender Docker e containerização de aplicações. Cada desafio aumenta o nível de complexidade, ensinando desde containers básicos até arquiteturas complexas com API Gateway e microserviços.

---

## 📁 Estrutura do Projeto

```
Projeto-Docker/
│
├── 📄 README.md                          # Este arquivo
│
├── 📂 desafio1/                          # Container Python simples
│   ├── app.py                            # Aplicação Python
│   ├── requirements.txt                  # Dependências
│   ├── Dockerfile                        # Instruções Docker
│   └── README.md                         # Documentação completa
│
├── 📂 desafio2/                          # Aplicação web Flask
│   ├── app.py                            # Servidor Flask
│   ├── requirements.txt                  # Dependências
│   ├── Dockerfile                        # Instruções Docker
│   └── README.md                         # Documentação completa
│
├── 📂 desafio3/                          # Sistema multi-container
│   ├── docker-compose.yml                # Orquestração Docker Compose
│   ├── README.md                         # Documentação completa
│   │
│   ├── 📂 frontend/                      # Serviço de documentação
│   │   ├── app.py                        # Interface web
│   │   ├── requirements.txt              # Dependências
│   │   └── Dockerfile                    # Instruções Docker
│   │
│   └── 📂 backend/                       # API REST
│       ├── app.py                        # API CRUD
│       ├── requirements.txt              # Dependências
│       └── Dockerfile                    # Instruções Docker
│
├── 📂 desafio4/                          # Comunicação entre microserviços
│   ├── docker-compose.yml                # Orquestração
│   ├── README.md                         # Documentação completa
│   │
│   ├── 📂 service1/                      # Provedor de dados
│   │   ├── app.py                        # Microserviço de usuários
│   │   └── Dockerfile                    # Instruções Docker
│   │
│   └── 📂 service2/                      # Consumidor de dados
│       ├── app.py                        # Microserviço consumidor
│       └── Dockerfile                    # Instruções Docker
│
└── 📂 desafio5/                          # API Gateway
    ├── docker-compose.yml                # Orquestração
    ├── README.md                         # Documentação completa
    │
    ├── 📂 gateway-service/               # Gateway central
    │   ├── app.py                        # Roteador de requisições
    │   ├── requirements.txt              # Dependências
    │   └── Dockerfile                    # Instruções Docker
    │
    ├── 📂 users-service/                 # Backend de usuários
    │   ├── app.py                        # API de usuários
    │   └── Dockerfile                    # Instruções Docker
    │
    └── 📂 orders-service/                # Backend de pedidos
        ├── app.py                        # API de pedidos
        └── Dockerfile                    # Instruções Docker
```

---

## 🎯 Desafios

### Desafio 1 - Container Python Simples

**📁 Pasta:** `desafio1/`

Container básico que executa uma aplicação Python simples, exibindo mensagens de boas-vindas no terminal.

**O que você vai aprender:**
- Criar Dockerfile básico
- Construir imagens Docker
- Executar containers simples
- Comandos fundamentais do Docker

**📖 [Ver documentação completa →](desafio1/README.md)**

---

### Desafio 2 - Aplicação Web Flask

**📁 Pasta:** `desafio2/`

Servidor web Flask containerizado com interface visual moderna e API REST para consulta de status.

**O que você vai aprender:**
- Mapeamento de portas Docker
- Servir aplicações web em containers
- Gerenciamento de logs
- Executar containers em background
- Otimização com .dockerignore

**📖 [Ver documentação completa →](desafio2/README.md)**

---

### Desafio 3 - Sistema Multi-Container

**📁 Pasta:** `desafio3/`

Sistema completo de gerenciamento de tarefas com arquitetura de microserviços: frontend (documentação) e backend (API REST) orquestrados com Docker Compose.

**O que você vai aprender:**
- Docker Compose para orquestração
- Comunicação entre containers
- Redes Docker customizadas
- API REST completa (CRUD)
- Arquitetura de microserviços

**📖 [Ver documentação completa →](desafio3/README.md)**

---

### Desafio 4 - Comunicação Entre Microserviços

**📁 Pasta:** `desafio4/`

Dois microserviços que se comunicam entre si: um provedor de dados de usuários e um consumidor que processa essas informações.

**O que você vai aprender:**
- Comunicação inter-container via HTTP
- DNS interno do Docker
- Dependências entre serviços
- Tratamento de erros em microserviços
- Variáveis de ambiente

**📖 [Ver documentação completa →](desafio4/README.md)**

---

### Desafio 5 - API Gateway com Microserviços

**📁 Pasta:** `desafio5/`

Arquitetura completa com API Gateway centralizando o acesso a múltiplos microserviços backend (usuários e pedidos).

**O que você vai aprender:**
- Padrão API Gateway
- Roteamento de requisições
- Service Discovery
- Port mapping estratégico
- Health checks distribuídos
- Arquitetura de microserviços avançada

**📖 [Ver documentação completa →](desafio5/README.md)**

---

## 🚀 Como Começar

1. **Clone o repositório:**
```bash
git clone https://github.com/giulms/Projeto-Docker.git
cd Projeto-Docker
```

2. **Escolha um desafio:**
   - [Desafio 1](desafio1/README.md) - Container Python Simples
   - [Desafio 2](desafio2/README.md) - Aplicação Web Flask
   - [Desafio 3](desafio3/README.md) - Sistema Multi-Container
   - [Desafio 4](desafio4/README.md) - Comunicação Entre Microserviços
   - [Desafio 5](desafio5/README.md) - API Gateway

3. **Siga a documentação de cada desafio** para instruções detalhadas

### 📋 Pré-requisitos

- **Docker Desktop** ([Windows](https://docs.docker.com/desktop/install/windows-install/) | [Mac](https://docs.docker.com/desktop/install/mac-install/) | [Linux](https://docs.docker.com/engine/install/))
- **Python 3.11+** (para testes locais) - [Download](https://www.python.org/downloads/)

---

## 📚 Recursos Adicionais

- [Documentação Oficial do Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Flask Documentation](https://flask.palletsprojects.com/)

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
