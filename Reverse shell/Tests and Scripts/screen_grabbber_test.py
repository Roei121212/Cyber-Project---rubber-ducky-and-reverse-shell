# module 1 https://github.com/ra1nty/DXcam
import dxcam

# module 2 https://github.com/ponty/pyscreenshot
# import pyscreenshot
'''this module was so slow i completely gave up on it'''

# module 3 https://github.com/asweigart/pyautogui
import pyautogui

# module 4 https://github.com/BoboTiG/python-mss
import mss

# time module to measure time
import time
# matplotlib module to draw the graph
import matplotlib.pyplot as plt

# initialize dxcam
camera = dxcam.create(output_idx=0, output_color="BGR")
camera.start(target_fps=1000, video_mode=True)


def dxcam_capture_30_frames():
    start_time = time.time()
    for i in range(30):
        camera.get_latest_frame()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


'''def pyscreenshot_capture_30_frames():
    start_time = time.time()
    for i in range(30):
        image = pyscreenshot.grab()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time'''


def pyautogui_capture_30_frames():
    start_time = time.time()
    for i in range(30):
        image = pyautogui.screenshot()
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


def mss_capture_30_frames():
    sct = mss.mss()
    monitor = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}
    start_time = time.time()
    for i in range(30):
        image = sct.grab(monitor)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time


# creating the dataset
data = {'DXCAM': dxcam_capture_30_frames(),
        'pyautogui': pyautogui_capture_30_frames(),
        'mss': mss_capture_30_frames()}

modules = list(data.keys())
values = list(data.values())

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.bar(modules, values, color='maroon',
        width=0.4)

plt.xlabel("different modules")
plt.ylabel("time (sec) to capture 30 frames")
plt.show()
