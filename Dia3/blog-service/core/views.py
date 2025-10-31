from django.http import JsonResponse
from django_redis import get_redis_connection
from django.db import connection

def health_check(request):
    # Check DB
    try:
        connection.cursor()
        db_status = "ok"
    except:
        db_status = "error"

    # Check Redis
    try:
        redis_conn = get_redis_connection("default")
        redis_conn.ping()
        redis_status = "ok"
    except:
        redis_status = "error"

    return JsonResponse({
        "database": db_status,
        "redis": redis_status,
        "status": "ok" if db_status == "ok" and redis_status == "ok" else "error",
    })


