from CNN_Model import cnn_model

from CNN_Model.utils.mnist_op_dataset import SYMBOL

meta = '../HandwrittenArithmeticExpressionRecognizer/static/' \
       'HandwrittenArithmeticExpressionRecognizer/model/model-200.meta'
path = '../HandwrittenArithmeticExpressionRecognizer/static/' \
       'HandwrittenArithmeticExpressionRecognizer/model/'


def recognize(images):
    model = cnn_model.Model()  # 定义识别模型类
    # model.load_model('./tools/model/model-200.meta', './tools/model/')  # 加载模型
    model.load_model(meta, path)  # 加载模型
    result = []
    for image in images:
        result.append(model.predict(image))
    value = ''
    for k in range(len(result)):
        for key in SYMBOL:
            if int(result[k][0]) == key:
                tmp = SYMBOL[key]
                value += str(tmp)
    print(value)
    try:
        cal_result = "= " + str(eval(value))
    except Exception as e:
        cal_result = '= ?' + str(e)
    return cal_result
