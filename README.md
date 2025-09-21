API Catálogos & Pedidos

API REST para catálogo de produtos e pedidos usando Django + DRF, JWT, PostgreSQL e drf-spectacular para documentação. Suporta execução com Docker Compose.

ℹ️ Alguns paths de endpoints abaixo são exemplos — confirme na sua documentação /api/docs e ajuste se necessário.

Badges (opcionais)










Demo

Coloque um GIF de uso rápido da API em docs/demo.gif e referencie aqui:

Dica para gerar: grave a tela (ex.: ScreenToGif no Windows), salve em docs/demo.gif e commit.

Sumário

Stack

Estrutura

Ambiente (.env)

Como rodar (local)

Como rodar (Docker)

Autenticação (JWT)

Documentação OpenAPI

Endpoints principais (exemplos)

Filtros/Busca/Ordenação

Deploy (produção)

Troubleshooting

Contribuição & Licença

Stack

Python / Django / Django REST Framework

PostgreSQL (psycopg)

JWT (djangorestframework-simplejwt)

drf-spectacular (OpenAPI)

django-filter (filtros)

corsheaders (CORS)

Docker Compose (opcional)

Estrutura
API_Catalogos/
├─ app/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ catalog/
├─ orders/
├─ manage.py
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
├─ .dockerignore
├─ .gitignore
└─ README.md

Ambiente (.env)

Crie .env na raiz:

# Django
DJANGO_SECRET_KEY=troque-para-uma-chave-segura
DJANGO_DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1

# Banco (local)
DB_NAME=api_catalogos
DB_USER=api_user
DB_PASSWORD=api_catalogo1463#
DB_HOST=localhost
DB_PORT=5432


No Docker, use DB_HOST=db (nome do serviço no compose).

Como rodar (local)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


API: http://127.0.0.1:8000

Admin: http://127.0.0.1:8000/admin

Como rodar (Docker)

Certifique-se que o Docker Desktop está aberto e rodando.

docker compose up --build
# em outro terminal:
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser


API: http://localhost:8000

Admin: http://localhost:8000/admin

DB: serviço db porta 5432

Para subir em background: docker compose up -d.
Para ver logs: docker compose logs -f web.

Autenticação (JWT)

Obter token: POST /api/token/

Refresh: POST /api/token/refresh/

curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"seu_usuario","password":"sua_senha"}'


Depois use:

Authorization: Bearer <access_token>

Documentação OpenAPI

Acesse a documentação interativa (Swagger):

/api/docs/ ou /api/schema/swagger-ui/

Esquema bruto: /api/schema/ (JSON/YAML)

Se não abrir, confira app/urls.py para as rotas do drf-spectacular.

Endpoints principais (exemplos)

Ajuste os paths conforme seu roteamento. Ex.: /api/products/, /api/categories/, /api/orders/.

Produtos

GET /api/products/ — lista

POST /api/products/ — cria (JWT)

GET /api/products/{id}/ — detalhe

PATCH/PUT /api/products/{id}/ — atualiza (JWT)

DELETE /api/products/{id}/ — remove (JWT)

Payload (POST/PUT):

{
  "name": "Teclado Mecânico",
  "description": "Switch azul, ABNT2",
  "price": 299.90,
  "sku": "KB-001",
  "stock": 42,
  "category": 1
}

Categorias

GET /api/categories/

POST /api/categories/ (JWT)

GET /api/categories/{id}/

PATCH/PUT /api/categories/{id}/

DELETE /api/categories/{id}/

Payload:

{ "name": "Periféricos" }

Pedidos

GET /api/orders/ — lista (JWT ou público conforme sua permissão)

POST /api/orders/ — cria pedido

GET /api/orders/{id}/

PATCH /api/orders/{id}/ — ex.: atualizar status

DELETE /api/orders/{id}/

Criar pedido (exemplo):

{
  "customer_name": "Ana Souza",
  "customer_email": "ana@email.com",
  "items": [
    { "product": 1, "quantity": 2 },
    { "product": 3, "quantity": 1 }
  ],
  "note": "Entregar no período da tarde"
}


Atualizar status:

curl -X PATCH http://localhost:8000/api/orders/10/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status":"PAID"}'

Filtros/Busca/Ordenação

Filtro por campo: ?category=1&price_min=100&price_max=500

Busca (se configurado): ?search=teclado

Ordenar: ?ordering=price ou ?ordering=-created_at

Paginação: ?page=2 (tamanho padrão PAGE_SIZE=10)

Os campos exatos dependem dos filtros definidos nas suas ViewSets. Confira em /api/docs/.

Deploy (produção)

Variáveis obrigatórias

DJANGO_DEBUG=0

DJANGO_SECRET_KEY bem forte (não comitar!)

ALLOWED_HOSTS=seu-dominio.com

Banco: DB_* apontando para o Postgres de produção

Coletar estáticos (se servir no mesmo container):

docker compose exec web python manage.py collectstatic --noinput


Servidor WSGI
Use gunicorn no container (ex.: gunicorn app.wsgi:application --bind 0.0.0.0:8000).
Se seu Dockerfile usa runserver em dev, considere uma CMD separada para prod.

CORS
Em prod, não use CORS_ALLOW_ALL_ORIGINS=True.
Defina:

CORS_ALLOWED_ORIGINS = ["https://seu-frontend.com"]

Troubleshooting

[Errno 11001] getaddrinfo failed
DB_HOST incorreto.

Local: DB_HOST=localhost

Docker: DB_HOST=db

Permissão negada no schema public
No Postgres:

GRANT ALL PRIVILEGES ON DATABASE api_catalogos TO api_user;
GRANT USAGE, CREATE ON SCHEMA public TO api_user;


Docker não conecta
Abra o Docker Desktop antes de docker compose up.

JWT 401
Gere token em /api/token/ e envie Authorization: Bearer <token>.

Contribuição & Licença

Issues e PRs são bem-vindos!

Não comite arquivos sensíveis (.env) ou gerados (__pycache__, .pyc, .idea etc.).

Defina uma licença (ex.: MIT) no arquivo LICENSE.
