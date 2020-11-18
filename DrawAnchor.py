import cv2
import os
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def draw_anchor(mainFolder):
    # data file
    # MainFolder = '/home/Ok/MyData'
    imgFolder = os.path.join(mainFolder, 'images')
    anotFolder = os.path.join(mainFolder, 'annotations')
    print(imgFolder, anotFolder)

    fileList = os.listdir(imgFolder)
    for file in fileList:
        fileName0 = os.path.splitext(file)[0]
        imgPath = os.path.join(imgFolder, file)
        imageToDraw = Image.open(imgPath)  # 打开一张图片
        anotName = fileName0 + '.xml'
        anotPath = os.path.join(anotFolder, anotName)
        tree = ET.parse(anotPath)
        root = tree.getroot()
        for box in root.iter('bndbox'):
            xmin = float(box.find('xmin').text)
            ymin = float(box.find('ymin').text)
            xmax = float(box.find('xmax').text)
            ymax = float(box.find('ymax').text)
            imageDraw = ImageDraw.Draw(imageToDraw)
            imageDraw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0))

        imageToDraw.show()


if __name__ == '__main__':
    mainFolder = './test_voc'
    draw_anchor(mainFolder)
