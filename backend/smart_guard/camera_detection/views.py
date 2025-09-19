from django.shortcuts import render, redirect, get_object_or_404
from .models import Capture
from .forms import ImageForm, VideoForm, BothForm


def capture_view(request):
    image_form = ImageForm(prefix="image")
    video_form = VideoForm(prefix="video")
    both_form = BothForm(prefix="both")

    if request.method == "POST":
        if 'image-submit' in request.POST:
            image_form = ImageForm(request.POST, request.FILES, prefix="image")
            if image_form.is_valid():
                image_form.save()
                return redirect('capture')
        elif 'video-submit' in request.POST:
            video_form = VideoForm(request.POST, request.FILES, prefix="video")
            if video_form.is_valid():
                video_form.save()
                return redirect('capture')
        elif 'both-submit' in request.POST:
            both_form = BothForm(request.POST, request.FILES, prefix="both")
            if both_form.is_valid():
                both_form.save()
                return redirect('capture')

    captures = Capture.objects.all().order_by('-captured_at')
    return render(request, "camera_detection/capture_page.html", {
        "image_form": image_form,
        "video_form": video_form,
        "both_form": both_form,
        "captures": captures,
    })


def capture_delete_view(request, capture_id):
    capture = get_object_or_404(Capture, id=capture_id)
    if request.method == "POST":
        capture.delete()
        return redirect('capture')
    return redirect('capture')


def delete_photo(request, capture_id):
    capture = get_object_or_404(Capture, id=capture_id)
    if request.method == "POST":
        capture.photo.delete(save=False)
        capture.photo = None
        capture.save()
        return redirect('capture')
    return redirect('capture')


def delete_video(request, capture_id):
    capture = get_object_or_404(Capture, id=capture_id)
    if request.method == "POST":
        capture.video.delete(save=False)
        capture.video = None
        capture.save()
        return redirect('capture')
    return redirect('capture')
