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
  - `GET /api/catalog/products/` — lista produtos (com **filtros**, **busca**, **ordenação**)
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
- PostgreSQL 16+ (opcional para dev, mas recomendado)
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
```.env
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
```powershell
python manage.py migrate
python manage.py createsuperuser
```

---

### 5) Rodar servidor
```powershell
python manage.py runserver
```
API: http://localhost:8000/

Swagger: http://localhost:8000/api/schema/swagger/

Redoc: http://localhost:8000/api/schema/redoc/

Admin: http://localhost:8000/admin/

---

### 🐳 Como rodar com Docker

### 1) .env para Docker
```.env
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
🛟 Problemas comuns

[Errno 11001] getaddrinfo failed
DB_HOST incorreto.

Local: localhost

Docker: db

permission denied for schema public
Usuário sem permissão suficiente. Conceda no Postgres:
```sql
GRANT ALL PRIVILEGES ON DATABASE api_catalogos TO api_user;
GRANT ALL ON SCHEMA public TO api_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO api_user;
```
Senha com # no .env
Use aspas: DB_PASSWORD="minha#senha".

Docker não responde
Verifique:
```
docker compose ps
docker compose logs db
docker compose logs web
```

---

### 🤝 Contribuição

git checkout -b feature/minha-feature

git commit -m "feat: minha feature"

git push origin feature/minha-feature

Abra um Pull Request

---

## 📜 Licença

Este projeto está licenciado sob a **MIT License** — veja o arquivo [LICENSE](LICENSE) para detalhes.

MIT License

Copyright (c) 2025 Marcos Henrique

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
