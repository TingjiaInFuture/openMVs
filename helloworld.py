import sensor
import time

alpha = 0.9  # 平滑系数
smoothed_avg_cx = 0  # 初始化平滑后的中心点X坐标
smoothed_avg_cy = 0  # 初始化平滑后的中心点Y坐标

def color_blob(img, threshold):
    global smoothed_avg_cx, smoothed_avg_cy
    blobs = img.find_blobs([threshold], x_stride=10, y_stride=10, area_threshold=10, pixels_threshold=10, merge=True, margin=1)
    if blobs:
        sum_cx = sum(blob.cx() for blob in blobs)
        sum_cy = sum(blob.cy() for blob in blobs)
        avg_cx = sum_cx // len(blobs)
        avg_cy = sum_cy // len(blobs)

        # 应用SRTT设计思想进行平滑处理
        smoothed_avg_cx = (alpha * avg_cx) + ((1 - alpha) * smoothed_avg_cx)
        smoothed_avg_cy = (alpha * avg_cy) + ((1 - alpha) * smoothed_avg_cy)

        return int(smoothed_avg_cx), int(smoothed_avg_cy)
    return -1, -1

# 初始化摄像头
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
clock = time.clock()

# 关闭自动增益和自动曝光
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False, exposure_us=1400)



# 定义颜色阈值
red = (36, 53, 29, 50, 15, 52)
blue = (38, 49, -31, -2, -41, -9)
r_las = (37, 46, 34, 78, 16, 60)

while True:
    clock.tick()
    img = sensor.snapshot()
    x, y = color_blob(img, r_las)
    if x != -1 and y != -1:
        img.draw_cross(x, y, color=(0, 0, 0))  # 在识别到的色块上绘制十字架
        print(x, y)
