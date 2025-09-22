# API de Catálogos (Django + DRF)

API para gestão de **catálogo de produtos** e **pedidos**, com **autenticação JWT**, **filtros/busca**, **paginação**, documentação **OpenAPI/Swagger** e suporte a **Docker**.

---

## 🧩 Funcionalidades

- Autenticação via **JWT (SimpleJWT)**
- Catálogo: **produtos** e **categorias**
- Pedidos: criação e listagem
- Filtros, busca e ordenação (**DRF + django-filter**)
- Paginação padrão (PageNumberPagination)
- Documentação com **drf-spectacular** (Swagger/Redoc)
- **PostgreSQL** (ou SQLite para dev, se quiser adaptar)
- CORS habilitado em dev
- Configuração por **`.env`**
- **Dockerfile** + **docker-compose** prontos

### Modelos (exemplo)
> Ajuste conforme seu código atual.
- **Categoria**: `name`, `slug`, `created_at`, `updated_at`
- **Produto**: `name`, `sku`, `price`, `category`, `stock`, `is_active`, `created_at`, `updated_at`
- **Pedido**: `customer_name`, `customer_email`, `items`, `total`, `status`, `created_at`

---

## 🚀 Rotas Principais

> Prefixos podem variar conforme seu `urls.py`. Abaixo um exemplo usual:

- **Catálogo**
  - `GET /api/catalog/products/` — lista produtos (**filtros**, **busca**, **ordenação**)
    - Busca: `?search=texto`
    - Filtros (ex.): `?category=slug-da-categoria&is_active=true`
    - Ordenação: `?ordering=price` ou `?ordering=-price`
  - `POST /api/catalog/products/` — cria produto (auth necessária)
  - `GET /api/catalog/products/<id>/` — detalha produto
  - `PATCH/PUT/DELETE /api/catalog/products/<id>/` — atualiza/remove (auth)
  - `GET /api/catalog/categories/` — lista categorias
  - `POST /api/catalog/categories/` — cria categoria (auth)

- **Pedidos**
  - `GET /api/orders/` — lista pedidos (auth recomendada)
  - `POST /api/orders/` — cria pedido

- **Auth (JWT)**
  - `POST /api/auth/token/` — obter **access** e **refresh**
  - `POST /api/auth/token/refresh/` — renovar **access**

- **Docs (OpenAPI)**
  - `GET /api/schema/` — OpenAPI JSON
  - `GET /api/schema/swagger/` — Swagger UI
  - `GET /api/schema/redoc/` — Redoc

---

## 🧰 Stack

- **Backend:** Django 5.x + Django REST Framework
- **Banco:** PostgreSQL (recomendado em prod)
- **Auth:** SimpleJWT
- **Docs:** drf-spectacular (Swagger/Redoc)
- **CORS:** django-cors-headers
- **.env:** python-dotenv
- **Container:** Docker + Docker Compose

---

## ⚙️ Como rodar localmente (sem Docker)

### 1) Pré-requisitos
- Python 3.12+
- PostgreSQL 16+ (opcional em dev, recomendado)
- Git

### 2) Clonar e criar venv
```powershell
# Substitua pela URL do SEU repositório
git clone <URL-do-seu-repo>
cd API_Catalogos

python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

---

### 3) Criar .env

Crie um arquivo .env na raiz do projeto:
```
# Django
DJANGO_SECRET_KEY=troque-esta-chave
DJANGO_DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco (Local)
DB_NAME=api_catalogos
DB_USER=api_user
DB_PASSWORD="sua#senha#forte"
DB_HOST=localhost
DB_PORT=5432
```

Dica: se a senha tiver #, ;, ! etc., mantenha em aspas.

---

### 4) Migrações e usuário admin
```
python manage.py migrate
python manage.py createsuperuser
```

---

### 5) Rodar servidor
```
python manage.py runserver
```

API: http://localhost:8000/

Swagger: http://localhost:8000/api/schema/swagger/

Redoc: http://localhost:8000/api/schema/redoc/

Admin: http://localhost:8000/admin/

---

### 🐳 Como rodar com Docker

---

### 1) .env para Docker
```
DJANGO_SECRET_KEY=troque-esta-chave
DJANGO_DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=api_catalogos
DB_USER=api_user
DB_PASSWORD="sua#senha#forte"
DB_HOST=db
DB_PORT=5432
```

No Docker, DB_HOST = db (nome do serviço no docker-compose.yml).

---

### 2) Subir os serviços
```
docker compose up --build
```

---

### 3) Migrações e admin (dentro do container)
```
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

API: http://localhost:8000/

Swagger: http://localhost:8000/api/schema/swagger/

---

### 📚 API — Fluxo de uso (exemplos)

---

### 1) Obter token (JWT)
```
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"seu_usuario","password":"sua_senha"}'
```

Resposta esperada:
```
{"access":"<jwt_access>","refresh":"<jwt_refresh>"}
```

Guarde o access e use nos próximos requests:
```
AUTH="Authorization: Bearer <jwt_access>"
```

---

### 2) Criar uma categoria
```
curl -X POST http://localhost:8000/api/catalog/categories/ \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"name":"Eletrônicos","slug":"eletronicos"}'
```

---

### 3) Criar um produto
```
curl -X POST http://localhost:8000/api/catalog/products/ \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{
    "name":"Fone Bluetooth",
    "sku":"FONE-BT-001",
    "price":"199.90",
    "category": 1,
    "stock": 50,
    "is_active": true
  }'
```

---

### 4) Listar produtos (com busca/filtro/ordenação)
```
# Busca por nome
curl -H "$AUTH" "http://localhost:8000/api/catalog/products/?search=fone"

# Filtro por categoria (ex.: slug)
curl -H "$AUTH" "http://localhost:8000/api/catalog/products/?category=eletronicos"

# Ordenar por preço desc
curl -H "$AUTH" "http://localhost:8000/api/catalog/products/?ordering=-price"
```

---

### 5) Criar um pedido
```
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{
    "customer_name": "João Silva",
    "customer_email": "joao@email.com",
    "items": [{"product": 1, "quantity": 2}],
    "total": "399.80",
    "status": "NEW"
  }'
```

---

### 🧪 Testes
```
# Local
python manage.py test

# Docker
docker compose exec web python manage.py test
```

---

### 🗂️ Estrutura do projeto (resumo)
```
API_Catalogos/
├─ app/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ catalog/
│  ├─ models.py
│  ├─ views.py
│  ├─ serializers.py
│  └─ urls.py
├─ orders/
│  ├─ models.py
│  ├─ views.py
│  ├─ serializers.py
│  └─ urls.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .dockerignore
├─ .gitignore
└─ .env  # (não versionado)
```

---

### 🛟 Problemas comuns

[Errno 11001] getaddrinfo failed
DB_HOST incorreto.

Local: localhost

Docker: db

permission denied for schema public

Usuário sem permissão suficiente. No Postgres:
```
GRANT ALL PRIVILEGES ON DATABASE api_catalogos TO api_user;
GRANT ALL ON SCHEMA public TO api_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO api_user;
```

Senha com # no .env
Use aspas: DB_PASSWORD="minha#senha".

---

### Docker não responde
Verifique:
```
docker compose ps
docker compose logs db
docker compose logs web
```

---

### 🤝 Contribuição
```
git checkout -b feature/minha-feature
git commit -m "feat: minha feature"
git push origin feature/minha-feature
# Abra um Pull Request
```

---

### 📜 Licença

Este projeto está licenciado sob a MIT License — veja o arquivo LICENSE
 para detalhes.

### O que você ainda precisa ajustar
- Trocar `<URL-do-seu-repo>` pela URL real do seu GitHub.
- (Opcional) Criar um arquivo `LICENSE` na raiz e colocar o texto da MIT lá (como você já colou no final da sua versão).  
- Garante que `.env` **não** está versionado (`.gitignore` deve conter `.env`).

Se quiser, eu já te mando os comandos de `git add/commit/push` pra subir essa versão.
