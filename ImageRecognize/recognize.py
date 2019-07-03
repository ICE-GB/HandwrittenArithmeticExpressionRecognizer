from CNN_Model import cnn_model


def recognize(images):
    model = cnn_model.Model()  # 定义识别模型类
    model.load_model('./tools/model/model-200.meta', './tools/model/')  # 加载模型
    result = []
    for image in images:
        result.append(model.predict(image))
    value = ''
    for k in range(len(result)):
        for key in cnn_model.SYMBOL:
            if int(result[k][0]) == key:
                tmp = cnn_model.SYMBOL[key]
                value += str(tmp)
    print(value)
    try:
        cal_result = "= " + str(eval(value))
    except Exception:
        cal_result = '= ?'
    return cal_result
