
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tasks import process_webhook_task
from apps.models import App


@csrf_exempt
def manage_repository_webhook(request, repository, app_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    app = App.objects.filter(id=app_id).exists()
    if not app:
        return JsonResponse({"status": "Not found", "message": "App not found."}, status=404)
    message = json.loads(request.body)
    if repository == 'bitbucket':
        process_webhook_task.delay('bitbucket', message, app_id)
    elif repository == 'github':
        process_webhook_task.delay('github', message, app_id)
    else:
        return JsonResponse({"status": 'error', 'message': 'Unknown repository'}, status=400)
    return JsonResponse({}, status=200)
