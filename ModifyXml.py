import os
import pdb
import xml.etree.ElementTree as ET
from PIL import Image
from xml.dom.minidom import parse
from xml.etree.ElementTree import ElementTree, Element


def read_xml(annoPath):
    tree = ET.parse(annoPath)
    root = tree.getroot()
    # xmlContent = open(annoPath).read()
    # return tree, root, xmlContent
    return tree, root


def test():
    imgRootPath = './test_voc/images/'
    imgSavePath = './test_save_voc/images/'
    annoRootPath = './test_voc/annotations/'
    annoSavePath = './test_save_voc/annotations/'
    for file in os.listdir(annoRootPath):
        fileName0 = os.path.splitext(file)[0]
        tree, root = read_xml(annoRootPath + file)
        objectList = root.findall('object')
        objectListLen = len(objectList)

        for i in range(0, objectListLen):
            tree_temp, root_temp = read_xml(annoRootPath + file)
            objectList = root_temp.findall('object')
            for j in range(0, objectListLen):
                if i == j:
                    bndbox = objectList[j].find('bndbox')
                    xmin = float(bndbox.find('xmin').text)
                    ymin = float(bndbox.find('ymin').text)
                    xmax = float(bndbox.find('xmax').text)
                    ymax = float(bndbox.find('ymax').text)
                    width = xmax - xmin
                    height = ymax - ymin
                    size = root_temp.find('size')
                    size.find('width').text = str(width)
                    size.find('height').text = str(height)
                else:
                    root_temp.remove(objectList[j])
            # print(annoSavePath + fileName0 + '_' + str(i + 1) + 'wrap' + '.xml')
            tree_temp.write(annoSavePath + fileName0 + '_' + str(i + 1) + 'wrap' + '.xml')

            img = Image.open(imgRootPath + fileName0 + '.jpg')
            region = img.crop((xmin, ymin, xmin + width, ymin + height))
            region.save(imgSavePath + fileName0 + '_' + str(i + 1) + 'wrap' + '.jpg')



if __name__ == '__main__':
    test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
