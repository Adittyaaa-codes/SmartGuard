from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# our user is military person so we will store their rank and unit
class User(models.Model):
    RANK_CHOICES = [
        ('PVT', 'Private'),
        ('CPL', 'Corporal'),
        ('SGT', 'Sergeant'),
        ('LT', 'Lieutenant'),
        ('CPT', 'Captain'),
        ('MAJ', 'Major'),
        ('COL', 'Colonel'),
        ('GEN', 'General'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    rank = models.CharField(max_length=3, choices=RANK_CHOICES)
    unit = models.CharField(max_length=100)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Check if the provided password is correct."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.rank} {self.first_name} {self.last_name} ({self.username})"
