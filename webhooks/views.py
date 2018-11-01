
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_webhook


@csrf_exempt
def manage_webhook(request, project_id):
    message = json.loads(request.body)
    process_webhook.delay(message, project_id)
    return JsonResponse({}, status=200)
