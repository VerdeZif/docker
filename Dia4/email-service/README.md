# Email / Notifications Service (Versión Extendida)

Microservicio independiente para gestión de notificaciones y envío de correos. Recibe mensajes desde otros microservicios (Blog/Auth) y los procesa de forma **asincrónica** con Celery y Redis.

**Puerto por defecto:** `8002`

---

## 🧩 Tecnologías

* Python 3.11
* Django 5.0
* Django REST Framework 3.15
* PostgreSQL
* Redis
* Celery 5.4
* Docker + Docker Compose

---

## 📦 Estructura del proyecto

```
email-service/
 ├── app/                  # Proyecto Django
 │    ├── settings.py
 │    └── ...
 ├── notifications/
 │    ├── models.py        # ContactMessage, NotificationLog
 │    ├── serializers.py
 │    ├── views.py         # ContactViewSet, NotifyViewSet
 │    └── tasks.py         # Tareas Celery
 ├── Dockerfile
 ├── docker-compose.yml
 ├── requirements.txt
 ├── .env
 ├── manage.py
 └── openapi.yaml
```

---

## ⚙️ Configuración de entorno

Crea un archivo `.env` en la raíz del proyecto:

```dotenv
# Django
DJANGO_SECRET_KEY=changeme

# Base de datos PostgreSQL
DB_HOST=email_db
DB_PORT=5432
DB_NAME=emaildb
DB_USER=user
DB_PASSWORD=password

# Redis
REDIS_URL=redis://redis:6379/0

# SMTP (opcional para envío real)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu-correo@gmail.com
SMTP_PASSWORD=TU_APP_PASSWORD
FROM_EMAIL=tu-correo@gmail.com
```

> Para Gmail, genera un **App Password** desde tu cuenta con 2FA activada.

---

## 🐳 Docker & Docker Compose

### Levantar los contenedores

```bash
docker-compose up --build
```

Servicios:

| Servicio      | Puerto | Función                         |
| ------------- | ------ | ------------------------------- |
| email-service | 8002   | Servidor Django                 |
| email_db      | 5435   | Base de datos PostgreSQL        |
| redis         | 6379   | Broker para Celery              |
| email_worker  | —      | Worker Celery procesando tareas |

### Migraciones y superuser

```bash
docker-compose exec email-service python manage.py migrate
docker-compose exec email-service python manage.py createsuperuser
```

---

## 🏗️ Endpoints

### 1️⃣ `/api/contact/` — Crear contacto

**POST**:

```json
{
  "name": "Carlos Rivas",
  "email": "carlos@mail.com",
  "message": "Me interesa una colaboración"
}
```

**Respuesta:**

```json
{
  "status": "queued"
}
```

* Valida campos requeridos
* Guarda `ContactMessage` en DB
* Envía correo **asimilado en Celery**

### 2️⃣ `/api/notify/` — Notificación interna

**POST**:

```json
{
  "to": "user@mail.com",
  "subject": "Nuevo post publicado",
  "body": "Se ha publicado un nuevo artículo"
}
```

**Respuesta:**

```json
{
  "status": "queued"
}
```

* Guarda `NotificationLog` en DB
* Encola envío de correo a Celery
* Idempotente si se reenvía con mismo UUID

### 3️⃣ `/healthz/` — Healthcheck

```json
{
  "db": true,
  "redis": true
}
```

* Comprueba conexión con DB y Redis

---

## ⚡ Celery

### Levantar worker

```bash
docker-compose exec email-service celery -A app.celery worker --loglevel=info
```

* Las tareas se encolan con `.delay()`
* Reintentos automáticos: 3 intentos, 5 segundos de espera

### Tarea `send_email_task` (ejemplo)

```python
@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, body, to):
    try:
        send_mail(subject, body, "noreply@email-service.com", [to], fail_silently=False)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)
```

---

## 💻 Pruebas con cURL / PowerShell

### Crear contacto

```bash
curl -X POST http://localhost:8002/api/contact/ \
-H "Content-Type: application/json" \
-d '{"name":"Carlos","email":"c@mail.com","message":"Hola"}'
```

### Enviar notificación

```powershell
Invoke-RestMethod -Uri http://localhost:8002/api/notify/ -Method POST -ContentType "application/json" -Body '{
  "to": "correo-que-recibe@gmail.com",
  "subject": "Prueba Celery",
  "body": "Este es un correo enviado desde la cola."
}'
```

### Healthcheck

```bash
curl http://localhost:8002/healthz/
```

---

## 📝 Logs y Observabilidad

* Celery imprime logs de cada tarea: `received`, `succeeded`, `retry`, `failure`
* Se recomienda revisar logs para **debug y seguimiento**
* Campos estructurados: `event`, `subject`, `to`, `timestamp`

---

## 📊 Diagrama conceptual de flujo

```text
+-------------+        POST         +---------------+        .delay()        +-----------+
| Blog/Auth   | ----------------->  | Email-Service | --------------------> | Celery    |
| (emisores)  |                     | /api/notify/  |                      | Worker    |
+-------------+                     +---------------+                      +-----------+
         |                                |
         | POST /api/contact/             | save to DB
         |------------------------------> |
                                          v
                                     ContactMessage
```

* Blog/Auth → `/api/notify/` → Email-Service → Celery Worker → envio de correo
* `/api/contact/` → guarda mensaje → encola tarea de envío

---

## ✅ Notas finales

* Puerto recomendado: `8002`
* Redis se usa como **broker de tareas**
* Idempotencia basada en `UUID` para mensajes repetidos
* Reintentos automáticos para errores de envío
* Correo real requiere SMTP configurado en `.env`
* Logs en consola permiten seguimiento y depura
