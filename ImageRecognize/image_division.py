import cv2
import numpy as np
from matplotlib import pyplot as plt

from ImageRecognize import recognize


def image_cut(point, thresh):
    x_sorted = sorted(point, key=lambda tup: tup[0])
    img_cuts = []
    temp = -10000  # 为识别除号设定的临时变量
    # *******************裁剪************************
    for j in range(len(x_sorted)):
        if j == temp or j == temp + 1 or j == temp + 2:
            pass
        else:
            if j + 2 >= len(x_sorted):
                img_predict = thresh[x_sorted[j][1]:x_sorted[j][1] + x_sorted[j][3]
                , x_sorted[j][0]: x_sorted[j][0] + x_sorted[j][2]]
            else:
                if abs(x_sorted[j + 1][0] - x_sorted[j + 2][0]) < 50:
                    if x_sorted[j + 1][1] > x_sorted[j + 2][1]:
                        img_predict = thresh[x_sorted[j + 2][1]:x_sorted[j + 1][1] + x_sorted[j + 1][3],
                                      x_sorted[j][0]: x_sorted[j][0] + x_sorted[j][2]]
                    else:
                        img_predict = thresh[x_sorted[j + 1][1]: x_sorted[j + 2][1] + x_sorted[j + 2][3],
                                      x_sorted[j][0]:x_sorted[j][0] + x_sorted[j][2]]
                    temp = j
                else:
                    if j == temp or j == temp + 1 or j == temp + 2:
                        pass
                    else:
                        img_predict = thresh[x_sorted[j][1]:x_sorted[j][1] + x_sorted[j][3]
                        , x_sorted[j][0]: x_sorted[j][0] + x_sorted[j][2]]
                        temp = -10000
            # plt.imshow(img_predict, 'gray')
            #             # plt.show()
            top, bottom, left, right = 0, 0, 0, 0
            height, width = img_predict.shape
            k = height - width
            if k < 0:
                top = abs(k) // 2
                bottom = abs(k) - top
            else:
                left = k // 2
                right = k - left
            tmp = cv2.copyMakeBorder(img_predict, top, bottom, left, right,
                                     cv2.BORDER_CONSTANT, value=(0, 0, 0))
            # *******************   变为28*28  ************************
            tmp = cv2.resize(tmp, (28, 28))
            tmp = np.reshape(tmp, (1, 784))
            img_cuts.append(tmp)
    return img_cuts


def image_process(path):
    im = cv2.imread(path)

    blur = cv2.GaussianBlur(im, (9, 9), 0)  # 高斯过滤，去除噪声点

    GrayImage = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)  # 变为灰度图像

    ret, thresh2 = cv2.threshold(GrayImage, 130, 255, cv2.THRESH_BINARY_INV)  # 图像二值化

    # image, contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)  # 寻找轮廓
    contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)  # 寻找轮廓



    points = []  # 记录每个轮廓左上角顶点

    row_number = 0  # 记录每行字符的个数
    result = []  # 识别结果

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])  # 将每个轮廓用矩形框框出来
        points.append((x, y, w, h))  # 将矩形框左上角顶点加入points
        row_number += 1  # 当前行的字符数量+1
        try:
            x_next, y_next, w_next, h_next = cv2.boundingRect(contours[i + 1])  # 获取下一个轮廓矩形框的左上角顶点坐标
            if abs(y - y_next) > h:  # 判断下一个字符与当前字符是否在同一行
                if len(points) == 1:
                    points = []
                    pass
                else:
                    cuts = image_cut(points, thresh2)

                    cal_result = recognize.recognize(cuts)
                    row_number = 0
                    points = []
                    im = cv2.putText(im, cal_result, (x + w, y + h),
                                     cv2.FONT_HERSHEY_SIMPLEX, 12, (255, 0, 0), 3)
        except IndexError:
            cuts = image_cut(points, thresh2)
            cal_result = recognize.recognize(cuts)
            row_number = 0
            points = []
            im = cv2.putText(im, cal_result, (x + w, y + h),
                             cv2.FONT_HERSHEY_SIMPLEX, 12, (255, 0, 0), 3)

    plt.imshow(thresh2, 'gray')
    plt.show()


if __name__ == '__main__':
    image_process('./001.png')
