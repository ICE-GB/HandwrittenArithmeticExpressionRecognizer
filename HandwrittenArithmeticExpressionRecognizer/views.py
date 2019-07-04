import base64
import json

import cv2
from django.contrib.staticfiles import finders
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from CNN_Model.cnn_model import Model
from CNN_Model.utils.mnist_op_dataset import SYMBOL
from ImageRecognize.image_division import image_process
from ImageRecognize.image_processing import get_image_cuts


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
    # images_s = image_process(img_path)
    data = cv2.imread('./target.png', 2)
    images_s = get_image_cuts(data, is_data=True, n_lines=1, data_needed=True)
    meta = finders.find('HandwrittenArithmeticExpressionRecognizer/model/model-200.meta')
    path = finders.find('HandwrittenArithmeticExpressionRecognizer/model/')
    cnn_model = Model()
    cnn_model.load_model(meta, path)
    equations = []
    results = []
    haer = ''
    for images in images_s:
        equation = ''
        result = ''
        digits = list(cnn_model.predict(images))
        # print(digits)
        for d in digits:
            equation += SYMBOL[d]
        # print(equation)
        try:
            result += str(eval(equation))
        except Exception as e:
            # print(e)
            result += '?    --' + str(e)
        equations.append([equation])
        results.append([result])
        haer += equation + '=' + result + '\n'
    print(equations)
    print(results)
    # print(haer)
    json_data = {
        "result": results,
        "expression": equations,
        "test": 'test'
    }
    return JsonResponse(json_data, safe=False)
