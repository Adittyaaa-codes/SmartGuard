from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.capture_upload_view, name='capture_upload'),
    path('captures/', views.capture_list_view, name='capture_list'),
]
