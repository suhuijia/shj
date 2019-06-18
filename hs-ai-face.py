# coding=utf-8

import multiprocessing
import os
import threading
import time
# import depth_distance
import webrtc_vad
import cv2
import numpy
import numpy as np
from primesense import openni2
from primesense import _openni2 as c_api
from PIL import Image, ImageDraw, ImageFont

import dlib

import webrtcvad
import collections
import sys
import signal
import pyaudio
from array import array
from struct import pack
import wave
import time



FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_DURATION_MS = 30       # supports 10, 20 and 30 (ms)
PADDING_DURATION_MS = 1500   # 1 sec jugement
CHUNK_SIZE = int(RATE * CHUNK_DURATION_MS / 1000)  # chunk to read
CHUNK_BYTES = CHUNK_SIZE * 2  # 16bit = 2 bytes, PCM
NUM_PADDING_CHUNKS = int(PADDING_DURATION_MS / CHUNK_DURATION_MS)
# NUM_WINDOW_CHUNKS = int(240 / CHUNK_DURATION_MS)
NUM_WINDOW_CHUNKS = int(400 / CHUNK_DURATION_MS)  # 400 ms/ 30ms  ge
NUM_WINDOW_CHUNKS_END = NUM_WINDOW_CHUNKS * 2

START_OFFSET = int(NUM_WINDOW_CHUNKS * CHUNK_DURATION_MS * 0.5 * RATE)

vad = webrtcvad.Vad(0)

pa = pyaudio.PyAudio()
stream = pa.open(format=FORMAT,
                 channels=CHANNELS,
                 rate=RATE,
                 input=True,
                 start=False,
                 # input_device_index=2,
                 frames_per_buffer=CHUNK_SIZE)


got_a_sentence = False
leave = False


vad_run_flag = True
vad_process_flag = True


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def getResult(self):
        return self.res

    def run(self):
        self.res = apply(self.func, self.args)


def handle_int(sig, chunk):
    global leave, got_a_sentence
    leave = True
    got_a_sentence = True


def record_to_file(path, data, sample_width):
    "Records from the microphone and outputs the resulting data to 'path'"
    # sample_width, data = record()
    data = pack('<' + ('h' * len(data)), *data)
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()


def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 32767  # 16384
    times = float(MAXIMUM) / max(abs(i) for i in snd_data)
    r = array('h')
    for i in snd_data:
        r.append(int(i * times))
    return r

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


signal.signal(signal.SIGINT, handle_int)


def voice_main():
    global leave, got_a_sentence
    record_id = 0
    while not leave:
        ring_buffer = collections.deque(maxlen=NUM_PADDING_CHUNKS)
        triggered = False
        voiced_frames = []
        ring_buffer_flags = [0] * NUM_WINDOW_CHUNKS
        ring_buffer_index = 0

        ring_buffer_flags_end = [0] * NUM_WINDOW_CHUNKS_END
        ring_buffer_index_end = 0
        buffer_in = ''
        # WangS
        raw_data = array('h')
        index = 0
        start_point = 0
        StartTime = time.time()
        # print("* recording: ")
        stream.start_stream()

        while not got_a_sentence and not leave:
            chunk = stream.read(CHUNK_SIZE)
            # add WangS
            raw_data.extend(array('h', chunk))
            index += CHUNK_SIZE
            TimeUse = time.time() - StartTime

            active = vad.is_speech(chunk, RATE)

            # sys.stdout.write('_')
            ring_buffer_flags[ring_buffer_index] = 1 if active else 0
            ring_buffer_index += 1
            ring_buffer_index %= NUM_WINDOW_CHUNKS

            ring_buffer_flags_end[ring_buffer_index_end] = 1 if active else 0
            ring_buffer_index_end += 1
            ring_buffer_index_end %= NUM_WINDOW_CHUNKS_END

            # start point detection
            if not triggered:
                ring_buffer.append(chunk)
                num_voiced = sum(ring_buffer_flags)
                if num_voiced > 0.8 * NUM_WINDOW_CHUNKS:
                    # sys.stdout.write(' trigger ')
                    print(u"* 开始讲话：")
                    sys.stdout.write('\n')
                    triggered = True
                    start_point = index - CHUNK_SIZE * 20  # start point
                    # voiced_frames.extend(ring_buffer)
                    ring_buffer.clear()
            # end point detection
            else:
                # voiced_frames.append(chunk)
                ring_buffer.append(chunk)
                num_unvoiced = NUM_WINDOW_CHUNKS_END - sum(ring_buffer_flags_end)
                if num_unvoiced > 0.90 * NUM_WINDOW_CHUNKS_END or TimeUse > 10:
                    print(u"* 结束讲话 ！")
                    sys.stdout.write('\n')
                    # sys.stdout.write(' Close ')
                    triggered = False
                    got_a_sentence = True

            sys.stdout.flush()

        sys.stdout.write('\n')
        # data = b''.join(voiced_frames)

        stream.stop_stream()
        # print("* done recording")
        got_a_sentence = False

        # write to file
        raw_data.reverse()
        for index in range(start_point):
            raw_data.pop()
        raw_data.reverse()
        raw_data = normalize(raw_data)
        record_id += 1
        record_to_file("recording%d.wav" % (record_id), raw_data, 2)
        '''
        ret =  client.asr(get_file_content('recording.wav'), 'wav', 16000, {
        'lan': 'zh',})
        if ret.has_key('result'):
            print(ret['result'][0].encode('utf8'))
        else:
            print('require higher quality audio..')
        '''
    #    leave = True

    stream.close()


def detect_face(cv_img, detector):

    img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
    # print(img.shape)
    w, h = img.shape[1], img.shape[0]
    # print(w, h)
    # detect faces
    dets = detector(img, 0)
    det_rect = []
    # print("Number of faces detected: {}".format(len(dets)))
    for i, d in enumerate(dets):
        # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #   i, d.left(), d.top(), d.right(), d.bottom()))       
        rect = [d.left(), d.top(), d.right(), d.bottom()]
        for i, x in enumerate(rect):
            if x < 0:
                rect[i] = 0
        if rect[2] > w:
            rect[2] = w
        elif rect[3] > h:
            rect[3] = h

        det_rect.append(rect)

    return det_rect


def count_distence(cv_img, depth_img, det_rects, scale=0.6):

    mean_distences = []
    scale_det_rects = []
    for det_rect in det_rects:
        x1, y1, x2, y2 = det_rect[0], det_rect[1], det_rect[2], det_rect[3]
        # cv2.rectangle(cv_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        rect_w = x2 - x1;  rect_h = y2 - y1
        diff_w = rect_w - rect_w*scale
        diff_h = rect_h - rect_h*scale
        x1 = int(x1 + diff_w/2);  x2 = int(x2 - diff_w/2)
        y1 = int(y1 + diff_h/2);  y2 = int(y2 - diff_h/2)

        scale_det_rects.append([x1, y1, x2, y2])
        # cv2.rectangle(cv_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        deep_locate = [640-x2, y1, 640-x1, y2]
        distence = depth_img[deep_locate[1]:deep_locate[3], deep_locate[0]:deep_locate[2], 0]
        nonzero_num = np.nonzero(distence)
        nonzero_area = nonzero_num[0].shape[0]  # only computer the number of nonzero point 
        # mean_distence = np.sum(distence)/((x2-x1)*(y2-y1))
        if nonzero_area == 0:
            nonzero_area = 1
        mean_distence = np.sum(distence)/nonzero_area
        mean_distence_metre = float(mean_distence) / 10000
        mean_distences.append(mean_distence_metre)

    return mean_distences, scale_det_rects


def draw_rect(cv_img, mean_distences, det_rects, scale_det_rects, index):
    # draw the nearset face rect
    detect_rect = det_rects[index]
    x1, y1, x2, y2 = detect_rect[0], detect_rect[1], detect_rect[2], detect_rect[3]
    cv2.rectangle(cv_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    scale_rect = scale_det_rects[index]
    cv2.rectangle(cv_img, (scale_rect[0], scale_rect[1]), (scale_rect[2], scale_rect[3]), (0, 255, 0), 2)
    mini_range = mean_distences[index]

    return mini_range


def judge_distence(mean_distences, min_distence=0.5, max_distence=1.6):

    if mean_distences is None:
        return False
    else:
        # mean_distences.sort()    # sort the distence between the face and the camera.
        sort_distences = sorted(mean_distences)
        for x in sort_distences:
            if x >= min_distence and x <= max_distence:
                idx = mean_distences.index(x)
                index = idx + 1
                return index
            else:
                sort_distences.remove(x)
                if sort_distences is None:
                    return False
                continue


if __name__ == '__main__':
    run_vad_thd = MyThread(voice_main, (), voice_main.__name__)
    run_vad_thd.setDaemon(True)  # child threads will exit while the main thread exit.
    run_vad_thd.start()

    # init dlib detector and open camera
    detector = dlib.get_frontal_face_detector()
    # win = dlib.image_window()
    cap = cv2.VideoCapture(0)

    # init openni2 and gained depth stream data
    openni2.initialize("C:\\Program Files (x86)\\OpenNI2\\Samples\\Bin")
    dev = openni2.Device.open_any()
    print("Open Video Devide Success !!!")
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 640, resolutionY = 480, fps = 30))

    font = ImageFont.truetype(".\\work\\simhei.ttf", 40, encoding="utf-8")


    is_person = False
    try:
        while cap.isOpened():
            # create new process for recognition
            # time.sleep(1)

            ret, cv_img = cap.read()
            # win_img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
            cv2_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(cv2_img)
            if cv_img is None:
                print("Do not have Data Frame !!!")
                break
            # return rect of face
            det_rects = detect_face(cv_img, detector)

            frame = depth_stream.read_frame()
            frame_data = frame.get_buffer_as_uint16()
            # frame_data = frame.get_buffer_as_uint8()
            depth_img = np.frombuffer(frame_data, dtype=np.uint16)
            depth_img.shape = (1, 480, 640)
            depth_img = np.concatenate((depth_img, depth_img, depth_img), axis=0)
            depth_img = np.swapaxes(depth_img, 0, 2)
            depth_img = np.swapaxes(depth_img, 0, 1)

            scale = 0.6
            mean_distences, scale_det_rects = count_distence(cv_img, depth_img, det_rects, scale)
            flag = judge_distence(mean_distences)

            # font = cv2.FONT_HERSHEY_SIMPLEX
            draw = ImageDraw.Draw(pil_img)
            if flag:
                # print(mini_range)
                info = "有人靠近!"
                index = flag - 1
                mini_range = draw_rect(cv2_img, mean_distences, det_rects, scale_det_rects, index)
                draw.text((20, 20), u"有人靠近！", (255, 0, 0), font=font)
            else:
                info = "No persons!!"
                mini_range = None

            cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            if mini_range != None:
                _ = draw_rect(cv2_img, mean_distences, det_rects, scale_det_rects, index)
            cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
            # cv2.imshow("image", depth_img)
            # win.set_image(win_img)
            cv2.imshow("Display", cv2_img)
            
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            is_person = flag
            if is_person:
                vad_process_flag = True
            else:
                vad_process_flag = False

            # print("Parent runing.")

    except KeyboardInterrupt:
        vad_run_flag = False
        run_vad_thd.join()

        print("exit Child.")
        print("exit Parent.")

