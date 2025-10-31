import time
import logging
import json

logger = logging.getLogger("blog_service.requests")  # Logger específico para requests JSON

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = round(time.time() - start_time, 3)

        log_data = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "INFO",
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration": duration
        }

        logger.info(json.dumps(log_data))  # Se registra solo en este logger
        return response
