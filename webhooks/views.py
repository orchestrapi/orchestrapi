
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_webhook_task


@csrf_exempt
def manage_bitbucket_webhook(request, app_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message':'Method not allowed'}, status=405)
    message = json.loads(request.body)
    process_webhook_task.delay('bitbucket', message, app_id)
    return JsonResponse({}, status=200)

@csrf_exempt
def manage_github_webhook(request, app_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message':'Method not allowed'}, status=405)
    message = json.loads(request.body)
    process_webhook_task.delay('github', message, app_id)
    return JsonResponse({}, status=200)
