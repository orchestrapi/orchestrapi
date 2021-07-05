
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from apps.models import App

from .tasks import process_webhook_task


@csrf_exempt
def manage_repository_webhook(request, repository, app_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    app = App.objects.filter(id=app_id).exists()
    if not app:
        return JsonResponse({"status": "Not found", "message": "App not found."}, status=404)
    message = json.loads(request.body)
    if not message:
        return JsonResponse({
            "status": "Invalid format", "message": "Invalid json format for webhook."}, status=400)

    if repository in ['bitbucket', 'github']:
        process_webhook_task.delay(repository, message, app_id)
    elif repository == 'gitlab':
        process_webhook_task.delay(
            repository, message, app_id,
            headers={
                'HTTP_X_GITLAB_EVENT': request.META.get('HTTP_X_GITLAB_EVENT', None)
            }
        )
    elif repository == 'docker':
        raise NotImplementedError("Docker repository not implemented yet!")
    else:
        return JsonResponse({"status": 'error', 'message': 'Unknown repository'}, status=400)
    return JsonResponse({}, status=200)
