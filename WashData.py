import os
import xml.etree.ElementTree as ET
import shutil


def mkdir(makePath):
    makePath = makePath.strip()
    makePath = makePath.rstrip("\\")
    isExists = os.path.exists(makePath)
    if not isExists:
        os.makedirs(makePath)
        print(makePath + ' ----- folder created')
        return True
    else:
        print(makePath + ' ----- folder existed')
        return False


def wash_data(xmlRootPath, xmlSavePath, imgRootPath, imgSavePath):
    mkdir(imgSavePath)
    mkdir(xmlSavePath)
    for file in os.listdir(xmlRootPath):
        fileName0 = os.path.splitext(file)[0]
        tree = ET.parse(xmlRootPath + file)
        fileName = tree.find('filename').text  # it is origin name
        tree.find('filename').text = file  # change file name to rot degree name
        print(xmlSavePath + file)
        tree.write(xmlSavePath + file)
        shutil.copy(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')
        # print(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')


if __name__ == '__main__':
    xmlRootPath = './test_voc/annotations/'
    xmlSavePath = './new_voc/annotations/'
    imgRootPath = './test_voc/images/'
    imgSavePath = './new_voc/images/'
    wash_data(xmlRootPath, xmlSavePath, imgRootPath, imgSavePath)
