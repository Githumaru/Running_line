from django.shortcuts import render
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from django.http import HttpResponse
from app_string.models import VideoRequest
from django.utils import timezone
from pymongo import MongoClient



def my_video_view(request):
    width, height = 100, 100
    duration = 3
    background_color = (200, 100, 0)
    text_color = (0, 200, 100)

    canvas = Image.new('RGB', (width, height), background_color)

    text = request.GET.get('text', '')  # Получаем текст из GET-параметра запроса
    k = len(text) * 8
    fps = len(text) * 3

    fontpath = "././ARIAL.ttf"
    font = ImageFont.truetype(fontpath, 20)

    title = request.POST.get('title')
    description = request.POST.get('description')


    client = MongoClient('mongodb://localhost:27017/')

    db = client['datatest']

    collection = db['videodata']

    # Создание и сохранение экземпляра модели VideoRequest
    video_request = VideoRequest(title=title, description=description)
    video_request.save()

    video_request.request_time = timezone.now()
    video_request.text = text
    video_request.save()

    video = cv2.VideoWriter('running_line.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for t in np.linspace(0, duration, int(duration * fps), endpoint=False):
        frame = np.copy(canvas)
        start_x = int(t * (-k) / duration) + 20
        start_y = int(height / 2) - 10
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        draw.text((start_x, start_y), text, font=font, fill=text_color)
        frame = np.array(frame)
        video.write(frame)

    video.release()

    document = {
        'created_at': video_request.created_at,
        'request_time': video_request.created_at,
        'text': text
    }

    collection.insert_one(document)

    # Читаем сгенерированное видео и возвращаем его в HTTP-ответе
    with open('running_line.mp4', 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=running_line.mp4'

    return response

