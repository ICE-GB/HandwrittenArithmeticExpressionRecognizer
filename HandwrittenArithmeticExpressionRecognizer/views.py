from django.shortcuts import render


def index(request):
    return render(request, 'HandwrittenArithmeticExpressionRecognizer/index.html')


def upload(request):
    return render(request, 'HandwrittenArithmeticExpressionRecognizer/upload.html')


def hand_write(request):
    return render(request, 'HandwrittenArithmeticExpressionRecognizer/hand_write.html')
