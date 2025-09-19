from django.db import models

# Create your models here.
from django.db import models

class Capture(models.Model):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Capture at {self.captured_at}"


