# -*- encoding: utf-8 -*-
import os, sys
import numpy as np
import cv2
import operator
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema


def smooth(x, window_len=9, window='hanning'):
    """smooth the data using a window with requested size.
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by introducing reflected copies of the signal
    (with the window size) in both ends so that transient parts are minimized
    in the begining and end part of the output signal.

    input:
        x: the input signal
        window_len: the dimension of the smoothing window
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.
    output:
        the smoothed signal

    example:
    import numpy as np
    t = np.linspace(-2,2,0.1)
    x = np.sin(t)+np.random.randn(len(t))*0.1
    y = smooth(x)

    see also:

    numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
    scipy.signal.lfilter

    TODO: the window parameter could be the window itself if an array instead of a string
    """
    # print(len(x), window_len)
    # if x.ndim != 1:
    #     raise ValueError, "smooth only accepts 1 dimension arrays."
    #
    # if x.size < window_len:
    #     raise ValueError, "Input vector needs to be bigger than window size."
    #
    # if window_len < 3:
    #     return x
    #
    # if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
    #     raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = np.r_[2 * x[0] - x[window_len:1:-1], x, 2 * x[-1] - x[-1:-window_len:-1]]
    # print(len(s))

    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = getattr(np, window)(window_len)
    y = np.convolve(w / w.sum(), s, mode='same')
    return y[window_len - 1:-window_len + 1]


class Frame:
    """define information about each frame"""
    def __init__(self, id, diff):
        self.id = id
        self.diff = diff

    def __lt__(self, other):
        if self.id == other.id:
            return self.id < other.id
        return self.id < other.id

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        return self.id == other.id and self.diff == other.diff

    def __ne__(self, other):
        return not self.__eq__(other)


def rel_change(a, b):
    x = (b - a) / max(a, b)
    return x


def getKeyFrames(prefix, frames_idxs):
    """ 提取视频关键帧，输入可视频或者图片文件夹 """
    ####################### 读取所有视频帧数据，计算帧差值 ###############
    curr_frame = None
    prev_frame = None
    frame_diffs = []
    frames = []
    i = 0
    for idx in frames_idxs:
        image_path = prefix + '-{:04d}.jpg'.format(idx)
        print(image_path)
        frame = cv2.imread(image_path)
        curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        if curr_frame is not None and prev_frame is not None:
            diff = cv2.absdiff(curr_frame, prev_frame)
            diff_sum = np.sum(diff)
            diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)
        prev_frame = curr_frame
        i = i + 1

    ######################## 不同关键帧提取方法 ########################
    ## 设置固定阈值标准
    USE_THRESH = False
    ## 固定阈值
    THRESH = 0.87

    ## 设置固定阈值标准
    USE_TOP_ORDER = False
    ## 提取排序前N个数据
    NUM_TOP_FRAMES = 50

    ## 设置局部极大值标准
    USE_LOCAL_MAXIMA = True
    ## 平滑窗口大小
    len_window = 5      ## 10， 15

    ## 计算关键帧
    keyframe_id_set = list()

    ## 1. 使用差序，帧间平均差最大的前几帧认为是关键帧
    if USE_TOP_ORDER:
        ## 对差值帧进行降序排列
        frames.sort(key=operator.attrgetter("diff"), reverse=True)
        for keyframe in frames[:NUM_TOP_FRAMES]:
            keyframe_id_set.append(keyframe.id)

    ## 2. 使用差异阈值，帧间平均差值大于阈值的帧认为是关键帧
    if USE_THRESH:
        for i in range(1, len(frames)):
            if (rel_change(float(frames[i - 1].diff), float(frames[i].diff)) >= THRESH):
                keyframe_id_set.append(frames[i].id)

    ## 3. 使用局部极大值，帧间平均差值局部最大的帧被认为是关键帧
    if USE_LOCAL_MAXIMA:
        diff_array = np.array(frame_diffs)
        sm_diff_array = smooth(diff_array, len_window)
        frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
        for i in frame_indexes:
            keyframe_id_set.append(frames[i - 1].id)

        # plt.figure(figsize=(40, 20))
        # plt.locator_params(axis='both', nbins=10)
        # plt.stem(sm_diff_array)
        # plt.savefig(os.path.join(dir, "plot.png"))

    return keyframe_id_set


if __name__ == "__main__":

    # file = "./ApplyEyeMakeup/v_ApplyEyeMakeup_g01_c03.avi"
    # video = cv2.VideoCapture(file)
    # frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    # print("frame_count: ", frame_count)
    # sys.exit(0)

    print(sys.executable)
    ## 设置固定阈值标准
    USE_THRESH = False
    ## 固定阈值
    THRESH = 0.87

    ## 设置固定阈值标准
    USE_TOP_ORDER = False
    ## 提取排序前N个数据
    NUM_TOP_FRAMES = 50

    ## 设置局部极大值标准
    USE_LOCAL_MAXIMA = True
    ## 平滑窗口大小
    len_window = 20

    ## 原视频地址
    # videopath = 'pikachu.mp4'
    videopath = "./ApplyEyeMakeup/v_ApplyEyeMakeup_g01_c03.avi"
    ## 保存视频帧数据位置
    dir = './extract_result/'
    os.makedirs(dir, exist_ok=True)

    print("target video: " + videopath)
    print("frame save directory: " + dir)
    ## 读取视频计算帧间差异
    cap = cv2.VideoCapture(str(videopath))
    curr_frame = None
    prev_frame = None
    frame_diffs = []
    frames = []
    success, frame = cap.read()
    i = 0
    while (success):
        curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
        if curr_frame is not None and prev_frame is not None:
            diff = cv2.absdiff(curr_frame, prev_frame)
            diff_sum = np.sum(diff)
            diff_sum_mean = diff_sum / (diff.shape[0] * diff.shape[1])
            frame_diffs.append(diff_sum_mean)
            frame = Frame(i, diff_sum_mean)
            frames.append(frame)
        prev_frame = curr_frame
        i = i + 1
        success, frame = cap.read()
    cap.release()

    ## 计算关键帧
    keyframe_id_set = list()

    ## 1. 使用差序，帧间平均差最大的前几帧认为是关键帧
    if USE_TOP_ORDER:
        ## 对差值帧进行降序排列
        frames.sort(key=operator.attrgetter("diff"), reverse=True)
        for keyframe in frames[:NUM_TOP_FRAMES]:
            keyframe_id_set.append(keyframe.id)

    ## 2. 使用差异阈值，帧间平均差值大于阈值的帧认为是关键帧
    if USE_THRESH:
        for i in range(1, len(frames)):
            if (rel_change(float(frames[i - 1].diff), float(frames[i].diff)) >= THRESH):
                keyframe_id_set.append(frames[i].id)

    ## 3. 使用局部极大值，帧间平均差值局部最大的帧被认为是关键帧
    if USE_LOCAL_MAXIMA:
        diff_array = np.array(frame_diffs)
        sm_diff_array = smooth(diff_array, len_window)
        frame_indexes = np.asarray(argrelextrema(sm_diff_array, np.greater))[0]
        for i in frame_indexes:
            keyframe_id_set.append(frames[i - 1].id)

        plt.figure(figsize=(40, 20))
        plt.locator_params(axis='both', nbins=10)
        plt.stem(sm_diff_array)
        plt.savefig(os.path.join(dir, "plot.png"))

    ## 保存所有的关键帧图像数据
    cap = cv2.VideoCapture(str(videopath))
    curr_frame = None
    keyframes = []
    success, frame = cap.read()
    idx = 0
    while (success):
        if idx in keyframe_id_set:
            name = "keyframe_" + str(idx) + ".jpg"
            cv2.imwrite(dir + name, frame)
            keyframe_id_set.remove(idx)
        idx = idx + 1
        success, frame = cap.read()
    cap.release()
