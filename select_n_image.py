import os
import random
import shutil

random.seed(66)

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' ----- folder created')
        return True
    else:
        print(path + ' ----- folder existed')
        return False

def get_pic(imgRootPath, xmlRootPath, imgSavePath, xmlSavePath):
    fileList = os.listdir(imgRootPath)
    # fileNumber = len(fileList)
    pickNumber = 500

    sample1 = random.sample(fileList, pickNumber)
    print(sample1)

    for file in sample1:
        fileName0 = os.path.splitext(file)[0]
        shutil.move(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')
        shutil.move(xmlRootPath + fileName0 + '.xml', xmlSavePath + fileName0 + '.xml')
        # print(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')
        # print(xmlRootPath + fileName0 + '.xml', xmlRootPath + fileName0 + '.xml')


if __name__ == '__main__':
    imgRootPath = './wrap_voc/images/'
    xmlRootPath = './wrap_voc/annotations/'
    imgSavePath = './wrap_voc_test_save/images/'
    xmlSavePath = './wrap_voc_test_save/annotations/'
    mkdir(imgRootPath)
    mkdir(xmlRootPath)
    mkdir(imgSavePath)
    mkdir(xmlSavePath)
    get_pic(imgRootPath, xmlRootPath, imgSavePath, xmlSavePath)