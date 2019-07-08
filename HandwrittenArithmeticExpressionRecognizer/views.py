import base64

import cv2
from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from CNN_Model.cnn_model import Model
from CNN_Model.utils.mnist_op_dataset import SYMBOL
from ImageRecognize.image_division import image_process


def index(request):
    return render(request, 'HandwrittenArithmeticExpressionRecognizer/index.html')


def upload(request):
    return render(request, 'HandwrittenArithmeticExpressionRecognizer/upload.html')


def hand_write(request):
    return render(request, 'HandwrittenArithmeticExpressionRecognizer/hand_write.html')


@csrf_exempt
def get_result(request):
    img_str = request.POST["img_data"]
    img = base64.b64decode(img_str)
    img_path = "./target.png"
    with open(img_path, "wb") as f:
        f.write(img)
    images_s = image_process(img_path)
    meta = finders.find('HandwrittenArithmeticExpressionRecognizer/model/model-200.meta')
    path = finders.find('HandwrittenArithmeticExpressionRecognizer/model/')
    cnn_model = Model()
    cnn_model.load_model(meta, path)
    equations = []
    results = []
    for images in images_s:
        equation = ''
        result = ''
        digits = list(cnn_model.predict(images))
        for d in digits:
            equation += SYMBOL[d]
        try:
            result += str(eval(equation))
        except Exception as e:
            # result += '?    --' + str(e)
            print(e)
            result += '?'
        equations.append([equation])
        results.append([result])
    print(equations)
    print(results)
    json_data = {
        "result": results,
        "expression": equations,
    }
    return JsonResponse(json_data, safe=False)
