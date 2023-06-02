from django.urls import path
from .views import my_video_view

urlpatterns = [
    path('running_line/', my_video_view, name='running_line'),
]
