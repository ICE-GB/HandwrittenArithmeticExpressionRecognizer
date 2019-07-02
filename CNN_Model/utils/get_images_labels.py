import numpy as np
from tqdm import tqdm
import cv2
import os


def get_list_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for files_path in files:
            ret.append(os.path.join(root, files_path))
    return ret


def get_images_labels():
    operators = ['plus', 'sub', 'mul', 'div', '(', ')']
    images = None
    labels = None
    for i, op in enumerate(operators):
        image_file_list = get_list_files('./cfs/' + op + '/')
        print('Loading the ' + op + ' operator...')
        for filename in tqdm(image_file_list):
            image = cv2.imread(filename, 2)
            if image.shape != (28, 28):
                image = cv2.resize(image, (28, 28))
            image = np.resize(image, (1, 28 * 28))
            image = (255 - image) / 255
            label = np.zeros((1, 10 + len(operators)))
            label[0][10 + i] = 1
            if images is None:
                images = image
                labels = label
            else:
                images = np.r_[images, image]
                labels = np.r_[labels, label]
    return images, labels
