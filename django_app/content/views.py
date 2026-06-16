from django.http import JsonResponse
from django.db import connection


def healthz(request):
    try:
        connection.ensure_connection()
        return JsonResponse({"status": "ok", "postgres": "ok"}, status=200)
    except Exception:
        return JsonResponse({"status": "error", "postgres": "down"}, status=503)
