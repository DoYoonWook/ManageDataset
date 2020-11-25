import os
import random
import shutil
import xml
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib


def read_xml(annoPath):
    tree = ET.parse(annoPath)
    root = tree.getroot()
    # xmlContent = open(annoPath).read()
    # return tree, root, xmlContent
    return tree, root


def analyse(xmlRootPath):
    height = {}
    width = {}
    ratio = {}
    for file in os.listdir(xmlRootPath):
        tree, root = read_xml(xmlRootPath + file)
        objectList = root.findall('object')
        for obj in objectList:
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)
            anchorHeight = ymax - ymin
            anchorWidth = xmax - xmin
            # anchorRatio = anchorWidth / anchorHeight
            anchorRatio = anchorHeight / anchorWidth
            if anchorHeight in height:
                height[anchorHeight] = height[anchorHeight] + 1
            else:
                height[anchorHeight] = 1

            if anchorWidth in width:
                width[anchorWidth] = width[anchorWidth] + 1
            else:
                width[anchorWidth] = 1

            if anchorRatio in ratio:
                ratio[anchorRatio] = ratio[anchorRatio] + 1
            else:
                ratio[anchorRatio] = 1
    # print(height)
    # print(width)
    # print(ratio)
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    heightKeys = height.items()
    heightValue = height.values()
    widthKeys = width.items()
    widthValue = width.values()
    ratioKeys = ratio.items()
    ratioValue = ratio.values()

    print(heightValue)
    plt.figure(figsize=(8, 8), dpi=80)
    # 绘制第一个图
    plt.subplot(2, 2, 1)
    plt.hist(heightValue, bins=len(heightValue), facecolor="blue", edgecolor="black", alpha=0.7)
    plt.title("height分布直方图")
    # 绘制第二个图
    plt.subplot(2, 2, 2)
    plt.hist(widthValue, bins=len(widthValue), facecolor="blue", edgecolor="black", alpha=0.7)
    plt.title("width分布直方图")
    # 绘制第三个图
    plt.subplot(2, 2, 3)
    plt.hist(ratioValue, bins=len(ratioValue), facecolor="blue", edgecolor="black", alpha=0.7)
    plt.title("height/width分布直方图")
    plt.savefig('anchorAnalyse')
    plt.show()


if __name__ == '__main__':
    xmlRootPath = './ori_voc/annotations/'
    analyse(xmlRootPath)
