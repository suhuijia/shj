# coding=UTF-8
__author__ = 'shj'

import sys
import os
import numpy as np
import cv2
import cv2.aruco as aruco

pad = 100
aruco_size = 50

A4_PPI = 200
A4_MM_TO_INCH = 25.4
A4_PIX_H = int(297 / A4_MM_TO_INCH * A4_PPI)
A4_PIX_W = int(210 / A4_MM_TO_INCH * A4_PPI)
A4_ROWS = 50
A4_COLS = 25
ROW_HEIGHT_PIX = int(A4_PIX_H / A4_ROWS)
COL_WIDTH_PIX = int(A4_PIX_W / A4_COLS)


def parse_xml(xml_path):
    """parse xml information"""
    import xml.dom.minidom
    if not os.path.exists(xml_path):
        return None, None, None, None, None

    DomTree = xml.dom.minidom.parse(xml_path)
    annotation = DomTree.documentElement
    filenamelist = annotation.getElementsByTagName('filename')  # [<DOM Element: filename at 0x381f788>]
    filename = filenamelist[0].childNodes[0].data
    objectlist = annotation.getElementsByTagName('object')
    size = annotation.getElementsByTagName('size')
    for ele in size:
        width = ele.getElementsByTagName('width')
        width = int(width[0].childNodes[0].data)
        height = ele.getElementsByTagName('height')
        height = int(height[0].childNodes[0].data)

    list_boxes = []
    list_type = []
    list_answer = []

    for objects in objectlist:
        namelist = objects.getElementsByTagName('name')
        objectname = namelist[0].childNodes[0].data
        question_type = objectname.split(' ')[0]
        answer_content = objectname.split(' ')[-1]
        list_type.append(question_type)
        list_answer.append(answer_content)

        bndbox = objects.getElementsByTagName('bndbox')
        for box in bndbox:
            x1_list = box.getElementsByTagName('xmin')
            x1 = int(x1_list[0].childNodes[0].data)
            y1_list = box.getElementsByTagName('ymin')
            y1 = int(y1_list[0].childNodes[0].data)
            x2_list = box.getElementsByTagName('xmax')
            x2 = int(x2_list[0].childNodes[0].data)
            y2_list = box.getElementsByTagName('ymax')
            y2 = int(y2_list[0].childNodes[0].data)
            list_boxes.append([x1, y1, x2, y2])

    print(list_boxes)
    print(list_type)
    print(list_answer)

    return list_boxes, list_type, list_answer, width, height


def create_aruco():
    """create four arucos on A4"""
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()

    img = np.ones((A4_PIX_H, A4_PIX_W, 3), dtype=np.uint8) * 255
    img_h, img_w, channel = img.shape
    for i in range(4):
        aruco_marker = aruco.drawMarker(aruco_dict, i, aruco_size)
        aruco_marker = cv2.cvtColor(aruco_marker, cv2.COLOR_GRAY2BGR)
        if i == 0:
            img[pad:pad+aruco_size, pad:pad+aruco_size] = aruco_marker
        elif i == 1:
            img[pad:pad+aruco_size, img_w-pad-aruco_size:img_w-pad] = aruco_marker
        elif i == 2:
            img[img_h-pad-aruco_size:img_h-pad, img_w-pad-aruco_size:img_w-pad] = aruco_marker
        else:
            img[img_h-pad-aruco_size:img_h-pad, pad:pad+aruco_size] = aruco_marker

    cv2.imwrite('../result.jpg', img)
    corners, ids, rejectedImgs = aruco.detectMarkers(img, aruco_dict, parameters=parameters)
    print(corners)
    print(ids)

    grayscale = aruco.drawDetectedMarkers(img, corners, ids, (0, 0, 255))
    cv2.imshow('frame', grayscale)
    cv2.imwrite("../detect_result.jpg", grayscale)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img


def get_gt_aruco_corners(gt_img_path):
    """get four point that is target corners"""
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    image = cv2.imread(gt_img_path)
    corners, ids, rejectedImgs = aruco.detectMarkers(image, aruco_dict, parameters=parameters)
    target_corners = [None, None, None, None]
    for i, id in enumerate(ids):
        target_corners[id[0]] = corners[i]

    for i in range(4):
        target_corners[i] = target_corners[i][0][i]

    return target_corners


def detect_aruco(gt_img_path, gt_xml_path, test_img_path):
    """detect four arucos and parse answer areas location"""

    list_boxes, list_type, list_answer, width, height = parse_xml(gt_xml_path)
    gt_img = cv2.imread(gt_img_path)
    height, width, channel = gt_img.shape

    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    image = cv2.imread(test_img_path)
    img_h, img_w, channel = image.shape
    corners, ids, rejectedImgs = aruco.detectMarkers(image, aruco_dict, parameters=parameters)
    print(corners)
    print(ids)
    if ids is None or 0 == len(ids):
        print("Don't detect aruco.")
        return False

    four_corners = [None, None, None, None]
    for i, id in enumerate(ids):
        four_corners[id[0]] = corners[i]

    print(four_corners)
    for ele in four_corners:
        if ele is None:
            print("Don't detect four aruco.")
            return False

    for i in range(4):
        four_corners[i] = four_corners[i][0][i]

    for c in four_corners:
        cv2.drawMarker(image, (int(c[0]), int(c[1])), (0, 0, 255))

    # target_corners = np.float32([[58, 58],[901, 58],[901, 1299],[58, 1299]])
    target_corners = get_gt_aruco_corners(gt_img_path)

    trans_Matrix = cv2.getPerspectiveTransform(np.float32(four_corners), np.float32(target_corners))
    print("trans_Matrix: ", trans_Matrix)

    image = cv2.warpPerspective(image, trans_Matrix, (width, height))
    for i, box in enumerate(list_boxes):
        cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 1)
        cv2.imwrite("../pic/{}.jpg".format(str(i)), image[box[1]:box[3], box[0]:box[2]])
    reverse_trans_Matrix = cv2.getPerspectiveTransform(np.float32(target_corners), np.float32(four_corners))
    print("rev_trans_Matrix: ", reverse_trans_Matrix)
    image = cv2.warpPerspective(image, reverse_trans_Matrix, (img_w, img_h), borderValue=255)


    cv2.imshow("show", image)
    cv2.imwrite("../compare.jpg", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image

if __name__ == '__main__':

    gt_xml_path = "../qr5.xml"
    gt_img_path = "../qr5.jpg"
    test_img_path = "../test_qr5.jpg"
    # create_aruco()
    # detect_aruco(gt_img_path, gt_xml_path, test_img_path)
    parse_xml(gt_xml_path)
