from django.db import models

# Create your models here.
from django.db import models

class Capture(models.Model):
    photo = models.ImageField(upload_to='photos/')
    video = models.FileField(upload_to='videos/')  # Accepts various file types (mp4, avi, etc.)
    captured_at = models.DateTimeField(auto_now_add=True)  # Stores date and time of capture

    def __str__(self):
        return f"Capture at {self.captured_at}"
