import os
import random
import shutil
import xml
import xml.etree.ElementTree as ET

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

def read_xml(annoPath):
    tree = ET.parse(annoPath)
    root = tree.getroot()
    # xmlContent = open(annoPath).read()
    # return tree, root, xmlContent
    return tree, root

def random_select(imgRootPath, xmlRootPath, imgSavePath, xmlSavePath, trainRate, testRate):
    random.seed(1)
    fileList = os.listdir(imgRootPath)
    fileNumber = len(fileList)
    trainList = random.sample(fileList, int(fileNumber * trainRate))
    tempList = fileList

    # 获得测试集
    for element in trainList:
        tempList.remove(element)
    testList = tempList

    for file in trainList:
        fileName0 = os.path.splitext(file)[0]
        # 复制图片
        shutil.copy(imgRootPath + file, imgSavePath + file)
        # 复制xml文件
        shutil.copy(xmlRootPath + fileName0 + '.xml', xmlSavePath + fileName0 + '.xml')

def special_select(imgRootPath, xmlRootPath, imgSavePath, xmlSavePath, selectName):
    fileList = os.listdir(xmlRootPath)
    for file in fileList:
        fileName0 = os.path.splitext(file)[0]
        tree, root = read_xml(xmlRootPath + file)
        objectList = root.findall('object')
        nameList = []
        for obj in objectList:
            objName = obj.find('name').text
            nameList.append(objName)
        # 只有这个是想要的类就复制这个图片
        if selectName in nameList:
            # 复制图片
            shutil.copy(imgRootPath + fileName0 + '.jpg', imgSavePath + fileName0 + '.jpg')
            # 复制xml
            shutil.copy(xmlRootPath + file, xmlSavePath + file)



if __name__ == '__main__':
    imgRootPath = './test_voc/images/'
    xmlRootPath = './test_voc/annotations/'
    # imgSavePath = './randomSelect_voc/images/'
    # xmlSavePath = './randomSelect_voc/annotations/'
    imgSavePath = './specialSelect_voc/images/'
    xmlSavePath = './specialSelect_voc/annotations/'
    mkdir(imgSavePath)
    mkdir(xmlSavePath)
    trainRate = 0.85
    testRate = 0.15
    selectName = 'lighter'
    # random_select(imgRootPath, xmlRootPath, imgSavePath, xmlSavePath, trainRate, testRate)
    special_select(imgRootPath, xmlRootPath, imgSavePath, xmlSavePath, selectName)



