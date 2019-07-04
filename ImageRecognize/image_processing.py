import numpy as np
import queue
import cv2
import os


def get_list_files(path):
    ret = []
    for root, dirs, files in os.walk(path):
        for files_path in files:
            ret.append(os.path.join(root, files_path))
    return ret


def get_x_y_cuts(data, n_lines=1):
    w, h = data.shape
    visited = set()
    q = queue.Queue()
    offset = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    cuts = []
    for y in range(h):
        for x in range(w):
            x_axis = []
            y_axis = []
            if data[x][y] < 200 and (x, y) not in visited:
                q.put((x, y))
                visited.add((x, y))
            while not q.empty():
                x_p, y_p = q.get()
                for x_offset, y_offset in offset:
                    x_c, y_c = x_p + x_offset, y_p + y_offset
                    if (x_c, y_c) in visited:
                        continue
                    visited.add((x_c, y_c))
                    try:
                        if data[x_c][y_c] < 200:
                            q.put((x_c, y_c))
                            x_axis.append(x_c)
                            y_axis.append(y_c)
                    except Exception as e:
                        print(e)
                        pass
                    # if x_c >= 200 or y_c >= 200 or x_c < 0 or y_c < 0:
                    #     continue
                    # else:
                    #     # print(x_c, '-', y_c)
                    #     if data[x_c][y_c] < 200:
                    #         q.put((x_c, y_c))
                    #         x_axis.append(x_c)
                    #         y_axis.append(y_c)
            if x_axis:
                min_x, max_x = min(x_axis), max(x_axis)
                min_y, max_y = min(y_axis), max(y_axis)
                if max_x - min_x > 3 and max_y - min_y > 3:
                    cuts.append([min_x, max_x + 1, min_y, max_y + 1])
    if n_lines == 1:
        cuts = sorted(cuts, key=lambda cut_x: cut_x[2])
        # pr_item = cuts[0]
        # count = 1
        len_cuts = len(cuts)
        new_cuts = [cuts[0]]
        pr_k = 0
        for i in range(1, len_cuts):
            pr_item = new_cuts[pr_k]
            now_item = cuts[i]
            if not (now_item[2] > pr_item[3]):
                new_cuts[pr_k][0] = min(pr_item[0], now_item[0])
                new_cuts[pr_k][1] = max(pr_item[1], now_item[1])
                new_cuts[pr_k][2] = min(pr_item[2], now_item[2])
                new_cuts[pr_k][3] = max(pr_item[3], now_item[3])
            else:
                new_cuts.append(now_item)
                pr_k += 1
        cuts = new_cuts
        cuts_s = [cuts]
        return cuts_s

    # cuts = sorted(cuts, key=lambda cut_x: cut_x[2])
    # len_cuts = len(cuts)
    # new_cuts = [cuts[0]]
    # pr_k = 0
    # for i in range(1, len_cuts):
    #     pr_item = new_cuts[pr_k]
    #     now_item = cuts[i]
    #     if not (now_item[2] > pr_item[3]):
    #         new_cuts[pr_k][0] = min(pr_item[0], now_item[0])
    #         new_cuts[pr_k][1] = max(pr_item[1], now_item[1])
    #         new_cuts[pr_k][2] = min(pr_item[2], now_item[2])
    #         new_cuts[pr_k][3] = max(pr_item[3], now_item[3])
    #     else:
    #         new_cuts.append(now_item)
    #         pr_k += 1
    # cuts = new_cuts

    if n_lines == 2:
        cuts = sorted(cuts, key=lambda cut_y: cut_y[0])
        cuts_s = []
        cuts_start = 0
        for i in range(len(cuts) - 1):
            if i + 3 > len(cuts):
                cuts_end = len(cuts)
                tmp = cuts[cuts_start:cuts_end]
                tmp = sorted(tmp, key=lambda cut_x: cut_x[2])
                cuts_s.append(tmp)
            if abs(cuts[i][0] - cuts[i + 1][0]) > 20:
                cuts_end = i + 1
                tmp = cuts[cuts_start:cuts_end]
                tmp = sorted(tmp, key=lambda cut_x: cut_x[2])
                cuts_s.append(tmp)
                cuts_start = cuts_end
        return cuts_s


def get_image_cuts(image, img_cut_dir='./', is_data=False, n_lines=1, data_needed=False, count=0):
    if is_data:
        data = image
    else:
        data = cv2.imread(image, 2)
    cuts_s = get_x_y_cuts(data, n_lines=n_lines)
    image_cuts_s = []
    for cuts in cuts_s:
        image_cuts = None
        for i, item in enumerate(cuts):
            count += 1
            max_dim = max(item[1] - item[0], item[3] - item[2])
            new_data = np.ones((int(1.4 * max_dim), int(1.4 * max_dim))) * 255
            x_min, x_max = (max_dim - item[1] + item[0]) // 2, (max_dim - item[1] + item[0]) // 2 + item[1] - item[0]
            y_min, y_max = (max_dim - item[3] + item[2]) // 2, (max_dim - item[3] + item[2]) // 2 + item[3] - item[2]
            int_max_dim = int(0.2 * max_dim)
            x_pixel1 = int_max_dim + x_min
            x_pixel2 = int_max_dim + x_max
            y_pixel1 = int_max_dim + y_min
            y_pixel2 = int_max_dim + y_max
            new_data[x_pixel1:x_pixel2, y_pixel1:y_pixel2] = data[item[0]:item[1], item[2]:item[3]]
            # new_data[int(0.2 * max_dim) + x_min:int(0.2 * max_dim) + x_max, int(0.2 * max_dim) + y_min:int(0.2 * max_dim) + y_max] = data[item[0]:item[1], item[2]:item[3]]
            standard_data = cv2.resize(new_data, (28, 28))
            if not data_needed:
                cv2.imwrite(img_cut_dir + str(count) + ".jpg", standard_data)
                print('save successful')
            if data_needed:
                data_flat = (255 - np.resize(standard_data, (1, 28 * 28))) / 255
                if image_cuts is None:
                    image_cuts = data_flat
                else:
                    image_cuts = np.r_[image_cuts, data_flat]
        image_cuts_s.append(image_cuts)
    if data_needed:
        return image_cuts_s
    return count
