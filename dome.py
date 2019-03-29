# -*- coding: utf-8 -*-

import cv2
import sys
from PIL import Image

# camera_idx为视频来源
def CatcUsbVideo(windows_name, camera_idx):
    cv2.namedWindow(windows_name)

    # 用cap接收视频来源
    cap = cv2.VideoCapture(camera_idx)
    print(camera_idx)

    # 获取视频的帧速率fps
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    # 获取视频的宽高
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # 设置视频的解码器
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    # 获取视频的总帧数
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print('视频详细信息：\n\tfps：', fps, '\n\t宽、高：', size, '\n\t总帧数：', frames, '\n\t解码器：', fourcc)

    # 告诉openCV使用人脸分类器
    classfier = cv2.CascadeClassifier("/home/ylhy/PycharmProjects/untitled/venv/lib/python3.6/site-packages/cv2/data/haarcascade_frontalface_alt2.xml")

    # 定义一个边框颜色
    color = (0, 255, 0)

    s = 0
    # 如果视频能被打开就开始循环
    while cap.isOpened():
        ok, frame = cap.read()
        if not ok:
            print("错误")
            break
        # 将当前视频所循环获取的帧转换为灰度视频进行识别，提高速度
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 开始人脸检测,把处理好的灰度视频传入
        # 1.2为图片缩放比例，3为需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        # 如果大于0说明检测到了人脸
        if len(faceRects) > 0:
            for faceRects in faceRects:
                x, y, w, h = faceRects
                cv2.rectangle(frame, (x - 10, y - 10),(x + w +10, y + h +10), color, 2)
            s = s + 1
            cv2.imwrite('/home/ylhy/桌面/image_'+str(s)+'.jpg', frame)
        cv2.imshow(windows_name, frame)

        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    CatcUsbVideo("开始",'/home/ylhy/桌面/as.mp4')
