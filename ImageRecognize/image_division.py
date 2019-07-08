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
                if abs(x_sorted[j + 1][0] - x_sorted[j + 2][0]) < 20:
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

            tmp = cv2.copyMakeBorder(tmp, 30, 30, 30, 30,
                                     cv2.BORDER_CONSTANT, value=(0, 0, 0))
            plt.imshow(tmp, 'gray')
            plt.show()
            # *******************   变为28*28  ************************
            tmp = cv2.resize(tmp, (28, 28))
            tmp = np.reshape(tmp, 784)
            # print(tmp.shape)
            img_cuts.append(tmp.tolist())
    return img_cuts


def extract_row(points, block_w, block_h):
    row_y = points[0][1]
    row_points_s = []
    for i in range(len(points)):
        if points[i][1] - row_y > block_h:
            row_points_s.append(points[0:i])
            row_points_s.extend(extract_row(points[i:], block_w, block_h))
            return row_points_s
    row_points_s.append(points[0:])
    return row_points_s


def extract_div(points, block_w, block_h):
    p_len = len(points) - 2
    print(p_len)
    for i in range(p_len):
        if i == p_len - 1:
            return points
        # elif abs(points[i][0] - points[i + 1][0]) < block_w * 1 / 2 and abs(
        #         points[i + 1][0] - points[i + 2][0]) < block_w * 1 / 3:
        elif points[i][3] < block_h * 1 / 3 and points[i + 1][3] < block_h * 1 / 3 and points[i + 2][
            3] < block_h * 1 / 3:
            tmp = points[0:i]
            div_x = points[i][0]
            div_y = min(points[i + 1][1], points[i + 2][1])
            div_w = points[i][2]
            div_h = abs(points[i + 1][1] - points[i + 2][1]) + max(points[i + 1][3], points[i + 2][3])
            div_point = [div_x, div_y, div_w, div_h]
            tmp.append(div_point)
            tmp.extend(points[i + 3:])
            points = tmp
            print(i, "提取除号", points)
            points = extract_div(points, block_w, block_h)
            return points


def img_cut_padding(img_cut):
    top, bottom, left, right = 0, 0, 0, 0
    height, width = img_cut.shape
    k = height - width
    if k < 0:
        top = abs(k) // 2
        bottom = abs(k) - top
    else:
        left = k // 2
        right = k - left
    tmp = cv2.copyMakeBorder(img_cut, top, bottom, left, right,
                             cv2.BORDER_CONSTANT, value=(0, 0, 0))

    tmp = cv2.copyMakeBorder(tmp, 30, 30, 30, 30,
                             cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # plt.imshow(tmp, 'gray')
    # plt.show()
    pass


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
    cuts = []

    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])  # 将每个轮廓用矩形框框出来
        points.append([x, y, w, h])  # 将矩形框左上角顶点加入points

    print("cv识别", points)
    block_h = sorted(points, key=lambda p_x: p_x[3], reverse=True)[0][3]
    block_w = sorted(points, key=lambda p_x: p_x[2], reverse=True)[0][2]
    print("块高", block_h)
    print("块宽", block_w)
    points = sorted(points, key=lambda p_x: p_x[0])
    print("x排序", points)
    points = sorted(points, key=lambda p_x: p_x[1])
    print("y排序", points)
    row_points_s = extract_row(points, block_w, block_h)
    print("分行points", row_points_s)
    finally_points = []
    for row_points in row_points_s:
        row_points = sorted(row_points, key=lambda p_x: p_x[0])
        row_points = extract_div(row_points, block_w, block_h)
        # print("每一行points:", row_points)
        finally_points.append(row_points)
    print("最终points", finally_points)
    try:
        for row_points in finally_points:
            img_cut = image_cut(row_points, thresh2)
            cuts.append(img_cut)
            print(len(img_cut), img_cut)
            for point in row_points:
                cv2.rectangle(im, (point[0], point[1]), (point[0] + point[2], point[1] + point[3]), (255, 0, 0), 3)
    except TypeError:
        print("结束！！！！")
    plt.imshow(im)
    plt.show()

    # for i in range(len(contours)):
    #     x, y, w, h = cv2.boundingRect(contours[i])  # 将每个轮廓用矩形框框出来
    #     points.append((x, y, w, h))  # 将矩形框左上角顶点加入points
    #     row_number += 1  # 当前行的字符数量+1
    #     try:
    #         x_next, y_next, w_next, h_next = cv2.boundingRect(contours[i + 1])  # 获取下一个轮廓矩形框的左上角顶点坐标
    #         if abs(y - y_next) > block_h:  # 判断下一个字符与当前字符是否在同一行
    #             print("换行")
    #             if len(points) == 1:
    #                 points = []
    #             else:
    #                 cuts.append(image_cut(points, thresh2))

    # cal_result = recognize.recognize(cuts)
    # row_number = 0
    # points = []
    # im = cv2.putText(im, cal_result, (x + w, y + h),
    #                  cv2.FONT_HERSHEY_SIMPLEX, 12, (255, 0, 0), 3)
    # except IndexError:
    #     cuts.append(image_cut(points, thresh2))
    # cal_result = recognize.recognize(cuts)
    # row_number = 0
    # points = []
    # im = cv2.putText(im, cal_result, (x + w, y + h),
    #                  cv2.FONT_HERSHEY_SIMPLEX, 12, (255, 0, 0), 3)
    # plt.imshow(thresh2, 'gray')
    # plt.show()
    print(len(cuts), cuts)
    return cuts


if __name__ == '__main__':
    image_process('./test3.jpg')
