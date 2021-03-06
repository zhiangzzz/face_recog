# -*- coding: utf-8 -*-
# 进行人脸录入 / face register
# 录入多张人脸 / support multi-faces

# Author:   coneypo
# Blog:     http://www.cnblogs.com/AdaminXie
# GitHub:   https://github.com/coneypo/Dlib_face_recognition_from_camera

# Mail:     coneypo@foxmail.com

# Created at 2018-05-11
# Updated at 2018-10-29

import dlib  # 人脸处理的库 Dlib
import numpy as np  # 数据处理的库 Numpy
import cv2  # 图像处理的库 OpenCv

import os  # 读写文件
import shutil  # 读写文件

# Dlib 正向人脸检测器
detector = dlib.get_frontal_face_detector()

# Dlib 68 点特征预测器
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# OpenCv 调用摄像头
cap = cv2.VideoCapture(0)

# 设置视频参数
cap.set(3, 480)

# 人脸截图的计数器
cnt_ss = 0

# 存储人脸的文件夹
current_face_dir = 0

# 保存的路径
path_make_dir = "data/data_faces_from_camera/"
path_csv = "data/data_csvs_from_camera/"


# (optional) 删除之前存的人脸数据文件夹
def pre_clear():
    folders_rd = os.listdir(path_make_dir)
    for i in range(len(folders_rd)):
        shutil.rmtree(path_make_dir + folders_rd[i])

    csv_rd = os.listdir(path_csv)
    for i in range(len(csv_rd)):
        os.remove(path_csv + csv_rd[i])


# 每次程序录入之前，删掉之前存的人脸数据
pre_clear()

# 人脸种类数目的计数器
person_cnt = 0

while cap.isOpened():
    # 480 height * 640 width
    flag, img_rd = cap.read()
    kk = cv2.waitKey(1)

    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)

    # 人脸数 faces
    faces = detector(img_gray, 0)

    # 待会要写的字体
    font = cv2.FONT_HERSHEY_COMPLEX

    # 按下 'n' 新建存储人脸的文件夹
    if kk == ord('n'):
        person_cnt += 1
        current_face_dir = path_make_dir + "person_" + str(person_cnt)
        print('\n')
        for dirs in (os.listdir(path_make_dir)):
            if current_face_dir == path_make_dir + dirs:
                shutil.rmtree(current_face_dir)
                print("删除旧的文件夹:", current_face_dir)
        os.makedirs(current_face_dir)
        print("新建的人脸文件夹: ", current_face_dir)

        # 将人脸计数器清零
        cnt_ss = 0

    if len(faces) != 0:
        # 检测到人脸

        # 矩形框
        for k, d in enumerate(faces):

            # 计算矩形大小
            # (x,y), (宽度width, 高度height)
            pos_start = tuple([d.left(), d.top()])
            pos_end = tuple([d.right(), d.bottom()])

            # 计算矩形框大小
            height = (d.bottom() - d.top())
            width = (d.right() - d.left())

            hh = int(height / 2)
            ww = int(width / 2)

            # 设置颜色 / The color of rectangle of faces detected
            color_rectangle = (255, 255, 255)
            if (d.right() + ww) > 640 or (d.bottom() + hh > 480) or (d.left() - ww < 0) or (d.top() - hh < 0):
                cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                color_rectangle = (0, 0, 255)
            else:
                color_rectangle = (255, 255, 255)

            cv2.rectangle(img_rd,
                          tuple([d.left() - ww, d.top() - hh]),
                          tuple([d.right() + ww, d.bottom() + hh]),
                          color_rectangle, 2)

            # 根据人脸大小生成空的图像
            im_blank = np.zeros((int(height * 2), width * 2, 3), np.uint8)

            # 按下 's' 保存摄像头中的人脸到本地
            if kk == ord('s'):
                cnt_ss += 1
                for ii in range(height * 2):
                    for jj in range(width * 2):
                        im_blank[ii][jj] = img_rd[d.top() - hh + ii][d.left() - ww + jj]
                cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", im_blank)
                print("写入本地：", str(current_face_dir) + "/img_face_" + str(cnt_ss) + ".jpg")

        # 显示人脸数
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

    # 添加说明
    cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "N: New face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "S: Save face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)

    # 按下 'q' 键退出
    if kk == ord('q'):
        break

    # 窗口显示
    # cv2.namedWindow("camera", 0) # 如果需要摄像头窗口大小可调
    cv2.imshow("camera", img_rd)

# 释放摄像头
cap.release()

# 删除建立的窗口
cv2.destroyAllWindows()