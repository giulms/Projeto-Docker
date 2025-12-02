# Desafio 1 - Container Python Simples 🐍

## 📖 Descrição da Solução

Este desafio implementa um container Docker básico que executa uma aplicação Python simples. A aplicação exibe mensagens de boas-vindas formatadas no terminal e então finaliza sua execução.

---

## 🏗️ Arquitetura e Decisões Técnicas

### Diagrama de Arquitetura

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

### Decisões Técnicas

| Decisão | Justificativa |
|---------|---------------|
| **Imagem `python:3.11-slim`** | Versão reduzida do Python, economiza ~700MB comparado à imagem completa |
| **Sem dependências externas** | Mantém o projeto simples e focado nos fundamentos do Docker |
| **Container efêmero** | Executa uma tarefa e finaliza, demonstrando o ciclo de vida básico |

---

## 🔍 Explicação Detalhada do Funcionamento

### Containers Envolvidos

- **1 container Python** executando `app.py`

### Rede

- **Não requer configuração de rede** (execução local isolada)

### Microserviços

- **Aplicação standalone** sem comunicação externa

### Fluxos de Dados

```
Usuário executa comando
        ↓
docker run desafio1-python
        ↓
Container inicia
        ↓
Python executa app.py
        ↓
Mensagens exibidas no terminal
        ↓
Container finaliza automaticamente
```

### Estrutura do Dockerfile

```dockerfile
FROM python:3.11-slim          # Imagem base leve
WORKDIR /app                    # Define diretório de trabalho
COPY requirements.txt .         # Copia arquivo de dependências
RUN pip install --no-cache-dir -r requirements.txt  # Instala dependências
COPY app.py .                   # Copia código da aplicação
CMD ["python", "app.py"]        # Comando para executar ao iniciar
```

---

## 🚀 Instruções de Execução

### Executar com Docker

```bash
# 1. Navegar até a pasta do desafio
cd desafio1

# 2. Construir a imagem Docker
docker build -t desafio1-python .

# 3. Executar o container
docker run desafio1-python
```

**Saída esperada:**
```
==================================================
Bem-vindo ao Desafio 1 - Docker com Python!
==================================================

📦 Esta aplicação está rodando em um container Docker
🐍 Desenvolvido com Python

Desafio concluído com sucesso! ✅
```

### Comandos Úteis

```bash
# Listar imagens criadas
docker images

# Listar containers (incluindo finalizados)
docker ps -a

# Remover a imagem
docker rmi desafio1-python

# Remover containers antigos
docker container prune
```

---

## 💡 Dicas e Boas Práticas

- ✅ Use imagens `slim` ou `alpine` quando possível
- ✅ Sempre especifique a versão da imagem base
- ✅ Agrupe comandos `RUN` para reduzir camadas
- ✅ Use `.dockerignore` para excluir arquivos desnecessários
- ✅ Teste localmente antes de containerizar

---

## 🆘 Problemas Comuns

### Erro: "docker: command not found"
**Solução:** Instale o Docker Desktop e verifique com `docker --version`

### Erro: "Cannot connect to the Docker daemon"
**Solução:** Certifique-se de que o Docker Desktop está rodando

### Erro: "Image build failed"
**Solução:** Verifique se o Dockerfile está na pasta correta e sem erros de sintaxe

---

## 📖 Documentação Adicional

- [Documentação Oficial do Docker](https://docs.docker.com/)
- [Python Docker Official Images](https://hub.docker.com/_/python)

---

<div align="center">

**[⬅️ Voltar ao Índice Principal](../README.md)** | **[Próximo Desafio ➡️](../desafio2/README.md)**

</div>
