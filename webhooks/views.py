
from django.http import JsonResponse

def manage_webhook(request, project_id):
    return JsonResponse({}, status=200)