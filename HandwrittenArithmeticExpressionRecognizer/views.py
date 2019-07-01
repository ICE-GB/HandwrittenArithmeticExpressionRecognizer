from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def upload(request):
    return render(request, 'upload.html')


def hand_write(request):
    return render(request, 'hand_write.html')
