from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests

# Create your views here.

def homepage(request):
    return render(request, 'main/homepage.html')

def get_started(request):
    if request.method == 'POST':
        image = request.FILES.get('product_image')
        title = request.POST.get('product_title')
        description = request.POST.get('description')
        files = {'image': (image.name, image, image.content_type)} if image else None
        data = {'product_title': title, 'description': description}
        response = requests.post('https://beatrice-ai.app.n8n.cloud/webhook-test/d47e5a40-6395-4fd7-aada-a1ab8f1dec73', files=files, data=data)
        gdrive_url = None
        raw_response = response.text
        try:
            result_json = response.json()
            if isinstance(result_json, dict):
                gdrive_url = result_json.get('gdrive')
            elif isinstance(result_json, list) and len(result_json) > 0:
                gdrive_url = result_json[0].get('gdrive')
        except Exception:
            gdrive_url = None
        return render(request, 'main/get_started.html', {'gdrive_url': gdrive_url, 'raw_response': raw_response, 'submitted': True})
    return render(request, 'main/get_started.html', {'submitted': False})
