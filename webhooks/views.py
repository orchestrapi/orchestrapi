
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def manage_webhook(request, project_id):
    return JsonResponse({}, status=200)