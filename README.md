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
