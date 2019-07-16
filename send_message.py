# -*- coding: utf-8 -*-

import win32con
import win32gui
import ctypes
import ctypes.wintypes
import json
import time
import logging
import sys

# 打印logging日志，写入文件
logging.basicConfig(filename = 'log.txt',
                    level = logging.INFO,
                    format = '%(asctime)s %(levelno)d %(message)s',
                    timefmt = '%H:%M:%s')

def gbk2utf8(s):
    return s.decode('gbk').encode('utf-8')


def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwnd, param: param.append(hwnd), hwndChildList)
    return hwndChildList


# 获取某个句柄的类名和标题
def get_window_attr(hWnd, win_name, cls_name=None):
    '''''
    显示窗口的属性
    :return:
    '''
    if not hWnd:
        return None

    # 中文系统默认title是gb2312的编码
    title = win32gui.GetWindowText(hWnd)
    # title = gbk2utf8(title)
    # print("title: ", title)
    clsname = win32gui.GetClassName(hWnd)
    # print("clsname: ", clsname)
    # print '窗口句柄:%s ' % (hWnd)
    # print '窗口标题:%s' % (title)
    # print '窗口类名:%s' % (clsname)
    # print ''
    if title == win_name or clsname == cls_name:
        # print(title)
        # print(win_name)
        return hWnd, title, clsname
    else:
        return None


FindWindow = ctypes.windll.user32.FindWindowW
SendMessage = ctypes.windll.user32.SendMessageW


class COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ('dwData', ctypes.wintypes.LPARAM),
        ('cbData', ctypes.wintypes.DWORD),
        ('lpData', ctypes.c_wchar_p)
        # formally lpData is c_void_p, but we do it this way for convenience
    ]

try:
    flag = False
    # cls_name = sys.argv[2]
    print("suhuijia")
    win_name = sys.argv[1]
    cls_name = None
    print(win_name)
    while not flag:
        # get the window handle
        time.sleep(0.5)

        # cls_name = "NDGuiFoundation"
        # win_name = "ai_guide"
        # win_name = sys.argv[1]
        # cls_name = None
        print(cls_name, win_name)
        hWndList = []
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
        # print(hWndList)
        # print(len(hWndList))
        # hwnd123 = win32gui.FindWindow(0, win_name)
        # print(hwnd123)
        ai_hnd = None
        for h in hWndList:
            # print show_window_attr(h, win_name)
            ret = get_window_attr(h, win_name, cls_name)
            print("ret:", ret)
            if ret is not None:
                hwnd, title, cls_name = ret
                # print "Found# ", hwnd, title, cls_name
                if title == win_name:
                    ai_hnd = hwnd

        # hwnd = get_window_attr(h, win_name, cls_name)
        # if hwnd is not None:
        #   print "hwnd", hwnd
        #   print "title", title
        print(ai_hnd)
        if ai_hnd is None:
            flag = False
            # print "Fail to find window."
            logging.info("Fail to find window.")
            continue        
            exit(-1)
        else:
            # print "Get win handler: ", ai_hnd
            logging.info("Get win handler: %s", ai_hnd)
            break

    # win32gui.CloseWindow(ai_hnd)
    title = win32gui.GetWindowText(ai_hnd)
    clsname = win32gui.GetClassName(ai_hnd)

    # 获取父句柄hwnd类名为clsname的子句柄
    # hwnd1 = win32gui.FindWindowEx(hwnd, None, clsname, None)

    cds = COPYDATASTRUCT()
    cds.dwData = 0

except:
    logging.exception("This is a exception.")


def say(s):
    msg = json.dumps({
       "MsgType": "Talk",
       "Param": s
    })
    cds.cbData = ctypes.sizeof(ctypes.create_unicode_buffer(msg))
    cds.lpData = ctypes.c_wchar_p(msg)
    SendMessage(ai_hnd, win32con.WM_COPYDATA, ctypes.byref(cds), ctypes.byref(cds))


def ask(s):
    msg = json.dumps({
     "MsgType": "RecoginizeByFile",
     "Param": s
    })
    cds.cbData = ctypes.sizeof(ctypes.create_unicode_buffer(msg))
    cds.lpData = ctypes.c_wchar_p(msg)
    SendMessage(ai_hnd, win32con.WM_COPYDATA, ctypes.byref(cds), ctypes.byref(cds))


def interrupt():
    msg = json.dumps({
       "MsgType": "interrupt",
       "Param": ""
    })
    cds.cbData = ctypes.sizeof(ctypes.create_unicode_buffer(msg))
    cds.lpData = ctypes.c_wchar_p(msg)
    SendMessage(ai_hnd, win32con.WM_COPYDATA, ctypes.byref(cds), ctypes.byref(cds))


def approach():
    msg = json.dumps({
       "MsgType": "approach",
       "Param": ""
    })
    cds.cbData = ctypes.sizeof(ctypes.create_unicode_buffer(msg))
    cds.lpData = ctypes.c_wchar_p(msg)
    SendMessage(ai_hnd, win32con.WM_COPYDATA, ctypes.byref(cds), ctypes.byref(cds))


def leave():
    msg = json.dumps({
       "MsgType": "leave",
       "Param": ""
    })
    cds.cbData = ctypes.sizeof(ctypes.create_unicode_buffer(msg))
    cds.lpData = ctypes.c_wchar_p(msg)
    SendMessage(ai_hnd, win32con.WM_COPYDATA, ctypes.byref(cds), ctypes.byref(cds))


if __name__ == '__main__':
    ask(".\\work\\null.wav")
