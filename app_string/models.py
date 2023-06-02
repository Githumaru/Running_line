from django.db import models
from django.utils import timezone

class VideoRequest(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    request_time = models.DateTimeField(default=timezone.now)  # Поле для хранения времени запроса
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'app_string'

