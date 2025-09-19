from django.db import models

# Create your models here.
from django.db import models

class Capture(models.Model):
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    captured_at = models.DateTimeField(auto_now_add=True)
    weapon_name = models.CharField(max_length=100, default='None', blank=True)
    weapon_number = models.PositiveIntegerField(default=0, blank=True)


    def __str__(self):
        return f"Capture at {self.captured_at}"


