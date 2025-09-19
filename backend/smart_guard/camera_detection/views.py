from django.shortcuts import render, redirect
from .models import Capture
from .forms import CaptureForm  # We'll need a ModelForm for uploads

def capture_upload_view(request):
    if request.method == "POST":
        form = CaptureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('capture_list')
    else:
        form = CaptureForm()
    return render(request, "camera_detection/capture_upload.html", {"form": form})

def capture_list_view(request):
    captures = Capture.objects.all().order_by('-captured_at')
    return render(request, "camera_detection/capture_list.html", {"captures": captures})
