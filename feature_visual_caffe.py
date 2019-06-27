# coding=utf-8

# python save numpy data
# numpy.savetxt("result.txt", numpy_data)

# python save list data
# file = open('data.txt', 'w')
# file.write(str(list_data))
# file.close

import numpy as np
import matplotlib.pyplot as plt
import sys
import caffe
import cv2
import sklearn
import os
import time

def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    plt.imshow(data)
    plt.savefig('feature5.png')



caffe.set_mode_cpu()
model_def = "./vgg/VGG_FACE_deploy.prototxt"
model_weights = "./vgg/VGG_FACE.caffemodel"

# 使用均值信息
mean_data=np.array([129.1863,104.7624,93.5940])
#初始化网络
net=caffe.Net(model_def,model_weights,caffe.TEST)

# 标准的变形
transformer = caffe.io.Transformer({'data':net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_mean('data',mean_data)
transformer.set_raw_scale('data', 255)
transformer.set_channel_swap('data', (2,1,0))


image_path_dir = "face_detection/face_feature_vgg/images/"

for filename in os.listdir(image_path_dir):
	print(filename)
	file_name = filename.split('.')[0]
	print(file_name)
	# net.blobs['data'].reshape(1,3,227,227)
	# 读取需要比较的两个图片文件，当然可以自己和自己比的
	image = caffe.io.load_image(image_path_dir + filename)

	# 标准化到224*224
	image = caffe.io.resize_image(image,(224,224))
	   
	cv2.imshow("uuu",image)
	cv2.waitKey(2000)

	# 导入图像1
	transformed_image = transformer.preprocess('data', image)
	net.blobs['data'].data[...] = transformed_image
	# 提取第一个人脸图片的特征值，不建议使用fc8/2622个人的分类特征，而是使用其上一层的fc7，4096个值
	output = net.forward()

	# 可视化特征
	feature = net.blobs['conv5_3'].data[0, :36]
	vis_square(feature, padval=0.5)
	break

	# feature = np.float64(net.blobs['fc7'].data)
	# print(feature.shape)
	# print(type(feature))
	# for i in range(4096):
	# 	print(feature[0][i])
	# # 将特征保存到txt文件中
	# np.savetxt(file_name+".txt", feature, fmt='%s')
	# print("################## save over ################")
