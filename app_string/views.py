from django.shortcuts import render
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from django.http import HttpResponse
from app_string.models import VideoRequest
from django.utils import timezone
from pymongo import MongoClient



def my_video_view(request):
    # Set video parameters
    width, height = 100, 100
    duration = 3
    background_color = (200, 100, 0)
    text_color = (0, 200, 100)
    
    # Create a canvas with the specified parameters
    canvas = Image.new('RGB', (width, height), background_color)
    
    # Get the text from the GET request parameter
    text = request.GET.get('text', '') 
    text_width = font.getsize(text)[0]
    k = text_width + 5
    fps = len(text) * 3
    
    # Load the font
    fontpath = "././ARIAL.ttf"
    font = ImageFont.truetype(fontpath, 20)
    
    # Get data from the POST request parameters
    title = request.POST.get('title')
    description = request.POST.get('description')

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['datatest']
    collection = db['videodata']

    # Create and save an instance of the VideoRequest model
    video_request = VideoRequest(title=title, description=description)
    video_request.save()
    
    # Set the request time and text for the video
    video_request.request_time = timezone.now()
    video_request.text = text
    video_request.save()
    
    # Create a video writer object
    video = cv2.VideoWriter('running_line.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    # Generate each frame of the video
    for t in np.linspace(0, duration, int(duration * fps), endpoint=False):
        frame = np.copy(canvas)
        start_x = int(t * (-k) / duration) + 70
        start_y = int(height / 2) - 10
        frame = Image.fromarray(frame)
        draw = ImageDraw.Draw(frame)
        draw.text((start_x, start_y), text, font=font, fill=text_color)
        frame = np.array(frame)
        video.write(frame)

    video.release()
    # Create a document with the request data
    document = {
        'created_at': video_request.created_at,
        'request_time': video_request.created_at,
        'text': text
    }
    # Insert the document into the MongoDB collection
    collection.insert_one(document)

    # Read the generated video and return it in the HTTP response
    with open('running_line.mp4', 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=running_line.mp4'

    return response

