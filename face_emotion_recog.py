#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
从视频中识别人脸，并实时标出面部特征点
"""

import dlib
import numpy as np
import cv2


class Face_emotion():
    """docstring for Face_emotion"""
    def __init__(self):
        # 使用特征提取器get_frontal_face_detector
        self.detector = dlib.get_frontal_face_detector()
        # dlib的68点模型，使用训练好的特征预测器
        self.predictor = dlib.shape_predictor("./dlib_landmarks/shape_predictor_68_face_landmarks.dat")

        # 创建cv2摄像头对象
        self.cap = cv2.VideoCapture(0)
        # 设置视频参数
        self.cap.set(3, 480)
        # 截取screenshoot的计数器
        self.cnt = 0


    def learning_face(self):
        """"""
        # 眉毛直线拟合数据缓冲
        line_brow_x = []
        line_brow_y = []

        # 判断摄像头初始化是否成功
        while (self.cap.isOpened()):
            flag, im_rd = self.cap.read()

            # 每帧数据延时1s
            k = cv2.waitKey(1)

            # 转化灰度图
            img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

            # 使用人脸检测器检测每一帧中含有的人脸，并返回人脸数rects
            faces = self.detector(img_gray, 0)

            # 显示在屏幕上的字体
            font = cv2.FONT_HERSHEY_SIMPLEX

            # 如果检测到人脸
            if len(faces) != 0:
                # 对每个人的脸部标出68个特征点
                for i in range(len(faces)):
                    for k, d in enumerate(faces):
                        # 用红色框标出人脸
                        cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 0, 255))
                        # 计算人脸边框的长
                        self.face_width = d.right() - d.left()

                        # 使用预测器得到68点数据的坐标
                        shape = self.predictor(im_rd, d)

                        # 显示出每一个特征点
                        for i in range(68):
                            cv2.circle(im_rd, (shape.part(i).x, shape.part(i).y), 1, (0, 255, 0), -1, 8)
                            cv2.putText(im_rd, str(i), (shape.part(i).x, shape.part(i).y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

                        # 分析任意n点的位置关系来作为表情识别的依据
                        mouth_width = (shape.part(54).x - shape.part(48).x) / self.face_width
                        mouth_hight = (shape.part(66).y - shape.part(62).y) / self.face_width

                        # 通过两个眉毛上的10个特征点，分析挑眉程度和皱眉程度
                        brow_sum = 0   # 高度之和
                        frown_sum = 0   # 两边眉毛距离之和
                        for j in range(17, 21):
                            brow_sum += (shape.part(j).y - d.top()) + (shape.part(j + 5).y - d.top())
                            frown_sum += shape.part(j+5).x - shape.part(j).x
                            line_brow_x.append(shape.part(j).x)
                            line_brow_y.append(shape.part(j).y)

                        # self.brow_k, self.brow_d = self.fit_slr(line_brow_x, line_brow_y)  # 计算眉毛的倾斜程度
                        tempx = np.array(line_brow_x)
                        tempy = np.array(line_brow_y)
                        z1 = np.polyfit(tempx, tempy, 1)  # 拟合成一次直线
                        self.brow_k = -1 * round(z1[0], 3)


                        brow_hight = (brow_sum / 10) / self.face_width  # 眉毛高度占比
                        brow_width = (frown_sum / 5) / self.face_width  # 眉毛距离占比


                        # 眼睛挣开程度
                        eye_sum = (shape.part(41).y - shape.part(37).y + shape.part(40).y - shape.part(38).y + 
                                    shape.part(47).y - shape.part(43).y + shape.part(46).y - shape.part(44).y)
                        eye_hight = (eye_sum / 4) / self.face_width


                        # 分情况讨论，张嘴可能是开心或是惊讶
                        if round(mouth_hight >= 0.03):
                            if eye_hight >= 0.056:
                                cv2.putText(im_rd, "Amazing", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, 4)
                            else:
                                cv2.putText(im_rd, "Happy", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, 4)


                        # 没有张嘴可能是生气或正常
                        else:
                            if self.brow_k <= -0.3:
                                cv2.putText(im_rd, "Angry", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, 4)
                            else:
                                cv2.putText(im_rd, "Nature", (d.left(), d.bottom() + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, 4)

                # 标出人脸数
                cv2.putText(im_rd, "Faces: "+str(len(faces)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
            else:
                # 没有检测到人脸
                cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

            # 添加说明
            im_rd = cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
            im_rd = cv2.putText(im_rd, "Q: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

            # 按下 s 键保存截图
            if (k == ord('s')):
                self.cnt += 1
                cv2.imwrite("screenshoot"+str(self.cnt)+'.jpg', im_rd)

            # 按下 q 键退出
            if (k == ord('q')):
                break

            cv2.imshow("Camera", im_rd)


        # 释放摄像头
        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    my_face = Face_emotion()
    my_face.learning_face()



        
