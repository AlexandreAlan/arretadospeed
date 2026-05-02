# ⚡ Arretado Speed

**Teste de Velocidade de Internet** — open source, self-hosted, rodando 24h/dia.

> **"Arretado"** é uma expressão nordestina que significa algo incrível, forte, de respeito.  
> Este projeto foi feito com essa energia: simples, direto e funcional.

---

## 🌐 Demo ao vivo

**[arretadospeed.morenadoaco.com.br](https://arretadospeed.morenadoaco.com.br)**

> ⚠️ **Nota sobre latência:** O servidor está hospedado em uma VPS nos **Estados Unidos**.
> Por isso, o ping medido reflete a distância real entre você e o servidor americano — e não
> a latência da sua rede local ou com provedores brasileiros. Para usuários no Brasil, espere
> valores entre **150 ms e 250 ms**, o que é completamente normal nessa condição.
> Os resultados de **Download** e **Upload** continuam precisos.

---

## 📸 Visão Geral

- Mede **ping** (mín/méd/máx), **jitter**, **download** e **upload**
- 4 conexões paralelas para simular tráfego real
- Gauge animado em tempo real durante o teste
- Nota de qualidade de conexão (**A+** até **F**)
- Painel de **casos de uso** (4K, gaming, videochamada, etc.)
- **Histórico local** dos últimos 5 testes (localStorage)
- **ID único** por teste com opção de compartilhamento
- Interface 100% responsiva (mobile-first)
- SSL/TLS via Let's Encrypt + Nginx

---

## 🏗️ Arquitetura

```
Browser
  │
  ▼
Nginx (porta 443 — HTTPS / TLS 1.2+)
  ├── /           → Frontend estático (HTML/CSS/JS)
  └── /api/       → Proxy reverso ──► FastAPI (porta 8001)
                                          │
                                          ▼
                                    PostgreSQL (porta 5432)
```

---

## 🛠️ Stack

| Camada      | Tecnologia                        |
|-------------|-----------------------------------|
| Frontend    | HTML5 + CSS3 + JS puro (sem framework) |
| Backend     | Python 3.12 + FastAPI + Uvicorn   |
| Banco       | PostgreSQL 15                     |
| ORM         | SQLAlchemy 2 (async) + asyncpg    |
| Servidor    | Nginx (reverse proxy + static)    |
| Containers  | Docker + Docker Compose           |
| SSL         | Let's Encrypt + Certbot           |
| Infra       | VPS Linux (Ubuntu) — EUA          |

---

## 📁 Estrutura do Projeto

```
arretadospeed/
│
├── frontend/
│   └── index.html          # Interface completa (SPA single-file)
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # Endpoints FastAPI
│   │   ├── database.py     # Conexão async com PostgreSQL
│   │   ├── models.py       # Modelo SQLAlchemy (speed_tests)
│   │   └── schemas.py      # Schemas Pydantic (validação)
│   ├── Dockerfile
│   └── requirements.txt
│
├── nginx/
│   └── nginx.conf          # Config HTTPS + proxy reverso
│
├── sql/
│   └── init.sql            # Script de criação do banco e tabela
│
├── .env.example            # Variáveis de ambiente (modelo)
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha:

```bash
cp .env.example .env
```

| Variável   | Padrão          | Descrição                    |
|------------|-----------------|------------------------------|
| `DB_USER`  | `arretado`      | Usuário do PostgreSQL        |
| `DB_PASS`  | `arretado123`   | Senha do PostgreSQL          |
| `DB_NAME`  | `arretadospeed` | Nome do banco de dados       |
| `DB_PORT`  | `5432`          | Porta do PostgreSQL          |

> **Importante:** nunca suba o arquivo `.env` real para o repositório. Ele já está no `.gitignore`.

---

## 🚀 Instalação e Deploy

### Pré-requisitos

- Docker e Docker Compose instalados
- PostgreSQL rodando na máquina host (ou ajustar `docker-compose.yml` para usar container)
- Nginx instalado na máquina host
- Domínio apontando para o IP da VPS
- Certbot para gerar o certificado SSL

---

### 1. Clone o repositório

```bash
git clone https://github.com/AlexandreAlan/arretadospeed.git
cd arretadospeed
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
nano .env   # edite com seus valores
```

### 3. Crie o banco de dados

```bash
sudo -u postgres psql -f sql/init.sql
```

### 4. Suba o backend com Docker

```bash
docker compose up -d --build
```

Verifique se está rodando:

```bash
docker compose ps
curl http://localhost:8001/api/ping
```

### 5. Configure o Nginx

Copie (ou crie um symlink) a configuração:

```bash
sudo cp nginx/nginx.conf /etc/nginx/sites-available/arretadospeed
sudo ln -s /etc/nginx/sites-available/arretadospeed /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

Ajuste o `server_name` dentro de `nginx/nginx.conf` para o seu domínio.

### 6. Gere o certificado SSL (Let's Encrypt)

```bash
sudo certbot --nginx -d seudominio.com.br
```

### 7. Aponte o frontend

O Nginx serve o frontend diretamente como arquivo estático. Certifique-se de que o `root` no `nginx.conf` aponta para o diretório correto:

```nginx
root /var/www/arretadospeed;
```

---

## 🔌 API Endpoints

| Método | Rota                    | Descrição                                      |
|--------|-------------------------|------------------------------------------------|
| `GET`  | `/api/ping`             | Retorna timestamp — usado para medir latência  |
| `GET`  | `/api/download`         | Stream de 100 MB para medir download           |
| `POST` | `/api/upload`           | Recebe payload para medir upload               |
| `GET`  | `/api/new-test-id`      | Gera um UUID único para o teste                |
| `POST` | `/api/result`           | Salva resultado completo no banco              |
| `GET`  | `/api/result/{test_id}` | Busca resultado por ID                         |
| `GET`  | `/api/client-info`      | Retorna IP do cliente                          |

---

## 🗄️ Banco de Dados

**Tabela:** `speed_tests`

| Coluna          | Tipo          | Descrição                          |
|-----------------|---------------|------------------------------------|
| `test_id`       | VARCHAR(36) PK | UUID do teste                     |
| `ip_address`    | VARCHAR(45)   | IP do cliente                      |
| `isp`           | VARCHAR(255)  | Provedor de internet               |
| `city`          | VARCHAR(100)  | Cidade detectada                   |
| `country`       | VARCHAR(100)  | País detectado                     |
| `latency_min`   | FLOAT         | Ping mínimo (ms)                   |
| `latency_avg`   | FLOAT         | Ping médio (ms)                    |
| `latency_max`   | FLOAT         | Ping máximo (ms)                   |
| `jitter`        | FLOAT         | Jitter (ms)                        |
| `download_mbps` | FLOAT         | Velocidade de download (Mbps)      |
| `upload_mbps`   | FLOAT         | Velocidade de upload (Mbps)        |
| `user_agent`    | TEXT          | User-Agent do browser              |
| `created_at`    | TIMESTAMPTZ   | Data/hora do teste (UTC)           |

---

## 🔧 Desenvolvimento local

Para rodar sem Docker (backend):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Exporte as variáveis de ambiente
export DATABASE_URL="postgresql+asyncpg://arretado:arretado123@localhost:5432/arretadospeed"

uvicorn app.main:app --reload --port 8001
```

O frontend é estático — basta abrir `frontend/index.html` no browser ou servir com qualquer servidor HTTP simples:

```bash
cd frontend
python -m http.server 8080
```

---

## 🩺 Health Check

O `docker-compose.yml` configura um health check automático no backend a cada 30 segundos:

```bash
docker inspect arretadospeed_backend | grep -A 10 Health
```

---

## 🔒 Segurança

- HTTPS obrigatório com redirecionamento automático de HTTP → HTTPS
- TLS 1.2 e 1.3 apenas (protocolos antigos desativados)
- Headers de segurança: `HSTS`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`
- Acesso a arquivos ocultos bloqueado no Nginx
- `.env` nunca commitado no repositório

---

## 📜 Licença

Este projeto é open source sob a licença **MIT**.  
Sinta-se livre para usar, modificar e distribuir.

---

## 👨‍💻 Autor

Desenvolvido por **Alexandre Alan**

- GitHub: [@AlexandreAlan](https://github.com/AlexandreAlan)
- LinkedIn: [alexandre-alan](https://www.linkedin.com/in/alexandre-alan-a5a8362ab)
