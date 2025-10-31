# Blog Service - Backend

Microservicio independiente para posts y categorías usando Django + DRF + PostgreSQL + Redis + Docker.  

**Puerto:** `8000`

---

## 1️⃣ Requisitos

- Docker & Docker Compose  
- Python 3.11 (opcional para desarrollo local)

---

## 2️⃣ Instalación y levantamiento con Docker

1. Clonar el repositorio:

```bash
git clone <tu-repo>
cd blog-service
```

2. Crear archivo `.env` con tus credenciales:

```
DB_HOST=postgres
DB_NAME=main_db
DB_USER=devuser
DB_PASS=devpass
REDIS_HOST=redis
REDIS_PORT=6379
DEBUG=1
```

3. Levantar servicios:

```bash
docker-compose up --build
```

Esto levanta:

- `blog_service` (Django + DRF)  
- `postgres` (base de datos)  
- `redis` (caché)

---

## 3️⃣ Migraciones y semillas

1. Crear y aplicar migraciones:

```bash
docker exec -it blog_service python manage.py makemigrations
docker exec -it blog_service python manage.py migrate
```

2. Cargar datos de ejemplo:

```bash
docker exec -it blog_service python manage.py seed_blog
```

Datos cargados:

- 5 categorías  
- 3 autores  
- 30 posts variados (algunos draft)

---

## 4️⃣ Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET    | /api/categories/ | Lista categorías activas |
| GET    | /api/posts/      | Lista posts publicados con búsqueda y paginación (`?search=&page=`) |
| GET    | /api/posts/{id}/ | Detalle de post |
| GET    | /healthz/        | Verifica conexión a DB y Redis |

### Ejemplos cURL

```bash
# Listar categorías
curl http://localhost:8000/api/categories/

# Listar posts (con búsqueda)
curl http://localhost:8000/api/posts/?search=django&page=1

# Detalle post por id
curl http://localhost:8000/api/posts/1/

# Healthcheck
curl http://localhost:8000/healthz/
```

---

## 5️⃣ Caché

Redis almacena en caché los endpoints:

- `GET /api/categories/` → TTL 60-120 s  
- `GET /api/posts/{id}/` → TTL 60-120 s

---

## 6️⃣ Logging JSON básico

Cada solicitud genera un log en formato JSON:

```json
{
  "time": "2025-10-27 07:12:34",
  "level": "INFO",
  "method": "GET",
  "path": "/api/posts/",
  "status": 200
}
```

Ver logs en PowerShell:

```powershell
docker logs -f blog_service | Select-String '{"time":'
```

---

## 7️⃣ Paginación y búsqueda

- Paginación: 10 publicaciones por página  
- Búsqueda simple en `title` y `body` mediante parámetro de consulta `?search=...`

---

## 8️⃣ Estructura del proyecto

```
blog-service/
  blog_service/      # Proyecto Django
  categories/        # App categorías
  authors/           # App autores
  posts/             # App posts
  core/              # Utilidades (cache, pagination)
  Dockerfile
  requirements.txt
  manage.py
  openapi.yaml       # Contrato mínimo
```

---

## 9️⃣ Contrato OpenAPI mínimo (openapi.yaml)

- `/api/categories/` → `[{"id", "name"}]`  
- `/api/posts/` → `results: [{"id","title","excerpt","author":{"id","display_name"},"category":{"id","name"},"published_at"}]`  
- `/api/posts/{id}/` → `{"id","title","body","author":{...},"category":{...},"published_at","views"}`

```
# Listo para pegar y compartir con Frontend
```