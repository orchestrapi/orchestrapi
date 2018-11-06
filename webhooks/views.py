
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_webhook


@csrf_exempt
def manage_webhook(request, app_id):
    message = json.loads(request.body)
    process_webhook.delay(message, app_id)
    return JsonResponse({}, status=200)
