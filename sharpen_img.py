# -*- coding: utf-8 -*-
# @Time : 2022/11/22  10:13 上午
import os
import numpy as np
import cv2
import kornia


def sharpen_image_high(srcimg, iter_num=1):
    """ 图像高锐化 """
    blurimg = cv2.GaussianBlur(srcimg, (7, 7), 25)
    outimg = cv2.addWeighted(srcimg, 1.5, blurimg, -0.5, gamma=0)
    for i in range(1, iter_num):
        blurimg = cv2.GaussianBlur(outimg, (0, 0), 25)
        outimg = cv2.addWeighted(outimg, 1.2, blurimg, -0.2, gamma=0)

    return outimg


def sharpen_image_median(srcimg, iter_num=1, w1=1.3):
    """ 图像正常锐化 """
    w2 = 1.0 - w1
    blurimg = cv2.GaussianBlur(srcimg, (5, 5), 25)
    outimg = cv2.addWeighted(srcimg, w1, blurimg, w2, gamma=0)
    for i in range(1, iter_num):
        blurimg = cv2.GaussianBlur(outimg, (0, 0), 25)
        outimg = cv2.addWeighted(outimg, w1-0.1*i, blurimg, w2+0.1*i, gamma=0)

    return outimg



class SharpenImg(object):
    """docstring for SharpenImg"""
    def __init__(self):
        super(SharpenImg, self).__init__()

    @staticmethod
    def Change(image, flag=0, num=2):
        """ 寻找kernel为[2*num+1, 2*num+1]区域的最值 """
        image_res = cv2.resize(image, (2000, 1000))
        image_res = cv2.copyMakeBorder(image_res, num, num, num, num, cv2.BORDER_REFLECT)
        h, w = image_res.shape
        iChange = np.zeros_like(image_res)
        for i in range(num, h - num):
            for j in range(num, w - num):
                kernel_arr = image_res[i - num:i + num + 1, j - num:j + num + 1]
                if flag == 0:
                    k = np.max(kernel_arr)
                else:
                    k = np.min(kernel_arr)
                iChange[i - num, j - num] = k

        out = cv2.resize(iChange, (image.shape[1], image.shape[0]))
        return out

    @staticmethod
    def unsharp_mask(srcimg):
        img = cv2.cvtColor(srcimg, cv2.COLOR_BGR2RGB)
        data = kornia.utils.image_to_tensor(img, keepdim=False)
        data = data.float() / 255.
        sharpen = kornia.filters.UnsharpMask((7, 7), (2.5, 2.5))
        sharpen_tensor = sharpen(data)
        difference = (sharpen_tensor - data).abs()
        # sharpen_image = kornia.utils.tensor_to_image(sharpen_tensor)
        difference_image = kornia.utils.tensor_to_image(difference)
        # sharpen_image = (sharpen_image * 255.0).astype(np.uint8)
        # sharpen_image = cv2.cvtColor(sharpen_image, cv2.COLOR_RGB2BGR)
        difference_image = (difference_image * 255.0).astype(np.uint8)
        difference_image = cv2.cvtColor(difference_image, cv2.COLOR_RGB2BGR)
        # cv2.imwrite("sharpen.jpg", sharpen_image)
        # cv2.imwrite("difference.jpg", difference_image)
        return difference_image

    def merge_image(self, srcimg, sharpenimg, diffimg):
        """ 融合原始图与锐化图的边缘过亮 """
        diffimg = np.expand_dims(diffimg, axis=2)
        diffimg = np.repeat(diffimg, 3, axis=2)
        mergeimg = sharpenimg * ((255 - diffimg) / 255.0) + srcimg * (diffimg / 255.0)
        mergeimg = np.clip(mergeimg, a_min=0, a_max=255)
        mergeimg = mergeimg.astype(np.uint8)
        return mergeimg

    def process(self, srcimg):
        """ 图像锐化处理 """
        ## 高锐化
        highSharpImg = sharpen_image_high(srcimg=srcimg, iter_num=3)
        diffimg = self.unsharp_mask(srcimg=srcimg)
        diffimg = cv2.cvtColor(diffimg, cv2.COLOR_BGR2GRAY)
        diffimg = self.Change(diffimg, flag=0)
        # diffimgblur = cv2.medianBlur(diffimg, 5)
        ## 融合结果
        diffimg = np.clip(diffimg*3.0, 0, 255).astype(np.uint8)
        mergeImg = self.merge_image(srcimg=srcimg, sharpenimg=highSharpImg, diffimg=diffimg)
        return mergeImg, highSharpImg



if __name__ == '__main__':

    imagedir = "/Users/a58/workspace/HDR/part5/noize_test2"
    savedir = "/Users/a58/workspace/HDR/part5/noize_test2"
    os.makedirs(savedir, exist_ok=True)

    Sharpen = SharpenImg()
    for file in sorted(os.listdir(imagedir)):
        if file.startswith('.'): continue
        file_path = os.path.join(imagedir, file)
        if os.path.isdir(file_path): continue
        if "JPG" not in file: continue
        print(file_path)
        image = cv2.imread(file_path)

        mergeImg, highSharpImg = Sharpen.process(srcimg=image)

        save_file = os.path.join(savedir, file)
        cv2.imwrite(save_file[:-4] + "_s2_m32_m.jpg", mergeImg)
        cv2.imwrite(save_file[:-4] + "_s2_m32_h.jpg", highSharpImg)