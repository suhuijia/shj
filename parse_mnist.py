#!/usr/bin/env python
#-*-coding:utf-8-*-

from PIL import Image
import struct
import cv2
import numpy as np
import os
import shutil


def gaussianblur(img_in):
    w_s = np.random.random_integers(1, 1)
    w_s = w_s * 2 + 1
    sigma_x_y = np.random.random_integers(0, 1, 2)
    img = cv2.GaussianBlur(img_in, (w_s, w_s), sigmaX=sigma_x_y[0], sigmaY=sigma_x_y[1])
    return img


def read_image(filename):
	f = open(filename,'rb')
	index = 0
	buf = f.read()
	f.close()

	magic, images, rows, columns = struct.unpack_from('>IIII' , buf , index)
	index += struct.calcsize('>IIII')
	print(magic, images, rows, columns)  #[2051, 10000, 28, 28]
	# flag = 100
	for i in xrange(images):
	#for i in xrange(2000):
		image = Image.new('L', (columns, rows))

		for x in xrange(rows):
			for y in xrange(columns):
				image.putpixel((y, x), int(struct.unpack_from('>B', buf, index)[0]))
				index += struct.calcsize('>B')

		image = image.resize((64, 64))
		# print(image)
		# print(type(image))
		# print(image.size)
		matrix = np.array(image)
		# print(type(matrix))
		matrix[matrix < 128] = 0
		matrix_rever = 255 - matrix
		y_list = []
		x_list = []
		for k in range(len(matrix_rever)):
			# matrix_list = matrix_rever[i].tolist()
			for j in range(len(matrix_rever[0])):
				sub = matrix_rever[k][j]
				if sub != 255:
					x_list.append(j)
					y_list.append(k)
				else:
					continue

		x_list.sort()
		y_list.sort()
		x_min = x_list[0]; x_max = x_list[-1]
		y_min = y_list[0]; y_max = y_list[-1]

		matrix_crop = matrix_rever[y_min:y_max+1, x_min:x_max+1]
	
		matrix_crop = gaussianblur(matrix_crop)

		image = Image.fromarray(matrix_crop)
		print 'save ' + str(i) + 'image'
		image.save('test/test_' + str(i) + '.jpg')

		# if i == flag:
		# 	break


def read_label(filename, saveFilename):
	f = open(filename, 'rb')
	index = 0
	buf = f.read()
	f.close()

	magic, labels = struct.unpack_from('>II' , buf , index)
	print(magic, labels)
	index += struct.calcsize('>II')

	labelArr = [0] * labels
	#labelArr = [0] * 2000

	for x in xrange(labels):
	#for x in xrange(2000):
		labelArr[x] = int(struct.unpack_from('>B', buf, index)[0])
		#print labelArr[x]
		index += struct.calcsize('>B')
		save = open(saveFilename, 'w')
		save.write(','.join(map(lambda x: str(x), labelArr)))
		save.write('\n')
		save.close()
		print 'save labels success'



def get_label(label_file):
	with open(label_file, 'r') as rf:
		data = rf.readlines()
	label_list = list(eval(data[0]))

	return label_list


if __name__ == '__main__':
	read_image('./MNIST_data/t10k-images.idx3-ubyte')
	read_label('./MNIST_data/t10k-labels.idx1-ubyte', 'test/label.txt')


	label_file = "./test/label.txt"
	label_list = get_label(label_file)
	orig_image_dir = "./test/"
	new_image_dir = "./data_crop/"

	for i in range(len(label_list)):
		image_label = label_list[i]
		image_file = "test_" + str(i) + ".jpg"
		new_dir_path = os.path.join(new_image_dir, str(image_label))
		if not os.path.exists(new_dir_path):
			os.makedirs(new_dir_path)
		else:
			pass

		orig_image_path = os.path.join(orig_image_dir, image_file)
		shutil.move(orig_image_path, new_dir_path)


	# 删除文件夹中文件
	# image_dir = "./test/"
	# for file in os.listdir(image_dir):
	# 	path = os.path.join(image_dir, file)
	# 	os.remove(path)
