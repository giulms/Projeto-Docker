# Desafio 2 - Aplicação Web Flask 🌐

## 📖 Descrição da Solução

Este desafio implementa um servidor web Flask containerizado que serve uma interface visual moderna e uma API REST para consulta de status. A aplicação demonstra como expor serviços web através de containers Docker.

---

## 🏗️ Arquitetura e Decisões Técnicas

### Diagrama de Arquitetura

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

### Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| **Flask** | Framework minimalista, perfeito para demonstrar conceitos básicos de web |
| **Porta 5000** | Porta padrão do Flask, facilita desenvolvimento |
| **.dockerignore** | Evita copiar arquivos desnecessários, otimiza build |
| **HTML/CSS inline** | Simplifica deployment, sem necessidade de arquivos estáticos |
| **Debug mode** | Facilita desenvolvimento com hot reload |

---

## 🔍 Explicação Detalhada do Funcionamento

### Containers Envolvidos

- **1 container Flask** na porta 5000

### Rede

- **Bridge network** (padrão do Docker)
- **Port mapping:** `Host:5000 → Container:5000`

### Microserviços

- **Serviço web standalone** sem dependências externas

### Fluxos de Dados

```
Cliente HTTP
    ↓
localhost:5000
    ↓
Docker Bridge Network
    ↓
Container Flask (porta 5000)
    ↓
Flask processa requisição
    ↓
Resposta HTML ou JSON
    ↓
Docker Bridge Network
    ↓
Cliente HTTP recebe resposta
```

### Endpoints Disponíveis

| Método | Rota | Descrição | Resposta |
|--------|------|-----------|----------|
| GET | `/` | Página principal | HTML estilizado |
| GET | `/api/status` | Status do servidor | JSON com informações |

#### Exemplo de Resposta da API

```json
{
  "status": "online",
  "message": "Servidor Docker está funcionando!",
  "timestamp": "2025-12-02T10:30:00",
  "container": "desafio2-python-flask",
  "framework": "Flask",
  "language": "Python"
}
```

### Estrutura do Dockerfile

```dockerfile
FROM python:3.11-slim          # Imagem base leve
WORKDIR /app                    # Define diretório de trabalho
COPY requirements.txt .         # Copia dependências primeiro (cache)
RUN pip install --no-cache-dir -r requirements.txt  # Instala Flask
COPY . .                        # Copia resto dos arquivos
EXPOSE 5000                     # Documenta porta usada
CMD ["python", "app.py"]        # Inicia servidor Flask
```

---

## 🚀 Instruções de Execução

### Executar com Docker

```bash
# 1. Navegar até a pasta do desafio
cd desafio2

# 2. Construir a imagem Docker
docker build -t desafio2-flask .

# 3. Executar o container (foreground)
docker run -p 5000:5000 desafio2-flask

# 3b. OU executar em background
docker run -d -p 5000:5000 --name flask-server desafio2-flask
```

### Gerenciamento do Container

```bash
# Ver logs em tempo real
docker logs -f flask-server

# Parar o container
docker stop flask-server

# Iniciar novamente
docker start flask-server

# Remover o container
docker rm flask-server

# Executar comandos dentro do container
docker exec -it flask-server bash
```

---

## 🧪 Testando a Aplicação

### Via Navegador

1. **Página Principal:**
   - Acesse: http://localhost:5000
   - Você verá uma interface moderna com gradiente roxo

2. **API de Status:**
   - Acesse: http://localhost:5000/api/status
   - Retorna JSON com informações do servidor

### Via cURL (Terminal)

```bash
# Testar página principal
curl http://localhost:5000

# Testar API de status (JSON)
curl http://localhost:5000/api/status

# Testar com formatação JSON bonita
curl http://localhost:5000/api/status | python -m json.tool
```

### Via PowerShell

```powershell
# Testar página principal
Invoke-WebRequest -Uri http://localhost:5000

# Testar API (formato JSON)
(Invoke-WebRequest -Uri http://localhost:5000/api/status).Content | ConvertFrom-Json
```

### Script de Teste Automatizado

```bash
# O script testa todos os endpoints automaticamente
python testar.py
```

---

## 📚 Conceitos Aprendidos

### 1. Port Mapping

```bash
-p <porta_host>:<porta_container>
-p 5000:5000
```

- **Porta Host (5000):** Porta no seu computador
- **Porta Container (5000):** Porta dentro do container
- Permite acessar serviços do container de fora

### 2. Modo Detached

```bash
docker run -d ...
```

- Container roda em background
- Terminal fica livre para outros comandos
- Use `docker logs` para ver saída

### 3. Nomeação de Containers

```bash
docker run --name meu-container ...
```

- Facilita gerenciamento
- Referência containers por nome ao invés de ID
- Necessário para comandos como `docker stop`

### 4. .dockerignore

Similar ao `.gitignore`, evita copiar para a imagem:
- `__pycache__/` - Cache do Python
- `*.pyc` - Bytecode compilado
- `venv/` - Ambientes virtuais
- `.env` - Variáveis sensíveis

### 5. Logs de Container

```bash
docker logs <container>        # Ver logs
docker logs -f <container>     # Seguir logs em tempo real
docker logs --tail 100 <container>  # Últimas 100 linhas
```

### 6. EXPOSE no Dockerfile

```dockerfile
EXPOSE 5000
```

- Documenta qual porta o container usa
- Não publica a porta automaticamente
- Use `-p` no `docker run` para publicar

---

## 🎯 Comparação: Local vs Docker

| Aspecto | Local | Docker |
|---------|-------|--------|
| **Ambiente** | Depende do Python instalado | Ambiente isolado e reproduzível |
| **Dependências** | Conflitos possíveis | Isoladas no container |
| **Portabilidade** | Requer setup manual | Funciona em qualquer máquina com Docker |
| **Limpeza** | Arquivos ficam no sistema | Remover container limpa tudo |

---

## 💡 Dicas e Boas Práticas

### Build Otimizado

```dockerfile
# ✅ BOM: Copia requirements.txt primeiro
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ RUIM: Copia tudo junto
COPY . .
RUN pip install -r requirements.txt
```

**Por quê?** Docker usa cache de camadas. Se apenas o código mudar, não reinstala dependências.

### Uso de .dockerignore

```
# Exemplo de .dockerignore
__pycache__/
*.pyc
venv/
.env
*.log
.git/
```

### Health Checks

Adicione ao Dockerfile:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:5000/api/status || exit 1
```

---

## 🆘 Problemas Comuns

### Erro: "Port is already allocated"

**Causa:** Porta 5000 já está em uso

**Solução:**
```powershell
# Windows: Ver processo usando a porta
Get-NetTCPConnection -LocalPort 5000

# Parar o processo
Stop-Process -Id <PID>

# Ou usar outra porta
docker run -p 5001:5000 desafio2-flask
```

### Erro: "ModuleNotFoundError: No module named 'flask'"

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

### Container inicia mas não responde

**Causa:** Flask rodando em 127.0.0.1 (localhost interno)

**Solução:** Flask deve escutar em `0.0.0.0`:
```python
app.run(host='0.0.0.0', port=5000)
```

---

## 🎯 Próximos Passos

Após completar este desafio, você está pronto para:

1. **[Desafio 3](../desafio3/README.md)** - Sistemas multi-container com Docker Compose
2. Experimentar com:
   - Variáveis de ambiente (`-e`)
   - Volumes para persistência (`-v`)
   - Múltiplas instâncias do mesmo serviço

---

## 📖 Documentação Adicional

- [Documentação do Flask](https://flask.palletsprojects.com/)
- [Docker Networking](https://docs.docker.com/network/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

<div align="center">

**[⬅️ Desafio Anterior](../desafio1/README.md)** | **[Voltar ao Índice](../README.md)** | **[Próximo Desafio ➡️](../desafio3/README.md)**

</div>
