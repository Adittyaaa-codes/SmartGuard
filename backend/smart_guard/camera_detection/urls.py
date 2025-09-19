from django.urls import path
from . import views

urlpatterns = [
    path('', views.capture_view, name='capture'),
    path('delete_capture/<int:capture_id>/', views.capture_delete_view, name='capture_delete'),
    path('delete_photo/<int:capture_id>/', views.delete_photo, name='delete_photo'),
    path('delete_video/<int:capture_id>/', views.delete_video, name='delete_video'),
]


