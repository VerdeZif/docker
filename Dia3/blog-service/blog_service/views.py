from django.http import JsonResponse
from django_redis import get_redis_connection
from django.db import connection

def healthz(request):
    try:
        connection.cursor()
        get_redis_connection("default").ping()
        return JsonResponse({"status": "ok"})
    except:
        return JsonResponse({"status": "error"}, status=500)
 