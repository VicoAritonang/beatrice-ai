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
        response = requests.post('https://portofolio-vico.app.n8n.cloud/webhook-test/587a1e56-5058-4c13-9120-ee036aa8cf0b', files=files, data=data)
        photo_url = None
        video_msg = None
        raw_response = response.text
        try:
            result_json = response.json()
            if isinstance(result_json, dict):
                photo_url = result_json.get('photo')
                video_msg = result_json.get('video')
            elif isinstance(result_json, list) and len(result_json) > 0:
                photo_url = result_json[0].get('photo')
                video_msg = result_json[0].get('video')
        except Exception:
            photo_url = None
            video_msg = None
        return render(request, 'main/get_started.html', {'photo_url': photo_url, 'video_msg': video_msg, 'raw_response': raw_response, 'submitted': True})
    return render(request, 'main/get_started.html', {'submitted': False})
